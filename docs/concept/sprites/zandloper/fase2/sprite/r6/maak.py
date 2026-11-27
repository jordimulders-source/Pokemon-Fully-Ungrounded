# r6: kleur van de omlijning (Jordi: "het gaat niet om dunnere lijn maar kleur"). Basis r4; ogen ongemoeid.
# A: zwart -> donker zandbruin (60,36,18), 1 nieuwe kleur
# B: alle zwarte buitenlijn -> selout 2 (96,58,24), zwart alleen nog binnen (ogen)
# C: zwart blijft alleen onderaan (onderste helft schaduwrand: randen met lege buur eronder), rest -> 2
import os; from PIL import Image; import numpy as np
d=os.path.dirname(os.path.abspath(__file__))
im=Image.open(os.path.join(d,'../r4/zandloper_fase2_r4.png')); a=np.array(im); pal=im.getpalette()
oog=np.zeros(a.shape,bool); oog[20:28,22:38]=True
zw=(a==1)&~oog
op=a>0; p=np.pad(op,1)
onder_leeg=op&~p[2:,1:-1]
def save(b,naam,pal2=pal):
    o=Image.fromarray(b,'P'); o.putpalette(pal2); o.save(os.path.join(d,naam),transparency=0)
# A
b=a.copy(); free=[i for i in range(16) if not (a==i).any()]
k=free[0] if free else 1; pa=list(pal)
b[zw]=k; pa[3*k:3*k+3]=[60,36,18]; save(b,'A_donkerbruin.png',pa)
# B
b=a.copy(); b[zw]=2; save(b,'B_selout.png')
# C
b=a.copy(); b[zw&~onder_leeg]=2; save(b,'C_zwart_onder.png')
print('vrije index',free, 'zwart buiten ogen',zw.sum())
