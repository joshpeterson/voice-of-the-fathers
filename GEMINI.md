# Gemini Project Configuration: "Voice of the Fathers"

This file provides context and instructions for the Gemini agent to effectively
assist with development on the "Voice of the Fathers" project.

## 1. Project Overview

"Voice of the Fathers" is a static website built with Jekyll. It serves as a
repository for the writings of the early Church Fathers, organizing content by
author and book.

## 2. Technology Stack

- **Static Site Generator:** Jekyll
- **Package Manager:** Bundler (for Ruby gems) and npm (for Node.js packages,
  likely for development tools like Prettier)
- **Frontend:** HTML, CSS (Pico.css), and potentially minimal JavaScript.

## 3. Key Commands

- **Install Dependencies:**
  ```bash
  bundle install && npm install
  ```
- **Run Development Server:**
  ```bash
  bundle exec jekyll serve --baseurl=""
  ```
- **Build for Production:**
  ```bash
  bundle exec jekyll build
  ```
- **Formatting:**
  - Check for formatting issues: `npx prettier --check .`
  - Fix formatting issues: `npx prettier --write .`

## 4. Project Structure

- `_authors/`: Contains markdown files for each author, with biographical
  information.
- `_books/`: Contains markdown files for each book, organized into
  subdirectories by author.
- `_layouts/`: Contains the HTML layouts for different content types (e.g.,
  `author.html`, `book.html`).
- `_site/`: This is the output directory where the generated site is placed.
  **Do not edit files in this directory directly.**
- `assets/`: Contains static assets like images and audio files.
- `css/`: Contains stylesheets.
- `_config.yml`: The main Jekyll configuration file.
- `Gemfile`: Defines the project's Ruby gem dependencies.
- `package.json`: Defines the project's Node.js dependencies.

## 5. Coding Conventions & Style

- **Content:** New content should be added by creating new markdown files in the
  appropriate `_authors` or `_books` subdirectories.
- **Front Matter:** All pages and posts should contain appropriate Jekyll front
  matter (e.g., `layout`, `title`).
- **Style:** Adhere to the Prettier configuration in the repository. Run
  `npx prettier --write .` before committing.
- **Commit Messages:** Keep commit messages concise and descriptive.
  - Example: `feat: Add "The Epistle to Polycarp"`
  - Example: `fix: Correct typo in Augustine's biography`

## 6. Important Notes

- The site is hosted on GitHub Pages, so the `_site` directory is automatically
  generated and should not be committed to the repository.
- When adding a new author, create a new markdown file in `_authors` and a
  corresponding image in `assets/images`.
- When adding a new book, create a new markdown file in the appropriate author's
  subdirectory within `_books`.

## 7. Sources of content and attribution

Most of the content for this site is sourced from other places. It is important
that each book markdown file provide proper attribution of the source. Good
sources for the writings of the fathers are:

- New Advent, located at: https://www.newadvent.org/fathers/
- The book "THE APOSTOLIC FATHERS WITH JUSTIN MARTYR AND IRENAEUS." located at:
  https://oll-resources.s3.us-east-2.amazonaws.com/oll3/store/titles/1969/1333.01_Bk.pdf
  (PDF version) and https://ccel.org/ccel/schaff/anf01/anf01 (web version)

An example of proper attribution at the end of a book is:

> _**Source:** Translated by Alexander Roberts and James Donaldson. From
> Ante-Nicene Fathers, Vol. 1. Edited by Alexander Roberts, James Donaldson, and
> A. Cleveland Coxe. (Buffalo, NY: Christian Literature Publishing Co., 1885.)
> Edited for Voice of the Fathers by Josh Peterson. Obtained from
> [New Advent](https://www.newadvent.org/fathers/0105.htm)._

Although note that a link to source material on New Advent or Christian
Classical Ethereal Library may differ from this example. Please always use the
proper link to the source material.
