# natief raster -> exacte 2x2-reductie met regels (niets getekend). python3 half.py view oy ox
import sys, numpy as np; from PIL import Image
C={'.':(255,255,255),'#':(20,15,10),'L':(240,190,100),'M':(225,165,80),'D':(190,130,60),'d':(170,110,50),'c':(245,225,175),'Y':(245,220,70),'y':(215,180,40)}
K=list(C); V=np.array([C[k] for k in K],float)
M={'L':'F','M':'F','D':'m','d':'s','c':'C','Y':'Y','y':'k'}
def labels(n):
    a=np.asarray(Image.open(f'nat_{n}.png').convert('RGB')).astype(float)
    lab=np.array(K)[((a[:,:,None,:]-V[None,None])**2).sum(-1).argmin(-1)]
    lab[:5]='.'; lab[49:]='.'
    if n=='back': lab[:,47:]='.'
    if n=='side': lab[:,51:]='.'
    return lab
def half(lab,oy,ox):
    H,W=lab.shape; h=(H-oy)//2; w=(W-ox)//2; g=[]
    for j in range(h):
        r=''
        for i in range(w):
            b=lab[oy+2*j:oy+2*j+2, ox+2*i:ox+2*i+2].ravel()
            nb=(b=='.').sum(); nd=(b=='#').sum()
            if nb>=3 or (nb==2 and nd==0 and False): r+='.'; continue
            if nb>=2: r+='o' if nd>=1 else '.'; continue   # rand: helft leeg -> omlijning of leeg
            if nd>=2: r+='o'; continue
            rest=[x for x in b if x not in '.#']
            vals,cnt=np.unique(rest,return_counts=True); r+=M[vals[cnt.argmax()]]
        g.append(r)
    # bijsnijden
    rows=[i for i,r in enumerate(g) if r.strip('.')]; g=g[rows[0]:rows[-1]+1]
    cols=[i for i in range(len(g[0])) if any(r[i]!='.' for r in g)]
    return [r[cols[0]:cols[-1]+1] for r in g]
if __name__=='__main__':
    n=sys.argv[1]; lab=labels(n)
    for oy in (0,1):
        for ox in (0,1):
            g=half(lab,oy,ox); open(f'half_{n}_{oy}{ox}.txt','w').write('\n'.join(g)+'\n'); print(n,oy,ox,len(g[0]),len(g))
