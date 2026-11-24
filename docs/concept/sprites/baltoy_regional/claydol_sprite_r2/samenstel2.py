# r2-model: het r1-samengestelde model (claydol_model/model_natief_samengesteld.png) met Jordi's punten (23 nov):
#  - "beide ogen plus neus mogen wat meer naar rechts voor het perspectief": ogen + afwerking + neus als één asset SCHUIF px naar rechts;
#    vrijgekomen pixels links = r5-steen uit kolom 25 van dezelfde rij.
#  - "echt duidelijk te zien dat je een oog hebt uitgewist": facetgrens rij 31-49 vloeiend doorgetrokken (boog door de facetrand van het
#    model boven (rij 26-30) en onder (rij 48-53)); links ervan wangsteen, rechts facetsteen (mediaan van model-steen/facet zelf).
import sys, numpy as np; from PIL import Image
SCHUIF=int(sys.argv[1]) if len(sys.argv)>1 else 2
B='claydol_model/'
M1=np.asarray(Image.open(B+'model_natief_samengesteld.png')).astype(int)
r5=np.asarray(Image.open(B+'natief_r5.png')).astype(int)
H,W=M1.shape[:2]; yy,xx=np.mgrid[0:H,0:W]
rood=lambda a:(a[:,:,0]-a[:,:,1])>40
L=M1.mean(2)
# 1) facet: boog x_b(y) = 68,3 - a*(y-40,5)^2 (a boven 0,0456, onder 0,0915; gemeten op de modelrand rij 27/34 en 48/50/53)
M=M1.copy(); bron=np.full((H,W),'m',dtype='<U2')
wang=np.median(r5[27:31,54:59].reshape(-1,3),axis=0).astype(int)        # wangsteen boven het oog (model)
facet=np.median(r5[36:45,69:72].reshape(-1,3),axis=0).astype(int)       # facetsteen (model)
for y in range(33,50):
    a=0.0456 if y<=40.5 else 0.0915; xb=int(round(68.3-a*(y-40.5)**2))
    xr=min(x for x in range(xb,80) if L[y,x]<40)   # kopomlijning rechts
    for x in range(59 if y>=47 else 61,xr):
        if rood(M1)[y,x]: continue
        if y>=47 and L[y,x]<40: continue
        v=wang if x<xb else facet
        if (M[y,x]!=v).any(): M[y,x]=v; bron[y,x]='w' if x<xb else 'f'
# 2) ogen + afwerking + neus als asset naar rechts
ogen=[(32.0,40.5,6.0,6.5),(50.5,41.5,6.5,6.5)]
A=np.zeros((H,W),bool)
for cx,cy,rx,ry in ogen: A|=np.sqrt(((xx-cx)/rx)**2+((yy-cy)/ry)**2)<=1.5
A&=(xx>=25)&(xx<=58)&(yy>=33)
A|=(xx>=38)&(xx<=44)&(yy>=33)&(yy<=51)
A&=~rood(M1)
A&=~((L<40)&((xx<=25)|(yy>=51)))          # kopomlijning hoort niet bij de asset
src=M.copy(); N=M.copy()
ys,xs=np.where(A)
for y,x in zip(ys,xs):                     # vrijgekomen plekken: r5-steen van kolom 25 in dezelfde rij (r5 heeft op x26-27 zijn eigen
    N[y,x]=r5[y,25] if L[y,25]>=40 else wang; bron[y,x]='5'   # oogomlijning; die terughalen gaf een dubbele lijn)
R=rood(M1)
for y,x in zip(ys,xs):
    if R[y,x+SCHUIF]: continue             # rode lijn blijft staan
    N[y,x+SCHUIF]=src[y,x]; bron[y,x+SCHUIF]='a'
Image.fromarray(N.astype('uint8')).save('claydol_sprite_r2/model_r2_s%d.png'%SCHUIF)
np.save('claydol_sprite_r2/bron_s%d.npy'%SCHUIF,bron)
print('schuif',SCHUIF,'asset',int(A.sum()),'wang',int((bron=='w').sum()),'facet',int((bron=='f').sum()),'r5-steen links vrij',int((bron=='5').sum()))
