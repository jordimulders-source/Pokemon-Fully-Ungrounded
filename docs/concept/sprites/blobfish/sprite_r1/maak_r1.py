# Blobfish r1: kale reductie (python3 half4.py kaal.png 3 2; fase gekozen uit 16 op ogen + lippen) -> alleen technische opschoning. Niets getekend.
# Stappen (elk telt zijn gewijzigde pixels per zone, zie NOTITIES.md):
#  A palet: tint 3 en 4 zijn in het model bijna gelijk (helderheid 73/76) -> samen (4)
#  B buitenlijn: zwart aan de schaduwkant (onder/rechts), selout lijnrood aan de lichtkant
#  C ruis: losse vulpixels (cluster van 1, 8-verbonden) in tint 4-9 nemen de meest voorkomende vulbuur aan;
#    lijnen, lichte tinten (vinstralen, lipglans: 10-11), oogwit/glans (12) bevroren
#  D gerichte reparaties per pixel, elk met modelmeting (lijst REP hieronder)
import numpy as np; from PIL import Image; from collections import Counter
K=Image.open('kaal.png'); kaal=np.asarray(K).astype(int); pal=K.getpalette()
info=np.load('kaal_info.npz'); nd=info['nd']
o=kaal.copy(); log=[]
def zet(y,x,v,stap):
    if o[y,x]!=v: log.append((stap,y,x,o[y,x],v)); o[y,x]=v
# A
for y,x in zip(*np.where(o==3)): zet(y,x,4,'A')
# B buitenlijn (techniek, SPRITE_KERN): 1 px, zwart aan de schaduwkant, selout (lijnrood, = modelkleur van de dunne
#   lijnen) aan de lichtkant. Schaduwkant = buitennormaal naar onder/rechts (licht linksboven). Dat valt samen met
#   het model: daar is de lijn onder/rechts dik en zwart, boven/links dun. Glans op de rand wordt ook lijn.
#   Daarna: een los stukje van 1 randpixel tussen buren van de andere soort neemt die soort aan.
m=o>0; pad=np.pad(m,1)
rand=m&~(pad[:-2,1:-1]&pad[2:,1:-1]&pad[1:-1,:-2]&pad[1:-1,2:])
ry,rx=np.where(rand); keus={}
for y,x in zip(ry,rx):
    ny=sum(dy for dy in (-1,0,1) for dx in (-1,0,1) if not m[y+dy,x+dx])
    nx=sum(dx for dy in (-1,0,1) for dx in (-1,0,1) if not m[y+dy,x+dx])
    keus[(y,x)]=1 if (ny+0.6*nx)>0 else 2
for (y,x),v in list(keus.items()):
    nb=[keus[(y+dy,x+dx)] for dy in (-1,0,1) for dx in (-1,0,1) if (dy or dx) and (y+dy,x+dx) in keus]
    if nb and all(b!=v for b in nb): keus[(y,x)]=nb[0]
for (y,x),v in keus.items(): zet(y,x,v,'B')
# C
VUL=set(range(4,10)); BUUR=set(range(4,11))
seen=np.zeros_like(m)
for y0,x0 in zip(*np.where(m)):
    if seen[y0,x0] or o[y0,x0] not in VUL: continue
    v=o[y0,x0]; st=[(y0,x0)]; cl=[]; seen[y0,x0]=1
    while st:
        y,x=st.pop(); cl.append((y,x))
        for dy in (-1,0,1):
            for dx in (-1,0,1):
                yy,xx=y+dy,x+dx
                if 0<=yy<64 and 0<=xx<64 and not seen[yy,xx] and o[yy,xx]==v: seen[yy,xx]=1; st.append((yy,xx))
    if len(cl)<2:
        for y,x in cl:
            nb=Counter(o[y+dy,x+dx] for dy in (-1,0,1) for dx in (-1,0,1) if (dy or dx) and o[y+dy,x+dx] in BUUR and o[y+dy,x+dx]!=v)
            if nb: zet(y,x,nb.most_common(1)[0][0],'C')
# D (y, x, nieuwe index, reden + meting) — ingevuld na eigen controle op 12x naast het model
REP=[(41,10,2,"verre oog: pupil weg in reductie; modelblok 3 donkere px, mediaan (92,42,44) = lijnrood")]
for y,x,v,r in REP: zet(y,x,v,'D:'+r)
p=Image.fromarray(o.astype('uint8'),'P'); p.putpalette(pal); p.save('blobfish_r1.png',transparency=0)

# zones (spritecoordinaten, zie NOTITIES.md)
Z={'gezicht (ogen+lippen)':(6,36,30,55),'kop/lijf':(6,30,40,55),'staart':(40,24,58,40),'rugvin':(28,26,40,36),'borstvin':(28,36,42,56)}
def zone(y,x):
    for n,(a,b,c,d) in Z.items():
        if a<=x<c and b<=y<d: return n
    return 'rest'
cnt=Counter((s[0],zone(y,x)) for s,y,x,_,_ in log)
for k,v in sorted(cnt.items()): print(k,v)
print('totaal gewijzigd',len(log),'van',(o>0).sum(),'kleuren',len(set(o.ravel()))-1)
open('afwijkingen.txt','w').write('\n'.join(f'{s}\t({x},{y})\t{a}->{b}\t{zone(y,x)}' for s,y,x,a,b in log)+'\n')
