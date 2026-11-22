# Close-up: sprite (12x) naast het model (zelfde uitsnede, 12x) met rastercoördinaten in spritepixels
import sys,numpy as np; from PIL import Image,ImageDraw
oy,ox=np.load('plaats.npy'); Z=np.load('zones_nat.npy'); ys,xs=np.nonzero(Z!='.')
H,W=np.load('zone_t.npy').shape; s=(ys.max()+1-ys.min())/H
bx=(xs.min()+xs.max()+1)/2-W*s/2; by=ys.min()
N=Image.open('natief.png').convert('RGB')
def crop(x0,y0,w,h,K=12,fn=None,src='../palpaca.png'):
    M=N.crop((int(round(bx+x0*s)),int(round(by+y0*s)),int(round(bx+(x0+w)*s)),int(round(by+(y0+h)*s)))).resize((w*K,h*K),Image.LANCZOS)
    S=Image.open(src).convert('RGBA').crop((ox+x0,oy+y0,ox+x0+w,oy+y0+h)); b=Image.new('RGBA',S.size,(200,220,255,255)); b.alpha_composite(S); S=b.convert('RGB').resize((w*K,h*K),0)
    v=Image.new('RGB',(w*K*2+8,h*K),(255,255,255)); v.paste(S,(0,0)); v.paste(M,(w*K+8,0)); d=ImageDraw.Draw(v)
    for i in range(w):
        for j in range(h):
            pass
    for i in range(0,w): 
        if (x0+i)%5==0: d.line([(i*K,0),(i*K,h*K)],fill=(0,0,255)); d.text((i*K+1,1),str(x0+i),fill=(0,0,255)); d.line([(w*K+8+i*K,0),(w*K+8+i*K,h*K)],fill=(0,0,255))
    for j in range(0,h):
        if (y0+j)%5==0: d.line([(0,j*K),(w*K,j*K)],fill=(0,0,255)); d.text((1,j*K+1),str(y0+j),fill=(0,0,255)); d.line([(w*K+8,j*K),(2*w*K+8,j*K)],fill=(0,0,255))
    return v
if __name__=='__main__':
    x0,y0,w,h=map(int,sys.argv[1:5]); crop(x0,y0,w,h,int(sys.argv[6]) if len(sys.argv)>6 else 12).save(sys.argv[5])
