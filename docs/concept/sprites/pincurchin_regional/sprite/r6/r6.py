# r6: eindkeuring-reparaties 1-8 op r5/V1 (PNG-paletindexen, coördinaten (x,y)); elke pixel eerst gecontroleerd.
from PIL import Image
import numpy as np
V1='../r5/V1_oog4x5_mond+1+2.png'
im=Image.open(V1); src=np.array(im)
R=[  # (x,y), van, naar
 ((10,31),1,2),((13,40),4,2),
 ((14,46),2,1),((15,48),2,1),((14,44),5,3),((15,45),5,3),
 ((15,44),2,3),((14,45),2,3),((16,45),2,3),((15,46),2,3),((15,47),2,3),((16,47),2,3),((16,46),4,3),((14,43),2,4),
 ((50,43),1,6),((52,44),1,6),((38,59),1,6),((39,61),1,6),
 ((39,45),5,4),((40,45),5,4),((41,45),5,4),((42,45),5,4),((32,47),3,4),((33,47),3,4),((34,47),3,4),
 ((45,43),3,2),((36,12),1,6),((10,18),1,6),((9,19),1,6)]
a=src.copy(); gedaan=set(); over=[]
for (x,y),van,naar in R:
    if a[y,x]!=van: over.append(((x,y),int(a[y,x]),van)); continue
    a[y,x]=naar; gedaan.add((x,y))
print('uitgevoerd',len(gedaan),'| overgeslagen (coord, huidig, verwacht):',over)
def bewaar(arr,pal,naam):
    p=Image.fromarray(arr.astype('uint8'),'P'); p.putpalette(pal); p.save(naam,transparency=0)
    q=Image.open(naam).convert('RGBA'); b=Image.new('RGBA',q.size,(255,255,255,255)); b.alpha_composite(q); b.resize((512,512),Image.NEAREST).save(naam.replace('.png','_8x.png'))
pal=im.getpalette()
bewaar(a,pal,'final_A.png')
pb=list(pal); assert tuple(pb[21:24])==(140,33,37),tuple(pb[21:24]); pb[21:24]=[156,38,42]
bewaar(a,pb,'final_B.png')
# bewijs
A=np.array(Image.open('final_A.png')); B=np.array(Image.open('final_B.png'))
d=np.argwhere(A!=src); buiten=[(x,y) for y,x in d if (x,y) not in gedaan]
print('A: gewijzigde px',len(d),'| buiten de genoemde pixels:',len(buiten))
print('B: indexen gelijk aan A:',(A==B).all(),'| paletverschil A/B alleen index 7:',
      [i for i in range(16) if Image.open('final_A.png').getpalette()[3*i:3*i+3]!=Image.open('final_B.png').getpalette()[3*i:3*i+3]])
# vergelijking met het voorstel van de keurder
vs=np.array(Image.open('../r5/eindkeuring/voorstel.png')); print('final_A == eindkeuring/voorstel.png:',(vs==A).all())
print('kleuren A',len(np.unique(A))-1)
V=Image.new('RGB',(3*522,512),'white')
for i,f in enumerate(['final_A_8x.png','final_B_8x.png']): V.paste(Image.open(f),(i*522,0))
q=Image.open(V1).convert('RGBA'); b=Image.new('RGBA',q.size,(255,255,255,255)); b.alpha_composite(q); V.paste(b.resize((512,512),Image.NEAREST).convert('RGB'),(2*522,0))
V.save('vel.png')
