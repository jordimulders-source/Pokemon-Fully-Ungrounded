# Gedeelde hulpjes frame 2 per script (27 nov). Engine-simulatie nagerekend uit src/pokemon_animation.c
# (zelfde aanpak als gengas/frame2/combi_c.py, uitgebreid met affine schaal/rotatie zoals ObjAffineSet).
import math, numpy as np
from PIL import Image, ImageDraw
GREEN = None

def sinv(i, amp):  # gSineTable: Sin(i,amp) = sin(2pi*i/256)*amp, afgekapt
    return int(math.sin(2*math.pi*(i % 256)/256)*amp)

def rgba(x, pal):
    o = Image.fromarray(x, 'P'); o.putpalette(pal); d = np.array(o.convert('RGBA')); d[x == 0, 3] = 0
    return d

def affine(src, sx=256, sy=256, rot=0):
    """Engine-affine (DOUBLE-modus) op een 64x64 RGBA-array: sx/sy zoals HandleSetAffineData
    (>256 = kleiner), rot in 0..65535. Nearest, rond het midden (32,32)."""
    if sx == 256 and sy == 256 and rot == 0:
        return src
    th = 2*math.pi*rot/65536
    pa, pb = sx*math.cos(th)/256, -sx*math.sin(th)/256
    pc, pd = sy*math.sin(th)/256, sy*math.cos(th)/256
    out = np.zeros((128, 128, 4), np.uint8)
    yy, xx = np.mgrid[0:128, 0:128]
    dx, dy = xx-64+0.5, yy-64+0.5
    u = np.floor(pa*dx+pb*dy+32).astype(int); v = np.floor(pc*dx+pd*dy+32).astype(int)
    ok = (u >= 0) & (u < 64) & (v >= 0) & (v < 64)
    out[ok] = src[v[ok], u[ok]]
    return out[32:96, 32:96] if False else out

# --- engine-animaties: functie t -> (x2, y2, sx, sy, rot) ---
def geen(t): return (0, 0, 256, 256, 0)
def v_slide(t):  # Anim_VerticalSlide, data0=40
    return (0, -sinv((t*384//40) % 256, 6) if t <= 40 else 0, 256, 256, 0)
def h_slide(t):  # Anim_HorizontalSlide, data0=40
    return (sinv((t*384//40) % 256, 6) if t <= 40 else 0, 0, 256, 256, 0)
def v_shake(t):  # Anim_VerticalShake, data0=60, tot 2304
    c = t*60
    return (0, sinv(c % 256, 3) if c <= 2304 else 0, 256, 256, 0)
def h_shake(t):  # Anim_HorizontalShake, data0=60, amp 3
    c = t*60
    return (sinv(c % 256, 3) if c <= 2304 else 0, 0, 256, 256, 0)
def v_shake_h_slide(t):  # Anim_VerticalShakeHorizontalSlide, +48 per tik tot 2048
    c = t*48
    if c > 2048: return geen(t)
    k = (c//512) % 4; m = c % 512
    x = [m//32, -(m*16)//512+16, -(m*16)//512, m//32-16][k]
    return (x, sinv(c % 128, 4), 256, 256, 0)
def v_squish_bounce(t, d0=16):  # Anim_VerticalSquishBounce (data0=16), 3*d0 tikken
    if t > d0*3: return geen(t)
    d3 = 0
    for i in range(t+1):
        if d0 < i < d0*2: d3 += 128//d0
    d4 = (t*(128//d0)) & 0xFF
    ys = sinv(d4, 32)+256; posy = (256-ys)//8 if ys > 256 else 0
    return (0, -sinv(d3, 10)-posy, 256-sinv(d4, 32), ys, 0)
def h_slide_wobble(t):  # Anim_HorizontalSlideWobble, 100 tikken
    if t > 100: return geen(t)
    idx = t*256//100; var = (t*512//100) & 0xFF
    return (sinv(idx, 8), 0, 256, 256, sinv(var, 3276) & 0xFFFF)

ANIMS = {'ANIM_V_SLIDE': v_slide, 'ANIM_H_SLIDE': h_slide, 'ANIM_V_SHAKE': v_shake, 'ANIM_H_SHAKE': h_shake,
         'ANIM_V_SHAKE_H_SLIDE': v_shake_h_slide, 'ANIM_V_SQUISH_AND_BOUNCE': v_squish_bounce,
         'ANIM_H_SLIDE_WOBBLE': h_slide_wobble, 'geen': geen}

def render_gif(f1, f2, pal, anim, pad, start=6, eind=40, Z=5, tot=110):
    F = [rgba(f1, pal), rgba(f2, pal)]
    imgs, dur = [], []
    for t in range(0, tot, 2):
        x2, y2, sx, sy, rot = ANIMS[anim](t)
        f = 1 if start <= t < eind else 0
        s = Image.fromarray(affine(F[f], sx, sy, rot) if (sx, sy, rot) != (256, 256, 0) else np.pad(F[f], ((32, 32), (32, 32), (0, 0))))
        c = Image.new('RGBA', (128, 128), (255, 255, 255, 255)); c.alpha_composite(s, (x2, y2))
        c = c.crop((16, 16, 112, 112))
        imgs.append(c.convert('RGB').resize((96*Z, 96*Z), Image.NEAREST)); dur.append(33)
    dur[-1] = 1000
    imgs[0].save(pad, save_all=True, append_images=imgs[1:], duration=dur, loop=0)

def save_anim_front(f1, f2, pal, pad):
    o = Image.fromarray(np.vstack([f1, f2]), 'P'); o.putpalette(pal); o.save(pad, transparency=0)

def vel(rijen, pal, pad, Z=4):
    """rijen: lijst van (naam, f1, f2, anim). Per variant frame 1 | frame 2 op 4x, naam + anim eronder."""
    W = 64*Z; H = 64*Z+30
    sh = Image.new('RGB', (len(rijen)*(2*W+24)+8, H+8), 'white'); d = ImageDraw.Draw(sh)
    for i, (naam, f1, f2, anim) in enumerate(rijen):
        x0 = 8+i*(2*W+24)
        for j, f in enumerate((f1, f2)):
            im = Image.alpha_composite(Image.new('RGBA', (64, 64), (255, 255, 255, 255)), Image.fromarray(rgba(f, pal)))
            sh.paste(im.convert('RGB').resize((W, W), Image.NEAREST), (x0+j*(W+4), 4))
            d.rectangle([x0+j*(W+4), 4, x0+j*(W+4)+W-1, 4+W-1], outline=(200, 200, 200))
        d.text((x0, W+10), f'{naam}: frame 1 | frame 2', fill=(0, 0, 0))
        d.text((x0, W+22), anim, fill=(0, 0, 0))
    sh.save(pad)
