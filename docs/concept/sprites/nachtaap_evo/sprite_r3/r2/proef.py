import sys; sys.path.insert(0,'r1'); from pal import *
def kopmasker(x,y):
    if not (x<=24 and 33<=y<=55): return False
    if y==33 or (y==34 and x>=19) or (y==35 and x>=21) or (y==36 and x>=22): return False
    return True
def licht(g,cx,cy,r5,r3,log=None):
    for y in range(27,50):
        for x in range(15,48):
            if kopmasker(x,y): continue
            if x>=44 and y<37: continue            # staart
            if 24<=x<=31 and y>=43: continue        # nabije voorpoot
            if x>=36 and y>=44: continue            # achterpoot (apart)
            v=g[y,x]
            if v not in (4,5): continue
            d=((x-cx)**2+((y-cy)*1.3)**2)**.5
            n=5 if d<r5 else (3 if d>r3 else 4)
            if n!=v:
                if log is not None: log.append(('licht/volume lijf',x,y,int(v),n))
                g[y,x]=n
if __name__=='__main__':
    g=np.load('r2/r2.npy').copy(); cx,cy,r5,r3=map(float,sys.argv[1:5]); licht(g,cx,cy,r5,r3)
    o=np.array(Image.open('referenties/oude_sprite.png')).astype(int)
    ims=[naar_img(x[20:63,0:63],8,(255,255,255)).convert('RGB') for x in (g,o)]
    V=Image.new('RGB',(ims[0].width*2+20,ims[0].height),(200,200,200))
    for i,im in enumerate(ims): V.paste(im,(i*(im.width+20),0))
    V.save('/tmp/claude-0/proef.png')
    for y in range(27,50): print('%2d  '%y+''.join(S[v] for v in g[y,14:50]))
