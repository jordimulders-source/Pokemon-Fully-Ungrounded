# Controle Gen 3: kleine tintvlakjes (<3 px, 4-buren), lichte pixels op de buitenrand, tinten per groep, dambord
import sys,numpy as np; from PIL import Image
GROEP={'zwart':[1],'kop':[2,3,11],'snavel/vl.lijn':[4],'lijf':[5,6,7,8],'teal':[15,9,10],'licht':[12,13,14]}
def comps(a):
    H,W=a.shape; seen=np.zeros_like(a,bool); out=[]
    for y in range(H):
        for x in range(W):
            if a[y,x]==0 or seen[y,x]: continue
            v=a[y,x]; st=[(y,x)]; seen[y,x]=1; c=[]
            while st:
                p=st.pop(); c.append(p)
                for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
                    q=(p[0]+dy,p[1]+dx)
                    if 0<=q[0]<H and 0<=q[1]<W and not seen[q] and a[q]==v: seen[q]=1; st.append(q)
            out.append((v,c))
    return out
def rand(a):
    p=np.pad(a,1); bg=(p[:-2,1:-1]==0)|(p[2:,1:-1]==0)|(p[1:-1,:-2]==0)|(p[1:-1,2:]==0)
    return (a>0)&bg
if __name__=='__main__':
    a=np.array(Image.open(sys.argv[1]))
    small=[(v,c) for v,c in comps(a) if len(c)<3 and v!=1]
    print('kleine vlakjes (<3px, excl. zwart):',len(small)); print('  ',[(int(v),[(int(x),int(y)) for y,x in c]) for v,c in small])
    r=rand(a); lp=[(int(x),int(y),int(a[y,x])) for y,x in zip(*np.where(r&np.isin(a,[8,10,13,14])))]
    print('lichte randpixels (8,10,13,14):',len(lp),lp)
    print('tinten per groep:',{k:[i for i in v if (a==i).any()] for k,v in GROEP.items()})
    print('kleuren gebruikt:',len(np.unique(a))-1)
