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
