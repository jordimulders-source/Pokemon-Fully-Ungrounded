# diff r2 -> r3 per zone (png-coords) + bevroren zones (moeten 0 zijn)
import numpy as np; from PIL import Image
a=np.array(Image.open('../r2/picaraio.png')).astype(int); b=np.load('r3.npy')
D=a!=b
Z={'1 vleugelpunten x46-63 y2-29':(46,2,63,29),'2 kuif x17-47 y0-10':(17,0,47,10),'3 verre vleugel x8-14 y0-12':(8,0,14,12),
   '4 buik x11-31 y23-44':(11,23,31,44),'5 bliksem x0-8 y29-36':(0,29,8,36),'6 achterhoofd x27-29 y9-20':(27,9,29,20),
   '7 rechterpoot x25-30 y45-52':(25,45,30,52),'8 bliksem->koord x8-12 y47-50':(8,47,12,50)}
F={'oog x19-22 y11-14':(19,11,22,14),'wang x21-24 y15-16':(21,15,24,16),'snavel x9-17 y13-17':(9,13,17,17),
   'staartkoord x9-38 y51-63':(9,51,38,63)}
def n(z): x0,y0,x1,y1=z; return int(D[y0:y1+1,x0:x1+1].sum())
for k,z in Z.items(): print('%-34s %3d'%(k,n(z)))
print('-- bevroren --')
for k,z in F.items(): print('%-34s %3d'%(k,n(z)))
st=((a>=5)&(a<=7)); wing=np.zeros_like(st); wing[2:30,40:64]=True
print('%-34s %3d'%('stippen (creme in vleugel)',int((D&st&wing).sum())))
sel=(a==15); print('%-34s %3d (van %d)'%('selout 15 r2 gewijzigd',int((D&sel).sum()),int(sel.sum())))
print('totaal',int(D.sum()))
ys,xs=np.where(D); 
cov=np.zeros_like(D)
for z in Z.values(): x0,y0,x1,y1=z; cov[y0:y1+1,x0:x1+1]=True
print('buiten de zones:',[(int(x),int(y)) for y,x in zip(*np.where(D&~cov))])
