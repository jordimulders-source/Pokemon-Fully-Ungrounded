from PIL import Image
import numpy as np
src='gemini/ronde8_hand_klauwen5.png'
im=Image.open(src).convert('RGB'); a=np.asarray(im).copy(); a0=a.astype(int)
r5=np.asarray(Image.open('gemini/ronde5.png').convert('RGB')).astype(int)
d=np.abs(a0-r5).sum(2)>60; ys,xs=np.where(d); print('diff r5-r8 bbox',xs.min(),xs.max(),ys.min(),ys.max(), 'buiten hand:',int(d[:, :760].sum()))
P=7.3; I0,J0=108,38
def cls(c):
    L=c.mean()
    return '.' if L>238 else ('o' if L<50 else ('k' if L<95 and c[2]-c[0]<12 else ('d' if L<125 else ('c' if L<158 else ('b' if L<185 else ('a' if L<225 else 'w'))))))
def cell(i,j):
    x0,y0=int(round(i*P)),int(round(j*P)); return np.median(a0[y0+2:y0+6,x0+2:x0+6].reshape(-1,3),0)
NEW={46:'....o.o.....obbcccoo............',
47:'...oo.co...obbcccco.............',
48:'...odddoo..obcccco..............',
49:'...obccdo.odbcccco..............',
50:'...obccco.obbcccco..............',
51:'...obcccdoobcccccdo.............',
52:'...obccccooccccccdo.............',
53:'...obccccoocccccccdo............',
54:'oooobbccccocccccccdo............',
55:'kkkodbccccddccccccccdo..........'}
# kleuren: mediaan per klasse uit de hand zelf
samp={}
for j in range(38,66):
    for i in range(108,140):
        c=cell(i,j); samp.setdefault(cls(c),[]).append(c)
COL={k:tuple(int(v) for v in np.median(np.array(v),0)) for k,v in samp.items()}; COL['.']=(255,255,255); print(COL)
n=0
for j,row in NEW.items():
    for p,ch in enumerate(row):
        i=I0+p
        x0,y0,x1,y1=int(round(i*P)),int(round(j*P)),int(round((i+1)*P)),int(round((j+1)*P))
        if p>=len(row.rstrip('.')): a[y0:y1,x0:x1]=(255,255,255)
        elif cls(cell(i,j))!=ch or p>=16: a[y0:y1,x0:x1]=COL[ch]; n+=1
print('cellen gewijzigd',n)
a[int(round(38*P)):int(round(46*P)), int(round(128*P)):]=(255,255,255)
a[int(round(46*P)):int(round(56*P)), int(round(130*P)):]=(255,255,255)
out=Image.fromarray(a); out.save('model/model_hand3_v2.png')
z=out.crop((700,230,1024,520)).resize((648,580),Image.NEAREST); z.save('/tmp/claude-0/-home-user-Pokemon-Fully-Ungrounded/3bd5ae97-6ac2-52a5-8d79-9a6104e8993f/scratchpad/hand/z2.png')
