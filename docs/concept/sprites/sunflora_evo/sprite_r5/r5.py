# r5 = r4 + MOET 1-3 en KAN 2-3 van de keurder (pixels uit het model: ronde bladonderkant). Hoofd bevroren (assert).
import numpy as np; from PIL import Image
im=Image.open('../sprite_r4/sunflora_evo_r4.png'); a=np.array(im).copy(); pal=im.getpalette()
r4=a.copy()
def zet(pts,i):
    for x,y in pts: a[y,x]=i
zet([(17,48),(18,48),(19,48),(20,48)],13); zet([(18,49),(19,49),(20,49)],12); zet([(21,49)],1); zet([(18,50),(19,50),(20,50)],1)
zet([(40,48),(41,48),(42,48),(43,48)],13); zet([(44,48)],12); zet([(41,49),(42,49),(43,49)],12); zet([(41,50),(42,50),(43,50)],1)
zet([(27,60)],0)
zet([(32,48),(31,49)],13); zet([(14,48)],0)
lijf=np.isin(r4,[11,12,13,14])|np.isin(a,[11,12,13,14])
# hoofd bevroren: alle gewijzigde pixels moeten in de lijfzone (rij>=46) liggen en niet aan hoofdkleuren raken
d=np.argwhere(a!=r4); print('gewijzigd',len(d)); assert all(y>=46 for y,x in d)
assert all(r4[y,x] in (0,1,11,12,13,14) for y,x in d), 'hoofdpixel geraakt'
def save(arr,p,name):
    o=Image.fromarray(arr,'P'); o.putpalette(p); o.save(name+'.png',transparency=0)
    Image.open(name+'.png').convert('RGBA').resize((512,512),Image.NEAREST).save(name+'_8x.png')
save(a,pal,'sunflora_evo_r5')
p2=list(pal)
for i,c in {11:(82,98,41),12:(115,172,49),13:(156,213,74),14:(189,255,115)}.items(): p2[3*i:3*i+3]=c
save(a,p2,'sunflora_evo_r5_sunfloragroen')
from PIL import ImageDraw
A=Image.open('sunflora_evo_r5_8x.png'); B=Image.open('sunflora_evo_r5_sunfloragroen_8x.png')
v=Image.new('RGB',(1060,560),'white'); v.paste(A,(10,40),A); v.paste(B,(540,40),B)
d=ImageDraw.Draw(v); d.text((10,10),'A: modelgroen',fill='black'); d.text((540,10),'B: Sunflora-groen',fill='black'); v.save('vel.png')
