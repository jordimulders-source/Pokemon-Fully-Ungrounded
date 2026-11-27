# deel.py rN y0 y1 out: sprite-rijen y0..y1 op 12x met rasternummers | bijbehorende natieve rijen (zelfde hoogte) | vorige ronde optioneel
from PIL import Image, ImageDraw; import numpy as np, sys
D='docs/concept/sprites/hitmonchan_regional/sprite/'
sys.path.insert(0,D); 
r=sys.argv[1]; y0,y1=int(sys.argv[2]),int(sys.argv[3]); out=sys.argv[4]; Z=14
S=np.load(D+f'{r}/idx.npy'); pal=eval(open(D+(f'{r}/pal.txt' if __import__('os').path.exists(D+f'{r}/pal.txt') else 'pal.txt')).read())
def randen(N,a,b,A,uit):
    k1=a/A; B=A+(b-a); k2=(N-b)/(uit-B); return [i*k1 if i<=A else (a+(i-A) if i<=B else b+(i-B)*k2) for i in range(uit+1)]
ry=randen(81,24,32,18,64)
nat=np.asarray(Image.open(D+'natief.png').convert('RGB'))
def img(L):
    a=np.zeros(L.shape+(3,),np.uint8); a[:]=255
    for k,c in enumerate(pal):
        if k: a[L==k]=c
    return a
sp=Image.fromarray(img(S[y0:y1])).resize((S.shape[1]*Z,(y1-y0)*Z),Image.NEAREST)
ny0=int(round(ry[y0])); ny1=int(round(ry[y1]))
nm=Image.fromarray(nat[ny0:ny1]); h=(y1-y0)*Z; nm=nm.resize((int(nm.width*h/nm.height),h),Image.NEAREST)
v=Image.new('RGB',(sp.width+nm.width+60,h+20),(255,255,255)); v.paste(sp,(30,20)); v.paste(nm,(sp.width+50,20))
d=ImageDraw.Draw(v)
for i in range(S.shape[1]):
    d.text((30+i*Z+2,4),str(i%10),fill=(200,0,0)); (i%5==0) and d.line([(30+i*Z,20),(30+i*Z,20+h)],fill=(255,0,0))
for j in range(y1-y0):
    d.text((2,20+j*Z+2),str(y0+j),fill=(200,0,0)); ((y0+j)%5==0) and d.line([(30,20+j*Z),(30+sp.width,20+j*Z)],fill=(255,0,0))
v.save(out)
