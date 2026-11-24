# r4.py: gesp in de VORM van Jordi's foto (kabouterriem), kleuren van r3-A (Jordi: "qua vorm").
# Basis = r3-B (bruine Machoke-riem zonder gesp, = r3-A buiten de gesp). Gesp 8x7 incl. zwarte omlijning, 1 px boven en onder de band uit,
# vlak creme (12) met glans (13) linksboven en schaduw (14, lichtbruin) rechts/onder; staand gat 2x3 in het midden waar de bruine band (15) doorheen zichtbaar is.
# Buiten riem/gesp diff 0 t.o.v. r3-A (assert). Geen nieuwe kleuren.
import sys, numpy as np; from PIL import Image
sys.path.insert(0,'../sprite_r1'); from gemeen import opslaan
im=Image.open('../sprite_r3/gnomad_B.png'); pal=[tuple(im.getpalette()[3*k:3*k+3]) for k in range(16)]
o=np.asarray(im).astype(int).copy()
def top(X): u=(X-25.0)/14.0; return 40.6+3.4*(1-u*u)+0.8*u
t=int(round(top(25)))
G=["kkkkkkkk",
   "kHCCCCCk",
   "kCCbbCOk",
   "kCCbbCOk",
   "kCCbbCOk",
   "kCOOOOOk",
   "kkkkkkkk"]
M={'k':1,'C':12,'H':13,'O':14,'b':15}
gesp=np.zeros((64,64),bool)
for j,r in enumerate(G):
    for i,c in enumerate(r): o[t-1+j,21+i]=M[c]; gesp[t-1+j,21+i]=True
r3=np.asarray(Image.open('../sprite_r3/gnomad_A.png')).astype(int)
d=o!=r3; riem3=np.asarray(Image.open('../sprite_r3/gnomad_B.png')).astype(int)!=np.asarray(Image.open('../sprite_r2/gnomad_A.png')).astype(int)
assert not (d&~gesp&~riem3).any(), np.argwhere(d&~gesp&~riem3)
opslaan(o,'gnomad.png',pal)
print('diff t.o.v. r3-A: gesp %d px, riem %d px, elders 0'%((d&gesp).sum(),(d&~gesp).sum()))
