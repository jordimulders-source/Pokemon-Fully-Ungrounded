# maak_r11.py: Gnometrotter Grass r11 = r10 met een eigen lichte groene ramp voor baard- en haarbladeren.
# Geen vrije index (bruin 2-4 en groen 5 liggen allemaal >= 37 RGB uit elkaar), dus: de muts neemt de donkere twee
# tinten (12 + 5, hooglicht 13), de bladeren de lichte (14, 13, schaduw 12). Plus 4 losse pixels opgeruimd. Rest 0 px.
import os, sys, numpy as np
from PIL import Image
from scipy import ndimage
HIER=os.path.dirname(os.path.abspath(__file__)); os.chdir(HIER)
sys.path.insert(0,'../sprite_r10'); cwd=os.getcwd(); os.chdir('../sprite_r10')
import maak_r10 as r10          # zones en r9-basis (B9) van r10
os.chdir(cwd)
bim=Image.open('../sprite_r10/gnometrotter_grass.png'); B=np.asarray(bim).astype(int); O=B.copy(); B9=r10.B
muts=r10.ZONES['muts']; blad=r10.ZONES['baard']|r10.ZONES['haar L']|r10.ZONES['haar R']
WIJZ={}
# muts: linkerblad (r9: 13) 14->13 (hooglicht), 13->12 (lijf), 12->5 (sikkel); rechterblad (r9: 12) 13->12 (rand langs nerf), 12->5
for y,x in zip(*np.nonzero(muts)):
    v=B[y,x]
    if B9[y,x] in (13,14): n={14:13,13:12,12:5}.get(v,v)
    elif B9[y,x]==12:      n={13:12,12:5}.get(v,v)
    else: n=v
    if n!=v: O[y,x]=n; WIJZ[(x,y)]='muts'
# losse pixels: vlakjes van 1 px tussen nerven/omlijning; de enige passende 4-buurtint is de nerf (5): erin opnemen.
# (32,15) is door de mutsverdeling al 5 geworden.
for x,y in ((18,32),(32,15),(32,16),(35,14)):
    nb=[O[y+dy,x+dx] for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)) if O[y+dy,x+dx] in (5,12,13,14)]
    v=max(set(nb),key=nb.count)
    if v!=O[y,x]: O[y,x]=v; WIJZ[(x,y)]='losse pixel'
# palet: bladeren licht geelgroen (model), muts donker; 5 iets lichter zodat het schaduwblad van de muts niet zwart wordt
pal=bim.getpalette()[:48]
NIEUW={14:(184,214,120),13:(136,182,92),12:(80,124,64),5:(42,74,44)}
OUD={i:tuple(pal[i*3:i*3+3]) for i in NIEUW}
for i,c in NIEUW.items(): pal[i*3:i*3+3]=list(c)
if __name__=='__main__':
    ver=O!=B
    assert not (ver&~(muts|blad)).any()
    tel={}
    for z in WIJZ.values(): tel[z]=tel.get(z,0)+1
    print('t.o.v. r10:',tel,'rest 0')
    with open('log_r11.txt','w') as f:
        for (x,y),z in sorted(WIJZ.items(),key=lambda t:(t[0][1],t[0][0])): f.write('%s x=%d y=%d %d->%d\n'%(z,x,y,B[y,x],O[y,x]))
        for i in NIEUW: f.write('palet %d: %s -> %s\n'%(i,OUD[i],NIEUW[i]))
    out=Image.new('P',(64,64)); out.putpalette(pal); out.putdata(O.astype('uint8').ravel().tolist())
    out.save('gnometrotter_grass.png'); out.resize((512,512),Image.NEAREST).save('gnometrotter_grass_8x.png')
    sys.path.insert(0,'../../gnometrotter_rock/sprite'); os.chdir('../../gnometrotter_rock/sprite')
    from kijk import sprite, model_op_schaal
    m=model_op_schaal('../../gnometrotter_grass/hybride/model_hybride.png',512); os.chdir(HIER)
    ps=[m,sprite('../sprite_r10/gnometrotter_grass.png').resize((512,512),Image.NEAREST),sprite('gnometrotter_grass.png').resize((512,512),Image.NEAREST)]
    W=Image.new('RGB',(3*520,512),'white')
    for k,p in enumerate(ps): W.paste(p,(k*520,0))
    W.save('vel.png')
