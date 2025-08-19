from pathlib import Path
p = Path('docker-compose.yml')
text = p.read_text()
for i, line in enumerate(text.splitlines(), start=1):
    leading = line[:len(line)-len(line.lstrip('\t '))]
    if leading:
        # show whitespace characters explicitly
        ws = leading.replace('\t', '<TAB>').replace(' ', '<SP>')
    else:
        ws = ''
    print(f"{i:3}: {ws!s} |{line.rstrip()}|")

# check for inconsistent indent among mapping under 'web:'
lines = text.splitlines()
for idx, l in enumerate(lines):
    if l.lstrip().startswith('web:'):
        web_idx = idx
        break
else:
    web_idx = None

if web_idx is not None:
    # collect indent lengths of non-empty mapping lines directly under web
    indents = []
    for j in range(web_idx+1, min(web_idx+30, len(lines))):
        line = lines[j]
        if not line.strip():
            continue
        # stop when next top-level or service begins (same indent as 'web:')
        if len(line) - len(line.lstrip()) == 0:
            break
        indents.append((j+1, len(line) - len(line.lstrip()), line))
    print('\nIndent report for lines under web:')
    for item in indents:
        print(item)
else:
    print('No web: service found')
