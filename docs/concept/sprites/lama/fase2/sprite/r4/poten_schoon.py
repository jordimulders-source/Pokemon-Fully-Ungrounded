# r4b: poten van r4 rustig maken (Jordi: "de poten zijn nog veel te blurry" · "de vorm is goed").
# Silhouet blijft exact; alleen vachttonen in de poten (rij 47-63): per rij per pootsegment licht | basis | schaduw.
from PIL import Image; import numpy as np
im=Image.open('r4/lama.png'); a=np.array(im); O=a.copy()
GLOVE={8,9,10,11,15}; VACHT={2,3,4,5,6,7}
NEAR=(6,5,4); FAR=(4,3,2); DONKER=(3,2,2)
for y in range(48,64):
    x=0
    while x<64:
        if a[y,x] in VACHT:
            s=x
            while x<64 and a[y,x] in VACHT: x+=1
            seg=list(range(s,x)); vals=[a[y,i] for i in seg]
            vals=[3 if v==7 else v for v in vals]
            m=np.mean(vals); ramp=NEAR if m>=4.3 else (FAR if m>=2.6 else DONKER)
            n=len(seg)
            for k,i in enumerate(seg):
                if n==1: c=ramp[1]
                elif k==0: c=ramp[0]
                elif k==n-1: c=ramp[2]
                else: c=ramp[1]
                O[y,i]=c
            # buitenlijn waar het segment aan transparant grenst: links zachte lijn 2, rechts donker 1
            if s>0 and a[y,s-1]==0 and n>=3: O[y,s]=2
            if x<64 and a[y,x]==0 and n>=3: O[y,x-1]=1
        else: x+=1
# hoefnageltjes (7) in de handschoenen laten staan
for y in range(55,64):
    for x in range(0,30):
        if a[y,x]==7: O[y,x]=7
# los irisgrijs in de achterbuik
for y in range(48,52):
    for x in range(30,60):
        if O[y,x]==8: O[y,x]=3
out=Image.fromarray(O,'P'); out.putpalette(im.getpalette()); out.save('r4/lama_b.png',transparency=0)
assert ((np.array(out)>0)==(a>0)).all()
print('veranderd',(O!=a).sum())
