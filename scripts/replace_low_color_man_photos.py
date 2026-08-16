"""
Replace least colorful man photos using specific correct Wikimedia Commons file titles.
Uses a curated list of known-good file titles found via API search.
"""
import os, ssl, json, urllib.request, urllib.parse, time, shutil
import cv2, numpy as np

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
MAN_DIR = os.path.join(BASE_DIR, 'step5_new_country', 'images', 'man')

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
HEADERS = {'User-Agent': 'CasualFashionStudy/1.0 Python/3.11 (Research)'}


def colorfulness(path):
    img = cv2.imread(path)
    if img is None:
        return 0.0
    (B, G, R) = cv2.split(img.astype('float'))
    rg, yb = np.absolute(R-G), np.absolute(0.5*(R+G)-B)
    return np.sqrt(np.std(rg)**2+np.std(yb)**2) + 0.3*np.sqrt(np.mean(rg)**2+np.mean(yb)**2)


def get_direct_url(commons_filename):
    enc = urllib.parse.quote(commons_filename)
    api = f'https://commons.wikimedia.org/w/api.php?action=query&titles=File:{enc}&prop=imageinfo&iiprop=url%7Csize&format=json'
    req = urllib.request.Request(api, headers=HEADERS)
    with urllib.request.urlopen(req, context=ctx, timeout=12) as r:
        data = json.loads(r.read())
    for pid, info in data.get('query', {}).get('pages', {}).items():
        for img in info.get('imageinfo', []):
            url = img.get('url', '')
            if url.lower().endswith(('.jpg', '.jpeg')):
                return url
    return None


def download(url, dest):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, context=ctx, timeout=25) as r:
        data = r.read()
    if len(data) > 12000:
        with open(dest, 'wb') as f:
            f.write(data)
        return len(data)
    return 0


# Curated list: (dest_filename, commons_title) - found via Commons search
# These are real, confirmed Commons file names
TARGETS = [
    ('man_41_travis_scott.jpg',      'Travis Scott by Gage Skidmore.jpg'),
    ('man_05_michael_b_jordan.jpg',  'Michael B. Jordan by Gage Skidmore 2.jpg'),
    ('man_15_justin_timberlake.jpg', 'Justin Timberlake 2018.jpg'),
    ('man_49_jared_leto.jpg',        'Jared Leto by Gage Skidmore 2.jpg'),
    ('man_14_chris_pratt.jpg',       'Chris Pratt by Gage Skidmore 2.jpg'),
    ('man_35_kevin_hart.jpg',        'Kevin Hart by Gage Skidmore 2.jpg'),
    ('man_08_keanu_reeves.jpg',      'Keanu Reeves 2022.jpg'),
    ('man_30_tom_cruise.jpg',        'Tom Cruise by Gage Skidmore 2.jpg'),
    ('man_16_john_krasinski.jpg',    'John Krasinski by Gage Skidmore.jpg'),
    ('man_26_matt_damon.jpg',        'Matt Damon by Gage Skidmore 2.jpg'),
]

results = []
for fname, commons_title in TARGETS:
    dest = os.path.join(MAN_DIR, fname)
    before = colorfulness(dest)
    print(f'\n[{fname}] Before: {before:.1f}')
    
    try:
        url = get_direct_url(commons_title)
        time.sleep(1.2)  # respect rate limit
    except Exception as e:
        print(f'  ✗ API error: {e}')
        results.append((fname, before, before, False))
        continue
    
    if not url:
        print(f'  ✗ Not found: {commons_title}')
        results.append((fname, before, before, False))
        continue
    
    print(f'  URL: {url[:80]}...')
    tmp = dest + '.tmp'
    try:
        sz = download(url, tmp)
    except Exception as e:
        print(f'  ✗ Download failed: {e}')
        if os.path.exists(tmp): os.remove(tmp)
        results.append((fname, before, before, False))
        continue
    
    if sz > 0:
        after = colorfulness(tmp)
        print(f'  Score: {after:.1f}')
        if after >= before * 0.9:  # accept if not much worse
            bak = dest + '.bak'
            if not os.path.exists(bak):
                shutil.copy2(dest, bak)
            shutil.move(tmp, dest)
            print(f'  ✓ Replaced: {before:.1f} -> {after:.1f}')
            results.append((fname, before, after, True))
        else:
            os.remove(tmp)
            print(f'  ✗ New image less colorful. Keeping original.')
            results.append((fname, before, before, False))
    else:
        if os.path.exists(tmp): os.remove(tmp)
        results.append((fname, before, before, False))

print('\n=== FINAL SUMMARY ===')
for fname, b, a, ok in results:
    print(f'{"✓ REPLACED" if ok else "✗ KEPT"}  {fname}: {b:.1f} -> {a:.1f}')
