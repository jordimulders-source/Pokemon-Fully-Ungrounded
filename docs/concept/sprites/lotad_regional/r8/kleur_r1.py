from PIL import Image
import numpy as np
def q(path,n):
    im=Image.open(path).convert('RGB')
    a=np.array(im).astype(float)
    L=0.3*a[...,0]+0.59*a[...,1]+0.11*a[...,2]
    sat=a.max(2)-a.min(2)
    white=(L>222)&(sat<40)
    a[white]=255
    qi=Image.fromarray(a.astype('uint8')).quantize(n,method=Image.MEDIANCUT,dither=Image.Dither.NONE)
    return np.array(qi.convert('RGB')).astype(float)
A=q('r8/gemini_r8_1.png',20); B=q('r1/gemini_r1.png',20)
def F(X):
    R,G,Bc=X[...,0],X[...,1],X[...,2]; L=0.3*R+0.59*G+0.11*Bc
    yy,xx=np.mgrid[0:X.shape[0],0:X.shape[1]]
    w=(X==255).all(2); ln=L<45
    return R,G,Bc,L,yy,xx,w,ln
R,G,Bc,L,y,x,w,ln=F(A); body=~w&~ln
a={}
a['hat']=body&(y<236)
a['bill']=body&~a['hat']&(x>=380)&(x<=500)&(y>=274)&(y<=313)&(L>150)
rest=body&~a['hat']&~a['bill']
a['legs']=rest&(R>G+4)&(y>370)
a['fringe']=rest&~a['legs']&((y>=322)|(L>150)|(x>588))
a['face']=rest&~a['legs']&~a['fringe']
R2,G2,B2,L2,y2,x2,w2,ln2=F(B); body2=~w2&~ln2
b={}
b['hat']=body2&(y2<232)
b['bill']=body2&(x2>=385)&(x2<=480)&(y2>=262)&(y2<=320)&(G2>R2-40)&(B2<130)&(R2>150)
b['legs']=body2&(y2>385)&(R2>G2+35)&~b['bill']
b['fringe']=body2&(y2>=300)&(y2<=440)&(R2-G2<35)&~b['bill']&~b['legs']&~b['hat']
b['face']=body2&(y2>=236)&(y2<=330)&(R2>G2+35)&~b['bill']
out=A.copy()
BILL=np.array([[181,153,87],[205,176,105],[229,199,124]])
for k in a:
    if k=='bill':
        lb_=L[a['bill']]; t=np.digitize(lb_,np.percentile(lb_,[25,60])); out[a['bill']]=BILL[t]; continue
    # r1 region colours with pixel counts, sorted by luminance -> cumulative percentiles
    cb,nb=np.unique(B[b[k]],axis=0,return_counts=True)
    keep=nb>nb.sum()*0.01; cb,nb=cb[keep],nb[keep]
    lb=0.3*cb[:,0]+0.59*cb[:,1]+0.11*cb[:,2]; o=np.argsort(lb); cb,nb=cb[o],nb[o]; cumb=np.cumsum(nb)/nb.sum()
    ca,inv,na=np.unique(A[a[k]],axis=0,return_inverse=True,return_counts=True)
    la=0.3*ca[:,0]+0.59*ca[:,1]+0.11*ca[:,2]; o=np.argsort(la)
    cum=np.zeros(len(ca)); c=0
    for i in o: cum[i]=c+na[i]/2; c+=na[i]
    cum/=c
    newc=np.array([cb[min(np.searchsorted(cumb,p),len(cb)-1)] for p in cum])
    out[a[k]]=newc[inv.ravel()]
out[ln&~w]=np.array([20,10,5])
# ogen: Lotad-oog (wit rondje met zwarte stip), op het 4-px raster
def eye(cx,cy,n,p):
    S=4
    for j in range(n):
        for i in range(n):
            dx=i-(n-1)/2; dy=j-(n-1)/2
            if dx*dx+dy*dy> ((n)/2)**2: continue
            col=np.array([255,255,255])
            if abs(dx)<=p/2 and abs(dy)<=p/2: col=np.array([16,16,16])
            out[int(cy+ (j-n/2)*S):int(cy+(j-n/2+1)*S), int(cx+(i-n/2)*S):int(cx+(i-n/2+1)*S)]=col
# oude ogen weg: niet-gezichtspixels in het oogvak krijgen de kleur van de dichtstbijzijnde gezichtspixel
for (x0,y0,x1,y1) in [(482,248,514,284),(394,246,420,280)]:
    box=np.zeros(a['face'].shape,bool); box[y0:y1,x0:x1]=True
    face_ok=a['face']&~box
    near=box&~a['hat']
    fy,fx=np.where(face_ok[y0-30:y1+30,x0-30:x1+30]); fy+=y0-30; fx+=x0-30
    for (yy_,xx_) in zip(*np.where(near)):
        k_=np.argmin((fy-yy_)**2+(fx-xx_)**2); out[yy_,xx_]=out[fy[k_],fx[k_]]
eye(498,266,5,1)   # nabij oog
eye(407,263,3,1)   # ver oog, smaller (driekwart)
Image.fromarray(out.clip(0,255).astype('uint8')).save('r8/r8_1_kleuren_r1.png')
row=Image.new('RGB',(3*420,400),'white')
for i,f in enumerate(['r1/gemini_r1.png','r8/gemini_r8_1.png','r8/r8_1_kleuren_r1.png']):
    row.paste(Image.open(f).convert('RGB').crop((300,70,720,470)),(i*420,0))
row.save('r8/kleuren_r1_vergelijk.png')
