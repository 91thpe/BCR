import os
from collections import defaultdict

base_url = "https://91thpe.github.io/BCR"

# Walk the entire repo and collect all asset files
# Exclude hidden folders, GitHub folders, and HTML/script files
EXCLUDE_DIRS = {'.git', '.github', 'node_modules'}
EXCLUDE_EXTS = {'.html', '.yml', '.yaml', '.py', '.md', '.json', '.txt'}

files = []
for root, dirs, filenames in os.walk('.'):
    # Skip excluded directories
    dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
    for filename in filenames:
        ext = os.path.splitext(filename)[1].lower()
        if ext in EXCLUDE_EXTS:
            continue
        filepath = os.path.join(root, filename)
        # Clean up path: remove leading ./
        clean = filepath.lstrip('.').lstrip('/')
        files.append(clean)

files.sort()

# Group by folder
groups = defaultdict(list)
for f in files:
    folder = '/'.join(f.split('/')[:-1]) or '(root)'
    groups[folder].append(f)

# Build table rows
rows = []
for folder in sorted(groups.keys()):
    rows.append(
        f'<tr><td colspan="2" class="section">{folder}</td></tr>'
    )
    for key in sorted(groups[folder]):
        url = f"{base_url}/{key}"
        name = key.split('/')[-1]
        rows.append(
            f'<tr><td><a href="{url}">{name}</a></td>'
            f'<td class="path">{key}</td></tr>'
        )

rows_html = "\n    ".join(rows)
total = len(files)

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="robots" content="noindex, nofollow">
  <title>BCR Asset Sitemap</title>
  <style>
    body {{ font-family: monospace; font-size: 12px; padding: 20px; background: #fff; color: #333; }}
    h1 {{ font-family: sans-serif; color: #FF6600; font-size: 18px; }}
    p {{ font-family: sans-serif; font-size: 13px; color: #666; }}
    table {{ border-collapse: collapse; width: 100%; }}
    td {{ padding: 3px 8px; border-bottom: 1px solid #f0f0f0; vertical-align: top; }}
    a {{ color: #FF6600; text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}
    .section {{ background: #FF6600; color: white; font-weight: bold;
                padding: 6px 8px; font-family: sans-serif; font-size: 11px;
                letter-spacing: 0.5px; text-transform: uppercase; }}
    .path {{ color: #999; font-size: 11px; }}
  </style>
</head>
<body>
  <h1>BCR Asset Sitemap</h1>
  <p>{total} assets</p>
  <table>
    {rows_html}
  </table>
</body>
</html>"""

with open('sitemap.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f"Generated sitemap.html with {total} files")
