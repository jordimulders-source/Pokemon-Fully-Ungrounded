# Overlay ogen+mond (natief x35-43, r9-17 -> sprite x20-28, y3-11) + metingen geest : schoorsteenrand.
from PIL import Image, ImageDraw; import numpy as np
n=np.array(Image.open('model/natief.png').convert('RGB')).astype(int)
a=np.array(Image.open('sprite_r9/sprite.png'))
def donker(c): return c[1]<150 and c[1]>c[0]+25
fout=[];mis=[]
for r in range(9,18):
    for x in range(35,44):
        m=donker(n[r,x]); d=a[r-6,x-15]==6
        if d and not m: fout.append((x-15,r-6))
        if m and not d: mis.append((x-15,r-6))
print('ogen+mond: donker r9 niet in model',fout,'| donker model niet in r9',mis)
def breedte(arr,y,test):
    xs=[x for x in range(arr.shape[1]) if test(arr[y,x])]; return (min(xs),max(xs),max(xs)-min(xs)+1) if xs else None
G=lambda v:v in (2,5,6,13); I=lambda v:v in (1,7,8,9,10,11,12)
gn=lambda c:c[1]>c[0]+25 and c.min()<235; inn=lambda c:not(c[1]>c[0]+25) and c.min()<235
# kop: breedste groene rij zonder arm (x<=47 natief / <=32 sprite) op oog-hoogte r10; rand: r23; hals: r21
kn=breedte(n[:, :48],10,gn); ks=breedte(a[:, :33],4,G)
rn=breedte(n[:, 20:45],24,inn); rs=breedte(a[:, 5:30],17,I)
hn=breedte(n[:, 29:40],21,gn); hs=breedte(a[:, 14:25],14,G)
print('kop  model',kn,' r9',ks); print('rand model',rn,' r9',rs); print('hals model',hn,' r9',hs)
print('kop/rand  model %.2f  r9 %.2f'%(kn[2]/rn[2],ks[2]/rs[2])); print('hals/rand model %.2f  r9 %.2f'%(hn[2]/rn[2],hs[2]/rs[2]))
Z=24; c=Image.open('sprite_r9/sprite.png').convert('RGBA'); b=Image.new('RGBA',c.size,(255,255,255,255)); b.alpha_composite(c)
big=b.convert('RGB').crop((14,0,44,20)).resize((30*Z,20*Z),Image.NEAREST); dr=ImageDraw.Draw(big)
for r in range(9,18):
    for x in range(35,44):
        if donker(n[r,x]): X=x-15-14; Y=r-6; dr.rectangle([X*Z+3,Y*Z+3,(X+1)*Z-4,(Y+1)*Z-4],outline=(255,0,0),width=2)
dr.rectangle([(20-14)*Z,3*Z,(29-14)*Z,12*Z],outline=(0,0,255),width=2); big.save('sprite_r9/overlay.png')
