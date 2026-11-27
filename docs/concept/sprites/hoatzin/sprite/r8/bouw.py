# Hoatzin r8 = r7 + verre voet (x18-30, y54-63) met aparte tenen uit het model. Diff 0 erbuiten (bewezen onderaan).
# Gemeten op het model (model.png, voet x302-516, y939-1054; zie vel.png, model met spriteraster):
#  - het been komt neer op x24-27; daaruit gaan twee tenen naar linksvoor en een korte achterteen naar rechts (x27-30, y57-58).
#  - bovenste teen: bovenrand y57,0 van x21,5 tot x24, punt linksonder op x19,7-20,5, y58,1-59,3.
#  - onderste teen (vóór de bovenste): bovenrand = de zwarte scheidingslijn van (21,7; 58,9) naar (25,8; 58,4); punt op x20,9-22, y59,3-60,2.
#  - tussen de twee punten een inkeping rond (20,7; 59,5); dekking (20,57) 33 % en (20,59) 74 % (vooral omlijning).
#  r7 had x20-25, y57-59 als dicht blok (selout-rij, lichte rij, zwarte rij) = de rechthoek.
#  Omzetting op spritepixels (punt 1 px, eindigt in zwart; selout linksboven; scheiding = zwarte lijn uit het model):
import sys,os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); from gemeen import *
im=Image.open(HIER+'/../r7/hoatzin_r7.png'); r7=np.array(im); PALR=im.getpalette()
o=r7.copy()
_=0; Kz=1; d=2; m=3; l=4
# punten met de lagere tenen-drempel uit r1 (stap poten: figuur vanaf ±20-33 %): bovenste punt (19,58) 31 %, onderste punt (21,60) 22 %.
VOET={  # (x,y): index
 (20,57):_, (21,57):d, (22,57):d, (23,57):m, (24,57):m, (25,57):m,               # bovenste teen: 1 rij, selout linksboven; been
 (19,58):Kz, (20,58):Kz, (21,58):Kz, (22,58):Kz, (23,58):m, (24,58):l, (25,58):Kz, # punt + onderrand bovenste teen = scheidingslijn; onderste teen
 (20,59):_, (21,59):d, (22,59):Kz, (23,59):Kz,                                    # inkeping tussen de punten; onderste teen (selout links, zwart onder)
 (21,60):Kz,                                                                       # punt onderste teen
}
for (X,Yy),k in VOET.items(): o[Yy,X]=k
zone=np.zeros((64,64),bool); zone[54:64,18:31]=True
out=Image.fromarray(o.astype('uint8'),'P'); out.putpalette(PALR); out.save(HIER+'/hoatzin_r8.png',transparency=0); np.save(HIER+'/r8.npy',o)
print('voet: %d px anders dan r7 | buiten de voetzone: %d (moet 0) | kleuren %d'%(int((o!=r7)[zone].sum()),int((o!=r7)[~zone].sum()),len(set(o.ravel())-{0})))
