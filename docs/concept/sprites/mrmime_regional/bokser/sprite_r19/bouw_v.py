# bouw_v.py: V-patroon (r7 'v_groot' = V_L, dezelfde pixels als r18 'V groot') in driekwart-perspectief:
# kolom van de verre (linker) helft geschrapt, twee kolommen van de nabije (rechter) helft herhaald; punt op de
# middenlijn ogen-kruis (x31). Alleen op romppixels (achter kop, ballen, borstvuist).
import numpy as np, sys
sys.path.insert(0,'../sprite_r7'); from build import save
a=np.load('ruw.npy')
V_L={18:(32,33),19:(32,38),20:(32,37),21:(32,37),22:(31,36),23:(32,36),24:(33,36),25:(33,36),26:(34,35),27:(35,35)}
oud={(x-5,y+6) for y,(p,q) in V_L.items() for x in range(p,q+1)}          # r18 'V groot'-plaats
kol=[26,28,29,30,31,31,32,32,33]                                           # 27 geschrapt, 31 en 32 herhaald
P=31-kol.index(30)                                                         # punt (oude kolom 30) op x31
nieuw={(P+i,y) for i,c in enumerate(kol) for (x,y) in oud if x==c}
for x,y in nieuw:
    if 24<=y<=35 and a[y,x] in(7,8): a[y,x]=3
save(a,'bokser')
for j in range(22,36): print('%2d '%j+''.join(str(v) if v else '.' for v in a[j,14:46]))
