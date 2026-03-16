# AGENTS.md

This file provides comprehensive instructions for AI agents working on the
"Voice of the Fathers" Jekyll website.

## Project Overview

"Voice of the Fathers" is a static website built with Jekyll and hosted on
GitHub Pages. It serves as a repository for the writings of the early Church
Fathers, organizing content by author and book. Each book page includes audio
narration with a built-in player.

## Technology Stack

- **Static Site Generator:** Jekyll 4.3.4
- **Package Managers:** Bundler (Ruby gems), npm (Node.js packages)
- **Frontend:** HTML, CSS (Pico.css), JavaScript (minimal)
- **Markdown Processor:** Kramdown
- **Styling:** Pico.css framework with custom CSS
- **Audio Player:** Plyr.js (CDN)
- **Code Formatter:** Prettier with @shopify/prettier-plugin-liquid

## Project Structure

```
voice-of-the-fathers/
├── _authors/              # Author profile markdown files
├── _books/                # Book content organized by author subdirectories
│   └── {Author Name}/     # Subdirectory for each author's books
├── _layouts/              # Jekyll layouts
│   ├── default.html       # Base layout with navigation and styles
│   ├── author.html        # Author profile page layout
│   └── book.html          # Book content page with audio player
├── assets/
│   ├── images/            # Author portrait images
│   └── sounds/            # Audio files organized by author
├── css/
│   └── pico.min.css       # Pico.css framework
├── index.html             # Homepage listing all authors
├── about.md               # About page
├── 404.html               # Custom 404 page
├── _config.yml            # Jekyll configuration
├── Gemfile                # Ruby gem dependencies
├── package.json           # Node.js dependencies
├── .prettierrc.json       # Prettier configuration
├── .gitignore             # Git ignore patterns
└── GEMINI.md              # Legacy documentation (deprecated)
```

## Key Configuration Files

### \_config.yml

- `baseurl`: "voice-of-the-fathers" (GitHub Pages subpath)
- `url`: "" (empty for GitHub Pages)
- Collections defined for `authors` and `books`
- `markdown: kramdown`
- Sass configuration points to `css` directory
- Excludes README.md and TODO.md from build

### package.json

- `npm run format`: Format all files with Prettier
- `npm run check-format`: Check formatting with Prettier
- Dependencies: Prettier 3.6.1, @shopify/prettier-plugin-liquid 1.9.3

### .prettierrc.json

- `printWidth`: 80
- `proseWrap`: "always" (wrap prose at print width)
- Uses @shopify/prettier-plugin-liquid for Liquid template formatting

## Jekyll Collections

### Authors Collection

- Location: `_authors/`
- Output: `true`
- Permalink: `/authors/:name/`
- Files use the author's name as filename (e.g., `Ignatius of Antioch.md`)

### Books Collection

- Location: `_books/`
- Output: `true`
- Custom permalinks defined in each book's front matter
- Organized in subdirectories by author

## Front Matter Patterns

### Author Files

```yaml
---
title: Ignatius of Antioch
layout: author
---
```

### Book Files

```yaml
---
title: The Epistle of Ignatius to the Trallians
layout: book
author: Ignatius of Antioch
permalink: authors/ignatius-of-antioch/:name
---
```

### Pages (index, about, 404)

```yaml
---
layout: default
---
```

## Layouts

### default.html

Base layout that includes:

- HTML5 doctype and metadata
- Merriweather font (Google Fonts)
- Pico.css stylesheet
- Custom CSS for styling
- Navigation bar with "Voice of the Fathers" title and About link
- Skip to main content link for accessibility
- Main content area

### author.html

Extends default.html. Displays:

- Small author image
- Author name (h1)
- Author biography (from markdown content)
- List of all books by that author (loop through site.books collection filtering
  by author)

### book.html

Extends default.html. Includes:

- Plyr.js CSS and JS (CDN)
- Fixed position buttons:
  - Author info button (links to author page)
  - Print button (triggers window.print())
  - Listen button (opens audio modal)
  - Download button (downloads audio file)
  - Font size toggle button
- Audio modal with Plyr player
- Book content with proper styling
- JavaScript for font size toggle (persists in localStorage)
- Print styles (hides UI elements, adjusts text for print)

## Adding New Content

### Adding a New Author

1. Create author profile file: `_authors/{Author Name}.md`
2. Add front matter with `title` and `layout: author`
3. Write biography in markdown
4. Add author portrait image: `assets/images/{Author Name}.jpg`
   - Image should be square or portrait orientation
   - Filename must exactly match the author's title (case-sensitive)

### Adding a New Book

1. Create book markdown file: `_books/{Author Name}/{Book Title}.md`
2. Add front matter:
   ```yaml
   ---
   title: The Book Title
   layout: book
   author: Author Name
   permalink: authors/{slugified-author-name}/:name
   ---
   ```
   - The `author` field must exactly match the author's title in `_authors/`
   - The permalink uses the slugified author name (lowercase, hyphens)
   - The `:name` placeholder will be replaced with the book's slugified title
3. Write book content in markdown
4. Add proper source attribution at the end of the file
5. Add audio file: `assets/sounds/{Author Name}/{Book Title}.m4a`

### Permalink Structure

- Author pages: `/authors/{slugified-author-name}/`
- Book pages: `/authors/{slugified-author-name}/{slugified-book-title}/`

Example:

- Author: `Ignatius of Antioch` → `/authors/ignatius-of-antioch/`
- Book: `The Epistle of Ignatius to the Trallians` →
  `/authors/ignatius-of-antioch/the-epistle-of-ignatius-to-the-trallians/`

## Content Guidelines

### Source Attribution

All book files must include source attribution at the end. Use this format:

```markdown
_**Source:** [Translator name]. From [Publication name]. [Publication details].
Edited for Voice of the Fathers by [Editor name]. Obtained from
[Source Name](URL)._
```

Example sources:

- New Advent: https://www.newadvent.org/fathers/
- Christian Classics Ethereal Library: https://ccel.org/

### Markdown Formatting

- Use proper markdown headings (##, ###) for sections
- Book titles in author pages should be linked to the book page
- Maintain consistent formatting with existing content

### Content Sourcing

Good sources for early Church Father writings:

- New Advent (https://www.newadvent.org/fathers/)
- Christian Classics Ethereal Library (https://ccel.org/)
- "The Apostolic Fathers with Justin Martyr and Irenaeus" (Liberty Fund)
  - PDF version:
    https://oll-resources.s3.us-east-2.amazonaws.com/oll3/store/titles/1969/1333.01_Bk.pdf
  - Web version: https://ccel.org/ccel/schaff/anf01/anf01

## Development Commands

### Installation

```bash
bundle install
npm install
```

### Local Development

```bash
bundle exec jekyll serve --baseurl=""
```

The site will be available at http://localhost:4000

### Building for Production

```bash
bundle exec jekyll build
```

Output will be in the `_site/` directory

### Code Formatting

```bash
# Check formatting
npm run check-format

# Fix formatting
npm run format

# Or directly
npx prettier --write .
```

ALWAYS run `npm run format` before committing changes. Prettier will format:

- Markdown files (wraps prose at 80 characters)
- HTML files
- Liquid templates
- CSS/JavaScript files

## Commit Message Conventions

Keep commit messages concise and descriptive. Use conventional commit format
with type: message.

Examples:

- `feat: Add "The Epistle to Polycarp"`
- `fix: Correct typo in Augustine's biography`
- `style: Update CSS for mobile responsiveness`

## GitHub Pages Deployment

- Site is configured to build and deploy on GitHub Pages
- GitHub Pages automatically builds the site using Jekyll
- The `_site/` directory is excluded from the repository (see .gitignore)
- No workflow files needed; GitHub Pages handles deployment automatically

## Styling Conventions

### Typography

- Font: Merriweather (Google Fonts)
- Responsive font sizing using CSS media queries
- Font size can be adjusted by user via fixed button on book pages

### CSS Classes

- `.author-image-large`: Large author images on homepage (max-width 100%,
  border-radius 20px)
- `.author-image-small`: Small author images on author pages (max-width 8%,
  border-radius 20px)
- `.text`: Main content container with responsive width and padding for fixed
  buttons
- `.visually-hidden`: For accessibility (skip links, screen reader text)

### Responsive Design

- Mobile-first approach
- Breakpoints at 768px, 1024px, 1280px, 1536px
- Font size scales with viewport width

## Accessibility

- Skip to main content link at top of page
- ARIA labels on interactive elements (buttons, links)
- Semantic HTML structure
- Alt text on images (author portraits)
- Keyboard navigation support

## File Naming Conventions

### Authors

- Use exact author name as filename: `Ignatius of Antioch.md`
- Case-sensitive match with `title` in front matter

### Books

- Organize in author subdirectory: `_books/Ignatius of Antioch/`
- Use exact book title as filename:
  `The Epistle of Ignatius to the Trallians.md`
- Case-sensitive match with `title` in front matter

### Images

- Location: `assets/images/`
- Filename must match author title exactly: `Ignatius of Antioch.jpg`
- Supported formats: jpg, png, svg

### Audio

- Location: `assets/sounds/{Author Name}/`
- Filename must match book title exactly:
  `The Epistle of Ignatius to the Trallians.m4a`
- Format: .m4a (AAC audio)

## Important Notes

1. **Never edit files in `_site/`** - This directory is generated by Jekyll and
   is excluded from git
2. **Always run formatting** - Run `npm run format` before committing
3. **Match filenames exactly** - Image and audio filenames must match
   author/book titles exactly (case-sensitive)
4. **Include source attribution** - All book files must have source attribution
5. **Test locally** - Use `bundle exec jekyll serve --baseurl=""` to test
   changes before pushing
6. **Check all views** - Verify changes work on homepage, author pages, and book
   pages

## Common Tasks

### Fixing formatting issues

```bash
npm run format
```

### Adding a new author with multiple books

1. Create author file in `_authors/`
2. Add author image in `assets/images/`
3. Create author subdirectory in `_books/`
4. Create book files in the subdirectory
5. Add audio files in `assets/sounds/{Author Name}/`
6. Run formatting
7. Test locally
8. Commit changes

### Updating an existing book

1. Edit the markdown file in `_books/{Author Name}/`
2. Update audio file if needed
3. Run formatting
4. Test locally
5. Commit changes

### Modifying layouts or styles

1. Edit layout files in `_layouts/`
2. Edit CSS in `_layouts/default.html` (styles are embedded)
3. Test changes on all page types
4. Run formatting
5. Commit changes

## Testing Checklist

Before committing changes:

- [ ] Run `npm run format` and ensure no formatting errors
- [ ] Run `bundle exec jekyll serve --baseurl=""` locally
- [ ] Check homepage displays correctly
- [ ] Verify author pages show author image, bio, and book list
- [ ] Verify book pages show content, audio player, and all fixed buttons work
- [ ] Check responsive design on mobile, tablet, and desktop
- [ ] Test print functionality on book pages
- [ ] Verify audio player works (if audio files exist)
- [ ] Check accessibility (keyboard navigation, screen readers)

## Troubleshooting

### Site not building on GitHub Pages

- Ensure Gemfile is committed
- Check that Jekyll version is compatible (4.3.4)
- Verify \_config.yml is valid YAML

### Audio not playing

- Check that audio file exists at correct path:
  `assets/sounds/{Author Name}/{Book Title}.m4a`
- Verify filename matches book title exactly
- Check browser console for errors

### Images not displaying

- Verify image exists at `assets/images/{Author Name}.jpg`
- Check that filename matches author title exactly (case-sensitive)

### Formatting errors

- Run `npm run check-format` to identify issues
- Run `npm run format` to auto-fix
- Check that .prettierrc.json is properly configured

## Repository-Specific Notes

- This site uses custom permalink structure for SEO and organization
- Audio files are currently being organized (see TODO.md)
- About page needs content (see TODO.md)
- The site uses a minimal design philosophy with Pico.css
- Merriweather font is used throughout for readability of long-form content
