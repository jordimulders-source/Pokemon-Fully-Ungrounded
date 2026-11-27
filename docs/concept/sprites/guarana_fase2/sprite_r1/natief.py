# Guarana fase 2, r1 stap 1: natief raster van Gemini r10 terughalen en de plakcompositie (plak/dubbel.py) op DAT raster opnieuw bouwen.
# Pitch gemeten (kamscore randsterkte, zie NOTITIES): cel = 5,12 px (1024/200), randen op 4,1 + k*5,12 (x en y); halve-cel-score 0,19 -> raster is echt.
# (10,24 en 15,36 scoren ook hoog omdat ze veelvouden van 5,12 zijn; op 4x zoom zijn de blokjes ±5 px.)
# dubbel.py-offsets [(45,40),(-45,45),(-45,40)] px -> afgerond op hele cellen: (9,8),(-9,9),(-9,8) cellen = (46,1,41,0),(-46,1,46,1),(-46,1,41,0) px.
import numpy as np; from PIL import Image
P=5.12; F=4.1
a=np.asarray(Image.open('gemini/r10.png').convert('RGB')).astype(int)
n=int((1024-F)//P)
cs=F+0.5+P/2+np.arange(n)*P
N=np.zeros((n,n,3),'uint8')
for j,y in enumerate(cs):
    for i,x in enumerate(cs):
        y0,y1=int(y-1),int(y+2); x0,x1=int(x-1),int(x+2)
        N[j,i]=np.median(a[y0:y1,x0:x1].reshape(-1,3),axis=0)
Image.fromarray(N).save('sprite_r1/natief_r10.png')
# --- compositie (logica van plak/dubbel.py, nu per natieve cel) ---
A=N.astype(int); r,g,b=A[...,0],A[...,1],A[...,2]
green=(g>r+10); light=(A.min(2)>200)
def cel(v): return int(round((v-F-0.5-P/2)/P))
boxes=[(120,430,320,700),(380,280,570,540),(695,425,890,690)]
offs=[(9,8),(-9,9),(-9,8)]
def fruitmask(box):
    x0,y0,x1,y1=[cel(v) for v in box]
    L=light[y0:y1,x0:x1].copy(); H,W=L.shape; bg=np.zeros_like(L)
    st=[(y,x) for y in range(H) for x in (0,W-1)]+[(y,x) for x in range(W) for y in (0,H-1)]
    while st:
        y,x=st.pop()
        if 0<=y<H and 0<=x<W and L[y,x] and not bg[y,x]: bg[y,x]=True; st+=[(y+1,x),(y-1,x),(y,x+1),(y,x-1)]
    m=np.zeros(light.shape,bool); m[y0:y1,x0:x1]=~bg&~green[y0:y1,x0:x1]; return m
def label8(m):
    lab=np.zeros(m.shape,int); k=0
    for y,x in zip(*np.where(m)):
        if lab[y,x]: continue
        k+=1; st=[(y,x)]; lab[y,x]=k
        while st:
            cy,cx=st.pop()
            for dy in (-1,0,1):
                for dx in (-1,0,1):
                    yy,xx=cy+dy,cx+dx
                    if 0<=yy<m.shape[0] and 0<=xx<m.shape[1] and m[yy,xx] and not lab[yy,xx]: lab[yy,xx]=k; st.append((yy,xx))
    return lab,k
out=N.copy(); BRON=np.zeros((n,n),int)  # 0 = r10 zelf, 1..3 = geplakte kopie van tros k
for k,(box,(dx,dy)) in enumerate(zip(boxes,offs),1):
    m=fruitmask(box)
    # alleen de samenhangende hoofdmassa van de tros kopieren (8-buren, >=20 cellen): losse snippers/plakrestjes niet
    lab,nl=label8(m); sz=np.bincount(lab.ravel()); keep=(lab>0)&(sz[lab]>=20)
    ys,xs=np.where(keep); Y2,X2=ys+dy,xs+dx; ok=(Y2>=0)&(Y2<n)&(X2>=0)&(X2<n)
    out[Y2[ok],X2[ok]]=N[ys[ok],xs[ok]]; BRON[Y2[ok],X2[ok]]=k
    out[m]=N[m]; BRON[m]=0          # origineel weer erop (zoals dubbel.py)
Image.fromarray(out).save('sprite_r1/natief_model.png')
fg=out.min(2)<215; yy,xx=np.where(fg); print('natief',n,'bbox x',xx.min(),xx.max(),'y',yy.min(),yy.max())
Image.fromarray(out).resize((n*5,n*5),Image.NEAREST).save('sprite_r1/natief_model_5x.png')
