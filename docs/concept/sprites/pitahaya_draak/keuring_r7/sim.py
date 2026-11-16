# Simuleert de MOET-lijst van keuring_r7 op sprite_r7/pitahaya_r7.png (assert op oude index).
import numpy as np; from PIL import Image
im=Image.open('../sprite_r7/pitahaya_r7.png'); a=np.array(im).copy()
MOET=[ # x,y,oud,nieuw
 (37,37,9,8),(38,38,9,8),          # 1 armlijn tot de schouder
 (42,37,2,8),                      # 2 roze pixel op de groene schouder
 (35,53,9,11),(36,53,9,10),(38,53,9,11),(39,53,9,10),  # 3 lichte tenen rechtervoet
 (35,54,1,8),                      # 4 lichtkant teen: selout
]
KAN=[]  # (37,34) 1->3 verworpen: maakt dambord (36,33)
def pas(lst,b):
    for x,y,o,n in lst:
        assert b[y,x]==o,(x,y,b[y,x],o); b[y,x]=n
    return b
b=pas(MOET,a.copy())
face=np.zeros((64,64),bool); face[22:35,18:37]=True
assert (b[face]==a[face]).all() and ((b>0)==(a>0)).all()
o=Image.fromarray(b.astype(np.uint8),'P'); o.putpalette(im.getpalette()); o.save('sim_moet_sprite.png',transparency=0)
print('MOET',len(MOET),'px; KAN',len(KAN),'px; gezicht en silhouet diff 0')
