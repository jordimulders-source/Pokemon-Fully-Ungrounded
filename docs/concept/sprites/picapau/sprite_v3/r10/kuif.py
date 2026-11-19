# r10: kuif/stekels rechts als kam ACHTER de kop: alleen kleur/schaduw in de zone x30-37, y18-32. Vorm = r8b.
import numpy as np; from PIL import Image, ImageDraw
src=Image.open('../r8b/picapau.png'); base=np.array(src); PAL=src.getpalette()
Z,G,D,V,L2=1,3,4,13,2
# kopcontour (binnenlijn) voor de stekelvoeten langs: x32 r23-26, x33 r27-28 (sluit aan op kroonlijn boven en buitenlijn onder)
LIJN=[(31,23),(32,24),(32,25),(33,26),(33,27),(33,28)]   # ronde kopcontour (cirkel rond het kopmidden)
# kopvlak direct links van de lijn: lichter (midden) zodat de kop als bol vóór de kam ligt
KOP=[(31,24),(31,25),(32,26),(32,27),(32,28)]
# stekelpixels (binnen) en stekelrand (boven) uit r8b
STEKTOP=[(33,23),(34,23),(34,26),(35,26)]
def var(k):
    a=base.copy()
    for p in LIJN: a[p[1],p[0]]=V          # A, B, C: binnenlijn langs de ronde achterkant van de kop, over de stekelvoeten
    if k=='B':
        for p in KOP: a[p[1],p[0]]=G       # kop vlak voor de lijn lichter: bol ligt voor de (donkere) kam
    if k=='C':
        for p in STEKTOP: a[p[1],p[0]]=Z   # kam verder weg/in schaduw: geen selout, rondom zwart
    return a
out={}
for k in 'ABC':
    a=var(k); out[k]=a
    d=np.argwhere(a!=base); assert all(30<=x<=37 and 18<=y<=32 for y,x in d)
    print(k,'gewijzigd',len(d),[(int(x),int(y)) for y,x in d])
    p=Image.fromarray(a,'P'); p.putpalette(PAL); p.save('picapau_kuif_%s.png'%k,transparency=0)
# vel
def rgb(a,s,bg=(255,255,255,255)):
    p=Image.fromarray(a,'P'); p.putpalette(PAL); p.info['transparency']=0; im=p.convert('RGBA')
    b=Image.new('RGBA',im.size,bg); b.alpha_composite(im); return b.convert('RGB').resize((64*s,64*s),0)
mi=Image.open('../../gemini/r5_verbeter.png').convert('RGB'); c=lambda s:4.13+(1+3*s)*5.12
X0,Y0,X1,Y1=16,12,40,36   # canvas-uitsnede kop; model: sprite-raster = canvas+(5,-10)
m=mi.crop((int(c(X0+5)),int(c(Y0-10)),int(c(X1+5)),int(c(Y1-10)))).resize(((X1-X0)*12,(Y1-Y0)*12),Image.LANCZOS)
tiles=[('r8b',base)]+[(k,out[k]) for k in 'ABC']
W=(X1-X0)*12; H=(Y1-Y0)*12
V_=Image.new('RGB',(len(tiles)*(W+10)+W+10,H+24+150),(200,200,200)); dr=ImageDraw.Draw(V_)
for i,(k,a) in enumerate(tiles):
    x=i*(W+10); V_.paste(rgb(a,12).crop((X0*12,Y0*12,X1*12,Y1*12)),(x,24)); dr.text((x+2,6),k,fill=(0,0,0))
    V_.paste(rgb(a,1),(x,H+34)); V_.paste(rgb(a,2),(x+70,H+34))
V_.paste(m,(len(tiles)*(W+10),24)); dr.text((len(tiles)*(W+10)+2,6),'model (Gemini r5), zelfde schaal',fill=(0,0,0))
h=Image.open('../../gemini/hoek3d/lijf45.png').convert('RGB'); h=h.crop((140,20,340,220)).resize((150,150))
V_.paste(h,(len(tiles)*(W+10),H+30)); V_.save('varianten_kuif.png'); print(V_.size)
