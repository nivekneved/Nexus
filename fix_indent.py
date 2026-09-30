with open('server.py', 'r', encoding='utf-8') as f:
    code = f.read()

lines = code.split('\n')
for i, line in enumerate(lines):
    if 'uvicorn.run("server:app"' in line:
        lines[i] = '    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True)'
        break

with open('server.py', 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))
print("Indent fixed")