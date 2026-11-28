# Batch 01 rugsprites: natief raster -> frontpalet -> 64x64. python3 bouw.py (vanuit batch_01/af)
# nat/nat_<slug>.png komt uit gereedschap/natief.py (pitch 13-19). Cholucha overgeslagen (Jordi keurt Gemini-rug af).
import numpy as np; from PIL import Image; from scipy import ndimage
SP='../../../../'
SOORT={'llamauler':'lama/fase2/af/lama.png','bandolingo':'olinguito_v2/af/olinguito.png',
 'coathief':'coathief/af/coathief.png','vigiloot':'wasbeer/af/wasbeer.png',
 'nocticue':'nachtaap/af/nachtaap.png','moonkey':'nachtaap_evo/af/nachtaap_evo.png'}
def rgb(a,pal,bg=(255,255,255)):
    p=list(pal); p[0:3]=list(bg); im=Image.fromarray(a.astype('uint8'),'P'); im.putpalette(p); return im.convert('RGB')
vel=[]
for s,f in SOORT.items():
    fr=Image.open(SP+f); pal=fr.getpalette()[:48]; front=np.array(fr)[:64]
    used=sorted(set(np.unique(front))-{0})
    a=np.array(Image.open('nat/nat_%s.png'%s).convert('RGB')).astype(int)
    bg=a.min(2)>215
    # lichtgrijze vloer/strepen (vrijwel kleurloos en licht) = transparant
    bg|=(a.max(2)-a.min(2)<12)&(a.mean(2)>170)
    P=np.array(pal).reshape(-1,3)[used]
    idx=np.array(used)[((a[:,:,None,:]-P[None,None])**2).sum(3).argmin(2)]; idx[bg]=0
    log=[]
    if s=='llamauler':  # poten zweven onder een witte strook: alles onder de strook weg
        rows=(idx>0).sum(1); ys=np.where(rows>0)[0]
        gap=[y for y in range(ys.min(),ys.max()) if rows[y]==0 and rows[y-1]>0]
        cut=gap[0] if gap else None
        if cut is None:  # strook niet helemaal leeg: kies de rij met de minste pixels in de onderste helft
            lo=ys.min()+(ys.max()-ys.min())//2; cut=lo+int(np.argmin(rows[lo:ys.max()]))
        log.append('afgesneden vanaf rij %d (%d px weg)'%(cut,(idx[cut:]>0).sum())); idx[cut:]=0
    # dunne vloerlijn onderaan: onderste rijen die breed en maar 1 rij hoog uitsteken -> weg als losse component
    lab,n=ndimage.label(idx>0,structure=np.ones((3,3)))
    sz=ndimage.sum(np.ones_like(lab),lab,range(1,n+1)); big=np.argmax(sz)+1
    ruis=0
    for k in range(1,n+1):
        if k!=big and sz[k-1]<6: idx[lab==k]=0; ruis+=int(sz[k-1])
    # losse ruispixels binnen de vorm (alleen als de tint dicht bij de buren ligt): pixel waarvan geen enkele 4-buur dezelfde index heeft en 3+ buren gelijk anders zijn
    los=0; o=idx.copy()
    for y in range(1,idx.shape[0]-1):
        for x in range(1,idx.shape[1]-1):
            v=o[y,x]
            if v==0: continue
            nb=[o[y-1,x],o[y+1,x],o[y,x-1],o[y,x+1]]
            if v not in nb and 0 not in nb:
                m=max(set(nb),key=nb.count)
                L=lambda i: sum(pal[3*i:3*i+3])/3
                if nb.count(m)>=3 and abs(L(v)-L(m))<45: idx[y,x]=m; los+=1  # alleen tintruis, geen oog/glans
    log.append('losse componenten weg %d px, ruispixels %d'%(ruis,los))
    ys,xs=np.where(idx>0); dy=63-ys.max(); dx=0
    if xs.min()+dx<0 or xs.max()+dx>63: dx=(64-(xs.max()-xs.min()+1))//2-xs.min()
    out=np.zeros((64,64),int)
    for y,x in zip(ys,xs): out[y+dy,x+dx]=idx[y,x]
    nk=len(set(np.unique(out))-{0})
    log.append('x %d-%d y %d-%d, %d kleuren'%(xs.min()+dx,xs.max()+dx,ys.min()+dy,63,nk))
    im=Image.fromarray(out.astype('uint8'),'P'); im.putpalette(pal); im.save('%s_rug.png'%s,transparency=0)
    rgb(out,pal).resize((512,512),Image.NEAREST).save('%s_rug_8x.png'%s)
    print(s,'|','; '.join(log))
    vel.append((rgb(front,pal),rgb(out,pal)))
C=64*4; V=Image.new('RGB',(2*C+24,len(vel)*(C+8)),(255,255,255))
for i,(a,b) in enumerate(vel):
    V.paste(a.resize((C,C),Image.NEAREST),(0,i*(C+8))); V.paste(b.resize((C,C),Image.NEAREST),(C+24,i*(C+8)))
V.save('vel.png')
