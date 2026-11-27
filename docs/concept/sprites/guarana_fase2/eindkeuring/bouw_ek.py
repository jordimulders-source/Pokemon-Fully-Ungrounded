"""Eindkeuring guarana fase 2: leest r16, past alleen benoemde pixels aan (belijning + schaduw).
Draaien vanuit guarana_fase2/: python3 eindkeuring/bouw_ek.py"""
from PIL import Image; import numpy as np, shutil, os
SRC='sprite_r16/guarana2_r16.png'; OUT='eindkeuring/guarana2_ek.png'
im=Image.open(SRC); pal=im.getpalette(); a=np.array(im); r16=a.copy()
H,W=a.shape
def g(x,y): return a[y,x] if 0<=x<W and 0<=y<H else 0
EDITS={}  # (x,y) -> (oud, nieuw, gebied)
def zet(x,y,new,oud,gebied):
    assert a[y,x]==oud,(x,y,a[y,x],oud); a[y,x]=new; EDITS[(x,y)]=(oud,new,gebied)
# --- 1. belijning: lichte groene tint op de buitenrand -> lijngroen (6) / zwart (1)
for x,y in [(31,1),(32,1),(33,1),(32,2)]: zet(x,y,6,7,'lus boven: bovenrand')
for x,y in [(36,7),(36,8),(36,9)]: zet(x,y,6,7,'rankje boven midden: linkerrand')
for x,y in [(37,6),(37,7),(37,8)]: zet(x,y,1,7,'rankje boven midden: rechterrand (outline shadow)')
zet(19,8,6,7,'bladpunt boven middentros')
for x,y in [(14,11),(15,11)]: zet(x,y,6,7,'blad links boven: bovenrand')
for x,y in [(2,17),(1,18),(2,18)]: zet(x,y,6,7,'bladpunt links')
zet(61,19,6,7,'bladpunt rechts (tussen 2 zwarte)')
zet(15,21,1,8,'blad boven linkertros: onderrand')
zet(19,24,1,7,'blad boven linkertros: onderrand')
for x,y in [(60,24),(61,24)]: zet(x,y,6,7,'bladpunt rechts onder')
for x,y in [(20,47),(20,48),(21,48),(21,49)]: zet(x,y,6,7,'grijprankje linksonder')
for x,y in [(33,50),(34,50)]: zet(x,y,6,7,'grijprankje onder midden')
# zwart aan de lichtkant midden in een rand
zet(24,38,6,1,'stam linkerrand')
zet(49,10,6,1,'lus rechts: bovenrand')
zet(6,39,1,2,'linkertros onderrand (lijnrood tussen zwart)')
# --- 2. schaduw: sikkels rechtsonder in de vruchten (midden 4 -> schaduw 3)
SIK=[]
SIK=[(22,17),(21,18),(30,17),(28,20),(27,21),(27,23),(28,23),(25,24),(26,24),(29,28),(25,30),   # middentros
     (7,27),(8,27),(4,31),(4,32),(3,33),(2,34),(2,35),(7,36),(6,37),(5,38),(9,41),             # linkertros
     (51,27),(53,32),(53,35),(50,38),(47,41)]                                                    # rechtertros
for x,y in SIK: zet(x,y,3,4,'schaduwsikkel rechtsonder in de vrucht')
# --- controles
assert (np.array(r16)==0).sum()==(a==0).sum() and ((r16==0)==(a==0)).all(), 'silhouet gewijzigd'
for i in (10,): assert ((r16==i)==(a==i)).all(), 'oogwit gewijzigd'
eye=np.zeros_like(a,bool)
# pupillen/oogranden: geen enkele pixel die aan oogwit grenst is gewijzigd
for (x,y) in EDITS:
    for dx in (-1,0,1):
        for dy in (-1,0,1):
            assert g(x+dx,y+dy)!=10, ('naast oog',x,y)
out=Image.new('P',(W,H)); out.putpalette(pal); out.frombytes(a.astype(np.uint8).tobytes())
out.save(OUT,transparency=0)
shutil.copy('sprite_r16/normal.pal','eindkeuring/normal.pal')
if __name__=='__main__':
    red=sum((a==i).sum() for i in (2,3,4,5))
    print('pixels anders dan r16:',(a!=r16).sum(),'| rood lijn/schaduw/midden/licht %:',[round(100*(a==i).sum()/red,1) for i in (2,3,4,5)])
    for k,v in sorted(EDITS.items(),key=lambda t:t[1][2]): print(k,v)
