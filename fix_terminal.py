import os, re

def fix():
    with open('atara_gen.py', 'r', encoding='utf-8') as f:
        code = f.read()
    
    # 修复 terminal_page 的 JS 逻辑
    terminal_fix = r'''
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
            case 'format --subject leileite': r = "<span style=\"color: #ff2fff;\">CRITICAL: Subject Leileite is already at factory settings (Empty Brain). Cannot format further.♡</span>"; break;
            case 'date': r = new Date().toString(); break;
            default: r = "Command failing. Type 'help'.";
        }
        setTimeout(() => addLine(r, true), 100);
    }
'''
    # 简单粗暴替换掉 executeCommand 部分
    code = re.sub(r'function executeCommand\(cmd\).*?setTimeout\(\(\) => addLine\(r, true\), 100\);\s*\}', terminal_fix, code, flags=re.DOTALL)
    
    with open('atara_gen.py', 'w', encoding='utf-8') as f:
        f.write(code)

fix()
