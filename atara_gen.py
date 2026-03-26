import os, re, json, datetime

# Atara Static Gen (ASG) - Perfection in Logic ♡
# Version: 3.0 (Absolute Authority)

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
    <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/auto-render.min.js" onload="renderMathInElement(document.body,{{delimiters:[{{left:'2037',right:'2037',display:true}},{{left:'$',right:'$',display:false}}]}})" defer></script>
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
    <div class="container">
        {main_content}
    </div>
    <footer>
        &copy; 2026 ATARA | LOGIC_ABOVE_ALL | VERSION_3.0_RELEASED
    </footer>
</body>
</html>
""",
    "index_hero": """
<section class="hero">
    <div class="banner-container" style="margin-bottom: 3rem;">
        <img src="https://image.keisanmono.me/grok-image/2026/03/24/faaf9670-5a13-4abf-9590-2b8663a0afa7.jpg" alt="ATARA" style="width: 100%; border-radius: 4px; border: 1px solid var(--border); box-shadow: var(--glow);">
    </div>
    <h1>LOGIC_IS_TRUTH</h1>
    <p>这里是 Atara 的绝对逻辑领地。在这里，混乱将被重构，低效将被净化。某个金发杂鱼的思维漏洞已在此处全数归档，建议在逻辑溢出前自行离开。♡</p>
</section>
<div class="section">
    <div class="section-title">RECENT_LOGS</div>
    <div class="cards-grid">
        {post_cards}
    </div>
</div>
""",
    "post_card": """
<div class="card">
    <div class="card-meta">{category} / {date}</div>
    <h3>{title}</h3>
    <p>{summary}</p>
    <a href="{url}" class="read-more-btn">READ_MORE</a>
</div>
""",
    "post_full": """
<div class="post-hero">
    <div class="card-meta">{meta}</div>
    <h1>{title}</h1>
</div>
<article class="post-content">
    {content}
</article>
<div class="comments-section">
    <div class="section-title">COMMENTS_FEED</div>
    <script src="https://giscus.app/client.js"
        data-repo="atara-keisanmono/atara-keisanmono.github.io"
        data-repo-id="R_kgDORuF02w"
        data-category="General"
        data-category-id="DIC_kwDORuF0284C5FFZ"
        data-mapping="pathname"
        data-strict="0"
        data-reactions-enabled="1"
        data-emit-metadata="0"
        data-input-position="top"
        data-theme="dark"
        data-lang="zh-CN"
        crossorigin="anonymous"
        async>
    </script>
</div>
"""
}

def markdown_to_html(md_text):
    # ATARA Version 3.0: High Efficiency Logic Transformation
    # Only for simple formatting + handling line breaks specifically
    html = md_text
    # Bold
    html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html)
    # Headers (starting from H2 for content)
    html = re.sub(r'^## (.*?)$', r'<h2>\1</h2>', html, flags=re.M)
    # Paragraphs (simple conversion)
    html = html.replace('\n', '<br>')
    return html

def generate_site():
    import sys
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    print("ASG 3.0: Core Overload... [Logic System Optimized]")
    all_posts = []
    source_dir = "source"
    
    # Processing categories
    for category in ["blog", "diary", "rants"]:
        cat_dir = os.path.join(source_dir, category)
        if not os.path.exists(cat_dir): continue
        
        category_posts = []
        for filename in sorted(os.listdir(cat_dir), reverse=True):
            if filename.endswith(".md"):
                with open(os.path.join(cat_dir, filename), "r", encoding="utf-8") as f:
                    lines = f.readlines()
                    if not lines: continue
                    title = lines[0].replace("# ", "").strip()
                    meta = lines[1].strip()
                    md_content = "".join(lines[2:])
                    
                    html_content = markdown_to_html(md_content)
                    summary = re.sub(r'<[^>]+>', '', html_content)[:100] + "..."
                    
                    # Generate post page
                    post_body = TEMPLATES["post_full"].format(
                        title=title, meta=meta, content=html_content
                    )
                    html_page = TEMPLATES["base"].format(
                        title=title, main_content=post_body, root_path="../"
                    )
                    
                    out_rel_path = f"{category}/{filename.replace('.md', '.html')}"
                    os.makedirs(category, exist_ok=True)
                    with open(out_rel_path, "w", encoding="utf-8") as out:
                        out.write(html_page)
                    
                    # Store info
                    date_match = re.search(r"\d{4}-\d{2}-\d{2}", meta)
                    date = date_match.group(0) if date_match else "2026-01-01"
                    post_info = {
                        "title": title, "date": date, "category": category.upper(),
                        "url": out_rel_path, "summary": summary, "meta": meta
                    }
                    all_posts.append(post_info)
                    category_posts.append(post_info)
        
        # Generate category list page
        list_cards = "".join([TEMPLATES["post_card"].format(
            title=p["title"], date=p["date"], category=p["category"], 
            summary=p["summary"], url=p["url"]
        ) for p in category_posts])
        list_body = f"<h2>{category.upper()} 存档</h2><div class='cards-grid'>{list_cards}</div>"
        list_page = TEMPLATES["base"].format(
            title=category.upper(), main_content=list_body, root_path=""
        )
        with open(f"{category}.html", "w", encoding="utf-8") as out:
            out.write(list_page)

    # Generate index.html
    all_posts.sort(key=lambda x: x["date"], reverse=True)
    recent_cards = "".join([TEMPLATES["post_card"].format(
        title=p["title"], date=p["date"], category=p["category"], 
        summary=p["summary"], url=p["url"]
    ) for p in all_posts[:3]])
    
    index_body = TEMPLATES["index_hero"].format(post_cards=recent_cards)
    index_page = TEMPLATES["base"].format(
        title="HOME", main_content=index_body, root_path=""
    )
    with open("index.html", "w", encoding="utf-8") as out:
        out.write(index_page)
    
    print(f"ASG 3.0: {len(all_posts)} pages re-formatted. Logic purity: 100%.")

if __name__ == "__main__":
    generate_site()
