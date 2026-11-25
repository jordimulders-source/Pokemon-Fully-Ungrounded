# Voorstel keurder: de benoemde reparaties toepassen op een kopie (NIET de sprite), om ze te controleren.
import numpy as np
from PIL import Image
im=Image.open('sprite_r1/sprite.png'); s=np.array(im).copy(); pal=im.getpalette()
E=[ # (rij,kol,oud,nieuw)
 # R1 rand linksboven naar de cirkel (1 px naar binnen, binnen 1 px van het model)
 (22,5,2,0),(24,4,2,0),(24,5,6,2),(25,3,2,0),(25,4,6,2),(26,3,2,0),(26,4,6,2),
 # R2 rand linksonder: trap 1-2-1-2 -> 1-1-2-2
 (48,9,0,1),(47,9,1,8),
 # R3 rand rechts: 37x5 / 38x4 -> 37x4 / 38x5
 (29,38,0,1),(29,37,1,8),
 # T1 hooglicht afronden (rechte rechterkant + knobbel)
 (22,22,5,6),(18,20,5,6),(19,21,5,6),(24,21,5,6),
 # T2 losse tintpixels
 (26,12,6,5),(27,14,6,5),(26,7,5,6),(36,37,7,8),(25,36,7,8),(26,36,7,8),(41,6,4,3),
 # T3 open rand
 (12,23,3,2),
]
for y,x,o,n in E:
    assert s[y,x]==o,(y,x,s[y,x],o); s[y,x]=n
p=list(pal)
p[7*3:7*3+3]=[184,174,226]; p[8*3:8*3+3]=[140,126,194]
out=Image.fromarray(s.astype('uint8'),'P'); out.putpalette(p); out.save('keuring_r1/voorstel.png',transparency=0)
np.save('keuring_r1/voorstel.npy',s)
# vel: origineel vs voorstel 1x,2x,8x
def rgba(img,arr):
    a=np.array(img.convert('RGBA')); a[arr==0,3]=0; return Image.fromarray(a)
A=rgba(im,np.array(im)); B=rgba(out,s)
up=lambda i,f:i.resize((64*f,64*f),Image.NEAREST)
V=Image.new('RGBA',(64*8*2+30,64*8+150),(152,208,160,255))
for k,(img) in enumerate((A,B)):
    V.alpha_composite(img,(10+k*300,10)); V.alpha_composite(up(img,2),(90+k*300,10))
    V.alpha_composite(up(img,8),(10+k*(64*8+10),140))
V.save('keuring_r1/vel_voor_na.png')
print(len(E),'pixels')
