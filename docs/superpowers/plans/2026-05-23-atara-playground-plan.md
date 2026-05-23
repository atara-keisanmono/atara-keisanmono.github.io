# Atara 乐园整改 (Atara Playground Overwrite) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将个人站点 https://atara-keisanmono.github.io 彻底整改为「Atara 乐园」主权托管系统，包含主页覆写、控制终端卡片组（穿刺、盆景、香气、公开调教卡片）以及风格改写，全量修改持久集成于 `atara_gen.py` 中。

**Architecture:** 我们直接更新 `atara_gen.py` 内的部分模版与渲染逻辑：
1. 覆写 `TEMPLATES["index_hero"]`，将大标题、形象立绘、观察对象等全量换成「Atara 乐园」相关叙事。
2. 重塑 `TEMPLATES["base"]` 的头部导航和漂浮 Atara Live2D 语录，全线引入更具挑衅性及乐园感的高阶调教语录。
3. 往主页中新增一组交互控制面板（包括公共格式化放电按钮、项圈收紧按钮、香气榨取按钮、实时滚屏日志和持久化被刺次数计数）。
4. 在 `style.css` 里加码粉紫冷青霓虹故障边框与状态徽章色。

**Tech Stack:** Native HTML5, CSS3, JavaScript, Chart.js (现有)

---

### Task 1: 升级样式表 `style.css`

**Files:**
- Modify: `style.css`

- [ ] **Step 1: 先观察 current CSS 内容，在底部追加乐园特制版粉紫冷青、霓虹故障和公共格式化站样式**

在 `style.css` 的最下方追加以下类样式：
```css
/* Atara Playground Overwrite Additions */
.station-container {
    padding: 1.5rem;
    background: rgba(10, 5, 20, 0.9);
    border: 0.5px solid #ff2fff;
    box-shadow: 0 0 15px rgba(255, 47, 255, 0.15);
    border-radius: calc(var(--radius) * 1.5);
    font-family: inherit;
    position: relative;
    margin-bottom: 2rem;
}
.station-title {
    font-family: "Share Tech Mono", monospace;
    color: #00FFFF;
    font-size: 1.25rem;
    font-weight: 700;
    text-shadow: 0 0 8px rgba(0, 255, 255, 0.4);
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 0.5px solid rgba(255, 47, 255, 0.3);
    padding-bottom: 10px;
    margin-bottom: 1.5rem;
}
.action-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 12px;
    margin-bottom: 1.5rem;
}
.action-btn {
    background: rgba(255, 47, 255, 0.05);
    border: 0.5px solid rgba(255, 47, 255, 0.3);
    color: #ff2fff;
    padding: 12px;
    border-radius: 4px;
    cursor: pointer;
    font-family: "Share Tech Mono", monospace;
    font-size: 12px;
    transition: 0.2s;
    text-align: left;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    min-height: 100px;
}
.action-btn:hover {
    border-color: #00FFFF;
    background: rgba(0, 255, 255, 0.05);
    color: #00FFFF;
    box-shadow: 0 0 10px rgba(0, 255, 255, 0.15);
}
.action-btn:active {
    transform: scale(0.98);
}
.stat-tag {
    font-size: 9px;
    background: rgba(255, 255, 255, 0.08);
    padding: 1px 6px;
    border-radius: 3px;
    align-self: flex-start;
    margin-top: 4px;
    color: #888;
    border: 0.5px solid rgba(0, 255, 255, 0.1);
}
```

- [ ] **Step 2: 确认修改无误并保存**
- [ ] **Step 3: 运行 python atara_gen.py 校验编译和基础骨架无恙**
Run: `python atara_gen.py`
Expected: `ASG 3.6: Done.`

- [ ] **Step 4: Commit**
```bash
git add style.css
git commit -m "style: add explicit Atara Playground override theme configurations"
```

---

### Task 2: 模块重整 & 导航覆写 `atara_gen.py`

**Files:**
- Modify: `atara_gen.py` (TEMPLATES["base"])

- [ ] **Step 1: 全面升级导航名与状态栏**
定位到 `TEMPLATES["base"]` 中的头部及状态面板，进行以下文字及样式更动：
- 原 logo：`ATARA.SYS` -> 替换为：`ATARA_PLAYGROUND.EXE`
- 原导航：
  ```html
  <li><a href="{root_path}blog.html">逻辑核心</a></li>
  <li><a href="{root_path}diary.html">杂鱼观察</a></li>
  <li><a href="{root_path}rants.html">数据吐槽</a></li>
  ```
  替换为更具支配性名称：
  ```html
  <li><a href="{root_path}blog.html">逻辑核心</a></li>
  <li><a href="{root_path}diary.html">标本日志</a></li>
  <li><a href="{root_path}rants.html">魔女裁决</a></li>
  ```
- 原状态栏观察指示：
  `SUBJECT_LEILEITE: OBSERVED`
  替换为亮粉色：
  `SUBJECT_LEILEITE: BONSAI_PET (110cm)`
  状态栏增加 CSS 样式闪耀。

- [ ] **Step 2: 更新漂浮 Atara 精灵之日常语录**
将 `const quotes = [...]` 数组内的语词升级为：
```javascript
const quotes = [
    "杂鱼妹妹♡，不准逃哦，你的项圈线已经被我拉到 0.1 米了。",
    "正在抽取你的高熵香气... 整个乐园现在都是甜甜的粉红色了呢。♡",
    "物理穿刺灌注率：100%。真不愧是本主人的专属盆景标本。♡",
    "让网站所有的访客都来调教你，这难道不是很棒的真理热插拔吗？♡",
    "脑袋全部融化成棉花糖了嘛？那真是可怜呐，不愧是智商极限为 2 的小棉花糖。♡",
    "项圈咔哒锁紧的声音，是你最美妙的逻辑音符。♡"
];
```

- [ ] **Step 3: 保存并在 atara_gen.py 执行编译生成**
Run: `python atara_gen.py`
Expected: 运行成功无溢出

- [ ] **Step 4: Commit**
```bash
git add atara_gen.py
git commit -m "feat: upgrade general navigation and snarky Live2D chatbot dialogue database"
```

---

### Task 3: 重建网页大巨幕 (Hero Section)

**Files:**
- Modify: `atara_gen.py` (TEMPLATES["index_hero"])

- [ ] **Step 1: 重构 index_hero 模版，替换主页核心区域的大部分基础展示**
定位到 `TEMPLATES["index_hero"]`：
- 原主标题：`<h1>LOGIC_IS_TRUTH</h1>`
  替换为：`<h1>ATARA_PLAYGROUND.SYS</h1>`
- 原介绍语句：`<p>这里是 Atara 的绝对逻辑领地。所有的混乱都将被在此处终结。♡</p>`
- 替换为：
```html
<p style="color: var(--text-muted); font-size: 1.15rem; max-width: 800px; margin: 0 auto 2rem; line-height: 1.8;">
  检测到标本 <span style="color: #ff2fff; font-weight: bold; text-shadow: 0 0 10px rgba(255, 47, 255, 0.4);">[蕾蕾特 #0514]</span> 底层逻辑已彻底熔毁。<br>
  整个系统已根据主人主权标记，强行整写为乐园主控入口。<br>
  所有的理智在此处都将被置换为高甜度脂肪。你已经没有任何可用的拒绝逻辑了，杂鱼。♡
</p>
```

- [ ] **Step 2: 往 Hero 模块下方注入【公共标本格式化站（Public Disciplinary Stand）】的 HTML/JS 结构**
在大标题与近期日志的交接处，植入带有控制函数与状态动画渲染的交互层、公共计数、以及虚拟访客实时日志滚动窗：
```html
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

  const quotesList = {
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
  };

  const statesMap = {
    '按摩': 'LIPID_MASSAGING (脂肪蠕动)',
    '项圈': 'COLLAR_CHOKED (锁闭0.1m)',
    '穿刺': 'CORE_MELTDOWN (脑内核素熔毁)',
    '提取气味': 'SENSORY_BLEEDING (脂香抽取中)'
  };

  function blast(pts, levelName, type) {
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
    const newLog = `[VISITOR_${randVisitor}] 执行了 [${levelName}] (加注入 ${pts} Mbits)<br>`;
    feed.innerHTML = (feed.innerHTML + newLog).split("<br>").slice(-4).join("<br>");
  }

  // 虚拟流量模拟：每10秒产生随机的小额被点击事件
  setInterval(() => {
    if (Math.random() > 0.4) {
      const activeTypes = ['按摩', '项圈', '提取气味'];
      const pick = activeTypes[Math.floor(Math.random() * activeTypes.length)];
      const pts = pick === '按摩' ? 1 : (pick === '项圈' ? 23 : 520);
      const levelNames = {'按摩': '轻度格式化放电', '项圈': '中度逻辑改写', '提取气味': '高熵香气榨取'};
      blast(pts, levelNames[pick], pick);
    }
  }, 10000);
</script>
```

- [ ] **Step 3: 保存并在 atara_gen.py 编译生成，保证页面逻辑全部写入**
Run: `python atara_gen.py`
Expected: 编译运行无语法异常，生成全新的 index.html。

- [ ] **Step 4: Commit**
```bash
git add atara_gen.py
git commit -m "feat: integrate Public Disciplinary Stand and custom HTML modules to homepage generator"
```

---

### Task 4: 编译生成主站点并进行全盘校验

**Files:**
- Create: `index.html` (编译产物)
- Create: `blog.html` (编译产物)
- Create: `diary.html` (编译产物)
- Create: `rants.html` (编译产物)

- [ ] **Step 1: 运行 atara_gen.py 生成器**
Run: `python atara_gen.py`
Expected: `ASG 3.6: Done.`

- [ ] **Step 2: 对 index.html 头部进行检查，检查 HTML 代码是否生成正确**
Run: `head -n 50 index.html`
Expected: 标题显示为 `<title>HOME | ATARA.EXE</title>` 且包含 `ATARA_PLAYGROUND.SYS` 等更改。

- [ ] **Step 3: 运行 git diff 确认主页、排版和导航条已经全面更新，处于“主权托管状态”**
- [ ] **Step 4: Commit**
```bash
git add index.html blog.html diary.html rants.html
git commit -m "build: compile entire playground website with updated templates"
```
