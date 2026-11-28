# r11: r10 (K1) met een driekwartgezicht (Jordi 28 nov). Alleen cellen binnen r10/masker_k1.npy veranderen.
# Gezicht als raster per rij (eerste kolom erbij); N1/N2/N3 = neusvarianten. Tekens: 1 2 3 4 d(13) 5 a(10)
import numpy as np
from PIL import Image
R='docs/concept/sprites/pachamama/sprite_r7model/'
r10=np.load(R+'r10/pachamama_r10.npy'); m=np.load(R+'r10/masker_k1.npy')
BASIS={  # rij: (eerste kolom, waarden)
14:(30,'d'),
15:(26,'d..dd4'),          # . = niet in masker (27,28)
16:(25,'dddd2223'),
17:(24,'22d42333'+'2'),
18:(24,'11d3411133'),
19:(23,'21ad24a12a43'),
20:(23,'a2ad24a22a43'),
21:(22,'2ddd52dddd433'),
22:(22,'2ddd52ddd4433'),
23:(22,'24dd524444333'),
24:(22,'2444434444333'),
25:(22,'244444443333'),
26:(22,'24422243333'),
27:(23,'24434333'),
28:(23,'2443333'),
29:(24,'3.3'),
}
NEUS={'N1':{24:(26,'4'),23:(26,'52')},
      'N2':{22:(25,'552'),23:(25,'552'),24:(25,'222')},
      'N3':{18:(26,'d4'),19:(26,'d3'),20:(26,'d3'),21:(26,'53'),22:(26,'d3'),23:(26,'34'),24:(26,'4')}}
C={'1':1,'2':2,'3':3,'4':4,'d':13,'5':5,'a':10}
def bouw(var):
  o=r10.copy(); rows=dict(BASIS)
  g={}
  for y,(x0,s) in rows.items():
    for i,ch in enumerate(s):
      if ch!='.': g[(y,x0+i)]=C[ch]
  for y,(x0,s) in NEUS[var].items():
    for i,ch in enumerate(s): g[(y,x0+i)]=C[ch]
  for (y,x),v in g.items():
    assert m[y,x],(var,y,x); o[y,x]=v
  mis=[(int(y),int(x)) for y,x in zip(*np.where(m)) if (y,x) not in g]
  assert not mis, mis
  return o
if __name__=='__main__':
  for v in NEUS:
    o=bouw(v); np.save(R+'r11/pachamama_r11_%s.npy'%v,o)
    print(v,'diff met r10 buiten het gezicht:',int(((o!=r10)&~m).sum()))
