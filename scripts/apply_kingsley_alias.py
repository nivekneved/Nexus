import os

target_dir = r"C:\Users\deven\OneDrive\Desktop\Agents"
directories_to_scan = [
    os.path.join(target_dir, 'core'),
    os.path.join(target_dir, 'agents'),
    os.path.join(target_dir, 'scripts'),
    os.path.join(target_dir, 'security'),
    target_dir
]

target_files = ['.env', 'server.py']

count = 0
for d in directories_to_scan:
    if not os.path.exists(d): continue
    for root, dirs, files in os.walk(d):
        if '.git' in root or '__pycache__' in root or '.venv' in root: continue
        for file in files:
            if file.endswith('.py') or file == '.env':
                path = os.path.join(root, file)

                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    modified = False

                    if 'Kingsley Vance Maurya' in content:
                        content = content.replace('Kingsley Vance Maurya', 'Kingsley Vance Maurya')
                        modified = True
                    if 'kingsley vance maurya' in content:
                        content = content.replace('kingsley vance maurya', 'kingsley vance maurya')
                        modified = True
                    if 'USER_NAME=Kingsley' in content:
                        content = content.replace('USER_NAME=Kingsley', 'USER_NAME=Kingsley')
                        modified = True

                    if modified:
                        with open(path, 'w', encoding='utf-8') as f:
                            f.write(content)
                        count += 1
                        print(f"Updated alias in: {path}")
                except Exception as e:
                    pass

print(f"\n[Nexus Alias Manager] Successfully scrubbed real name and injected Kingsley Vance Maurya across {count} system files.")
