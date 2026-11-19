"""Gedeelde palet- en rasterhulpjes voor de viscacha-overworld (eigen methode, zonder Gemini).
Rasters zijn tekst: '.'=transparant, 1-f = paletindex (hex)."""
import numpy as np
from PIL import Image
# Frontkleuren (af/normal.pal) + omlijning: 1 = bovenrand (donkere tint), 2 = zwart (onder/opzij)
PAL = [
 (152,208,160), # 0 transparant
 (80,44,24),    # 1 omlijning boven (donkerbruin)
 (0,0,0),       # 2 omlijning onder/opzij (zwart)
 (128,72,42),   # 3 donkerbruin (front 2): ooglid, diepe binnenlijn
 (190,110,64),  # 4 bruin (front 3): diepe schaduw, verre poten
 (208,148,82),  # 5 schaduw zand (front 4)
 (238,184,100), # 6 zand (front 5) hoofdvlak
 (252,222,150), # 7 licht zand (front 11)
 (222,194,136), # 8 creme schaduw (front 6)
 (244,232,196), # 9 creme (front 7)
 (176,132,24),  # a goud (front 8)
 (228,192,52),  # b geel (front 9)
 (252,232,98),  # c lichtgeel (front 10)
 (160,114,68),  # d oorbinnenkant/staartbruin (front 12)
 (248,248,248), # e wit (glans)
 (140,124,104), # f snorhaar (front 15)
]
def parse(txt):
    rows=[r for r in txt.strip('\n').split('\n')]
    a=np.zeros((32,32),np.uint8)
    for y,r in enumerate(rows):
        r=r.split('|')[-1] if '|' in r else r
        for x,c in enumerate(r[:32]):
            if c not in '. ': a[y,x]=int(c,16)
    return a
def totext(a):
    return '\n'.join('%2d|'%y+''.join('.' if v==0 else '%x'%v for v in a[y]) for y in range(a.shape[0]))
def rgba(a,pal=PAL,bg=None):
    o=np.zeros(a.shape+(4,),np.uint8)
    for k in range(1,16): o[a==k]=pal[k]+(255,)
    im=Image.fromarray(o,'RGBA')
    if bg:
        b=Image.new('RGBA',im.size,bg+(255,)); b.alpha_composite(im); im=b
    return im
def front_rgba(path,palpath):
    im=Image.open(path); a=np.array(im)
    L=open(palpath).read().split('\n')[3:19]; P=[tuple(int(v) for v in l.split()) for l in L]
    return rgba(a,P),a
