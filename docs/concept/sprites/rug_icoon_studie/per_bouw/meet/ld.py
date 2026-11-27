import os,sys,numpy as np
from PIL import Image
R='/home/user/Pokemon-Fully-Ungrounded'
sys.path.insert(0,R+'/docs/concept/sprites/rug_icoon_studie/verhoudingen')
import laad
def front(sp):
    D=R+'/graphics/pokemon/'+sp
    return laad.front(sp,D+'/anim_front_gba.png',D+'/normal_gba.pal')
def icon_gba(sp):
    D=R+'/graphics/pokemon/'+sp; im=Image.open(D+'/icon_gba.png'); q=im.getpalette()[:48]
    return laad.rgba(np.array(im)[:32,:32],[tuple(q[3*k:3*k+3]) for k in range(16)])
def icon_new(sp): return laad.icoon(sp)
def idx(sp,w):
    D=R+'/graphics/pokemon/'+sp
    if w=='f': return np.array(Image.open(D+'/anim_front_gba.png'))[:64,:64]
    if w=='g': return np.array(Image.open(D+'/icon_gba.png'))[:32,:32]
    return np.array(Image.open(D+'/icon.png'))[:32,:32]
import re
_G=None
def ipi_gba(sp):
    global _G
    if _G is None:
        _G={}; d=R+'/src/data/pokemon/species_info/'
        for fn in os.listdir(d):
            for mm in re.finditer(r'\[SPECIES_([A-Z0-9_]+)\]\s*=\s*\{(.*?)\n    \},',open(d+fn).read(),re.S):
                v=re.search(r'iconPalIndex = (?:P_GBA_STYLE_SPECIES_ICONS \? (\d) : )?(\d)',mm.group(2))
                if v: _G[mm.group(1).lower()]=int(v.group(1) or v.group(2))
    return _G.get(sp,0)
def icon_gba(sp):
    D=R+'/graphics/pokemon/'+sp; im=Image.open(D+'/icon_gba.png')
    return laad.rgba(np.array(im)[:32,:32],laad.pal(R+'/graphics/pokemon/icon_palettes/pal%d.pal'%ipi_gba(sp)))
