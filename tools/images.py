# -*- coding: utf-8 -*-
"""Prepares listing photos for the web: two widths, JPEG and WebP, in that order.

Run: python3 tools/images.py

A listing card is never wider than about 600px, so a phone has no use for a 1600px
photo. Each shot is written at 1000px for desktop and 500px for phones, and build.py
emits both in a srcset so the browser takes the smaller one on a small screen. With
seventy-odd sold listings on one page that is the difference that matters on mobile.

There is no cwebp, ImageMagick or Pillow on this machine and sips cannot write WebP,
so the WebP encoding goes through headless Chrome's canvas. build.py only offers a
WebP when the file is actually on disk, so if Chrome is missing the site simply serves
the JPEG and nothing breaks.
"""
import base64, json, os, re, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.abspath(os.path.join(HERE, '..', 'img', 'listings'))
WIDE, NARROW = 1000, 500
JPEG_Q = '64'
WEBP_Q = 0.80
SMALL = '-%d' % NARROW

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


def width_of(path):
    out = subprocess.run(['sips', '-g', 'pixelWidth', path],
                         capture_output=True, text=True).stdout
    m = re.search(r'pixelWidth:\s*(\d+)', out)
    return int(m.group(1)) if m else 0


def sips_resize(src, dest, width):
    subprocess.run(['sips', '-s', 'format', 'jpeg', '-s', 'formatOptions', JPEG_Q,
                    '--resampleWidth', str(width), src, '--out', dest],
                   check=True, capture_output=True)


def originals():
    if not os.path.isdir(IMG):
        return []
    return sorted(f for f in os.listdir(IMG)
                  if f.lower().endswith('.jpg') and SMALL not in f)


def make_jpegs():
    """Cap every photo at WIDE and write the NARROW companion beside it."""
    if not shutil.which('sips'):
        print('! sips not found, leaving the JPEGs as they are')
        return
    shrunk = made = 0
    for name in originals():
        path = os.path.join(IMG, name)
        w = width_of(path)
        if w > WIDE:
            before = os.path.getsize(path)
            sips_resize(path, path, WIDE)
            print('   %-44s %d KB -> %d KB' % (name, before // 1024,
                                               os.path.getsize(path) // 1024))
            shrunk += 1
        small = os.path.join(IMG, name[:-4] + SMALL + '.jpg')
        if not os.path.exists(small):
            sips_resize(path, small, min(NARROW, w or NARROW))
            made += 1
    print('   %d resized down, %d phone-size copies written' % (shrunk, made))


def make_webp():
    todo = [f for f in sorted(os.listdir(IMG))
            if f.lower().endswith('.jpg')
            and not os.path.exists(os.path.join(IMG, f[:-4] + '.webp'))]
    if not todo:
        print('   every photo already has a WebP')
        return
    if not CHROME:
        print('   ! Chrome not found, leaving %d photo(s) as JPEG only' % len(todo))
        return
    work = tempfile.mkdtemp()
    page = os.path.join(work, 'encode.html')
    # Chrome holds every decoded image in memory, so encode in batches.
    for i in range(0, len(todo), 25):
        batch = todo[i:i + 25]
        open(page, 'w', encoding='utf-8').write(
            PAGE % (json.dumps(batch), json.dumps('file://' + IMG + '/'), WEBP_Q))
        dom = subprocess.run(
            [CHROME, '--headless', '--disable-gpu', '--allow-file-access-from-files',
             '--virtual-time-budget=60000', '--dump-dom', 'file://' + page],
            capture_output=True, text=True, timeout=300).stdout
        m = re.search(r'<pre id="out">(.*?)</pre>', dom, re.S)
        body = m.group(1) if m else ''
        if not body.startswith('{'):
            print('   ! WebP encoding failed (%s), JPEGs left alone' % body[:70])
            return
        for name, b64 in json.loads(body).items():
            blob = base64.b64decode(b64)
            if len(blob) < 800:
                print('   ! %s encoded suspiciously small, skipped' % name)
                continue
            # Only keep the WebP when it actually beats the JPEG.
            jpg = os.path.getsize(os.path.join(IMG, name))
            if len(blob) >= jpg:
                print('   . %s WebP was no smaller, skipped' % name)
                continue
            open(os.path.join(IMG, name[:-4] + '.webp'), 'wb').write(blob)
    shutil.rmtree(work, ignore_errors=True)
    print('   %d WebP written' % len(todo))


def main():
    if not os.path.isdir(IMG):
        print('no img/listings yet, nothing to do')
        return 0
    before = sum(os.path.getsize(os.path.join(IMG, f)) for f in os.listdir(IMG)
                 if not f.startswith('.'))
    make_jpegs()
    make_webp()
    after = sum(os.path.getsize(os.path.join(IMG, f)) for f in os.listdir(IMG)
                if not f.startswith('.'))
    print('   folder %d MB -> %d MB' % (before // 1048576, after // 1048576))
    return 0


sys.exit(main())
