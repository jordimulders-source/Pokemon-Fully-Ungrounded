# Ronde 6 vanaf v16_r5, alleen de iris (Jordi: "rechts in het oog moeten dus 2 donkerdere tinten komen dan de basis rode kleur").
# Iris rechts als sikkel: basis 9 -> donker 1 (8, bestaand) -> donker 2 (11, nieuw) naar de rechterrand, volgens de oogronding.
import numpy as np; from PIL import Image; from scipy import ndimage
PAL=np.array([(0,0,0),(24,16,16),(60,22,28),(88,32,34),(138,56,50),(182,86,76),(204,108,92),(214,122,102),
              (168,20,24),(222,50,44),(236,128,112),(112,12,18)],float)
def save(o,fn,sc=1):
  im=Image.fromarray(o.astype('uint8'),'P'); p=[int(v) for v in PAL.ravel()]; im.putpalette(p+[0]*(768-len(p)))
  if sc>1: im=im.resize((o.shape[1]*sc,o.shape[0]*sc),Image.NEAREST)
  im.save(fn,transparency=0)
def rgb(o,sc):
  a=PAL[o].astype('uint8'); a[o==0]=(230,230,230); return Image.fromarray(a).resize((o.shape[1]*sc,o.shape[0]*sc),Image.NEAREST)
o0=np.load('../v16_r5/idx.npy'); o=o0.copy()
J,I=np.mgrid[0:64,0:64]
ring=(o==1)&(I>=24)&(I<=40)&(J>=20)&(J<=38)
inside=ndimage.binary_fill_holes(ring)&~ring
IR=inside&np.isin(o,[8,9,10])
ys,xs=np.where(inside); ecx,ecy=xs.mean()+.5,ys.mean()+.5
rx=(xs.max()-xs.min()+1)/2; ry=(ys.max()-ys.min()+1)/2
u=(I+.5-ecx)/rx; v=(J+.5-ecy)/ry
# afstand tot de rechterrand van de iris langs de oogronding: sikkel = verschoven ellips
d1=((u+0.45)**2/1.0**2+v**2)>1.0      # buiten een naar links verschoven ellips -> donker 1
d2=((u+0.25)**2/0.95**2+v**2)>1.0     # verder naar rechts -> donker 2
m1=IR&(o==9)&d1&(u>0); m2=IR&np.isin(o,[8,9])&d2&(u>0)
o[m1]=8; o[m2]=11
# overal een tussenbaan: basis direct links van donker 2 -> donker 1
m3=IR&(o==9)&np.roll(o==11,-1,axis=1); o[m3]=8; m1=m1|m3
np.save('idx.npy',o); save(o,'sprite.png'); save(o,'sprite_8x.png',8)
y0,y1,x0,x1=ys.min()-2,ys.max()+3,xs.min()-2,xs.max()+3
a=rgb(o0[y0:y1,x0:x1],16); b=rgb(o[y0:y1,x0:x1],16)
c=Image.new('RGB',(a.width*2+24,a.height),(230,230,230)); c.paste(a,(0,0)); c.paste(b,(a.width+24,0)); c.save('oog_16x.png')
dif=o!=o0
L=PAL.mean(1)
rep=[f'v16_r6 (vanaf r5): alleen iris. {int(dif.sum())} px gewijzigd: 9->8 (donker 1): {int(m1.sum())}, ->11 (donker 2, nieuw): {int(m2.sum())}',
 f'buiten de iris gewijzigd: {int((dif&~IR).sum())}; pupil/hooglicht/ring gewijzigd: {int((dif&~np.isin(o0,[8,9])).sum())}',
 f'helderheid iris: basis 9={L[9]:.0f}, donker 1 (8)={L[8]:.0f}, donker 2 (11, nieuw (112,12,18))={L[11]:.0f}, ring (1)={L[1]:.0f}; paletkleuren: 12 incl. transparant']
print('\n'.join(rep)); open('wijzigingen.txt','w').write('\n'.join(rep)+'\n')
C=' #2345.7RILD'
for y in range(y0,y1): print(''.join(C[t] for t in o0[y,x0:x1]),'  ',''.join(C[t] for t in o[y,x0:x1]))
