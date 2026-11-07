# Jordi 7 nov: "ja b is beter, alleen het oog mag nog wel wat schaduw". Varianten op potoo_B (zonder wit).
# C1: lichte kant linksboven in donkergrijs (2), rest zwart = schaduw rechtsonder. C2: idem, smaller (1 px) + zachte reflectie rechtsonder.
import numpy as np; from PIL import Image
im=Image.open('potoo_B.png'); a=np.array(im); pal=im.getpalette()
E=np.zeros_like(a,bool); E[4:14,29:39]=(a[4:14,29:39]==1)
def sh(m,dy,dx):
    o=np.zeros_like(m); H,W=m.shape
    o[max(dy,0):H+min(dy,0),max(dx,0):W+min(dx,0)]=m[max(-dy,0):H+min(-dy,0),max(-dx,0):W+min(-dx,0)]; return o
# binnenrand linksboven: pixels van E waarvan het punt 2 px naar linksboven niet in E ligt
lit2=E&~sh(E,2,2); lit1=E&~sh(E,1,1)
# rand niet tegen de buitenlijn: alleen binnenste pixels behouden waar de ring zat
C1=a.copy(); C1[lit2]=2
C2=a.copy(); C2[lit1]=2; ref=E&~sh(E,-1,-1)&~lit1; C2[ref]=2
ys,xs=np.where(E); cy,cx=ys.mean(),xs.mean()
inn=E&sh(E,1,0)&sh(E,-1,0)&sh(E,0,1)&sh(E,0,-1)
Y,X=np.indices(a.shape); d=(X-cx)+(Y-cy)
C3=a.copy(); C3[inn&(d<-1.5)]=2
C4=a.copy(); C4[inn&(d<-0.5)]=2; C4[inn&(d<-3.5)]=3
for n,arr in (('C1',C1),('C2',C2),('C3',C3),('C4',C4)):
    o=Image.fromarray(arr,'P'); o.putpalette(pal); o.save(f'potoo_{n}.png',transparency=0); print(n,int((arr!=a).sum()))
z=8; vs=[a,C1,C2,C3,C4]
sheet=Image.new('RGB',(5*(24*z+10),24*z+80),(255,255,255))
for i,arr in enumerate(vs):
    o=Image.fromarray(arr,'P'); o.putpalette(pal); rgb=o.convert('RGB'); m=Image.fromarray(((arr!=0)*255).astype('uint8'))
    bg=Image.new('RGB',(64,64),(255,255,255)); bg.paste(rgb,(0,0),m)
    sheet.paste(bg.crop((22,0,46,24)).resize((24*z,24*z),Image.NEAREST),(i*(24*z+10),0)); sheet.paste(bg,(i*(24*z+10)+60,24*z+8))
sheet.save('vel_schaduw.png')
