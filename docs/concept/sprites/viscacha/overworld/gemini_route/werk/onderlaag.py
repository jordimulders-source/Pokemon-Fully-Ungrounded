import numpy as np; from PIL import Image; import sys, json
s=float(sys.argv[1]); thr=float(sys.argv[2]) if len(sys.argv)>2 else 0.35
C={'.':(255,255,255),'#':(20,15,10),'L':(240,190,100),'M':(225,165,80),'D':(190,130,60),'d':(170,110,50),'c':(245,225,175),'Y':(245,220,70),'y':(215,180,40)}
K=list(C); V=np.array([C[k] for k in K],float)
crop={'front':(0,46),'back':(0,47),'side':(0,51)}
out={}
for n in ['front','back','side']:
    a=np.asarray(Image.open(f'nat_{n}.png').convert('RGB')).astype(float)[:,crop[n][0]:crop[n][1]]
    d=((a[:,:,None,:]-V[None,None])**2).sum(-1); idx=d.argmin(-1)
    lab=np.array(K)[idx]
    lab[:5]='.'; lab[49:]='.'
    ys,xs=np.where(lab!='.'); y0,y1,x0,x1=ys.min(),ys.max()+1,xs.min(),xs.max()+1
    lab=lab[y0:y1,x0:x1]; H,W=lab.shape
    h,w=round(H*s),round(W*s); st=1/s
    g=[]
    for j in range(h):
        row=''
        for i in range(w):
            wts={}
            # supersample
            for yy in np.linspace(j*st,(j+1)*st,7)[:-1]+st/12:
                for xx in np.linspace(i*st,(i+1)*st,7)[:-1]+st/12:
                    k=lab[min(H-1,int(yy)),min(W-1,int(xx))]; wts[k]=wts.get(k,0)+1
            tot=sum(wts.values()); bgw=wts.get('.',0)/tot
            if bgw>0.5: row+='.'; continue
            if wts.get('#',0)/tot>=thr: row+='#'; continue
            nb={k:v for k,v in wts.items() if k not in '.#'}
            row+=max(nb,key=nb.get) if nb else '#'
        g.append(row)
    out[n]=g
    print(n,W,H,'->',w,h)
    for j,r in enumerate(g): print('%2d '%j+r)
M={'.':'.','#':'o','L':'F','M':'F','D':'m','d':'s','c':'C','Y':'Y','y':'k'}
for n,g in out.items(): open(f'onder_{n}.txt','w').write('\n'.join(''.join(M[c] for c in r) for r in g)+'\n')
