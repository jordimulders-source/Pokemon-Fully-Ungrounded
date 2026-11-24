# r5_naar_sprite.py: tuinbroekvorm uit Gemini r5 (crème + zak) per spritepixel geteld (oppervlakteaandeel), gepast op de romp van r10_k8:
# r5 bovenrand borststuk y480 -> sprite 32 (onder de vachtbolletjes), kruis y785 -> 55; linker lijfrand x317 -> 18.5, hand x603 -> 43 (alleen verhoudingen, niet de pose)
import numpy as np
from PIL import Image
from scipy import ndimage
a=np.asarray(Image.open('gemini/r5.png').convert('RGB')).astype(int)
R,G,B=a[...,0],a[...,1],a[...,2]; L=a@[0.299,0.587,0.114]
cr=(L>200)&(R-B<80)&(R-B>20); cr[:370]=False
lab,n=ndimage.label(cr); sz=ndimage.sum(cr,lab,range(1,n+1)); m=lab==(int(np.argmax(sz))+1)
f=ndimage.binary_fill_holes(m); hole=f&~m; hl,hn=ndimage.label(hole); hs=ndimage.sum(hole,hl,range(1,hn+1)); zak=hl==(int(np.argmax(hs))+1)
sy=(55-32)/(785-480); sx=(43-18.5)/(603-317)
def frac(mask):
    out=np.zeros((64,64))
    ys,xs=np.where(mask)
    X=18.5+(xs-317)*sx; Y=32+(ys-480)*sy
    cnt=np.zeros((64,64)); np.add.at(cnt,(np.floor(Y).astype(int).clip(0,63),np.floor(X).astype(int).clip(0,63)),1)
    return cnt/(1/sx*1/sy)
CF=frac(f); ZF=frac(zak)
np.save('sprite_r6/creme_frac.npy',CF); np.save('sprite_r6/zak_frac.npy',ZF)
if __name__=='__main__':
    print('   '+''.join(str(i%10) for i in range(14,50)))
    for y in range(24,58): print('%2d '%y+''.join('Z' if ZF[y,x]>=.5 else ('o' if CF[y,x]>=.5 else ('.' if CF[y,x]>=.2 else ' ')) for x in range(14,50)))
