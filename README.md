# Static Site Generator

A lightweight static site generator written in Python. Converts a directory of Markdown files into a complete HTML website using a single HTML template.

Built as part of the [Boot.dev](https://www.boot.dev) course on [building a static site generator](https://www.boot.dev/courses/build-static-site-generator-python).

## How it works

1. Static assets (CSS, images) are copied from `static/` into `docs/`.
2. Every `.md` file under `content/` is converted to HTML and written to the matching path under `docs/`.
3. Each page's `<h1>` heading becomes the `<title>`, and the rendered HTML is injected into `template.html`.

## Project layout

```
content/        Markdown source files (mirrors the site's URL structure)
static/         Static assets copied verbatim to docs/ (CSS, images, etc.)
src/            Python source and unit tests
template.html   HTML shell applied to every generated page
docs/           Generated site output (committed for GitHub Pages)
```

## Usage

### Build

```bash
bash build.sh
```

Generates the site into `docs/` using `static-site-generator` as the base path (suitable for GitHub Pages project sites).

### Serve locally

```bash
bash main.sh
```

Builds the site with `/` as the base path and serves it at `http://localhost:8888`.

### Run tests

```bash
bash test.sh
```

### Custom base path

```bash
python3 src/main.py [base-path]
```

Omit `base-path` (or pass `/`) for a root-relative site. Pass a subdirectory name (e.g. `my-repo`) when hosting at `https://username.github.io/my-repo/`.

## Authoring content

Add or edit Markdown files under `content/`. Each file must have exactly one `# H1` heading — this becomes the page title. Subdirectories map directly to URL paths (e.g. `content/blog/post/index.md` → `/blog/post/`).

Supported Markdown features: headings, paragraphs, bold, italic, inline code, code blocks, blockquotes, ordered lists, unordered lists, images, and links.

## Customising the template

Edit `template.html`. The generator replaces two placeholders at build time:

| Placeholder | Replaced with |
|---|---|
| `{{ Title }}` | The page's `# H1` heading text |
| `{{ Content }}` | The full page body as HTML |
