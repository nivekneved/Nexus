with open('server.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if 'uvicorn.run("server:app"' in line:
        new_lines.append('    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True)\n')
    else:
        new_lines.append(line)

with open('server.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
