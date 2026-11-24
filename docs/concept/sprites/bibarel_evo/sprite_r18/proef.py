import numpy as np
from PIL import Image
from scipy import ndimage
ch='.KbcdfSCeLMogWwD'; I={c:i for i,c in enumerate(ch)}
im=Image.open('sprite_r17/sprite.png'); PAL=np.array(im.getpalette()[:48]).reshape(16,3).astype('uint8'); a=np.asarray(im).astype(int); o=a.copy()
mn=np.load('sprite_r18/model_min.npy')
FUR=[I[c] for c in 'fdc']; CR=[I[c] for c in 'CMS']
star=np.isin(a,FUR)&(mn<75); star[:27]=False
lab,n=ndimage.label(star|(a==I['b']),structure=np.ones((3,3)))
for k in range(1,n+1):
    m=lab==k
    if (m&star).sum()>=1 and m.sum()>=3: o[m&star]=I['b']
# crème rand
N4=((1,0),(-1,0),(0,1),(0,-1))
for y in range(64):
    for x in range(64):
        if a[y,x] in CR and any(0<=y+dy<64 and 0<=x+dx<64 and o[y+dy,x+dx] in FUR for dx,dy in N4): o[y,x]=I['D']
np.save('sprite_r18/proef.npy',o)
P=PAL.copy(); P[I['b']]=(76,40,12); P[I['D']]=(144,100,32)
img=Image.fromarray(P[o]); img.putalpha(Image.fromarray(((o>0)*255).astype('uint8')))
bg=Image.new('RGB',(64,64),(152,208,160)); bg.paste(img,(0,0),img); bg.resize((512,512),Image.NEAREST).save('/tmp/claude-0/-home-user-Pokemon-Fully-Ungrounded/7bc2735f-b867-5692-94ea-d6711f144b87/scratchpad/proef.png')
for y in range(24,60): print('%2d '%y+''.join(ch[v] if v==a[yy,xx] else ch[v].lower() if ch[v]!='b' else '#' for xx,v in enumerate(o[y]) for yy in [y])[4:56])
