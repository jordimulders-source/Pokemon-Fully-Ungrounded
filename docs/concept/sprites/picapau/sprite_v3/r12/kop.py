# r12: kop links bolt uit naar links (A max 1, B max 2, C max 3 px); snavel schuift mee (zelfde pixels).
# Werkwijze: per rij het stuk links van x=23 als geheel naar links schuiven (kleur blijft: selout, snavel, verre wang),
# opvullen met de vlakkleur van x=22; bovenrand rij 21-22 links van het oor: selout-run + lichtgeel eronder.
import numpy as np; from PIL import Image, ImageDraw
src=Image.open('../r11/picapau.png'); R11=np.array(src); PAL=src.getpalette(); V,H=13,2
S={ # verschuiving per rij 23..38
 'A':dict(zip(range(23,39),[0,1,1,1,1, 1,1,1,1,1, 1,1,0,0,0,0])),
 'B':dict(zip(range(23,39),[1,2,2,2,2, 2,2,2,2,2, 2,2,1,1,1,0])),
 'C':dict(zip(range(23,39),[2,3,3,3,3, 3,3,3,3,3, 3,3,2,2,2,1]))}
TOP={'A':(23,20),'B':(22,19),'C':(21,18)}   # (start rij 21, start rij 22)
XA=23
def maak(k):
    a=R11.copy()
    for y,s in S[k].items():
        if s==0: continue
        row=R11[y].copy(); L=np.where(row[:XA]>0)[0].min()
        new=row.copy(); new[L-s:XA-s]=row[L:XA]; new[XA-s:XA]=row[XA-1]
        a[y]=new
    x21,x22=TOP[k]
    for x in range(x21,24): a[21,x]=V
    for x in range(x22,x21): a[22,x]=V
    for x in range(x21,24): a[22,x]=H
    return a
def rand(a,y):
    xs=np.where(a[y,:30]>0)[0]; return int(xs.min()) if len(xs) else None
res={}
for k in 'ABC':
    a=maak(k); res[k]=a; d=np.argwhere(a!=R11)
    assert all(x<=23 and 21<=y<=38 for y,x in d)
    print(k,'gewijzigd',len(d),'px; rand per rij 21-38:',[rand(a,y) for y in range(21,39)])
    p=Image.fromarray(a,'P'); p.putpalette(PAL); p.save('picapau_kop_%s.png'%k,transparency=0)
print('r11 rand',[rand(R11,y) for y in range(21,39)])
def rgb(arr,s):
    q=Image.fromarray(arr,'P'); q.putpalette(PAL); q.info['transparency']=0; im=q.convert('RGBA')
    b=Image.new('RGBA',im.size,(255,255,255,255)); b.alpha_composite(im); return b.convert('RGB').resize((64*s,64*s),0)
X0,Y0,X1,Y1=8,14,34,42; W=(X1-X0)*12; Hh=(Y1-Y0)*12
mi=Image.open('../../gemini/r5_verbeter.png').convert('RGB'); c=lambda s:4.13+(1+3*s)*5.12
m=mi.crop((int(c(X0+5)),int(c(Y0-10)),int(c(X1+5)),int(c(Y1-10)))).resize((W,Hh),Image.LANCZOS)
tiles=[('r11',R11)]+[(k,res[k]) for k in 'ABC']
v=Image.new('RGB',(5*(W+10),Hh+60+140),(200,200,200)); dr=ImageDraw.Draw(v)
for i,(t,arr) in enumerate(tiles):
    x=i*(W+10); v.paste(rgb(arr,12).crop((X0*12,Y0*12,X1*12,Y1*12)),(x,24)); dr.text((x+2,6),t,fill=(0,0,0))
    dr.text((x+2,Hh+28),'rand r21-38: '+','.join(str(rand(arr,y)) for y in range(21,39)),fill=(0,0,0))
    v.paste(rgb(arr,1),(x,Hh+50)); v.paste(rgb(arr,2),(x+70,Hh+50))
v.paste(m,(4*(W+10),24)); dr.text((4*(W+10)+2,6),'model (zelfde schaal)',fill=(0,0,0)); v.save('varianten_kop.png')
