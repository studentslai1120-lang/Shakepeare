#!/usr/bin/env python3
"""用程式畫出 26 張印象派風格的油畫風格插圖（images/X_word.jpg）。
先用色塊畫出場景，再用數萬筆短而厚的筆觸重新「塗」一遍。需要：pip install numpy pillow
用法：python3 make_images.py          （全部）
      python3 make_images.py D I Y    （只畫指定字母）"""
import sys, os, json, numpy as np
from PIL import Image, ImageDraw, ImageFilter
W, H = 960, 640
Y, X = np.mgrid[0:H, 0:W].astype(np.float32)
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'images')
def C(h): return tuple(int(h[i:i+2], 16) for i in (1, 3, 5))

class Cv:
    def __init__(s): s.im = Image.new('RGB', (W, H))
    def grad(s, y0, y1, *cols):
        t = np.linspace(0, 1, y1 - y0); n = len(cols) - 1
        a = np.zeros((y1 - y0, 3))
        for k in range(3): a[:, k] = np.interp(t, np.linspace(0, 1, n + 1), [C(c)[k] for c in cols])
        s.im.paste(Image.fromarray(np.repeat(a[:, None, :], W, 1).astype(np.uint8)), (0, y0))
    def fill(s, fn, c, blur=1.5):
        m = Image.new('L', (W, H), 0); fn(ImageDraw.Draw(m))
        if blur: m = m.filter(ImageFilter.GaussianBlur(blur))
        s.im.paste(C(c), (0, 0), m)
    def disc(s, x, y, r, c, b=2): s.fill(lambda d: d.ellipse([x-r, y-r, x+r, y+r], fill=255), c, b)
    def ell(s, x, y, rx, ry, c, b=4): s.fill(lambda d: d.ellipse([x-rx, y-ry, x+rx, y+ry], fill=255), c, b)
    def poly(s, p, c, b=1.5): s.fill(lambda d: d.polygon(p, fill=255), c, b)
    def rect(s, x0, y0, x1, y1, c, b=1.5): s.fill(lambda d: d.rectangle([x0, y0, x1, y1], fill=255), c, b)
    def line(s, p, w, c, b=1): s.fill(lambda d: d.line(p, fill=255, width=w), c, b)
    def glow(s, x, y, r, c, k=1.0):
        m = (255 * k * np.exp(-((X-x)**2 + (Y-y)**2) / (r*r))).clip(0, 255).astype(np.uint8)
        s.im.paste(C(c), (0, 0), Image.fromarray(m))
    def hills(s, base, amp, c, seed, f=1.0):
        r = np.random.default_rng(seed); ph = r.uniform(0, 6.28, 3); x = X[0] / W * 6.28 * f
        yv = base + amp * (np.sin(x+ph[0])*.6 + np.sin(x*2.3+ph[1])*.3 + np.sin(x*5.1+ph[2])*.1)
        m = (Y > yv[None, :]).astype(np.uint8) * 255
        s.im.paste(C(c), (0, 0), Image.fromarray(m).filter(ImageFilter.GaussianBlur(1.2)))
    def dots(s, n, box, cols, r0, r1, seed=3):
        r = np.random.default_rng(seed); d = ImageDraw.Draw(s.im)
        for _ in range(n):
            x, y, rr = r.uniform(box[0], box[2]), r.uniform(box[1], box[3]), r.uniform(r0, r1)
            d.ellipse([x-rr, y-rr, x+rr, y+rr], fill=C(cols[r.integers(len(cols))]))
    def water(s, y0, tint, k=.75):
        h = min(y0, H - y0); a = np.asarray(s.im.crop((0, y0-h, W, y0)).transpose(Image.FLIP_TOP_BOTTOM)).astype(np.float32)
        for i in range(h): a[i] = np.roll(a[i], int(14*np.sin(i/2.7)*(.25+i/h)), axis=0)
        a = a*k + np.array(C(tint))*(1-k); s.im.paste(Image.fromarray(a.astype(np.uint8)), (0, y0))
    def tree(s, x, b, h, tc, lc):
        s.rect(x-h*.03, b-h*.45, x+h*.03, b, tc)
        for dx, dy, rx, ry in [(0, -.62, .26, .22), (-.16, -.5, .2, .17), (.17, -.5, .2, .17), (0, -.8, .17, .16)]:
            s.ell(x+dx*h, b+dy*h, rx*h, ry*h, lc, 5)
    def bare(s, x, y, ang, ln, w, c, d=6, seed=5):
        r = np.random.default_rng(seed)
        def go(x, y, a, l, w, d):
            if d == 0 or l < 6: return
            x2, y2 = x + l*np.cos(a), y - l*np.sin(a); s.line([(x, y), (x2, y2)], max(1, int(w)), c, .8)
            go(x2, y2, a + r.uniform(.2, .6), l*.74, w*.68, d-1); go(x2, y2, a - r.uniform(.2, .6), l*.74, w*.68, d-1)
        go(x, y, ang, ln, w, d)
    def tower(s, x, b, w, h, c):
        s.rect(x-w/2, b-h, x+w/2, b, c); s.poly([(x-w*.62, b-h), (x+w*.62, b-h), (x, b-h-w*1.3)], c)
    def boat(s, x, y, sc, hull, sail):
        s.poly([(x-40*sc, y), (x+40*sc, y), (x+26*sc, y+13*sc), (x-26*sc, y+13*sc)], hull)
        s.poly([(x, y-4*sc), (x, y-66*sc), (x+34*sc, y-8*sc)], sail)
    def stars(s, n, c='#fff6c8', y1=330): s.dots(n, (0, 0, W, y1), [c], 1, 2.6, 9)

def paint(im, seed):
    """印象派筆觸：由大到小四輪短筆觸，色彩上下跳動（冷暖點彩），並加上厚塗的受光／背光邊。"""
    rng = np.random.default_rng(seed)
    out = im.filter(ImageFilter.GaussianBlur(14)); d = ImageDraw.Draw(out)
    for n, w, L, bl, jit in [(5000, 36, 80, 16, 14), (20000, 17, 44, 7, 15), (55000, 8, 24, 3.5, 13), (70000, 4, 12, 1.5, 10)]:
        ref = np.asarray(im.filter(ImageFilter.GaussianBlur(bl)), np.float32); g = ref.mean(2)
        gx, gy = np.gradient(g, axis=1), np.gradient(g, axis=0)
        xs, ys = rng.integers(0, W, n), rng.integers(0, H, n)
        ang = np.arctan2(gy[ys, xs], gx[ys, xs]) + np.pi/2
        calm = np.hypot(gx[ys, xs], gy[ys, xs]) < .9
        ang = np.where(calm, rng.normal(0.12, .55, n), ang + rng.normal(0, .3, n))
        ln = L * rng.uniform(.55, 1.5, n); dx, dy = np.cos(ang)*ln/2, np.sin(ang)*ln/2
        tint = np.array([[16, 6, -14], [-14, 0, 16], [6, -4, 8], [0, 0, 0]])[rng.integers(0, 4, n)]
        col = ref[ys, xs] + rng.normal(0, jit, (n, 3)) + tint + rng.normal(0, jit, (n, 1))
        col = col.clip(0, 255)
        for i in range(n):
            a, b = (xs[i]-dx[i], ys[i]-dy[i]), (xs[i]+dx[i], ys[i]+dy[i]); ww = int(w * rng.uniform(.75, 1.25))
            if w >= 8:
                o = max(1.0, w * .14)
                d.line([(a[0]+o, a[1]+o), (b[0]+o, b[1]+o)], fill=tuple(int(v) for v in col[i]*.72), width=ww)
                d.line([(a[0]-o*.6, a[1]-o*.6), (b[0]-o*.6, b[1]-o*.6)], fill=tuple(int(min(255, v*1.12+6)) for v in col[i]), width=ww)
            d.line([a, b], fill=tuple(int(v) for v in col[i]), width=ww)
    a = np.asarray(out, np.float32) + rng.normal(0, 2.0, (H, W, 1))
    v = 1 - .14*(((X-W/2)/(W/2))**2 + ((Y-H/2)/(H/2))**2)[..., None]
    return Image.fromarray((a * v).clip(0, 255).astype(np.uint8))

def S(L):
    c = Cv()
    if L == 'A':
        c.grad(0, H, '#2b2447', '#7a4a66', '#b27a7a'); c.glow(720, 150, 170, '#ffe2a8', .8); c.disc(720, 150, 46, '#fff3cf', 3)
        c.hills(400, 40, '#3b3252', 1, 1.2); c.hills(500, 36, '#211b30', 2, 1.8)
        c.bare(210, 560, 1.5, 120, 14, '#120e1a'); c.bare(760, 560, 1.6, 90, 11, '#120e1a', 5, 8); c.ell(480, 560, 520, 50, '#8d7f9a', 30)
    if L == 'B':
        c.grad(0, H, '#f2b66e', '#f6d08e', '#f0e0b8'); c.glow(480, 360, 300, '#ffe9a0', .9)
        for x, y, rx, ry, col in [(260, 190, 150, 110, '#fff1d4'), (420, 150, 190, 130, '#fff8e6'), (610, 190, 170, 120, '#ffe3c0'), (770, 130, 130, 90, '#fff1d4'), (160, 110, 110, 80, '#ffe6c4')]: c.ell(x, y, rx, ry, col, 12)
        c.hills(470, 30, '#c9a24d', 3, 1.5); c.hills(540, 24, '#8f7a36', 4, 2.2); c.dots(500, (0, 450, W, H), ['#e8c864', '#c9a24d', '#a86f2f'], 2, 5)
    if L == 'C':
        c.grad(0, H, '#16233f', '#3d5c7a', '#9fb7c4'); c.glow(250, 140, 200, '#dfeeff', .7); c.disc(250, 140, 38, '#f4f8ff', 2)
        c.hills(430, 25, '#26364f', 5, 1.4); c.tower(700, 470, 70, 230, '#141c2c'); c.rect(682, 330, 718, 370, '#e3d9a0', 3)
        c.hills(520, 18, '#1a2535', 6, 2.5); c.dots(14, (60, 520, 520, 600), ['#aeb9c4', '#8e9ba8'], 14, 22, 7); c.ell(480, 540, 520, 60, '#c9d6de', 28)
    if L == 'D':
        c.grad(0, 400, '#0d1b4a', '#27437f', '#4d6fb0'); c.stars(180); c.glow(640, 130, 200, '#fff0b0', .6); c.disc(640, 130, 52, '#fff6d0', 2)
        c.hills(400, 8, '#18284f', 7, 1.2); c.rect(0, 400, W, H, '#1b2f5f', 0); c.water(400, '#1c3366', .55); c.glow(640, 520, 90, '#fff0b0', .35)
    if L == 'E':
        c.grad(0, H, '#f8e3b6', '#f7c58c', '#f4a56a'); c.glow(480, 380, 260, '#fff3c4', .9); c.disc(480, 380, 54, '#fffbe6', 3)
        c.hills(410, 20, '#b8a458', 8, 1.3); c.hills(470, 22, '#cdb05c', 9, 2); c.hills(540, 20, '#e0be5a', 10, 2.8)
        c.dots(700, (0, 440, W, H), ['#f1d36b', '#d8aa3e', '#fff0a8', '#b98a30'], 2, 6)
    if L == 'F':
        c.grad(0, H, '#625f73', '#a98f8a', '#d8b894'); c.hills(380, 30, '#6d6a62', 11, 1.1); c.hills(440, 22, '#7d7460', 12, 1.8)
        c.poly([(430, 410), (520, 410), (860, H), (100, H)], '#d9c39a', 4); c.bare(190, 470, 1.55, 100, 11, '#2a2420', 5, 13)
        c.ell(560, 470, 11, 26, '#1d1815', 1); c.disc(560, 436, 9, '#1d1815', 1); c.ell(548, 460, 20, 17, '#4b3a2a', 2)
    if L == 'G':
        c.grad(0, H, '#d8ecee', '#f2efd6', '#f7e8cf'); c.hills(400, 25, '#a9cfa4', 14, 1.2); c.hills(470, 28, '#8ec28f', 15, 1.9)
        c.ell(480, 440, 520, 70, '#f4f9f4', 30); c.dots(400, (0, 380, W, H), ['#ffffff', '#e6f6ff', '#fff6dd'], 1.5, 3.2)
    if L == 'H':
        c.grad(0, 380, '#bcd6f0', '#e5e4f0', '#f9e8e0'); c.glow(640, 372, 220, '#fff0d6', .8); c.disc(640, 372, 40, '#fffaf0', 3)
        c.ell(220, 130, 150, 40, '#f8efee', 14); c.ell(700, 90, 170, 34, '#fdf3ef', 14); c.rect(0, 380, W, H, '#b8d6ea', 0); c.water(380, '#a7c8e4', .5)
        c.boat(300, 430, 1.4, '#f2ece2', '#fffaf0')
    if L == 'I':
        c.grad(0, 400, '#3d1030', '#a3283a', '#ef7042', '#ffc477'); c.glow(480, 380, 280, '#ff9a55', .9); c.disc(480, 380, 90, '#ffd68a', 3)
        c.rect(0, 400, W, H, '#8c1c2c', 0); c.water(400, '#7a1627', .45); c.poly([(0, H), (0, 520), (180, 560), (330, H)], '#1e0a12', 2); c.poly([(960, H), (960, 500), (780, 560), (640, H)], '#1e0a12', 2)
    if L == 'J':
        c.grad(0, H, '#f4b9a0', '#fbdca8', '#fff2cc'); c.glow(480, 300, 280, '#fff6c0', .9); c.disc(480, 300, 70, '#fffbe0', 3)
        c.hills(330, 50, '#d9a4b4', 16, 1.2); c.hills(400, 44, '#a98fc0', 17, 1.7); c.hills(480, 40, '#7480b8', 18, 2.3); c.ell(480, 440, 520, 50, '#fff0e0', 26); c.hills(560, 30, '#4d6aa0', 19, 1.5)
    if L == 'K':
        c.grad(0, 430, '#34436a', '#8c7f9a', '#d19a82'); c.rect(0, 430, W, H, '#5a6a8a', 0); c.water(430, '#4d5d7c', .5)
        c.tower(690, 440, 90, 270, '#1b1d2e'); c.rect(668, 245, 712, 300, '#e8b86a', 3); c.disc(690, 272, 14, '#ffe9a0', 2)
        c.poly([(0, 480), (240, 440), (520, 480), (520, H), (0, H)], '#1f2233', 3)
    if L == 'L':
        c.grad(0, H, '#1a1230', '#472250', '#6a2b5a'); c.hills(430, 24, '#1c3a2c', 20, 1.4); c.hills(500, 20, '#15301f', 21, 2.2)
        for x, y in [(160, 220), (400, 170), (640, 240), (820, 150)]: c.glow(x, y, 90, '#ff9a5a', .85); c.disc(x, y, 15, '#ffe2a0', 2)
        c.dots(600, (0, 460, W, H), ['#e0457f', '#ff8fb0', '#ff9a4a', '#a83a8a', '#ffd0a0'], 3, 7)
    if L == 'M':
        c.grad(0, H, '#fbe3e6', '#fff1e4', '#fff8ec'); c.glow(760, 120, 240, '#fff6c8', .8); c.hills(380, 20, '#cfe6bd', 22, 1.3); c.hills(450, 24, '#b9d9a8', 23, 2.1)
        c.dots(500, (0, 400, W, H), ['#ffffff', '#ffd0da', '#fff0a8', '#d9c8f0'], 2, 5); c.ell(480, 470, 130, 34, '#e8c9a0', 3)
        c.ell(480, 440, 108, 34, '#fffaf2', 3); c.poly([(380, 440), (420, 380), (560, 380), (590, 440)], '#d9b48a', 2)
    if L == 'N':
        c.grad(0, H, '#8f919b', '#c9b793', '#e3c58f'); c.hills(400, 28, '#b9893f', 24, 1.2); c.hills(470, 30, '#8a6a34', 25, 1.9)
        c.bare(330, 520, 1.5, 130, 14, '#2a1d12', 6, 26); c.dots(700, (0, 430, W, H), ['#d9923a', '#b8702a', '#e6b050', '#7a5a2a'], 2, 5); c.ell(700, 330, 220, 40, '#d6d3d8', 22)
    if L == 'O':
        c.grad(0, H, '#1f2d57', '#3f64a0', '#7f9fc4'); c.glow(740, 130, 180, '#e8f0ff', .7); c.disc(740, 130, 36, '#f4f8ff', 2)
        c.tree(130, 470, 330, '#1a1f1a', '#1f3f2e'); c.tree(840, 480, 300, '#1a1f1a', '#1b3a2a'); c.hills(440, 26, '#2f5a3a', 27, 1.3); c.hills(520, 24, '#244a2e', 28, 2)
        c.dots(520, (0, 430, W, H), ['#f4d03f', '#ffe36a', '#8a63c9', '#b090e0'], 2, 6)
    if L == 'P':
        c.grad(0, H, '#12060d', '#4a1218', '#c0431f'); c.glow(480, 560, 420, '#ff8a30', .95); c.glow(480, 600, 180, '#ffd060', .9)
        c.hills(470, 40, '#10060a', 29, 1.4); c.poly([(380, H), (470, 500), (520, 500), (620, H)], '#ff9a30', 6); c.hills(560, 20, '#0b0407', 30, 2.4)
        c.dots(220, (100, 80, 860, 560), ['#ff9a30', '#ffd060', '#ff6a20'], 1.5, 3.8)
    if L == 'Q':
        c.grad(0, H, '#191845', '#4b3f8f', '#8a73b8'); c.glow(480, 250, 340, '#ffe08a', .95); c.glow(480, 250, 120, '#fff6d0', .95); c.disc(480, 250, 32, '#ffffff', 2)
        c.dots(700, (0, 0, W, 520), ['#ffe9a8', '#ffd770', '#fff6d8'], 1, 3.2); c.hills(520, 20, '#241f4a', 31, 1.4)
    if L == 'R':
        c.grad(0, H, '#44375f', '#a45a7a', '#f2a46a', '#fbd08a'); c.glow(480, 390, 260, '#ffd99a', .85); c.hills(430, 24, '#4a3a60', 32, 1.2); c.hills(500, 26, '#2b2040', 33, 1.7)
        c.rect(468, 270, 482, 450, '#140f1c', 1); c.rect(436, 308, 514, 322, '#140f1c', 1)
    if L == 'S':
        c.grad(0, 380, '#7f8fb5', '#c9a8a8', '#f2c9a0'); c.glow(300, 360, 220, '#ffe0b0', .7); c.rect(0, 380, W, H, '#8a8fb0', 0)
        x = 0
        for i in range(14):
            w = 70 + (i*37) % 50; hh = 70 + (i*53) % 110
            c.rect(x, 380-hh, x+w, 380, ['#5a5068', '#6a5a70', '#7a6070'][i % 3], 1); c.dots(5, (x+8, 380-hh+10, x+w-8, 370), ['#ffd98a'], 3, 4, i); x += w + 4
        c.water(380, '#6f7aa0', .55); c.boat(250, 520, 1.5, '#1d1822', '#1d1822'); c.boat(700, 560, 1.9, '#241c2a', '#e9dcc4')
    if L == 'T':
        c.grad(0, H, '#9cc7e8', '#d8e6d8', '#fbe9b7'); c.glow(760, 160, 200, '#fff3c0', .8); c.hills(400, 26, '#9fbe6a', 34, 1.2); c.hills(470, 26, '#c9bf62', 35, 1.9)
        c.ell(640, 540, 330, 26, '#8a8a3c', 6); c.tree(300, 540, 300, '#4a3420', '#4f7a3a'); c.dots(500, (0, 450, W, H), ['#e8d070', '#c9b050', '#f4e8a0', '#8aa850'], 2, 5)
    if L == 'U':
        c.grad(0, H, '#1b1230', '#5a2440', '#8c3438'); c.glow(480, 180, 260, '#d8506a', .6); c.hills(500, 20, '#0f0a18', 36, 1.2)
        for x, w, h in [(300, 90, 220), (480, 130, 300), (660, 90, 200)]:
            c.rect(x-w/2, 520-h, x+w/2, 520, '#120c1c', 1)
            for k in range(4): c.rect(x-w/2+k*w/4, 520-h-18, x-w/2+k*w/4+w/8, 520-h, '#120c1c', 1)
        c.rect(468, 330, 492, 380, '#f0c060', 3); c.line([(130, 0), (170, 90), (140, 110), (190, 230)], 5, '#fff6c0', 2); c.glow(190, 230, 60, '#fff6c0', .6)
    if L == 'V':
        c.grad(0, 380, '#16284a', '#4a6a9a', '#a8c0dc'); c.glow(480, 170, 260, '#e8f0ff', .85); c.disc(480, 170, 80, '#f8fbff', 3)
        c.rect(0, 380, W, H, '#8aa8c8', 0); c.water(380, '#6f90b8', .5); c.tree(90, 420, 330, '#10182a', '#152238'); c.tree(880, 430, 300, '#10182a', '#152238')
        c.dots(14, (200, 470, 760, 600), ['#f4f8ff', '#e6f0ff'], 14, 24, 37)
    if L == 'W':
        c.grad(0, H, '#a8d8f5', '#d6ecda', '#f6f1d0'); c.glow(800, 110, 180, '#fff8d0', .8); c.hills(380, 22, '#8ccc78', 38, 1.3); c.hills(450, 24, '#6fba5e', 39, 2)
        c.dots(800, (0, 400, W, H), ['#ffffff', '#ffd23f', '#ff6b6b', '#ff9ecb', '#b48df0'], 2, 6)
        for i in range(12):
            x, y = 120 + i*65, 200 + (i*47) % 170; col = ['#ff9a3c', '#5aa0f0', '#ffd23f'][i % 3]
            c.ell(x-8, y, 9, 6, col, 1); c.ell(x+8, y, 9, 6, col, 1)
    if L == 'X':
        c.grad(0, H, '#c8452f', '#ef8a3c', '#fbc66a'); c.glow(480, 330, 300, '#ffe0a0', .8); c.hills(430, 30, '#7a4a3a', 40, 1.2)
        c.poly([(260, 300), (700, 300), (480, 230)], '#e9d8b8', 1); c.rect(260, 300, 700, 322, '#d9c7a4', 1)
        for i in range(6): c.rect(280+i*72, 322, 304+i*72, 470, '#f0e2c4', 1)
        c.rect(240, 470, 720, 500, '#d9c7a4', 1); c.rect(220, 500, 740, 530, '#c9b794', 1); c.hills(560, 28, '#5a362c', 41, 1.7)
    if L == 'Y':
        c.grad(0, H, '#8fc3ee', '#c8e2ee', '#f3f0dc')
        for x, y, rx, ry in [(200, 120, 150, 40), (560, 90, 190, 46), (820, 160, 140, 34)]: c.ell(x, y, rx, ry, '#ffffff', 10)
        c.hills(360, 24, '#9cc882', 42, 1.2); c.hills(430, 26, '#7fb86a', 43, 1.7); c.hills(510, 24, '#5fa04e', 44, 2.3)
        c.rect(600, 330, 720, 410, '#efe2c2', 1); c.poly([(588, 332), (732, 332), (660, 280)], '#b2442f', 1); c.tree(180, 440, 220, '#4a3420', '#3f7a3a'); c.tree(820, 450, 200, '#4a3420', '#4a8a3e')
    if L == 'Z':
        c.grad(0, H, '#2a6fd6', '#6aa6e8', '#bfe1f7'); c.glow(480, 90, 300, '#fff6c0', .9); c.disc(480, 90, 58, '#fffdf0', 3)
        c.ell(180, 210, 130, 34, '#ffffff', 10); c.ell(780, 250, 150, 38, '#ffffff', 10); c.hills(440, 22, '#78b85a', 45, 1.3); c.hills(500, 24, '#5fa044', 46, 2)
        c.dots(800, (0, 420, W, H), ['#e63b2e', '#ff7a2e', '#d02a2a', '#ffd23f'], 2, 6)
    return c.im

if __name__ == '__main__':
    raw = open(os.path.join(HERE, '..', 'js', 'data.js'), encoding='utf-8').read()
    data = json.loads(raw.split('=', 1)[1].strip().rstrip(';'))
    only = [a.upper() for a in sys.argv[1:]]
    os.makedirs(OUT, exist_ok=True)
    for e in data:
        L = e['letter']
        if only and L not in only: continue
        paint(S(L), ord(L)).save(os.path.join(OUT, f"{L}_{e['word'].lower()}.jpg"), quality=88, optimize=True)
        print('done', L, e['word'], flush=True)
