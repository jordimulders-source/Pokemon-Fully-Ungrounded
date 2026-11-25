# r21 -> r22: Jordi "fix allemaal" (vier ter-info-punten). Vorm alleen lokaal en naar het model; silhouet blijft.
# Draaien vanuit deze map: python3 repareer_r22.py
from PIL import Image
import numpy as np
im=Image.open('r21/sprite.png'); P=im.getpalette(); a=np.array(im); b=a.copy()
ch={}
def zet(x,y,oud,nieuw,zone):
    assert b[y,x]==oud,(zone,x,y,int(b[y,x]),oud); b[y,x]=nieuw; ch.setdefault(zone,[]).append((x,y,oud,nieuw))

# P3 lenslijn links (13,31-32): twee paarse pixels lagen buiten de zwarte lijn (rand 2 px). Lijn naar x13 zoals rij 30 en 33+,
#    de ring (7) schuift in op x14: buitencontour lens per rij 14,13,13,13,13... = rond, lijn 1 px.
for y in (31,32):
    zet(13,y,7,1,'P3 lensrand links'); zet(14,y,1,7,'P3 lensrand links')

# P2 lenslijnen aan de lichtkant -> eigen donkerste tint 8 (Claydol: ogen rondom in eigen 9, geen zwart; Claydol-ring: 5 linksboven,
#    zwart rechts). Lichtkant = boven het lensmidden en links van de diagonaal (Popplio-regel uit SPRITE_KERN: zwart van linksmidden
#    via linksonder tot onder en aan de schaduwkant). Lensmidden = irismidden (18,5; 34,5). Alleen lenshuislijn + binnenlijn, oog/pupil niet.
cx,cy=18.5,34.5
for y in range(25,35):
    for x in range(13,24):
        if b[y,x]==1 and (x-cx)+(y-cy)<0 and (y-cy)<0 and np.hypot(x-cx,y-cy)<9.5:
            zet(x,y,1,8,'P2 lenslijn lichtkant')

# P1 linkerrand groot paneel (rij 34-48): framelijn doorlopend zoals het model (licht frame direct binnen de buitenlijn).
#    Per rij: eerste paneelpixel na zwart = frame; na lijf = buitenlijn 9 (paneel-outline base, lichtkant) en de pixel erna = frame.
#    Frame C in het glansvlak (rij 34-37, zoals de rasterlijnen daar), B eronder (zoals de rest van de onderste framelijn).
#    Rij 43: lijf stak 2 px in het paneel (bult 33 tussen 32 en 30) -> paneel-outline, rand per rij 33,32,32,31,30,30,29,29.
zet(32,43,5,9,'P1 paneelrand'); zet(31,43,5,9,'P1 paneelrand')
PAN={9,10,11,12}
for y in range(34,48):
    x=next(x for x in range(25,45) if b[y,x] in PAN)
    fx=x if b[y,x-1]==1 else x+1
    if b[y,x-1]!=1 and b[y,x]!=9: zet(x,y,b[y,x],9,'P1 paneelrand')
    f=12 if y<=37 else 11
    if b[y,fx]!=f: zet(fx,y,b[y,fx],f,'P1 paneelrand')
# (31,44) was de losse B: ligt nu in de doorlopende framelijn.

# P4 kaprand: de donkere streep onder het grijze vlak, gemeten in het model (kolomprofiel in stappen van 1/4 px):
#    x30-33 op y 27,3-27,5, x34 27,75, x35 28,25, x36 28,5; x28-29 en links daarvan geen streep. -> rij 27 x30-34, rij 28 x35-36.
zet(34,27,3,4,'P4 kaprand')
zet(35,28,2,4,'P4 kaprand'); zet(36,28,3,4,'P4 kaprand')

assert ((a==0)==(b==0)).all(),'silhouet gewijzigd'
o=Image.fromarray(b,'P'); o.putpalette(P); o.save('r22/sprite.png',transparency=0)
for z,v in ch.items(): print(z,len(v),[(x,y,int(o_),n) for x,y,o_,n in v])
print('totaal',int((a!=b).sum()))
