# Sprite ronde 1, stap b: render64 -> palet. Materiaal uit de tint, toon uit de schaduw van het
# model (de render is de toonkaart), omlijning 1 px: selout (donkerste eigen toon) aan de lichtkant
# linksboven, donkerbruin aan de schaduwkant. Handwerk (ogen, mond, details) gaat daarna in handwerk.py.
import numpy as np
from PIL import Image
from scipy import ndimage as nd
R=np.load('render64.npy'); col=R[...,:3]; fig=R[...,3]>0.5
r,g,b=col[...,0],col[...,1],col[...,2]; lum=col.mean(-1)
from kleur_pal import PAL, N, I

mat=np.full((64,64),'',object)
mat[fig&(b-r>30)]='bl'; mat[fig&(r-b>22)&(mat=='')]='br'; mat[fig&(mat=='')]='wi'
mat[fig&(lum<70)]='oog'
# kleine eilandjes van een materiaal (<3 px) opslokken door de buren
for m in ('bl','br','wi'):
    lab,n=nd.label(mat==m)
    for k in range(1,n+1):
        z=lab==k
        if z.sum()<3:
            nb=mat[nd.binary_dilation(z)&~z]; nb=[x for x in nb if x not in ('',m)]
            if nb: mat[z]=max(set(nb),key=nb.count)
out=np.zeros((64,64),int)
for m in ('bl','br','wi'):
    z=mat==m
    if not z.any(): continue
    L=nd.gaussian_filter(np.where(z,lum,0),0.6)/np.maximum(nd.gaussian_filter(z*1.,0.6),1e-6)
    p30,p82=np.percentile(L[z],30),np.percentile(L[z],82)
    t=np.where(L<p30,1,np.where(L>p82,3,2))
    out[z]=[I[f'{m}{k}'] for k in t[z]]
out[mat=='oog']=I['oog']
# omlijning: buitenste rij pixels van de figuur
rand=fig&~nd.binary_erosion(fig)
gy,gx=np.gradient(nd.gaussian_filter(fig*1.,1.5))   # wijst naar binnen
licht=(gx+gy)>0.02   # naar binnen = rechtsonder, dus de rand ligt linksboven: lichtkant
for y,x in zip(*np.nonzero(rand)):
    m=mat[y,x] if mat[y,x] in ('bl','br','wi') else 'br'
    out[y,x]=I[f'{m}0'] if licht[y,x] else I['lijn']
# binnenlijn waar materialen elkaar raken: de donkerste toon aan de kant van het achterste deel
achter={('br','bl'):'bl',('bl','wi'):'wi',('br','wi'):'wi'}
for y in range(64):
    for x in range(64):
        if not fig[y,x] or rand[y,x] or mat[y,x] not in ('bl','br','wi'): continue
        for dy,dx in ((0,1),(1,0),(0,-1),(-1,0)):
            m2=mat[y+dy,x+dx]
            if m2 in ('bl','br','wi') and m2!=mat[y,x]:
                a=achter.get((mat[y,x],m2)) or achter.get((m2,mat[y,x]))
                if a==mat[y,x]: out[y,x]=I[f'{a}0']
np.save('kleur.npy',out)
img=np.array([PAL[N[i]] for i in out.ravel()],np.uint8).reshape(64,64,3)
Image.fromarray(img).save('kleur.png'); Image.fromarray(img).resize((512,512),Image.NEAREST).save('kleur_8x.png')
with open('normal.pal','w') as f:
    f.write('JASC-PAL\n0100\n16\n'+''.join('%d %d %d\n'%c for c in PAL.values())+'0 0 0\n'*(16-len(PAL)))
