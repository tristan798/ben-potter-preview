# -*- coding: utf-8 -*-
"""Writes a .webp beside every listing .jpg that does not have one yet.

Run: python3 tools/webp.py

There is no cwebp, ImageMagick or Pillow on this machine and sips cannot write WebP,
so the encoding goes through headless Chrome's canvas. build.py only emits a <picture>
when the .webp is actually on disk, so if Chrome is missing the site simply serves the
JPEG and nothing breaks.
"""
import base64, json, os, re, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(HERE, '..', 'img', 'listings')
QUALITY = 0.82

CHROME = next((p for p in (
    '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    '/Applications/Chromium.app/Contents/MacOS/Chromium',
    shutil.which('google-chrome') or '',
    shutil.which('chromium') or '',
    shutil.which('chromium-browser') or '',
) if p and os.path.exists(p)), None)

PAGE = """<!doctype html><meta charset="utf-8"><body><pre id="out">PENDING</pre>
<script>
const names = %s, base = %s, q = %s;
(async () => {
  const res = {};
  for (const n of names) {
    const img = new Image();
    await new Promise((ok, no) => { img.onload = ok; img.onerror = () => no(n); img.src = base + n; });
    const c = document.createElement('canvas');
    c.width = img.naturalWidth; c.height = img.naturalHeight;
    c.getContext('2d').drawImage(img, 0, 0);
    res[n] = c.toDataURL('image/webp', q).split(',')[1];
  }
  document.getElementById('out').textContent = JSON.stringify(res);
})().catch(e => { document.getElementById('out').textContent = 'ERROR ' + e; });
</script>"""


def main():
    if not os.path.isdir(IMG):
        print('no img/listings yet, nothing to do')
        return 0
    todo = [f for f in sorted(os.listdir(IMG))
            if f.lower().endswith('.jpg')
            and not os.path.exists(os.path.join(IMG, f[:-4] + '.webp'))]
    if not todo:
        print('every listing photo already has a WebP')
        return 0
    if not CHROME:
        print('! Chrome not found, leaving %d photo(s) as JPEG only' % len(todo))
        return 0

    work = tempfile.mkdtemp()
    page = os.path.join(work, 'encode.html')
    base = 'file://' + os.path.abspath(IMG) + '/'
    open(page, 'w', encoding='utf-8').write(
        PAGE % (json.dumps(todo), json.dumps(base), QUALITY))
    dom = subprocess.run(
        [CHROME, '--headless', '--disable-gpu', '--allow-file-access-from-files',
         '--virtual-time-budget=30000', '--dump-dom', 'file://' + page],
        capture_output=True, text=True, timeout=180).stdout
    m = re.search(r'<pre id="out">(.*?)</pre>', dom, re.S)
    body = m.group(1) if m else ''
    if not body.startswith('{'):
        print('! WebP encoding failed (%s), leaving the JPEGs alone' % body[:80])
        return 0
    for name, b64 in json.loads(body).items():
        dest = os.path.join(IMG, name[:-4] + '.webp')
        blob = base64.b64decode(b64)
        if len(blob) < 1000:
            print('   ! %s encoded suspiciously small, skipped' % name)
            continue
        open(dest, 'wb').write(blob)
        print('   %s (%d KB)' % (os.path.basename(dest), len(blob) // 1024))
    shutil.rmtree(work, ignore_errors=True)
    return 0


sys.exit(main())
