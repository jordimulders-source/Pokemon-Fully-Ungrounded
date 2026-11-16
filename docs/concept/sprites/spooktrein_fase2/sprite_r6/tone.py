# Per spritepixel: aandelen modeltonen (natief): W wit(>240) L licht(200-240) M mid(140-200) D diep(60-140) O lijn(<60)
import sys, numpy as np; from PIL import Image
s,X0,Y0,oy,XC,k=[float(v) for v in open('../sprite_r2/sprite.meta').read().split()]
a=np.asarray(Image.open('../sprite_r5/natief.png').convert('RGB')).astype(float); L=a@[0.3,0.59,0.11]
def nx_of(mx): return mx if mx<XC else XC+(mx-XC)/k
def block(sx,sy):
    ya,yb=Y0+(sy-oy)/s, Y0+(sy+1-oy)/s; xa,xb=nx_of(X0+sx/s), nx_of(X0+(sx+1)/s)
    out=[];
    for y in range(int(np.floor(ya)),int(np.ceil(yb))):
        for x in range(int(np.floor(xa)),int(np.ceil(xb))):
            if 0<=y<199 and 0<=x<199:
                # gewicht = overlap
                w=(min(y+1,yb)-max(y,ya))*(min(x+1,xb)-max(x,xa))
                if w>0: out.append((L[y,x],w))
    return out
T=np.zeros((5,64,64))
for sy in range(64):
    for sx in range(64):
        for v,w in block(sx,sy):
            c=0 if v>240 else 1 if v>=200 else 2 if v>=140 else 3 if v>=60 else 4
            T[c,sy,sx]+=w
T/=T.sum(0,keepdims=True); np.save('tones.npy',T)
if len(sys.argv)>4:
    x0,y0,x1,y1=map(int,sys.argv[1:5]); o=np.asarray(Image.open(sys.argv[5] if len(sys.argv)>5 else 'sprite.png')).astype(int); ch='.#23456789abcd'
    nm='WLMDO'
    print('   '+''.join('%5d'%x for x in range(x0,x1+1)))
    for y in range(y0,y1+1):
        row=''
        for x in range(x0,x1+1):
            t=T[:,y,x]; fg=t[1:].sum()
            dom=nm[1+t[1:].argmax()] if fg>0.15 else 'W'
            row+='  %s%s%s'%(ch[o[y,x]],dom,'%d'%min(9,int(t[1+t[1:].argmax()]/max(fg,1e-9)*10)) if fg>0.15 else ' ')
        print('%2d '%y+row)
