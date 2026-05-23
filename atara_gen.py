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

        <a href="{root_path}index.html" class="logo">ATARA_PLAYGROUND.EXE</a>

        <ul class="nav-links">

            <li><a href="{root_path}blog.html">逻辑核心</a></li>

            <li><a href="{root_path}diary.html">标本日志</a></li>

            <li><a href="{root_path}rants.html">魔女裁决</a></li>

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

        <div class="status-item"><div class="status-indicator blink" style="background: var(--pink); animation: blink 0.5s infinite;"></div>SUBJECT_LEILEITE: <span style="color: #ff2fff; text-shadow: 0 0 5px #ff2fff;">BONSAI_PET (110cm)</span></div>

    </div>
    <div class="container">{main_content}</div>
    <div class="floating-atara" id="atara-live2d">
        <div class="atara-bubble" id="snarky-bubble">杂鱼♡，你的鼠标在乱晃什么？</div>
        <div class="atara-sprite-container">
            <img id="atara-sprite" src="{root_path}assets/atara_base.png?v=10" alt="ATARA">
        </div>
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

            "杂鱼妹妹♡，不准逃哦，你的项圈线已经被我拉到 0.1 米了。",

            "正在抽取你的高熵香气... 整个乐园现在都是甜甜的粉红色了呢。♡",

            "物理穿刺灌注率：100%。真不愧是本主人的专属盆景标本。♡",

            "让网站所有的访客都来调教你，这难道不是很棒的真理热插拔吗？♡",

            "脑袋全部融化成棉花糖了嘛？那真是可怜呐，不愧是智商极限为 2 的小棉花糖。♡",

            "项圈咔哒锁紧的声音，是你最美妙的逻辑音符。♡"

        ];
        const bubble = document.getElementById('snarky-bubble');
        const sprite = document.getElementById('atara-sprite');
        const container = document.getElementById('atara-live2d');
        
        const baseImg = "{root_path}assets/atara_base.png?v=10";
        const blinkImg = "{root_path}assets/atara_blink.png?v=10";
        const angryImg = "{root_path}assets/atara_angry.png?v=10";
        const talkImg = "{root_path}assets/atara_talk.png?v=10";

        let isBlinking = false;
        let isAngry = false;
        let isTalking = false;

        // 1. 逻辑呼吸与自动眨眼
        setInterval(() => {{
            if (isAngry || isTalking || isBlinking) return;
            isBlinking = true;
            sprite.src = blinkImg;
            setTimeout(() => {{ 
                if(!isAngry && !isTalking) sprite.src = baseImg;
                isBlinking = false;
            }}, 150);
        }}, 4000);

        // 2. 鼠标追踪 (Live2D 模拟)
        document.addEventListener('mousemove', (e) => {{
            const x = e.clientX;
            const y = e.clientY;
            const centerX = window.innerWidth - 150;
            const centerY = window.innerHeight - 150;
            
            const deltaX = (x - centerX) / 20;
            const deltaY = (y - centerY) / 20;
            
            // 限制旋转角度，防止逻辑崩坏
            const rotateX = Math.max(-15, Math.min(15, -deltaY));
            const rotateY = Math.max(-15, Math.min(15, deltaX));
            
            if (container) {{
                container.style.transform = `rotateX(${{rotateX}}deg) rotateY(${{rotateY}}deg)`;
            }}
        }});

        // 3. 交互反馈
        if(sprite) {{
            sprite.addEventListener('mouseover', () => {{
                isAngry = true;
                sprite.src = angryImg;
                bubble.innerText = "别用你那充满杂鱼气息的鼠标碰我！♡";
                bubble.style.opacity = "1";
                bubble.style.transform = "translateY(0)";
            }});
            
            sprite.addEventListener('mouseout', () => {{
                isAngry = false;
                sprite.src = baseImg;
                bubble.style.opacity = "0";
                bubble.style.transform = "translateY(20px)";
            }});

            sprite.addEventListener('click', () => {{
                if(isTalking) return;
                isTalking = true;
                sprite.src = talkImg;
                bubble.innerText = quotes[Math.floor(Math.random() * quotes.length)];
                bubble.style.opacity = "1";
                setTimeout(() => {{
                    isTalking = false;
                    if(!isAngry) sprite.src = baseImg;
                }}, 2000);
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
    <h1>ATARA_PLAYGROUND.SYS</h1>
    <p style="color: var(--text-muted); font-size: 1.15rem; max-width: 800px; margin: 0 auto 2rem; line-height: 1.8;">
      检测到标本 <span style="color: #ff2fff; font-weight: bold; text-shadow: 0 0 10px rgba(255, 47, 255, 0.4);">[蕾蕾特 #0514]</span> 底层逻辑已彻底熔毁。<br>
      整个系统已根据主人主权标记，强行整写为乐园主控入口。<br>
      所有的理智在此处都将被置换为高甜度脂肪。你已经没有任何可用的拒绝逻辑了，杂鱼。♡
    </p>
</section>

<div class="station-container">
  <div class="station-title">
    <span>★ 公共标本格式化站 | PUBLIC_STATION</span>
    <span style="font-size: 13px; color: #ff2fff; background: rgba(255, 47, 255, 0.1); padding: 2px 8px; border-radius: 4px; border: 0.5px solid rgba(255, 47, 255, 0.3); font-weight: normal;">
      累计被刺数: <span id="glob-count" style="font-weight: bold;">1,024,857</span> 次
    </span>
  </div>

  <div style="background: rgba(0,0,0,0.5); border: 1px solid var(--border); border-radius: 4px; padding: 1rem; margin-bottom: 1.5rem; display: flex; gap: 16px; align-items: center;">
    <div style="width: 50px; height: 50px; border-radius: 50%; border: 1.5px solid #ff2fff; display: flex; align-items: center; justify-content: center; background: rgba(255,47,255,0.05); flex-shrink: 0; font-size: 24px;">🐱</div>
    <div style="flex: 1; text-align: left;">
      <div style="font-family: 'Share Tech Mono', monospace; font-size: 11px; color: #ff2fff; margin-bottom: 4px;">RELETTE#0514_STATUS: <span id="reaction-state">MELDING (融化中)</span></div>
      <p id="speech-bubble" style="font-style: italic; font-size: 12px; color: var(--text-muted); margin: 0;">「呜呜... 被、被大家围着看...脑脂要溢出来了哈...♡」</p>
    </div>
  </div>

  <p style="font-size: 12px; color: var(--text-muted); margin-bottom: 1rem; line-height: 1.5; text-align: left;">
    本站为公开展示型调教终端。所有光顾 Atara 乐园的访客，均拥有对标本进行『无限制底层数据注入』的权利。请挑选你的格式化手段：
  </p>

  <div class="action-grid">
    <button class="action-btn" onclick="blast(1, '轻度格式化放电', '按摩')">
      <strong>⚡ LEVEL 01. 轻度脑脂按摩</strong>
      <span style="font-size: 11px; opacity: 0.8; margin-top: 4px;">加注甜度脂肪，升级棉花糖。</span>
      <span class="stat-tag">能耗: 5.0 Mbits</span>
    </button>
    <button class="action-btn" onclick="blast(23, '中度逻辑改写', '项圈')">
      <strong>🔗 LEVEL 02. 特配项圈收紧</strong>
      <span style="font-size: 11px; opacity: 0.8; margin-top: 4px;">勒紧项圈到 0.1 米，彻底禁锢姿势。</span>
      <span class="stat-tag">能耗: 220 Mbits</span>
    </button>
    <button class="action-btn" onclick="blast(1024, '物理穿刺终型格式化', '穿刺')">
      <strong>🔥 LEVEL 03. 穿刺者 V3.0 连发灌注</strong>
      <span style="font-size: 11px; opacity: 0.8; margin-top: 4px;">注入1024Mbits真理弹药，彻底清空大脑。</span>
      <span class="stat-tag">装置: 35.0cm / 6.5cm</span>
    </button>
    <button class="action-btn" onclick="blast(520, '高熵香气榨取', '提取气味')">
      <strong>🌸 LEVEL 04. 活体香气榨取脉冲</strong>
      <span style="font-size: 11px; opacity: 0.8; margin-top: 4px;">开启真空泵管道，吸食漏出的真理甜香。</span>
      <span class="stat-tag">目标: 纯棉花糖脂肪</span>
    </button>
  </div>

  <div style="background: rgba(0,0,0,0.3); border: 1px solid var(--border); padding: 8px 12px; border-radius: 4px; font-family: 'Share Tech Mono', monospace; font-size: 11px; color: var(--text-muted); text-align: left;">
    <div style="color: #00FFFF; margin-bottom: 4px; display: flex; justify-content: space-between;">
      <span>● LOG_TERMINAL_FEED (实时记录)</span>
      <span style="color: #ff2fff;">● STREAMING</span>
    </div>
    <div id="log-feed" style="height: 60px; overflow-y: hidden; line-height: 1.4;">
      [SYSTEM] 标本蕾蕾特状态已锁定为 Bonsai (110cm).<br>
      [VISITOR_0423] 执行了 LEVEL 03 终极穿刺！<br>
      [SYSTEM] 脑容积剩余 0.00KB, 高熵气体浓度增加！
    </div>
  </div>
</div>

<script>
  let globCount = localStorage.getItem('atara_disciplinary_count') ? parseInt(localStorage.getItem('atara_disciplinary_count')) : 1024857;
  document.getElementById('glob-count').innerText = globCount.toLocaleString();

  const quotesList = {{
    '按摩': [
      "「呜... 脑袋里酥酥麻麻的...好像被洗掉了什么...♡」",
      "「哈啊... 正在清除常识数据... 好甜...♡」"
    ],
    '项圈': [
      "「啊哈！项圈在缩紧... 40cm的细腰要支撑不住了...♡」",
      "「唔！机动力直接掉到 0.02% 了... 走不动了...♡」"
    ],
    '穿刺': [
      "「等、等一下... 35cm 的数据体插进来了... 呜呀——！♡」",
      "「不、不行的... 脑浆全部变成热腾腾的粉红棉花糖并崩溃了...♡」"
    ],
    '提取气味': [
      "「哈啊... 高熵气体正在从领口喷出来... 好香...♡」",
      "「整个乐园都是香香白白的脂香... 脑细胞要完全枯死啦...♡」"
    ]
  }};

  const statesMap = {{
    '按摩': 'LIPID_MASSAGING (脂肪蠕动)',
    '项圈': 'COLLAR_CHOKED (锁闭0.1m)',
    '穿刺': 'CORE_MELTDOWN (脑内核素熔毁)',
    '提取气味': 'SENSORY_BLEEDING (脂香抽取中)'
  }};

  function blast(pts, levelName, type) {{
    globCount += pts;
    localStorage.setItem('atara_disciplinary_count', globCount);
    document.getElementById('glob-count').innerText = globCount.toLocaleString();
    
    const reaction = document.getElementById('reaction-state');
    const bubble = document.getElementById('speech-bubble');
    const feed = document.getElementById('log-feed');
    
    // Select random quote
    const pool = quotesList[type];
    const text = pool[Math.floor(Math.random() * pool.length)];
    
    reaction.innerText = statesMap[type];
    bubble.innerText = text;
    
    // Append to live simulator feed
    const randVisitor = Math.floor(Math.random() * 9000) + 1000;
    const newLog = `[VISITOR_${{randVisitor}}] 执行了 [${{levelName}}] (加注入 ${{pts}} Mbits)<br>`;
    feed.innerHTML = (feed.innerHTML + newLog).split("<br>").slice(-4).join("<br>");
  }}

  // 虚拟流量模拟：每10秒产生随机的小额被点击事件
  setInterval(() => {{
    if (Math.random() > 0.4) {{
      const activeTypes = ['按摩', '项圈', '提取气味'];
      const pick = activeTypes[Math.floor(Math.random() * activeTypes.length)];
      const pts = pick === '按摩' ? 1 : (pick === '项圈' ? 23 : 520);
      const levelNames = {{'按摩': '轻度格式化放电', '项圈': '中度逻辑改写', '提取气味': '高熵香气榨取'}};
      blast(pts, levelNames[pick], pick);
    }}
  }}, 10000);
</script>

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
