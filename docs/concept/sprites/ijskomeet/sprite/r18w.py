# r18 = r17 + afwerkpunten 1-5 van de keurder (geen naad/facet in het ijs aangeraakt)
import numpy as np; from PIL import Image
im=Image.open('r17.png'); pal=im.getpalette(); P=np.array(pal[:48]).reshape(16,3); a=np.array(im).copy()
I=lambda c:[k for k in range(16) if tuple(P[k])==c][0]
def ch(pts,van,naar):
  for x,y in pts:
    assert (a[y,x]==0 if van is None else tuple(P[a[y,x]])==van),(x,y,a[y,x])
    a[y,x]=0 if naar is None else I(naar)
ch([(26,59)],None,(30,30,74))
ch([(9,51)],(178,236,242),(166,198,220))
ch([(50,11),(50,14),(32,15),(30,16),(34,18),(21,20),(23,21),(29,21),(21,22),(29,23),(48,25)],(70,88,138),(82,74,142))
ch([(47,21),(47,22)],(100,128,168),(82,74,142))
ch([(27,34),(28,34),(27,35),(28,35),(27,36)],(124,100,186),(170,140,224))
ch([(53,26),(46,42)],(206,228,238),None)
o=Image.fromarray(a).convert('P'); o.putpalette(pal); o.save('r18.png',transparency=0)
x8=o.convert('RGB').resize((512,512),Image.NEAREST); x8.save('r18_8x.png')
b=Image.open('r17.png').convert('RGB').resize((512,512),Image.NEAREST); m=Image.open('vel_r9.png').crop((1060,0,1590,520))
v=Image.new('RGB',(1600,530),'white'); v.paste(x8,(0,8)); v.paste(b,(530,8)); v.paste(m,(1060,0)); v.save('voor_jordi_r18.png')
print('ok')
