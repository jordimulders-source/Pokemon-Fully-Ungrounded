# Gedeeld: schaal, overlap, palet, opslaan.
import numpy as np; from PIL import Image
U0,U1,V0,V1=75,160,23,104      # natieve figuur x75-159, y23-103 (85x81)
def schaal(breed):
    if breed==43: return 0.5,10,22,41
    s=breed/(U1-U0); h=int(round((V1-V0)*s))
    X0=(64-breed)//2; Y0=63-h   # onderaan, onderste rij 62
    return s,X0,Y0,h
def overlap(X,Y,s,X0,Y0):
    u0=U0+(X-X0)/s; u1=U0+(X+1-X0)/s; v0=V0+(Y-Y0)/s; v1=V0+(Y+1-Y0)/s
    out=[]
    for v in range(int(np.floor(v0)),int(np.ceil(v1))):
        hv=min(v+1,v1)-max(v,v0)
        if hv<=0: continue
        for u in range(int(np.floor(u0)),int(np.ceil(u1))):
            hu=min(u+1,u1)-max(u,u0)
            if hu>0: out.append((u,v,hu*hv*s*s))
    return out
PAL=[(152,208,160),(20,16,18),
     (111,59,33),(156,90,59),(188,113,78),(213,137,101),   # terracotta: lijn, donker, midden*, licht (r1 hoed/kop/poten)
     (88,68,46),(120,108,77),(161,132,92),(223,195,127),   # kraag r1: donker, midden, licht, hooglicht
     (179,155,90),(228,199,123),                           # snavel r1
     (255,255,255),(228,180,156),                          # Lotad-oog: wit; oogrand = Lotads lichtblauw-verhouding op terra licht (r2)
     (105,81,57)]                                           # pootonderkant r1 (tweede tint)
NAAM={1:'zwart',2:'terra lijn',3:'terra donker',4:'terra midden',5:'terra licht',6:'bruin donker',7:'kraag midden',8:'kraag licht',9:'kraag hooglicht',10:'snavel midden',11:'snavel licht',12:'wit',13:'oogrand (licht terra)',14:'poot onder 2'}
def opslaan(o,pad):
    im=Image.fromarray(o.astype('uint8'),'P'); p=[]
    for c in PAL: p+=list(c)
    p+=[0]*(768-len(p)); im.putpalette(p); im.save(pad,transparency=0)
def rgb(o,bg=None):
    a=np.array([PAL[k] for k in o.ravel()]).reshape(o.shape+(3,)).astype('uint8')
    if bg is not None: a[o==0]=bg
    return a
