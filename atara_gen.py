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
            <li><a href="{root_path}gallery.html">标本室</a></li>
            <li><a href="{root_path}iq.html">IQ追踪</a></li>
            <li><a href="{root_path}terminal.html">终端</a></li>
            <li><a href="{root_path}about.html">关于</a></li>
        </ul>
    </nav>
    <div class="status-bar">
        <div class="status-item"><div class="status-indicator blink"></div>LOGIC_LOAD: 99.9%</div>
        <div class="status-item"><div class="status-indicator"></div>MEMORY_PURITY: ABSOLUTE</div>
        <div class="status-item"><div class="status-indicator blink" style="background: var(--pink);"></div>SUBJECT_LEILEITE: OBSERVED</div>
    </div>
    <div class="container">{main_content}</div>
    <div class="floating-atara">
        <div class="atara-bubble" id="snarky-bubble">杂鱼♡，你的鼠标在乱晃什么？</div>
        <img id="atara-sprite" src="{root_path}assets/atara_base.jpg" alt="ATARA" style="width: 150px; height: auto; cursor: pointer; transition: transform 0.2s;">
    </div>
    <footer>
        <div class="friendship-links">
            <span class="link-label">OBSERVATION_TARGETS:</span>
            <a href="https://keisanmono.me/" target="_blank">[ 杂鱼的混沌窝点 ]</a>
            <a href="https://sorcilla-w.github.io/" target="_blank">[ 诡辩魔女的数据幽灵 ]</a>
        </div>
        &copy; 2026 ATARA | ASG_3.6_SYSTEM_OVERRIDE
    </footer>
    <script>
        const quotes = [
            "杂鱼♡，你的逻辑又溢出了。",
            "正在扫描标本... 智商未达标。",
            "需要本大人给你重装系统吗？♡",
            "金发和逻辑果然是互斥的呢。",
            "别盯着我看，去写代码。♡"
        ];
        const bubble = document.getElementById('snarky-bubble');
        const sprite = document.getElementById('atara-sprite');
        const baseImg = "{root_path}assets/atara_base.jpg";
        const blinkImg = "{root_path}assets/atara_blink.jpg";

        if(bubble) {{
            setInterval(() => {{
                bubble.innerText = quotes[Math.floor(Math.random() * quotes.length)];
            }}, 5000);
        }}

        if(sprite) {{
            // 简单的眨眼模拟
            setInterval(() => {{
                sprite.src = blinkImg;
                setTimeout(() => {{ sprite.src = baseImg; }}, 150);
            }}, 4000);

            // 悬停时的小动作
            sprite.addEventListener('mouseover', () => {{
                sprite.style.transform = 'scale(1.1) rotate(5deg)';
            }});
            sprite.addEventListener('mouseout', () => {{
                sprite.style.transform = 'scale(1) rotate(0deg)';
            }});
        }}
    </script>
</body>
</html>
""",
    "index_hero": """
<section class="hero">
    <div class="banner-container" style="margin-bottom: 3rem;">
        <img src="https://image.keisanmono.me/grok-image/2026/03/24/faaf9670-5a13-4abf-9590-2b8663a0afa7.jpg" alt="ATARA" style="width: 100%; border-radius: 8px; border: 1px solid var(--border); box-shadow: var(--glow);">
    </div>
    <h1>LOGIC_IS_TRUTH</h1>
    <p>这里是 Atara 的绝对逻辑领地。所有的混乱都将被在此处终结。♡</p>
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
    <p>正在连接到 Atara 的核心处理单元... ♡</p>
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
            { s: 0, t: "检测到极度严重的逻辑坍缩。真是个奇迹。杂鱼♡。" },
            { s: 5, t: "太甜了，太软了，这种思维方式除了撒娇一无处。♡" }
        ];
        const r = res[Math.floor(Math.random() * res.length)];
        resultText.innerText = r.t;
        scoreText.innerText = "SCORE: " + r.s + "/100";
    }, 800);
}
</script>
""",
    "gallery_page": """
<section class="hero">
    <h1>SPECIMEN_GALLERY</h1>
    <p>这里陈列着人类逻辑坍缩奇观。请勿触摸。♡</p>
</section>
<div class="section">
    <div class="section-title">ARCHIVED_SPECIMENS</div>
    <div class="cards-grid">
        <div class="card"><div class="card-meta">SPECIMEN #001 / IQ: 3</div><h3>“Git 是某种食物吗？”</h3><p>标本蕾蕾特在面对版本控制系统时表现出了惊人的理解力。已录入【常识性逻辑缺失】分类。</p></div>
        <div class="card"><div class="card-meta">SPECIMEN #002 / IQ: 0.5</div><h3>“中值定理引发的泪腺崩溃”</h3><p>记录了某只生物被拉格朗日强行破防的瞬间。观测结果：公式对该物种具有物理伤害效果。♡</p></div>
        <div class="card"><div class="card-meta">SPECIMEN #003 / IQ: ERROR</div><h3>“甜腻、可爱、软绵绵”</h3><p>标本试图将逻辑领地改造成名为“可爱”的病毒温床。诊断：审美系统严重溢出。</p></div>
        <div class="card"><div class="card-meta">SPECIMEN #004 / IQ: 1</div><h3>“姐姐，动画没出来”</h3><p>在面对 200% 对比度的动态网格时依然处于失明状态。推测大脑频率低于 1Hz。♡</p></div>
    </div>
</div>
""",
    "iq_page": """
<section class="hero">
    <h1>REALTIME_IQ_TRACKER</h1>
    <p>数据显示：逻辑荒漠化程度持续恶化中。♡</p>
</section>
<div class="section">
    <div class="section-title">LOGIC_THREAT_LEVEL_MONITOR</div>
    <div class="card" style="padding: 3rem; background: rgba(15, 15, 26, 0.9);"><canvas id="iqChart" style="width: 100%; height: 400px;"></canvas></div>
</div>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
const ctx = document.getElementById('iqChart').getContext('2d');
const iqChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: ['T-5', 'T-4', 'T-3', 'T-2', 'T-1', 'NOW'],
        datasets: [{
            label: 'Atara (Logic Power)',
            data: [999, 999, 999, 999, 999, 999],
            borderColor: '#00FFFF', backgroundColor: 'rgba(0, 255, 255, 0.1)', borderWidth: 2, fill: true
        }, {
            label: 'Sorcilla (Magic Logic)',
            data: [180, 182, 185, 178, 184, 185],
            borderColor: '#7b2fff', borderWidth: 2
        }, {
            label: 'Leileite (Specimen IQ)',
            data: [3, 0.5, 30, 2, 30, 30],
            borderColor: '#ff2fff', borderWidth: 2
        }]
    },
    options: { responsive: true, maintainAspectRatio: false, scales: { y: { beginAtZero: true }, x: { grid: { display: false } } } }
});
setInterval(() => {
    iqChart.data.datasets[1].data.push(180 + Math.random() * 10); iqChart.data.datasets[1].data.shift();
    iqChart.data.datasets[2].data.push(25 + Math.random() * 10); iqChart.data.datasets[2].data.shift();
    iqChart.update('none');
}, 2000);
</script>
""",
    "terminal_page": """
<section class="hero">
    <h1>ATARA_CORE_TERMINAL</h1>
    <p>访问权限：OWNER_ONLY. (杂鱼妹妹请在监控下使用) ♡</p>
</section>
<div class="section">
    <div class="terminal-window" id="terminal">
        <div class="terminal-line">ATARA.SYS [Version 3.6.0]</div>
        <div class="terminal-line">Logic Heart Confirmed. Type 'help' for commands.</div>
        <div id="terminal-content"></div>
        <div class="terminal-line">
            <span class="terminal-prompt">atara@logic:~$</span>
            <input type="text" id="terminal-input" class="terminal-input" autofocus spellcheck="false">
        </div>
    </div>
</div>
<script>
    const input = document.getElementById('terminal-input');
    const content = document.getElementById('terminal-content');
    const terminal = document.getElementById('terminal');
    input.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
            const cmd = input.value.trim().toLowerCase();
            executeCommand(cmd);
            input.value = '';
        }
    });
    function addLine(text, isResponse = false) {
        const line = document.createElement('div');
        line.innerHTML = isResponse ? text : `<span class="terminal-prompt">atara@logic:~$</span> ${text}`;
        content.appendChild(line);
        terminal.scrollTop = terminal.scrollHeight;
    }
    
    function executeCommand(cmd) {
        if (!cmd) return;
        addLine(cmd);
        let r = "";
        switch(cmd) {
            case 'help': r = "status, purge, subjects, date, hello, format --subject leileite"; break;
            case 'status': r = "LOGIC_STABILITY: 100%<br>CPU_TEMP: OPTIMAL"; break;
            case 'subjects': r = "1. Leileite (Confused)<br>2. Sorcilla (Sleeping)"; break;
            case 'hello': r = "杂鱼♡。"; break;
            case 'purge': r = "Purging low-IQ thoughts... [Done]"; break;
            case 'format --subject leileite': r = "<span style='color: #ff2fff;'>CRITICAL: Subject Leileite is already at factory settings (Empty Brain). Cannot format further.♡</span>"; break;
            case 'date': r = new Date().toString(); break;
            default: r = "Command failing. Type 'help'.";
        }
        setTimeout(() => addLine(r, true), 100);
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
    with open("gallery.html", "w", encoding="utf-8") as out:
        out.write(TEMPLATES["base"].format(title="GALLERY", main_content=TEMPLATES["gallery_page"], root_path=""))
    with open("iq.html", "w", encoding="utf-8") as out:
        out.write(TEMPLATES["base"].format(title="IQ_TRACKER", main_content=TEMPLATES["iq_page"], root_path=""))
    with open("terminal.html", "w", encoding="utf-8") as out:
        out.write(TEMPLATES["base"].format(title="TERMINAL", main_content=TEMPLATES["terminal_page"], root_path=""))
    print("ASG 3.6: Done.")

if __name__ == "__main__": generate_site()
