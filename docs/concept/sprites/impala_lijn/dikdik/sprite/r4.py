# r4 = r3 + oog als ronde vorm uit het model (geen meerderheid per cel).
# Gemeten in het model (natief raster + 1024-model): ring buitenrand natief x36-47, y36-47 = 7,0 spritepx,
# middelpunt sprite (15,85 ; 22,8); donkere binnenkant (iris+pupil) oppervlak-straal 2,6 px (~21 px);
# glimlicht natief c40-41 r40-41 = cel (15,22); pupil (zwart) rond (16,23); zwarte bovenlijn natief r38; bruine iris onderaan natief r44-45.
# A = 7x7 schijf, ring 1 px rondom.  B = 8x8 schijf, ring 1 px boven/links, 2 px onder/rechts (middelpunt (16,23), dichter bij het model).
# Diff 0 buiten de oogzone x11-19, y18-26 (sprite-lokaal; canvas x21-29, y24-32).
import json, numpy as np
from collections import Counter
from PIL import Image
src=json.load(open('r3/grid.json')); OX,OY=src['OX'],src['OY']; R3=src['grid']
ZONE=(11,18,19,26)
# binnenkant per cel uit het natieve oog (12x12): de bijna zwarte iris (55,36,31) leest in het model als pupil -> zwart,
# alleen de iets lichtere irisrand rechts in D en de bruine onderhelft (natief r44-45 '3/7') in S; glimlicht (15,22).
BINNEN={(14,20):'0',(15,20):'0',(16,20):'0',
        (13,21):'0',(14,21):'0',(15,21):'0',(16,21):'D',(17,21):'D',
        (13,22):'0',(14,22):'0',(15,22):'C',(16,22):'0',(17,22):'D',
        (13,23):'0',(14,23):'0',(15,23):'0',(16,23):'0',(17,23):'D',
        (14,24):'S',(15,24):'S',(16,24):'S'}
def schijf(rows): return {(x,y) for y,(a,b) in rows.items() for x in range(a,b+1)}
VAR={'A':schijf({19:(14,16),20:(13,17),21:(12,18),22:(12,18),23:(12,18),24:(13,17),25:(14,16)}),
     'B':schijf({19:(14,17),20:(13,18),21:(12,19),22:(12,19),23:(12,19),24:(12,19),25:(13,18),26:(14,17)})}
OUDOOG={(x,y) for y in range(19,26) for x in range(12,19)}
# hoeken die bij r3 oog waren en nu vacht worden: vachttint uit de omgeving in het model (M), traanvlek blijft D
VACHT={(18,20):'M',(18,24):'M',(13,25):'M',(17,25):'M',(13,19):'M',(17,19):'M'}
PAL={'.':(0,0,0),'0':(24,16,20),'D':(66,34,18),'S':(108,58,26),'M':(160,92,40),'L':(194,120,56),'C':(244,221,190),'c':(212,174,132),
     'N':(106,76,64),'n':(140,110,94),'H':(132,102,70),'h':(184,148,106),'I':(62,66,78),'J':(86,92,104),'K':(110,116,128)}
ORDER=list(PAL)
for v,disc in VAR.items():
    g=[list(r) for r in R3]; log=[]
    def put(x,y,c,why):
        assert ZONE[0]<=x<=ZONE[2] and ZONE[1]<=y<=ZONE[3]
        if g[y][x]!=c: log.append((x,y,g[y][x],c,why)); g[y][x]=c
    for (x,y) in OUDOOG-disc:
        if (x,y) in VACHT: put(x,y,VACHT[(x,y)],'buiten de ronde oogvorm: vacht')
    for (x,y) in disc:
        put(x,y,BINNEN.get((x,y),'C'),'ronde oogvorm uit het model')
    H=len(g); W=len(g[0])
    buiten=sum(1 for y in range(H) for x in range(W) if g[y][x]!=R3[y][x] and not (ZONE[0]<=x<=ZONE[2] and ZONE[1]<=y<=ZONE[3]))
    print(v,'gewijzigd t.o.v. r3:',len(log),'diff buiten oogzone:',buiten)
    img=np.zeros((64,64),'uint8')
    for y in range(H):
        for x in range(W): img[OY+y,OX+x]=ORDER.index(g[y][x])
    pal=[]; [pal.extend(PAL[k]) for k in ORDER]; pal+=[0,0,0]*(16-len(ORDER))
    im=Image.fromarray(img,'P'); im.putpalette(pal); im.save(f'r4/dikdik_r4{v}.png',transparency=0)
    Image.open(f'r4/dikdik_r4{v}.png').convert('RGBA').resize((512,512),Image.NEAREST).save(f'r4/dikdik_r4{v}_8x.png')
    json.dump({'OX':OX,'OY':OY,'grid':[''.join(r) for r in g]},open(f'r4/grid_{v}.json','w'),indent=0)
    with open(f'r4/log_{v}.txt','w') as f:
        for e in log: f.write('(%d,%d) %s->%s  %s\n'%e)
    for y in range(18,27): print('   %2d '%y+''.join(g[y][9:22]))
# keuzevel: kop 12x van A, B en model
m0=Image.open('../referenties/model_r3b.png').convert('RGB'); a=np.asarray(m0).astype(int); fg=a.min(2)<225
ys,xs=np.nonzero(fg); x0,y0,y1=xs.min(),ys.min(),ys.max()+1; p=(y1-y0)/52
X0,Y0,X1,Y1=4,12,24,32; Z=12
tiles=[]
for v in 'AB':
    s=Image.open(f'r4/dikdik_r4{v}.png').convert('RGBA').crop((OX+X0,OY+Y0,OX+X1,OY+Y1)).resize(((X1-X0)*Z,(Y1-Y0)*Z),Image.NEAREST)
    t=Image.new('RGBA',s.size,(236,236,236,255)); t.paste(s,(0,0),s); tiles.append(t)
tiles.append(m0.crop((int(x0+X0*p),int(y0+Y0*p),int(x0+X1*p),int(y0+Y1*p))).resize(((X1-X0)*Z,(Y1-Y0)*Z),Image.LANCZOS).convert('RGBA'))
V=Image.new('RGBA',(3*tiles[0].width+40,tiles[0].height+20),(255,255,255,255))
for i,t in enumerate(tiles): V.paste(t,(10+i*(t.width+10),10))
V.save('r4/oog_keuze.png')
