import numpy as np; from PIL import Image; import sys
o=np.asarray(Image.open(sys.argv[1] if len(sys.argv)>1 else 'sprite.png')).astype(int)
def comps(mask):
    seen=np.zeros((64,64),bool); out=[]
    for y in range(64):
        for x in range(64):
            if mask[y,x] and not seen[y,x]:
                st=[(y,x)]; seen[y,x]=True; cur=[]
                while st:
                    cy,cx=st.pop(); cur.append((cx,cy))
                    for dy,dx in ((-1,0),(1,0),(0,-1),(0,1)):
                        yy,xx=cy+dy,cx+dx
                        if 0<=yy<64 and 0<=xx<64 and mask[yy,xx] and not seen[yy,xx]: seen[yy,xx]=True; st.append((yy,xx))
                out.append(cur)
    return out
W=np.zeros((64,64),bool); W[22:45,3:56]=True
for v,n in ((9,'tint 9'),(13,'tint d'),(1,'zwart'),(10,'roest'),(7,'licht hout'),(8,'midden hout')):
    sm=[c for c in comps((o==v)&W) if len(c)<3]; print(n,'clusters <3 px in wagen:',len(sm),sm[:12])
fg=o>0; p=np.pad(fg,1); e=fg&~(p[:-2,1:-1]&p[2:,1:-1]&p[1:-1,:-2]&p[1:-1,2:])
li=[(x,y,o[y,x]) for y,x in zip(*np.where(e)) if o[y,x] in (2,3,4,6,7,8,10)]
print('lichte tint op buitenrand:',len(li),li[:20])
print('tint 6 in geest (y<27):',[(x,y) for y,x in zip(*np.where(o[:27]==6))])
