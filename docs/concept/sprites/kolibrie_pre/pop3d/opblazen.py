"""Kolibrie pre-evo: 3D-model door silhouet A zelf op te blazen (hoogteveld = wortel van de afstand tot de rand),
zodat de omtrek gelijk is aan het goedgekeurde silhouet (Jordi: "79% overlap is waarom het fout gaat").
Delen (kop, buik, vleugel, staart, bek, oog, pootjes) in spritecoördinaten van A; kop en vleugel krijgen een eigen bolling.
Draaien vanuit deze map: python3 opblazen.py"""
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage as nd
K = 12                      # 64 -> 768
A = np.asarray(Image.open('../silhouet/silhouet_v3a_hand_1x.png').convert('L')) < 128
PALET = {
    'fluweel (als eindvorm)': dict(body='#6E5A8C', head='#3E2E52', wing='#4A3A63', belly='#D9CFE8'),
    'dons (jong, doffer)': dict(body='#8A7F96', head='#5E5470', wing='#5A4F68', belly='#EEE8F2'),
    'hillstar + violet': dict(body='#8C7A6A', head='#6A5A62', wing='#5E4E5E', belly='#F2EEE8'),
}
VAST = dict(beak='#262030', gape='#F4C83C', eye='#120C18', glint='#FFFFFF', feet='#262030')
LINE = np.array((34, 24, 44), float)
def hexc(h): return np.array([int(h[i:i + 2], 16) for i in (1, 3, 5)], float)

BEK_BOVEN = [(19.8, 27.0), (11.0, 23.2), (11.2, 24.9), (19.8, 29.0)]   # spritecoördinaten (pixelhoeken), volgt A
BEK_ONDER = [(19.8, 29.2), (12.0, 30.0), (12.4, 31.0), (19.8, 31.0)]
def masker():
    lijf = A.copy(); lijf[:, :19] = False
    up = np.kron(lijf.astype(float), np.ones((K, K)))
    M = nd.gaussian_filter(up, K * 0.7) > 0.5
    im = Image.new('L', (64 * K, 64 * K), 0); dr = ImageDraw.Draw(im)
    for p in (BEK_BOVEN, BEK_ONDER): dr.polygon([(x * K, y * K) for x, y in p], fill=255)
    return M | (np.asarray(im) > 0)
def ell(cx, cy, rx, ry, ang=0):
    yy, xx = np.mgrid[0:64 * K, 0:64 * K] / K
    a = np.radians(ang); dx, dy = xx - cx, yy - cy
    u = dx * np.cos(a) + dy * np.sin(a); v = -dx * np.sin(a) + dy * np.cos(a)
    return (u / rx) ** 2 + (v / ry) ** 2 <= 1
def delen(M):
    yy, xx = np.mgrid[0:64 * K, 0:64 * K] / K
    d = {}
    d['head'] = M & ell(29.5, 28.8, 10.6, 8.2) & (xx >= 19.3)
    d['beak'] = M & (xx < 19.9)
    d['gape'] = M & ell(20.0, 29.1, 1.3, 1.5)
    d['belly'] = M & ell(30.5, 44.5, 7.5, 10.5, -15) & ~d['head']
    d['wing'] = M & ell(42.0, 44.5, 12.5, 4.2, 62) & ~d['head']
    d['tail'] = M & (xx > 43.5) & (yy > 52.5) & ~d['wing']
    d['feet'] = M & (yy > 52.0) & ((ell(32.0, 53.0, 1.6, 1.6)) | ell(37.0, 53.2, 1.8, 1.6))
    d['eye'] = ell(25.2, 27.8, 1.7, 1.9)
    d['glint'] = ell(24.7, 27.1, 0.6, 0.6)
    return d
def hoogte(M, d):
    h = np.sqrt(nd.distance_transform_edt(M))
    hk = np.sqrt(nd.distance_transform_edt(d['head'])) * 1.15 + 3
    hw = np.sqrt(nd.distance_transform_edt(d['wing'])) * 0.9 + h * 0.85
    h = np.maximum(h, np.where(d['head'], hk, 0)); h = np.where(d['wing'], np.maximum(h, hw), h)
    return nd.gaussian_filter(h, 5.0)
def render(palet, out=256):
    M = masker(); d = delen(M); h = hoogte(M, d)
    gy, gx = np.gradient(h * 6)
    n = np.dstack([-gx, gy, np.ones_like(h) * 1.0]); n /= np.linalg.norm(n, axis=2, keepdims=True)
    L = np.array((-0.5, 0.6, 0.62)); L /= np.linalg.norm(L)
    lit = n @ L
    col = {**PALET[palet], **VAST, 'tail': PALET[palet]['wing']}
    rgb = np.ones((64 * K, 64 * K, 3)) * 255
    rgb[M] = hexc(col['body'])
    for g in ('belly', 'wing', 'tail', 'head', 'beak', 'feet', 'gape'):
        rgb[d[g]] = hexc(col[g])
    sh = M & (lit < 0.42) & ~d['gape'] & ~d['belly'] | (d['belly'] & (lit < 0.2))
    rgb[sh] *= 0.78
    hl = M & (lit > 0.93) & ~d['beak'] & ~d['feet']
    rgb[hl] = rgb[hl] * 0.75 + 255 * 0.25
    oog = d['eye'] & M
    rgb[oog] = hexc(col['eye']); rgb[d['glint'] & M] = 255
    # omlijning: silhouet + grenzen kop/lijf, vleugel, bek, oog
    rand = M & ~nd.binary_erosion(M, iterations=5)
    grens = np.zeros_like(M)
    for g in ('head', 'wing', 'beak', 'eye', 'gape'):
        x = d[g] & M
        grens |= x & ~nd.binary_erosion(x, iterations=3)
    rgb[rand | grens] = LINE
    img = Image.fromarray(rgb.clip(0, 255).astype(np.uint8))
    ys, xs = np.nonzero(M); m = 2 * K
    b = (xs.min() - m, ys.min() - m, xs.max() + m, ys.max() + m); s = max(b[2] - b[0], b[3] - b[1])
    cx, cy = (b[0] + b[2]) // 2, (b[1] + b[3]) // 2
    img = img.crop((cx - s // 2, cy - s // 2, cx + s // 2, cy + s // 2)).resize((out, out), Image.LANCZOS)
    return img, M
def overlap(M):
    m1 = np.asarray(Image.fromarray((M * 255).astype(np.uint8)).resize((64, 64), Image.BOX)) >= 128
    return (m1 & A).sum() / (m1 | A).sum(), m1
if __name__ == '__main__':
    F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 13)
    FB = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 17)
    cell = 262; V = Image.new('RGB', (12 + cell * 4, 44 + (256 + 30) * 2), 'white'); dr = ImageDraw.Draw(V)
    dr.text((12, 12), 'Kolibrie pre-evo: 3D-model = silhouet A opgeblazen (omtrek gelijk aan A)', font=FB, fill=(30, 30, 30))
    img, M = render('fluweel (als eindvorm)')
    iou, m1 = overlap(M)
    sil = Image.fromarray(np.where(A, 0, 255).astype(np.uint8)).convert('RGB').resize((256, 256), Image.NEAREST)
    ov = np.full((64, 64, 3), 255, np.uint8); ov[m1 & A] = (90, 170, 90); ov[A & ~m1] = (220, 60, 60); ov[m1 & ~A] = (60, 90, 220)
    for i, (im, lab) in enumerate([(sil, 'silhouet A (goedgekeurd)'), (img, 'model (fluweel)'), (Image.fromarray(ov).resize((256, 256), Image.NEAREST), f'model over A: overlap {iou:.0%}')]):
        V.paste(im, (12 + cell * i, 44)); dr.text((14 + cell * i, 44 + 260), lab, font=F, fill=(60, 60, 60))
    foto = Image.open('../referenties/jordi_1_zittend_jong.webp').convert('RGB').crop((200, 140, 740, 710)); foto.thumbnail((256, 256))
    V.paste(foto, (12 + cell * 3, 44)); dr.text((14 + cell * 3, 44 + 260), 'foto 1 (bron)', font=F, fill=(60, 60, 60))
    for i, naam in enumerate(['dons (jong, doffer)', 'hillstar + violet']):
        img, _ = render(naam); V.paste(img, (12 + cell * (i + 1), 44 + 286)); dr.text((14 + cell * (i + 1), 44 + 286 + 260), naam, font=F, fill=(60, 60, 60))
    f3 = Image.open('../referenties/jordi_3_nestjongen.png').convert('RGB').crop((0, 225, 220, 447)).resize((256, 256))
    V.paste(f3, (12 + cell * 3, 44 + 286)); dr.text((14 + cell * 3, 44 + 286 + 260), 'foto 3 (bek)', font=F, fill=(60, 60, 60))
    V.save('vel_ronde3.png'); print('overlap', iou)
