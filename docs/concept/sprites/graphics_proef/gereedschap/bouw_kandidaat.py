# Bouwt de kandidaten (gumfish rug, sunperor rug, sunperor frame 2) uit de natieve rasters.
# python3 gereedschap/bouw_kandidaat.py   (vanuit docs/concept/sprites/graphics_proef)
import numpy as np; from PIL import Image
SP='../'; K='kandidaat/'
def mapc(nat,pal,allowed):
    a=np.array(Image.open(nat).convert('RGB')).astype(int); bg=a.min(2)>215
    P=np.array(pal[:48]).reshape(-1,3)[allowed]
    d=((a[:,:,None,:]-P[None,None])**2).sum(3); idx=np.array(allowed)[d.argmin(2)]; idx[bg]=0
    return idx
def save(arr,pal,name):
    im=Image.fromarray(arr.astype('uint8'),'P'); im.putpalette(pal); im.info['transparency']=0
    im.save(K+name,transparency=0)
    p=list(pal); p[0:3]=[255,255,255]; w=Image.fromarray(arr.astype('uint8'),'P'); w.putpalette(p)
    w.convert('RGB').resize((arr.shape[1]*8,arr.shape[0]*8),Image.NEAREST).save(K+name.replace('.png','_8x.png'))
log=[]
# ---- 1. Gumfish rug
fr=Image.open(SP+'blobfish/af/blobfish.png'); gp=fr.getpalette(); f=np.array(fr)
used=sorted(set(np.unique(f))-{0})
g=mapc('nat_gumfish_rug_p1.png',gp,used)
G=[(x,y,f[y,x]) for y in range(31,39) for x in range(9,20) if f[y,x] in (10,11,13)]  # glans van de front
gl=g.copy()
for x,y,v in G: gl[y-13,x+18]=v
log.append('gumfish glans: %d px gewijzigd'%(gl!=g).sum())
ys,xs=np.where(gl>0); x0,x1,y1=xs.min(),xs.max(),ys.max()
out=np.zeros((64,64),int); dx=(64-(x1-x0+1))//2-x0; dy=63-y1
for y,x in zip(ys,xs): out[y+dy,x+dx]=gl[y,x]
save(out,gp,'gumfish_rug.png')
gum=(g,out,dx,dy)
# ---- 2. Sunperor rug
fr=Image.open(SP+'koningstiran/af/sapa_inca.png'); sp=fr.getpalette(); sf=np.array(fr)
s=mapc('nat_sunperor_rug_p1.png',sp,list(range(1,16))); r=s.copy()
# gezichtsblauw dat op lila (9) viel -> binnen beakgroep 13/14
r[23,35]=14; r[25,36]=13
# (b) losse donkere oogjes in de kroon
r[18,14]=10; r[18,16]=7
# (a) gaten links en rechts van de nek
for x in range(17,24):
    if r[22,x]==0: r[22,x]=1
for y in range(23,28):
    for x in range(16,24):
        if r[y,x]==0: r[y,x]=2
for x in range(38,42):
    if r[22,x]==0: r[22,x]=1
for y in range(23,28):
    for x in range(37,45):
        if r[y,x]==0: r[y,x]=2
for x in range(37,45):
    if r[28,x]==0: r[28,x]=1
log.append('sunperor rug: %d px gewijzigd t.o.v. kale omzetting'%(r!=s).sum())
out2=np.zeros((64,64),int); out2[9:64,0:63]=r[0:55,:]
save(out2,sp,'sunperor_rug.png')
# ---- 3. Sunperor frame 2
t=mapc('nat_sunperor_frame2_p1.png',sp,list(range(1,16))); t2=t.copy()
t2[20,22]=14   # (23,21) in 64-coords: lila -> snavelgrijs
t2[25,24]=6    # (25,26): zalmkleur in de bek, viel op bruin 4, tweeling ernaast is 6
log.append('sunperor frame2: %d px gewijzigd'%(t2!=t).sum())
f2=np.zeros((64,64),int); f2[1:64,1:64]=t2
save(f2,sp,'sunperor_frame2.png')
log.append('frame2 verschilt van front in %d px'%(f2!=sf).sum())
anim=np.vstack([sf,f2]); save(anim,sp,'sunperor_anim_front.png')
p=list(sp); fr1=[]
for a in (sf,f2):
    im=Image.fromarray(a.astype('uint8'),'P'); im.putpalette(p)
    fr1.append(im.convert('RGB').resize((256,256),Image.NEAREST))
fr1[0].save(K+'sunperor_anim.gif',save_all=True,append_images=[fr1[1]],duration=400,loop=0)
# ---- vergelijkingsvel
def rgb(a,pal):
    p=list(pal); p[0:3]=[255,255,255]; im=Image.fromarray(a.astype('uint8'),'P'); im.putpalette(p); return im.convert('RGB')
def pad64(a):
    o=np.zeros((64,64),int); h,w=a.shape; o[64-min(h,64):,:min(w,64)]=a[max(0,h-64):,:64]; return o
rows=[]
gn=Image.open('nat_gumfish_rug_p1.png').convert('RGB')
sn=Image.open('nat_sunperor_rug_p1.png').convert('RGB'); fn=Image.open('nat_sunperor_frame2_p1.png').convert('RGB')
sets=[(gn,rgb(out,gp),rgb(f,gp)),(sn,rgb(out2,sp),rgb(sf,sp)),(fn,rgb(f2,sp),rgb(sf,sp))]
W=3*(80*8)+40; H=len(sets)*(80*8)
vel=Image.new('RGB',(W,H),(255,255,255))
for i,trio in enumerate(sets):
    for j,im in enumerate(trio):
        vel.paste(im.resize((im.width*8,im.height*8),Image.NEAREST),(j*(80*8+20),i*80*8))
vel.save(K+'vergelijking.png')
print('\n'.join(log))
for n in ['gumfish_rug.png','sunperor_rug.png','sunperor_frame2.png']:
    a=np.array(Image.open(K+n)); print(n,Image.open(K+n).mode,a.shape,'kleuren',len(set(np.unique(a))-{0}))
