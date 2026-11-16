import sys,numpy as np
from PIL import Image
im=Image.open('docs/concept/sprites/gengas/af/gengas.png');a=np.array(im);pal=im.getpalette()
grey=np.isin(a,[11,12,13,14])
# componenten van grijs (8-buren)
lab=np.zeros(a.shape,int);n=0
for y,x in zip(*np.where(grey)):
    if lab[y,x]: continue
    n+=1;st=[(y,x)];lab[y,x]=n
    while st:
        cy,cx=st.pop()
        for dy in(-1,0,1):
            for dx in(-1,0,1):
                yy,xx=cy+dy,cx+dx
                if 0<=yy<64 and 0<=xx<64 and grey[yy,xx] and not lab[yy,xx]: lab[yy,xx]=n;st.append((yy,xx))
# omlijning (1) die aan een maan grenst en niet aan het lijf hoort -> bij de maan
body_col=np.isin(a,[2,3,4,5,6,7,8,9,10,15])
for y,x in zip(*np.where(a==1)):
    nb=[(y+dy,x+dx) for dy in(-1,0,1) for dx in(-1,0,1) if 0<=y+dy<64 and 0<=x+dx<64]
    ml=[lab[p] for p in nb if lab[p]]
    if ml and not any(body_col[p] for p in nb): lab[y,x]=ml[0]
sizes={i:(lab==i).sum() for i in range(1,n+1)}
cent={i:tuple(np.mean(np.where(lab==i),1).round()) for i in sizes}
#print(sizes,cent)
# alleen de vier grote manen (de kleine grijze stukjes zijn tanden)
big=[i for i in sizes if sizes[i]>50]
manen=np.isin(lab,big)
np.save('docs/concept/sprites/gengas/frame2/manen_lab.npy',np.where(manen,lab,0))
lijf=a.copy();lijf[manen]=0
lijf[6:9,35:37]=0  # losse omlijningsrest van de bovenste maan
o=Image.fromarray(lijf,'P');o.putpalette(pal);o.save('docs/concept/sprites/gengas/frame2/lijf_zonder_manen.png')
rgba=o.convert('RGBA');rgba.putdata([(255,255,255,255) if p[:3]==(0,255,255) else p for p in rgba.getdata()])
rgba.convert('RGB').resize((512,512),Image.NEAREST).save('docs/concept/sprites/gengas/frame2/lijf_zonder_manen_8x.png')
