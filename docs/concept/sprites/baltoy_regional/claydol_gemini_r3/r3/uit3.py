import sys, numpy as np; sys.path.insert(0,'.'); sys.path.insert(0,'r3')
from PIL import Image, ImageDraw
import bouw
from bouw3 import S, G3, R2
from kaal3 import kaal
bouw.P3[12]=(190,92,84)
bouw.opslaan(S,'r3/claydol_g3r3.png'); rgb=bouw.rgb
rgb(S).resize((512,512),0).save('r3/claydol_g3r3_8x.png')
# controle: png terugladen == array
chk=np.array(Image.open('r3/claydol_g3r3.png')); print('png kleuren',len(np.unique(chk)))
S0,A,*_=kaal(); M8=Image.fromarray(A.astype('uint8'))
r3=rgb(S); r2=rgb(R2); bouw.P3[12]=(220,90,86); g3=rgb(G3); bouw.P3[12]=(190,92,84)
V=Image.new('RGB',(4*530+10,1000),(236,236,236)); d=ImageDraw.Draw(V)
for i,(t,im) in enumerate([('r3',r3),('r2',r2),('g3',g3),('model r3 geschrapt',M8)]):
    d.text((10+i*530,5),t+' (8x)',fill=(0,0,0)); V.paste(im.resize((512,512),0),(10+i*530,20))
d.text((10,545),'onderkop 12x: r3 | r2 | g3 | model',fill=(0,0,0))
for i,im in enumerate([r3,r2,g3,M8]): V.paste(im.crop((8,29,50,40)).resize((42*12,11*12),0),(10+i*530,560))
d.text((10,710),'1x licht / donker',fill=(0,0,0))
Image.open('r3/claydol_g3r3.png').save('/tmp/_r3.png'); sp=Image.open('/tmp/_r3.png').convert('RGBA')
for i,bg in enumerate([(255,255,255),(48,48,56)]):
    b=Image.new('RGBA',(64,64),bg+(255,)); b.alpha_composite(sp); V.paste(b.convert('RGB'),(10+i*80,725))
V=V.crop((0,0,V.width,800)); V.save('r3/vel.png')
