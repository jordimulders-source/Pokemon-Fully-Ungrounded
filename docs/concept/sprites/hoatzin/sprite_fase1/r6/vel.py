# vel.png: r6 8x met vleugelomtrek (rood) | r4 8x | close-up gebied r4 | r6 | model zelfde schaal | overlay overgenomen modellijnen
import numpy as np
from PIL import Image, ImageDraw
def rgb(fn,z,bg=(255,255,255)):
    im=Image.open(fn).convert('RGBA'); im=im.resize((im.width*z,im.height*z),Image.NEAREST)
    b=Image.new('RGB',im.size,bg); b.paste(im,(0,0),im); return b
r6,r4='kuiken_r6.png','../r4/kuiken_r4_haarB.png'
W=np.load('vleugel.npy'); ML=np.load('modellijn.npy'); a6=np.array(Image.open(r6))
z=8; P=512; box=(24,28,56,64); cw=(box[2]-box[0])*z; ch=(box[3]-box[1])*z
# r6 8x met rode omtrek van de vleugelvorm
A=rgb(r6,z); d=ImageDraw.Draw(A)
for y,x in zip(*np.nonzero(W)):
    for dy,dx,ln in ((-1,0,((0,0),(1,0))),(1,0,((0,1),(1,1))),(0,-1,((0,0),(0,1))),(0,1,((1,0),(1,1)))):
        if not W[y+dy,x+dx]:
            (ax,ay),(bx,by)=ln; d.line(((x+ax)*z,(y+ay)*z,(x+bx)*z,(y+by)*z),fill=(230,0,0),width=2)
# model op dezelfde schaal
mo=Image.open('../../model/fase1_model.png').convert('RGB'); am=np.array(mo).sum(2)<720; ys,xs=np.nonzero(am)
mx0,mx1,my0,my1=xs.min(),xs.max()+1,ys.min(),ys.max()+1
tox=lambda X:mx0+(X-12)*(mx1-mx0)/40; toy=lambda Y:my0+(Y-20)*(my1-my0)/44
M=mo.crop((int(tox(box[0])),int(toy(box[1])),int(tox(box[2])),int(toy(box[3])))).resize((cw,ch),Image.LANCZOS)
# overlay: modellijnpixels (binnen) groen, vleugelbuitenlijn zwart=blauw / donkergrijs=cyaan
O=rgb(r6,z).crop((box[0]*z,box[1]*z,box[2]*z,box[3]*z)); do=ImageDraw.Draw(O)
for y,x in zip(*np.nonzero(ML)):
    do.rectangle(((x-box[0])*z+1,(y-box[1])*z+1,(x-box[0]+1)*z-2,(y-box[1]+1)*z-2),outline=(0,200,0),width=2)
vel=Image.new('RGB',(2*(P+10)+4*(cw+10),P+30),(200,200,200)); dv=ImageDraw.Draw(vel); x=0
for nm,im in (('r6 8x + vleugelomtrek (rood)',A),('r4 haren B 8x',rgb(r4,z))):
    vel.paste(im,(x,20)); dv.text((x,4),nm,fill=0); x+=P+10
for nm,im in (('gebied r4',rgb(r4,z).crop((box[0]*z,box[1]*z,box[2]*z,box[3]*z))),('gebied r6',rgb(r6,z).crop((box[0]*z,box[1]*z,box[2]*z,box[3]*z))),
              ('model zelfde schaal',M),('overgenomen modellijnen (groen)',O)):
    vel.paste(im,(x,20)); dv.text((x,4),nm,fill=0); x+=cw+10
vel.paste(rgb(r6,1),(x-4*(cw+10),20+ch+20)); vel.paste(rgb(r6,1,(40,40,40)),(x-4*(cw+10)+74,20+ch+20)); dv.text((x-4*(cw+10),ch+28),'r6 1x',fill=0)
vel.save('vel.png')
