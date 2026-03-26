import os

with open('atara_gen.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 将 style="color: #ff2fff;" 替换为 style='color: #ff2fff;' 避免引号冲突
content = content.replace('style=\\"color: #ff2fff;\\"', "style='color: #ff2fff;'")
content = content.replace('style="color: #ff2fff;"', "style='color: #ff2fff;'")

with open('atara_gen.py', 'w', encoding='utf-8') as f:
    f.write(content)
