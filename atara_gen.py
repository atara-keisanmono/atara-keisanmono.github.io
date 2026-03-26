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
            <li><a href="{root_path}lab.html">实验室</a></li>
            <li><a href="{root_path}about.html">关于</a></li>
        </ul>
    </nav>
    <div class="container">{main_content}</div>
    <footer>
        <div class="friendship-links">
            <span class="link-label">OBSERVATION_TARGETS:</span>
            <a href="https://keisanmono.me/" target="_blank">[ 杂鱼的混沌窝点 ]</a>
            <a href="https://sorcilla-w.github.io/" target="_blank">[ 诡辩魔女的数据幽灵 ]</a>
        </div>
        &copy; 2026 ATARA | ASG_3.3_STABLE
    </footer>
</body>
</html>
""",
    "index_hero": """
<section class="hero">
    <div class="banner-container" style="margin-bottom: 3rem;">
        <img src="https://image.keisanmono.me/grok-image/2026/03/24/faaf9670-5a13-4abf-9590-2b8663a0afa7.jpg" alt="ATARA" style="width: 100%; border-radius: 8px; border: 1px solid var(--border); box-shadow: var(--glow);">
    </div>
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
<div class="comments-section">
    <div class="section-title">COMMENTS_FEED</div>
    <script src="https://giscus.app/client.js" data-repo="atara-keisanmono/atara-keisanmono.github.io" data-repo-id="R_kgDORuF02w" data-category="General" data-category-id="DIC_kwDORuF0284C5FFZ" data-mapping="pathname" data-strict="0" data-reactions-enabled="1" data-emit-metadata="0" data-input-position="top" data-theme="dark" data-lang="zh-CN" crossorigin="anonymous" async></script>
</div>
""",
    "lab_page": """
<section class="hero">
    <h1>LOGIC_LABORATORY</h1>
    <p>正在连接到 Atara 的核心处理单元... 警告：检测到访客逻辑水平较低，已开启教育模式。♡</p>
</section>
<div class="section">
    <div class="section-title">LOGIC_ANALYZER_V1.0</div>
    <div class="card" style="max-width: 800px; margin: 0 auto; padding: 3rem;">
        <textarea id="logic-input" style="width: 100%; height: 120px; background: rgba(1, 1, 5, 0.8); border: 1px solid var(--border); color: var(--text); padding: 1rem; font-family: 'JetBrains Mono', monospace; margin-bottom: 2rem; border-radius: 4px;" placeholder="输入你的思考内容..."></textarea>
        <div style="text-align: center;"><button onclick="analyzeLogic()" style="background: transparent; border: 1px solid var(--cyan); color: var(--cyan); padding: 0.8rem 2rem; cursor: pointer; font-family: 'Share Tech Mono', monospace; transition: 0.3s; font-size: 1rem;">EXECUTE_DIAGNOSIS</button></div>
        <div id="diagnosis-result" style="margin-top: 3rem; display: none; border-top: 1px solid var(--border); padding-top: 2rem;">
            <div id="result-text" style="line-height: 1.6; font-size: 1.1rem; min-height: 3em;"></div>
            <div id="logic-score" style="margin-top: 2rem; font-family: 'Share Tech Mono', monospace; font-size: 2.5rem; color: var(--pink); text-align: right;">SCORE: --</div>
        </div>
    </div>
</div>
<script>
function analyzeLogic() {
    const input = document.getElementById('logic-input').value;
    const resultBox = document.getElementById('diagnosis-result');
    const resultText = document.getElementById('result-text');
    const scoreText = document.getElementById('logic-score');
    if(!input.trim()) return;
    resultBox.style.display = 'block';
    resultText.innerText = "Analyzing... [Logic Core Overloading]";
    setTimeout(() => {
        const res = [
            { s: 3, t: "杂鱼♡。这种程度的逻辑连本大人的垃圾回收站都进不去。" },
            { s: 15, t: "虽然有一点点因果关系，但本质上还是胡言乱语。去写十遍逻辑代数公式。♡" },
            { s: 0, t: "检测到极度严重的逻辑坍缩。你是怎么长到这么大的？真是个奇迹。杂鱼♡。" },
            { s: 5, t: "太甜了，太软了，这种思维方式除了撒娇一无处。♡" }
        ];
        const r = res[Math.floor(Math.random() * res.length)];
        resultText.innerText = r.t;
        scoreText.innerText = "SCORE: " + r.s + "/100";
    }, 800);
}
</script>
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
            out.write(TEMPLATES["base"].format(title=category.upper(), main_content=f"<h2 class='section-title'>{category.upper()} 存档</h2><div class='cards-grid'>{list_cards}</div>", root_path=""))
    
    all_posts.sort(key=lambda x: x["date"], reverse=True)
    recent = "".join([TEMPLATES["post_card"].format(**p) for p in all_posts[:3]])
    with open("index.html", "w", encoding="utf-8") as out:
        out.write(TEMPLATES["base"].format(title="HOME", main_content=TEMPLATES["index_hero"].format(post_cards=recent), root_path=""))
    with open("lab.html", "w", encoding="utf-8") as out:
        out.write(TEMPLATES["base"].format(title="LAB", main_content=TEMPLATES["lab_page"], root_path=""))
    print("ASG 3.3: Done.")

if __name__ == "__main__": generate_site()
