#!/usr/bin/env python3
"""InWorld TTS script - converts markdown book files to WAV audio."""

import argparse
import base64
import io
import os
import re
import sys
import wave
from pathlib import Path

import requests


def synthesize(text: str, api_key: str, voice_id: str, model_id: str = "inworld-tts-1.5-max") -> bytes:
    """Send text to InWorld API and return raw audio bytes."""
    url = "https://api.inworld.ai/tts/v1/voice"
    
    headers = {
        "Authorization": f"Basic {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "text": text,
        "voiceId": voice_id,
        "modelId": model_id,
        "audioConfig": {
            "audioEncoding": "LINEAR16",
            "sampleRateHertz": 44100
        }
    }
    
    response = requests.post(url, json=payload, headers=headers, timeout=60)
    
    if response.status_code != 200:
        error = response.json().get("message", response.text)
        raise RuntimeError(f"API error ({response.status_code}): {error}")
    
    data = response.json()
    audio_b64 = data["audioContent"]
    return base64.b64decode(audio_b64)


def parse_wav(data: bytes) -> tuple[bytes, int, int, int]:
    """Parse WAV header and return (pcm_data, num_channels, sample_rate, bytes_per_sample)."""
    with wave.open(io.BytesIO(data), 'rb') as w:
        channels = w.getnchannels()
        rate = w.getframerate()
        frames = w.readframes(w.getnframes())
        return frames, channels, rate, w.getsampwidth()


def create_wav(pcm_data: bytes, channels: int, sample_rate: int, bytes_per_sample: int) -> bytes:
    """Create WAV file from PCM data."""
    buffer = io.BytesIO()
    with wave.open(buffer, 'wb') as w:
        w.setnchannels(channels)
        w.setsampwidth(bytes_per_sample)
        w.setframerate(sample_rate)
        w.writeframes(pcm_data)
    return buffer.getvalue()


def parse_chapters(content: str) -> list[tuple[str, str]]:
    """Parse markdown content into chapters (heading, text)."""
    pattern = r'(^|\n)(##\s+.+)(\n|$)'
    
    parts = re.split(pattern, content, flags=re.MULTILINE)
    
    chapters = []
    current_heading = "Introduction"
    current_text = []
    
    for part in parts:
        if part and part.startswith("## "):
            if current_text:
                chapters.append((current_heading, "".join(current_text).strip()))
            current_heading = part.replace("## ", "").strip()
            current_text = []
        elif part:
            current_text.append(part)
    
    if current_text:
        chapters.append((current_heading, "".join(current_text).strip()))
    
    return chapters


def split_to_chunks(text: str, max_chars: int = 2000) -> list[str]:
    """Split text into chunks of max_chars, trying to break at sentence boundaries."""
    if len(text) <= max_chars:
        return [text]
    
    chunks = []
    current = []
    current_len = 0
    
    sentences = re.split(r'(?<=[.!?])\s+', text)
    
    for sentence in sentences:
        sentence_len = len(sentence)
        
        if current_len + sentence_len > max_chars and current:
            chunks.append(" ".join(current))
            current = []
            current_len = 0
        
        current.append(sentence)
        current_len += sentence_len
    
    if current:
        chunks.append(" ".join(current))
    
    if any(len(c) > max_chars for c in chunks):
        chunks = [text[i:i+max_chars] for i in range(0, len(text), max_chars)]
    
    return chunks


def main():
    parser = argparse.ArgumentParser(description="Convert markdown book to combined WAV audio using InWorld TTS")
    parser.add_argument("input", help="Input markdown file (e.g., _books/Author/Book.md)")
    parser.add_argument("-o", "--output-dir", default=".", help="Output directory for WAV files")
    parser.add_argument("--voice-id", default="default-ghad8ngjnvrz1rh74yggug__josh", help="Voice ID to use (default: Josh)")
    parser.add_argument("--model", default="inworld-tts-1.5-max", help="Model ID (default: inworld-tts-1.5-max)")
    parser.add_argument("--api-key", default=os.getenv("INWORLD_API_KEY"), help="API key (or set INWORLD_API_KEY env var)")
    
    args = parser.parse_args()
    
    if not args.api_key:
        print("Error: --api-key required or set INWORLD_API_KEY environment variable", file=sys.stderr)
        sys.exit(1)
    
    # Read input
    with open(args.input, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Skip front matter
    if content.startswith("---"):
        end = content.find("---", 3)
        if end != -1:
            content = content[end + 3:]
    
    content = content.strip()
    
    if not content:
        print("Error: input file is empty", file=sys.stderr)
        sys.exit(1)
    
    # Parse chapters
    chapters = parse_chapters(content)
    print(f"Found {len(chapters)} chapters")
    
    # Create output directory
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Get base name from input file
    book_name = Path(args.input).stem
    
    all_pcm_data = []
    channels = sample_rate = bytes_per_sample = None
    
    chapter_num = 1
    
    for heading, text in chapters:
        if not text:
            continue
        
        full_text = f"{heading}. {text}"
        print(f"\n[{chapter_num}] {heading} ({len(text)} chars)")
        
        chunks = split_to_chunks(full_text, 2000)
        
        chapter_pcm_data = []
        for i, chunk in enumerate(chunks):
            if len(chunks) > 1:
                print(f"  Chunk {i+1}/{len(chunks)} ({len(chunk)} chars)...")
            else:
                print(f"  {len(chunk)} chars...")
            
            wav_data = synthesize(chunk, args.api_key, args.voice_id, args.model)
            
            pcm, ch, sr, bps = parse_wav(wav_data)
            if channels is None:
                channels, sample_rate, bytes_per_sample = ch, sr, bps
            
            chapter_pcm_data.append(pcm)
        
        chapter_pcm = b"".join(chapter_pcm_data)
        all_pcm_data.append(chapter_pcm)
        
        chapter_num += 1
    
    combined_pcm = b"".join(all_pcm_data)
    combined_wav = create_wav(combined_pcm, channels, sample_rate, bytes_per_sample)
    
    wav_filename = f"{book_name}.wav"
    with open(output_dir / wav_filename, "wb") as f:
        f.write(combined_wav)
    print(f"\nSaved: {wav_filename} ({len(combined_wav)} bytes)")
    
    print("\nDone!")


if __name__ == "__main__":
    main()