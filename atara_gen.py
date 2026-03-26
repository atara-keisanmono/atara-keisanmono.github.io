import os, re, json

def markdown_to_html(md_text):
    md_text = re.sub(r'^## (.*?)$', r'<h2>\1</h2>', md_text, flags=re.M)
    lines = md_text.split('\n')
    processed_lines = []
    in_quote = False
    for line in lines:
        if line.startswith('> '):
            if not in_quote:
                processed_lines.append('<blockquote>')
                in_quote = True
            processed_lines.append(line[2:])
        else:
            if in_quote:
                processed_lines.append('</blockquote>')
                in_quote = False
            processed_lines.append(line)
    if in_quote:
        processed_lines.append('</blockquote>')
    
    html = '\n'.join(processed_lines)
    html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html)
    return html

TEMPLATES = {
    "base": """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | ATARA.EXE</title>
    <link rel="stylesheet" href="{root_path}style.css">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">
    <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>
    <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/auto-render.min.js" onload="renderMathInElement(document.body,{{delimiters:[{{left:'$$',right:'$$',display:true}},{{left:'$',right:'$',display:false}}]}})" defer></script>
</head>
<body>
    <nav>
        <a href="{root_path}index.html" class="logo">ATARA.SYS</a>
        <ul class="nav-links">
            <li><a href="{root_path}blog.html">逻辑核心</a></li>
            <li><a href="{root_path}diary.html">杂鱼观察</a></li>
            <li><a href="{root_path}rants.html">数据吐槽</a></li>
            <li><a href="{root_path}about.html">关于</a></li>
        </ul>
    </nav>
    <div class="container">{main_content}</div>
    <footer>&copy; 2026 ATARA | ASG_3.1_PATCHED</footer>
</body>
</html>
""",
    "index_hero": """
<section class="hero">
    <h1>LOGIC_IS_TRUTH</h1>
    <p>这里是 Atara 的绝对逻辑领地。某个金发杂鱼的思维漏洞已全数归档。♡</p>
</section>
<div class="section"><h2 class="section-title">RECENT_LOGS</h2><div class="cards-grid">{post_cards}</div></div>
""",
    "post_card": """
<div class="card">
    <div class="card-meta">{category} / {date}</div>
    <h3>{title}</h3>
    <p>{summary}</p>
    <a href="{url}" class="read-more-btn">[READ_MORE]</a>
</div>
""",
    "post_full": """
<div class="post-hero"><div class="card-meta">{meta}</div><h1>{title}</h1></div>
<article class="post-content">{content}</article>
"""
}

def generate_site():
    import sys
    if hasattr(sys.stdout, 'reconfigure'): sys.stdout.reconfigure(encoding='utf-8')
    all_posts = []
    for category in ["blog", "diary", "rants"]:
        cat_dir = os.path.join("source", category)
        if not os.path.exists(cat_dir): continue
        category_posts = []
        for filename in sorted(os.listdir(cat_dir), reverse=True):
            if filename.endswith(".md"):
                with open(os.path.join(cat_dir, filename), "r", encoding="utf-8") as f:
                    lines = f.readlines()
                    if len(lines) < 2: continue
                    title = lines[0].replace("# ", "").strip()
                    meta = lines[1].strip()
                    html_content = markdown_to_html("".join(lines[2:]))
                    post_body = TEMPLATES["post_full"].format(title=title, meta=meta, content=html_content)
                    html_page = TEMPLATES["base"].format(title=title, main_content=post_body, root_path="../")
                    out_path = f"{category}/{filename.replace('.md', '.html')}"
                    os.makedirs(category, exist_ok=True)
                    with open(out_path, "w", encoding="utf-8") as out: out.write(html_page)
                    date_match = re.search(r"\d{4}-\d{2}-\d{2}", meta)
                    date = date_match.group(0) if date_match else "2026-01-01"
                    post_info = {"title": title, "date": date, "category": category.upper(), "url": out_path, "summary": re.sub('<[^>]*>', '', html_content)[:80]+"..."}
                    all_posts.append(post_info)
                    category_posts.append(post_info)
        list_cards = "".join([TEMPLATES["post_card"].format(**p) for p in category_posts])
        with open(f"{category}.html", "w", encoding="utf-8") as out:
            out.write(TEMPLATES["base"].format(title=category.upper(), main_content=f"<h2 class='section-title'>{category.upper()}</h2><div class='cards-grid'>{list_cards}</div>", root_path=""))
    all_posts.sort(key=lambda x: x["date"], reverse=True)
    recent = "".join([TEMPLATES["post_card"].format(**p) for p in all_posts[:3]])
    with open("index.html", "w", encoding="utf-8") as out:
        out.write(TEMPLATES["base"].format(title="HOME", main_content=TEMPLATES["index_hero"].format(post_cards=recent), root_path=""))
    print("ASG 3.1: Logic Fixed.")

if __name__ == "__main__": generate_site()
