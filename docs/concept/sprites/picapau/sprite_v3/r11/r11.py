# r11 op r10/picapau_kuif_A.png: (1) bovenste stekel terug naar r7-vorm + binnenlijn A aangesloten, (2) kop links ronder.
import numpy as np; from PIL import Image, ImageDraw
src=Image.open('../r10/picapau_kuif_A.png'); A=np.array(src); a=A.copy(); r7=np.array(Image.open('../r7/picapau.png')); PAL=src.getpalette()
V,H=13,2
# 1 stekel: r7-waarden in x31-35 / y21-25, daarna binnenlijn van A over de stekelvoet (x31 r22-23, x32 r24; sluit aan op A's lijn x33 r26-28)
for y in range(21,26):
    for x in range(31,36): a[y,x]=r7[y,x]
for x,y in [(31,22),(31,23),(32,24)]: a[y,x]=V
# 2 kop links: rand per rij 21..27 = 24,20,18,17,16,16,16 (looplengtes 4,2,1,1 als cirkelkwart)
for x,y,v in [(20,22,V),(18,23,V),(20,23,H),(17,24,V),(18,24,H),(16,25,V),(17,25,H)]: a[y,x]=v
d=np.argwhere(a!=A)
z1=[(int(x),int(y)) for y,x in d if x>=30]; z2=[(int(x),int(y)) for y,x in d if x<30]
print('zone 1 stekel',len(z1),z1); print('zone 2 kop links',len(z2),z2)
p=Image.fromarray(a,'P'); p.putpalette(PAL); p.save('picapau.png',transparency=0)
def rgb(arr,s):
    q=Image.fromarray(arr,'P'); q.putpalette(PAL); q.info['transparency']=0; im=q.convert('RGBA')
    b=Image.new('RGBA',im.size,(255,255,255,255)); b.alpha_composite(im); return b.convert('RGB').resize((64*s,64*s),0)
rgb(a,8).save('picapau_8x.png')
X0,Y0,X1,Y1=12,12,40,40; W=(X1-X0)*12
mi=Image.open('../../gemini/r5_verbeter.png').convert('RGB'); c=lambda s:4.13+(1+3*s)*5.12
m=mi.crop((int(c(X0+5)),int(c(Y0-10)),int(c(X1+5)),int(c(Y1-10)))).resize((W,W),Image.LANCZOS)
v=Image.new('RGB',(3*(W+10),W+24+140),(200,200,200)); dr=ImageDraw.Draw(v)
for i,(t,arr) in enumerate([('r10 A',A),('r11',a)]):
    v.paste(rgb(arr,12).crop((X0*12,Y0*12,X1*12,Y1*12)),(i*(W+10),24)); dr.text((i*(W+10)+2,6),t,fill=(0,0,0))
    v.paste(rgb(arr,1),(i*(W+10),W+34)); v.paste(rgb(arr,2),(i*(W+10)+70,W+34))
v.paste(m,(2*(W+10),24)); dr.text((2*(W+10)+2,6),'model (zelfde schaal)',fill=(0,0,0)); v.save('kop_r10A_r11_model.png')
