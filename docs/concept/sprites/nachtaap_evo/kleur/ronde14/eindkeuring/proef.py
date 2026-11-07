# Proef van de voorgestelde reparaties (schrijft alleen proefbestanden in eindkeuring/, nooit de sprite zelf)
import numpy as np
from PIL import Image
R='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/nachtaap_evo/kleur/ronde14/'
im=Image.open(R+'nachtaap.png'); a=np.array(im); b=a.copy()
FIX=[ # (x,y,oud,nieuw)
 # F1 onderrand voeten zwart (schaduwkant)
 (9,59,14,1),(10,61,14,1),(23,58,14,1),(24,58,14,1),(25,58,14,1),(31,59,14,1),
 # F2 tenen uitlijnen (geen dambord/hark)
 (35,59,14,12),(36,59,12,14),    # achtervoet
]
for x,y,o,n in FIX:
    assert a[y,x]==o,(x,y,a[y,x],o); b[y,x]=n
print('gewijzigd',int((a!=b).sum()),'alpha-diff',int(((a>0)!=(b>0)).sum()))
out=Image.fromarray(b,'P'); out.putpalette(im.getpalette()); out.save(R+'eindkeuring/proef_fix.png',transparency=0)
def rgba(arr):
    i=Image.fromarray(arr,'P'); i.putpalette(im.getpalette()); r=i.convert('RGBA'); px=r.load()
    for y in range(64):
        for x in range(64):
            if arr[y,x]==0: px[x,y]=(0,0,0,0)
    return r
S=6; vel=Image.new('RGBA',(64*S*2+30+140,64*S*2+30),(255,255,255,255))
for j,bg in enumerate([(248,248,248),(36,36,44)]):
    for i,arr in enumerate([a,b]):
        c=rgba(arr).crop((0,44,48,64)).resize((48*S,20*S),Image.NEAREST)
        x=10+i*(48*S+10); y=10+j*(20*S+10)
        vel.paste(bg+(255,),(x,y,x+48*S,y+20*S)); vel.alpha_composite(c,(x,y))
        vel.paste(bg+(255,),(x,300+j*80,x+70,300+j*80+70)); vel.alpha_composite(rgba(arr),(x+3,300+j*80+3))
vel.save(R+'eindkeuring/proef_voor_na.png')
