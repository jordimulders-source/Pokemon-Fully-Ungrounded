"""Palette swaps op sprite_bijl_r1 (alleen paletindices, pixels identiek)."""
from PIL import Image, ImageDraw
import sys, os
D = os.path.dirname(os.path.abspath(__file__))
base = Image.open(os.path.join(D, '../sprite_bijl_r1/terreurvogel_bijl_r1.png'))
pal0 = base.getpalette()[:48]
SNAVEL = {
 'steen (r1)':   [(76,70,64),(104,97,89),(176,168,154)],
 'vuursteen':    [(46,46,54),(78,78,90),(140,140,150)],
 'zandsteen':    [(110,82,56),(160,124,86),(214,184,138)],
 'fossielbot':   [(96,84,62),(150,134,104),(212,200,170)],
}
LIJF = {
 'model':        [(77,70,65),(126,109,88),(162,142,112)],
 'donker umber': [(52,40,36),(86,66,56),(122,96,78)],
 'antraciet':    [(40,40,44),(70,68,72),(108,102,100)],
}
VARS = [('steen (r1)','model'),('vuursteen','model'),('zandsteen','model'),('fossielbot','model'),
        ('steen (r1)','donker umber'),('vuursteen','donker umber'),('fossielbot','donker umber'),
        ('steen (r1)','antraciet'),('vuursteen','antraciet'),('zandsteen','antraciet')]
S = 6
cols = 5; W, H = 64*S, 64*S + 20
vel = Image.new('RGB', (cols*W, ((len(VARS)+cols-1)//cols)*H), 'white')
dr = ImageDraw.Draw(vel)
for i,(sn,lf) in enumerate(VARS):
    p = list(pal0)
    for k,c in enumerate(SNAVEL[sn]): p[(3+k)*3:(3+k)*3+3] = c
    for k,c in enumerate(LIJF[lf]):   p[(6+k)*3:(6+k)*3+3] = c
    im = base.copy(); im.putpalette(p + [0]*(768-len(p)))
    naam = f'v{i+1}'
    im.save(os.path.join(D, f'{naam}.png'), transparency=0)
    rgba = Image.open(os.path.join(D, f'{naam}.png')).convert('RGBA').resize((64*S,64*S), Image.NEAREST)
    x, y = (i%cols)*W, (i//cols)*H
    vel.paste(rgba, (x, y+20), rgba)
    dr.text((x+6, y+4), f'{naam}: snavel {sn} / lijf {lf}', fill='black')
vel.save(os.path.join(D, 'vel_swaps.png'))
