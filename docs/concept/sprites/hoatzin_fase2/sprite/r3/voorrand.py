# Lichte voorrand van de voorste vleugel op het natieve model: grootste verbonden lichte band (L>=T) in het armgebied
import numpy as np, os; from PIL import Image
N=np.asarray(Image.open('natief.png').convert('RGB')).astype(float); L=N.mean(2); Z=np.load('zones_nat.npy'); H,W=L.shape
T=float(os.environ.get('VT',125)); yy,xx=np.mgrid[:H,:W]
m=np.isin(Z,['M','W'])&(L>=T)&(xx>=80)&(xx<=125)&(yy>=60)&(yy<=160)
lab=np.zeros((H,W),int); n=0; sz=[0]
for y0,x0 in zip(*np.where(m)):
    if lab[y0,x0]: continue
    n+=1; st=[(y0,x0)]; lab[y0,x0]=n; c=0
    while st:
        a,b=st.pop(); c+=1
        for d in (-1,0,1):
            for e in (-1,0,1):
                p,q=a+d,b+e
                if 0<=p<H and 0<=q<W and m[p,q] and not lab[p,q]: lab[p,q]=n; st.append((p,q))
    sz.append(c)
k=int(np.argmax(sz)); band=lab==k
np.save('voorrand_nat.npy',band)
im=N.copy(); im[band]=(0,255,0)
Image.fromarray(im.astype('uint8')).crop((40,50,140,180)).resize((500,650),Image.NEAREST).save('voorrand.png')
print('band px',band.sum(),'ys',np.where(band)[0].min(),np.where(band)[0].max())
