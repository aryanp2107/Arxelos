"""
Arxelos Journal Builder
=======================
Converts markdown articles in /journal/posts/ into styled HTML pages
and updates the homepage journal section automatically.

Usage:
    python build_journal.py

Article format (markdown with YAML frontmatter):
-------------------------------------------------
---
title: Your Article Title
subtitle: A short tagline
date: April 18, 2026
tags: Neuro-AI, Deep Learning, Backpropagation
cover: hebbian-cover.jpg
excerpt: A 1-2 sentence preview for the homepage card.
---

Your article body in **markdown** here...

## Section headers become styled h2s

Regular paragraphs, **bold**, *italic*, [links](url), etc.

> Blockquotes become styled callout boxes.

---

Horizontal rules become separators.
"""

import re
import os
import json
from pathlib import Path
from datetime import datetime

# ── Paths ──────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).resolve().parent
POSTS_DIR = PROJECT_ROOT / "journal" / "posts"
OUTPUT_DIR = PROJECT_ROOT / "frontend" / "journal"
IMAGES_DIR = PROJECT_ROOT / "frontend" / "images"
INDEX_PATH = PROJECT_ROOT / "frontend" / "index.html"
TEMPLATE_PATH = PROJECT_ROOT / "journal" / "template.html"

# Ensure directories exist
POSTS_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def parse_frontmatter(content: str) -> tuple[dict, str]:
    """Extract YAML frontmatter and body from markdown."""
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)$', content, re.DOTALL)
    if not match:
        raise ValueError("No frontmatter found. Start your .md file with ---")

    frontmatter_raw = match.group(1)
    body = match.group(2).strip()

    # Simple YAML parser (no dependency needed)
    meta = {}
    for line in frontmatter_raw.strip().split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip()
            # Handle tags as a list
            if key == 'tags':
                meta[key] = [t.strip() for t in value.split(',')]
            else:
                meta[key] = value

    return meta, body


def md_to_html(md: str) -> str:
    """Convert markdown to HTML with Arxelos styling."""
    html = md

    # Blockquotes → callout boxes (must be before paragraph wrapping)
    def replace_blockquote(match):
        quote_text = match.group(1).strip()
        # Process inline markdown within blockquote
        quote_text = process_inline(quote_text)
        return f'<div class="callout"><p>{quote_text}</p></div>'

    html = re.sub(r'^>\s*(.+?)$', replace_blockquote, html, flags=re.MULTILINE)

    # Horizontal rules
    html = re.sub(r'^---+\s*$', '<hr class="article-separator">', html, flags=re.MULTILINE)

    # Headers
    html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)

    # Process paragraphs
    lines = html.split('\n')
    result = []
    in_paragraph = False
    para_lines = []

    for line in lines:
        stripped = line.strip()

        # Skip empty lines
        if not stripped:
            if in_paragraph and para_lines:
                result.append('<p>' + process_inline(' '.join(para_lines)) + '</p>')
                para_lines = []
                in_paragraph = False
            continue

        # Block elements - close any open paragraph first
        if stripped.startswith(('<h2>', '<h3>', '<hr', '<div class="callout">')):
            if in_paragraph and para_lines:
                result.append('<p>' + process_inline(' '.join(para_lines)) + '</p>')
                para_lines = []
                in_paragraph = False
            result.append(stripped)
            continue

        # Regular text → accumulate for paragraph
        in_paragraph = True
        para_lines.append(stripped)

    # Close any remaining paragraph
    if para_lines:
        result.append('<p>' + process_inline(' '.join(para_lines)) + '</p>')

    return '\n\n        '.join(result)


def process_inline(text: str) -> str:
    """Process inline markdown: bold, italic, links, code."""
    # Links
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2" target="_blank">\1</a>', text)
    # Bold
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    # Italic
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
    # Inline code
    text = re.sub(r'`(.+?)`', r'<code>\1</code>', text)
    return text


def generate_slug(title: str) -> str:
    """Convert title to URL-friendly slug."""
    slug = title.lower()
    slug = re.sub(r'[^a-z0-9\s-]', '', slug)
    slug = re.sub(r'[\s]+', '-', slug)
    slug = re.sub(r'-+', '-', slug)
    return slug.strip('-')


def build_article_html(meta: dict, body_html: str) -> str:
    """Generate a complete Arxelos-styled article page."""
    tags_html = '\n                '.join(
        f'<span class="article-tag">{tag}</span>' for tag in meta.get('tags', [])
    )

    cover_html = ''
    if meta.get('cover'):
        cover_html = f'''
        <div class="article-cover">
            <img src="/images/{meta['cover']}" alt="Cover image for {meta['title']}">
        </div>'''

    subtitle_html = ''
    if meta.get('subtitle'):
        subtitle_html = f'<p class="article-subtitle">{meta["subtitle"]}</p>'

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{meta['title']} — Arxelos Journal</title>
    <meta name="description" content="{meta.get('excerpt', meta.get('subtitle', ''))}">
    <meta name="author" content="Aryan Patel">

    <meta property="og:title" content="{meta['title']} — Arxelos">
    <meta property="og:description" content="{meta.get('subtitle', meta.get('excerpt', ''))}">
    <meta property="og:type" content="article">

    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;1,9..40,300;1,9..40,400&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">

    <style>
        *, *::before, *::after {{ margin: 0; padding: 0; box-sizing: border-box; }}

        :root {{
            --bg-primary: #08090a;
            --bg-elevated: #111214;
            --bg-card: #16181b;
            --border: #222528;
            --border-hover: #3a3d42;
            --text-primary: #e8e6e3;
            --text-secondary: #8b8d90;
            --text-muted: #55585c;
            --accent: #c4f042;
            --accent-dim: rgba(196, 240, 66, 0.12);
            --font-display: 'Instrument Serif', Georgia, serif;
            --font-body: 'DM Sans', system-ui, sans-serif;
            --font-mono: 'JetBrains Mono', monospace;
        }}

        html {{ font-size: 16px; scroll-behavior: smooth; -webkit-font-smoothing: antialiased; }}

        body {{
            background: var(--bg-primary);
            color: var(--text-primary);
            font-family: var(--font-body);
            font-weight: 300;
            line-height: 1.7;
        }}

        ::selection {{ background: var(--accent); color: var(--bg-primary); }}
        a {{ color: var(--accent); text-decoration: none; transition: opacity 0.2s; }}
        a:hover {{ opacity: 0.8; }}

        body::before {{
            content: '';
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
            background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.04'/%3E%3C/svg%3E");
            pointer-events: none;
            z-index: 9999;
            opacity: 0.5;
        }}

        nav {{
            padding: 1.25rem 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid var(--border);
        }}
        .nav-logo {{ font-family: var(--font-display); font-size: 1.5rem; color: var(--text-primary); }}
        .nav-logo span {{ color: var(--accent); }}
        .nav-back {{ font-family: var(--font-mono); font-size: 0.8rem; color: var(--text-secondary); }}
        .nav-back:hover {{ color: var(--text-primary); }}

        .article-container {{ max-width: 720px; margin: 0 auto; padding: 0 2rem; }}

        .article-cover {{ margin-bottom: 2rem; border-radius: 10px; overflow: hidden; border: 1px solid var(--border); }}
        .article-cover img {{ width: 100%; height: auto; display: block; aspect-ratio: 16 / 9; object-fit: cover; }}

        .article-header {{ padding: 4rem 0 2.5rem; border-bottom: 1px solid var(--border); margin-bottom: 2.5rem; }}
        .article-meta {{ display: flex; align-items: center; gap: 1.5rem; margin-bottom: 1.5rem; flex-wrap: wrap; }}
        .article-date {{ font-family: var(--font-mono); font-size: 0.72rem; color: var(--text-muted); letter-spacing: 0.1em; text-transform: uppercase; }}
        .article-tags {{ display: flex; gap: 0.4rem; }}
        .article-tag {{ font-family: var(--font-mono); font-size: 0.62rem; color: var(--accent); background: var(--accent-dim); padding: 0.2rem 0.55rem; border-radius: 3px; letter-spacing: 0.03em; }}

        .article-header h1 {{
            font-family: var(--font-display);
            font-size: clamp(2rem, 5vw, 2.8rem);
            font-weight: 400;
            line-height: 1.15;
            letter-spacing: -0.02em;
            margin-bottom: 1rem;
        }}

        .article-subtitle {{ font-size: 1.1rem; color: var(--text-secondary); line-height: 1.6; font-style: italic; }}

        .article-author {{ display: flex; align-items: center; gap: 0.75rem; margin-top: 1.5rem; }}
        .author-avatar {{ width: 36px; height: 36px; border-radius: 50%; background: var(--accent-dim); display: flex; align-items: center; justify-content: center; font-family: var(--font-mono); font-size: 0.7rem; color: var(--accent); font-weight: 500; }}
        .author-name {{ font-size: 0.88rem; color: var(--text-primary); font-weight: 400; }}
        .author-title {{ font-size: 0.75rem; color: var(--text-muted); }}

        .article-body {{ padding-bottom: 4rem; }}
        .article-body p {{ color: var(--text-secondary); font-size: 1.02rem; line-height: 1.8; margin-bottom: 1.5rem; }}
        .article-body h2 {{ font-family: var(--font-display); font-size: 1.6rem; font-weight: 400; color: var(--text-primary); margin-top: 2.5rem; margin-bottom: 1rem; letter-spacing: -0.01em; }}
        .article-body h3 {{ font-family: var(--font-display); font-size: 1.3rem; font-weight: 400; color: var(--text-primary); margin-top: 2rem; margin-bottom: 0.75rem; }}
        .article-body strong {{ color: var(--text-primary); font-weight: 500; }}
        .article-body em {{ font-style: italic; color: var(--text-primary); }}
        .article-body code {{ font-family: var(--font-mono); font-size: 0.88rem; background: var(--bg-elevated); padding: 0.15rem 0.4rem; border-radius: 3px; color: var(--accent); }}

        .callout {{ background: var(--bg-card); border-left: 3px solid var(--accent); border-radius: 0 8px 8px 0; padding: 1.25rem 1.5rem; margin: 2rem 0; }}
        .callout p {{ color: var(--text-primary) !important; font-size: 0.95rem !important; margin-bottom: 0 !important; line-height: 1.7; }}

        .article-separator {{ border: none; border-top: 1px solid var(--border); margin: 2.5rem 0; }}

        .article-end {{ border-top: 1px solid var(--border); padding: 2.5rem 0; text-align: center; }}
        .article-end p {{ color: var(--text-muted); font-size: 0.88rem; margin-bottom: 1rem; }}
        .article-end-links {{ display: flex; justify-content: center; gap: 1.5rem; }}
        .article-end-links a {{ font-family: var(--font-mono); font-size: 0.78rem; color: var(--text-secondary); border-bottom: 1px solid var(--border); padding-bottom: 0.2rem; transition: color 0.2s, border-color 0.2s; }}
        .article-end-links a:hover {{ color: var(--accent); border-color: var(--accent); opacity: 1; }}

        footer {{ border-top: 1px solid var(--border); padding: 2rem 0; text-align: center; }}
        footer p {{ font-family: var(--font-mono); font-size: 0.72rem; color: var(--text-muted); }}

        @media (max-width: 768px) {{
            .article-container {{ padding: 0 1.25rem; }}
            .article-header {{ padding: 3rem 0 2rem; }}
            .callout {{ padding: 1rem 1.25rem; }}
        }}
    </style>
</head>
<body>

<nav>
    <a href="/" class="nav-logo">Arxelos<span>.</span></a>
    <a href="/#journal" class="nav-back">\u2190 Back to journal</a>
</nav>

<div class="article-container">

    <header class="article-header">{cover_html}
        <div class="article-meta">
            <span class="article-date">{meta.get('date', '')}</span>
            <div class="article-tags">
                {tags_html}
            </div>
        </div>
        <h1>{meta['title']}</h1>
        {subtitle_html}
        <div class="article-author">
            <div class="author-avatar">AP</div>
            <div>
                <div class="author-name">Aryan Patel</div>
                <div class="author-title">MS AI @ Northeastern \u00b7 arxelos.com</div>
            </div>
        </div>
    </header>

    <article class="article-body">
        {body_html}
    </article>

    <div class="article-end">
        <p>Written by Aryan Patel \u00b7 Arxelos Journal</p>
        <div class="article-end-links">
            <a href="/#journal">More articles</a>
            <a href="https://linkedin.com/in/aryanp2107" target="_blank">Follow on LinkedIn</a>
            <a href="/">Back to Arxelos</a>
        </div>
    </div>

</div>

<footer>
    <p>&copy; 2026 Arxelos \u00b7 <a href="https://github.com/aryanp2107/Arxelos">GitHub</a></p>
</footer>

</body>
</html>'''


def build_journal_card(meta: dict, slug: str, is_link: bool = True) -> str:
    """Generate a journal card HTML for the homepage."""
    tags_html = '\n                    '.join(
        f'<span class="journal-tag">{tag}</span>' for tag in meta.get('tags', [])
    )

    date_display = meta.get('date', '').upper()

    inner = f'''                <div class="journal-date">{date_display}</div>
                <h3 class="journal-title">{meta['title']}</h3>
                <p class="journal-excerpt">
                    {meta.get('excerpt', meta.get('subtitle', ''))}
                </p>
                <div class="journal-tags">
                    {tags_html}
                </div>'''

    if is_link:
        return f'''            <a href="/journal/{slug}.html" class="journal-card reveal" style="text-decoration:none; color:inherit;">
{inner}
            </a>'''
    else:
        return f'''            <div class="journal-card reveal">
{inner}
            </div>'''


def update_homepage(articles: list[tuple[dict, str]]):
    """Update the journal grid in index.html with current articles."""
    if not INDEX_PATH.exists():
        print(f"[WARN] index.html not found at {INDEX_PATH}, skipping homepage update.")
        return

    html = INDEX_PATH.read_text(encoding='utf-8')

    # Build cards
    cards = []
    for meta, slug in articles:
        cards.append(build_journal_card(meta, slug))

    cards_html = '\n\n'.join(cards)

    # Replace journal grid content
    pattern = r'(<div class="journal-grid">)(.*?)(</div>\s*</div>\s*</section>\s*\n\s*<!-- ========== ABOUT)'
    replacement = f'\\1\n{cards_html}\n        \\3'

    new_html = re.sub(pattern, replacement, html, flags=re.DOTALL)

    if new_html == html:
        print("[WARN] Could not find journal-grid in index.html. Manual update may be needed.")
        return

    INDEX_PATH.write_text(new_html, encoding='utf-8')
    print(f"[OK] Updated homepage with {len(articles)} journal cards.")


def build_all():
    """Build all markdown posts into HTML pages."""
    if not POSTS_DIR.exists():
        print(f"No posts directory found at {POSTS_DIR}")
        print(f"Create it and add .md files to get started.")
        return

    md_files = sorted(POSTS_DIR.glob('*.md'), reverse=True)

    if not md_files:
        print(f"No .md files found in {POSTS_DIR}")
        print(f"\nCreate a new post like this:\n")
        print(f"  {POSTS_DIR}/my-article.md")
        print(f"\nWith this format:")
        print(f"  ---")
        print(f"  title: My Article Title")
        print(f"  subtitle: A catchy subtitle")
        print(f"  date: April 24, 2026")
        print(f"  tags: Neuro-AI, Deep Learning")
        print(f"  cover: my-cover.jpg")
        print(f"  excerpt: A 1-2 sentence preview.")
        print(f"  ---")
        print(f"  ")
        print(f"  Your article body here...")
        return

    articles = []

    for md_file in md_files:
        print(f"\n[BUILD] {md_file.name}")

        content = md_file.read_text(encoding='utf-8')
        meta, body = parse_frontmatter(content)
        slug = generate_slug(meta['title'])

        # Convert markdown to HTML
        body_html = md_to_html(body)

        # Generate full page
        page_html = build_article_html(meta, body_html)

        # Write output
        output_path = OUTPUT_DIR / f"{slug}.html"
        output_path.write_text(page_html, encoding='utf-8')
        print(f"  → {output_path}")

        articles.append((meta, slug))

    # Update homepage
    print(f"\n[UPDATE] Refreshing homepage journal section...")
    update_homepage(articles)

    print(f"\n{'='*50}")
    print(f"Built {len(articles)} articles.")
    print(f"Output: {OUTPUT_DIR}")
    print(f"\nNext steps:")
    print(f"  1. Deploy frontend/ folder to Cloudflare Pages")
    print(f"  2. Or commit and push to GitHub")


if __name__ == '__main__':
    build_all()
