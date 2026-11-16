import sys; sys.path.insert(0,'sprite_r1'); import numpy as np; from PIL import Image, ImageDraw; import pal; from render import img
A=pal.A
# V2: zelfde kleurtonen, grotere helderheidsstappen (L lijn 1/2/3/4/5/6 ±31/51/72/115/165/203 i.p.v. 36/62/83/118/155/187)
A2=list(A); A2[1]=(50,18,42); A2[2]=(82,34,66); A2[3]=(108,52,86); A2[4]=(156,94,120); A2[5]=(204,148,160); A2[6]=(234,194,188)
def lum(c): return round(.299*c[0]+.587*c[1]+.114*c[2])
print('A ',[lum(c) for c in A[1:7]]); print('A2',[lum(c) for c in A2[1:7]])
r4=np.load('sprite_r5/r4_idx.npy').astype('uint8'); V1=np.load('sprite_r5/V1_idx.npy').astype('uint8'); V3=np.load('sprite_r5/V3_idx.npy').astype('uint8')
def save(o,P,n):
    p=Image.fromarray(o,'P'); fl=[v for c in P for v in c]; p.putpalette(fl+[0]*(768-len(fl))); p.save(f'sprite_r5/{n}.png',transparency=0)
    assert (np.asarray(Image.open(f'sprite_r5/{n}.png'))==o).all(); img(o,P,8).save(f'sprite_r5/{n}_8x.png')
save(V1,A,'dustly_r5_V1'); save(V1,A2,'dustly_r5_V2'); save(V3,A2,'dustly_r5_V3')
LICHT,DONKER=(248,248,240),(40,40,48)
m=Image.open('gemini/r6_a.png').convert('RGB').crop((150,150,880,880)).resize((512,512),Image.LANCZOS)
cells=[(m,'model r6_a'),(img(r4,A,8,LICHT),'r4'),(img(V1,A,8,LICHT),'V1 vlakken'),(img(V1,A2,8,LICHT),'V2 contrast'),(img(V3,A2,8,LICHT),'V3 lijn')]
W=5*512+6*16; out=Image.new('RGB',(W,24+512+24+140),(255,255,255)); d=ImageDraw.Draw(out)
for i,(c,n) in enumerate(cells): out.paste(c.convert('RGB'),(16+i*528,24)); d.text((16+i*528,6),n,fill=(0,0,0))
y=24+512+24; x=16
for bgc in (LICHT,DONKER):
    for (o,P) in ((r4,A),(V1,A),(V1,A2),(V3,A2)):
        for s in (1,2):
            c=img(o,P,s,bgc).convert('RGB'); out.paste(c,(x,y)); x+=c.width+6
        x+=14
    x+=30
out.save('sprite_r5/vel.png'); print('ok')
