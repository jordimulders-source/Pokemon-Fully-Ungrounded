# Groen spookwiel uit model r5: in de wielzone per spritepixel het aandeel donkere ringpixels (lum<150, groen) in het
# natieve blok; >= T -> #467e4b (ringlijn/naaf), anders #72d779 (licht). Alleen groene r3-pixels in de zone. Niets getekend.
import sys, numpy as np; from PIL import Image
T=float(sys.argv[1]) if len(sys.argv)>1 else 0.45
a=np.asarray(Image.open('natief.png').convert('RGB')).astype(int); L=a@[0.3,0.59,0.11]
s,X0,Y0,oy,XC,k=[float(v) for v in open('r1.meta').read().split()]
r3=np.asarray(Image.open('../sprite_r3/sprite.png')).astype(int)
ZX,ZY=(83,109),(124,149)          # natieve wielzone (r5)
def frac(j,i):
    xs=X0+(i+(np.arange(8)+0.5)/8)/s; ys=Y0+(j-oy+(np.arange(8)+0.5)/8)/s
    p=[(int(y),int(x)) for y in ys for x in xs]
    g=[q for q in p if a[q][1]>a[q][0]+20]                      # alleen groene modelpixels
    if not g: return None
    return np.mean([L[q]<150 for q in g])
def build(T):
    o=r3.copy(); n=0
    for j in range(64):
        for i in range(64):
            nx=X0+(i+0.5)/s; ny=Y0+(j-oy+0.5)/s
            if not (ZX[0]<=nx<ZX[1] and ZY[0]<=ny<ZY[1]) or r3[j,i] not in (3,4,5): continue
            f=frac(j,i)
            if f is None: continue
            v=5 if f>=T else 3
            if v!=o[j,i]: o[j,i]=v; n+=1
    return o,n
if __name__=='__main__':
    o,n=build(T); print('T',T,'gewijzigd',n)
    ch={0:'.',1:'O',3:'+',4:'o',5:'#',6:'N'}
    for y in range(44,58): print(y,''.join(ch.get(v,'w') for v in o[y,16:36]))
    np.save(f'wiel_T{T}.npy',o)
