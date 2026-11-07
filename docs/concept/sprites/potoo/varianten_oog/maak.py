# Jordi 7 nov: "probeer eens eentje met een groot zwart oog? zonder wit erin" / "ter vergelijking". Varianten op kleur_r6.
# A: glans en reflectie zwart (zelfde maat). B: ook de grijze oogring zwart (groter oog).
import numpy as np; from PIL import Image; from collections import deque
im=Image.open('../kleur_r6/potoo.png'); a=np.array(im); pal=im.getpalette()
eye=np.zeros_like(a,bool); q=deque([(8,33)]); eye[8,33]=1
while q:
    y,x=q.popleft()
    for dy,dx in((1,0),(-1,0),(0,1),(0,-1)):
        yy,xx=y+dy,x+dx
        if 3<=yy<=13 and 28<=xx<=40 and not eye[yy,xx] and a[yy,xx] in (1,2,8): eye[yy,xx]=1; q.append((yy,xx))
A=a.copy(); A[eye]=1
pad=np.pad(eye,1); nb=pad[:-2,1:-1]|pad[2:,1:-1]|pad[1:-1,:-2]|pad[1:-1,2:]
ring=nb&~eye&(a==5); ring[:3]=False
B=A.copy(); B[ring]=1
for n,arr in (('A',A),('B',B)):
    o=Image.fromarray(arr,'P'); o.putpalette(pal); o.info['transparency']=0; o.save(f'potoo_{n}.png',transparency=0)
    print(n,'gewijzigd',int((arr!=a).sum()))
vs=[a,A,B]; z=8
sheet=Image.new('RGB',(3*64*z+20,64*z+80),(255,255,255))
for i,arr in enumerate(vs):
    o=Image.fromarray(arr,'P'); o.putpalette(pal); rgb=o.convert('RGB')
    m=Image.fromarray(((arr!=0)*255).astype('uint8'))
    bg=Image.new('RGB',(64,64),(255,255,255)); bg.paste(rgb,(0,0),m)
    sheet.paste(bg.resize((64*z,64*z),Image.NEAREST),(i*(64*z+10),0)); sheet.paste(bg,(i*(64*z+10)+5,64*z+8))
sheet.save('vel_oog.png')
