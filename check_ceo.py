with open('static/index.html', encoding='utf-8') as f:
    lines = f.readlines()
start = [i for i, l in enumerate(lines) if 'id="pane-ceo-cockpit"' in l][0]
print(f'Start: {start}')
end = [i for i, l in enumerate(lines) if '</section>' in l and i > start][0]
print(f'End: {end}')
