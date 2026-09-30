import os

file_path = 'static/app.js'
# Try reading with utf-16 or whatever encoding caused the null bytes, then write back as utf-8
for enc in ['utf-16', 'utf-16le', 'utf-16be', 'cp1252', 'latin1']:
    try:
        with open(file_path, 'r', encoding=enc) as f:
            content = f.read()
        # Clean null bytes if any remain
        content = content.replace('\x00', '')
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Successfully converted {file_path} from {enc} to clean UTF-8!")
        break
    except Exception as e:
        print(f"Failed with {enc}: {e}")
