# Kale reductie: natief model (200x199, pitch 5,12) -> 64x64.
# 1) natieve pixels kwantiseren naar 15 modelkleuren (gemeten per zone op het natieve model, k-means per zone)
# 2) per spritepixel (blok van 12 modelpx = 2,34 natieve px) stemmen de natieve pixels met hun overlap-oppervlak;
#    dekking < 0,45 -> transparant; omlijning (index 1/2) wint als hij >= 0,28 van het blok dekt (les ijskomeet: donker wint).
# Standaard: oppervlak-middeling + kwantiseren (les Hauntflare); met 'stem' meerderheid per blok.
# Met argument 'deglitter' worden eerst de glitterspikkels uit het natieve model gehaald (afwijking 1 van Jordi).
import sys, json, numpy as np; from PIL import Image
PAL=[[0,255,0],[45,18,28],[112,56,43],[222,160,115],[240,208,162],[250,234,196],
     [173,38,92],[236,86,158],[246,130,170],[219,52,135],
     [150,29,49],[225,58,73],[250,128,128],[250,222,105],[205,150,55],[255,240,165]]
P=np.array(PAL[1:],float)
# zone pijl (natief y>=125): geen kopkleuren (3,4,5), wel lichtgeel 15 (gemeten streeptop [255,238,162]); elders geen 15
n=np.asarray(Image.open('natief.png').convert('RGB')).astype(float)
nw=(765-n.sum(2))>60
# achtergrond = bijna-wit dat met de rand verbonden is (de lichte kop is geen achtergrond)
wit=n.sum(2)>=735; bg=np.zeros_like(wit); Hn,Wn=wit.shape
st=[(y,x) for y in range(Hn) for x in (0,Wn-1)]+[(y,x) for x in range(Wn) for y in (0,Hn-1)]
while st:
    y,x=st.pop()
    if not(0<=y<Hn and 0<=x<Wn) or bg[y,x] or not wit[y,x]: continue
    bg[y,x]=1; st+=[(y+1,x),(y-1,x),(y,x+1),(y,x-1)]
# ingesloten gaten (lussen): zuiver wit (som>=750) in componenten van >= 20 natieve px is ook achtergrond
zw=(n.sum(2)>=750)&~bg; seen=np.zeros_like(zw)
for y0 in range(Hn):
    for x0 in range(Wn):
        if not zw[y0,x0] or seen[y0,x0]: continue
        st=[(y0,x0)]; comp=[]; seen[y0,x0]=1
        while st:
            y,x=st.pop(); comp.append((y,x))
            for q in ((y+1,x),(y-1,x),(y,x+1),(y,x-1)):
                if 0<=q[0]<Hn and 0<=q[1]<Wn and zw[q] and not seen[q]: seen[q]=1; st.append(q)
        if len(comp)>=20:
            for p in comp: bg[p]=1
nw=~bg
lum=n@[0.299,0.587,0.114]
DG='deglitter' in sys.argv
MODE='stem' if 'stem' in sys.argv else ('fam' if 'fam' in sys.argv else 'gem')
FAMS={'kop':[3,4,5],'roze':[7,8,9],'rood':[10,11,12],'geel':[13,14,15]}
if DG:
    # glitter = geisoleerde natieve pixel die >= 28 lichter is dan de mediaan van zijn 3x3-buren (hooguit 1 even lichte buur) (alleen binnen het dier,
    # en niet in de losse twinkelsterretjes buiten het lijf: alleen waar >= 6 van de 8 buren ook dier zijn)
    m=n.copy(); H,W=lum.shape; cnt=0
    for y in range(1,H-1):
        for x in range(1,W-1):
            if not nw[y,x]: continue
            nb=[(y+dy,x+dx) for dy in (-1,0,1) for dx in (-1,0,1) if (dy or dx)]
            inb=[p for p in nb if nw[p]]
            if len(inb)<6: continue
            med=np.median([lum[p] for p in inb])
            gelijk=sum(1 for p in inb if lum[p]>=lum[y,x]-20)   # buren die net zo licht zijn
            if lum[y,x]-med>=28 and gelijk<=1:                  # alleen geisoleerde lichte stip (1-2 natieve px), geen streep
                m[y,x]=np.median([n[p] for p in inb],axis=0); cnt+=1
    print('glitter weg (natieve px):',cnt); n=m
D=((n[...,None,:]-P[None,None])**2).sum(3)
D[:125,:,14]=1e9; D[125:,:,2:5]=1e9
D[:,92:,2:5]=1e9                       # kopkleuren (goud/creme) alleen in kop en hals (natief x<92)
Y,X=np.mgrid[:D.shape[0],:D.shape[1]]; D[~((X<72)&(Y>=45)),1]=1e9   # bruin alleen in de kop (rond het gezicht); elders donkere lijn = 1
q=D.argmin(2)+1
q[~nw]=0
Image.fromarray(q.astype('uint8')).save('natief_q%s.png'%('_dg' if DG else ''))
S=12/5.12; OX=(106-4.25)/5.12-0.5; OY=(120-4.25)/5.12-0.5   # spritepixel (0,0) begint op modelpx (106,120)
out=np.zeros((64,64),'uint8'); WT=np.zeros((64,64,16)); GEM=np.zeros((64,64,3))
for j in range(64):
    for i in range(64):
        y0=OY+j*S; x0=OX+i*S; w=np.zeros(16); acc=np.zeros(3); accw=1e-9; accs=np.zeros((16,3)); accws=np.zeros(16)
        for yy in range(int(np.floor(y0)),int(np.ceil(y0+S))):
            for xx in range(int(np.floor(x0)),int(np.ceil(x0+S))):
                if not(0<=yy<q.shape[0] and 0<=xx<q.shape[1]): continue
                oy=max(0,min(yy+1,y0+S)-max(yy,y0)); ox=max(0,min(xx+1,x0+S)-max(xx,x0))
                w[q[yy,xx]]+=oy*ox
                if q[yy,xx]>2: acc+=n[yy,xx]*oy*ox; accw+=oy*ox
                accs[q[yy,xx]]+=n[yy,xx]*oy*ox; accws[q[yy,xx]]+=oy*ox
        w/=S*S
        WT[j,i]=w; GEM[j,i]=acc/accw
        if 1-w[0]<0.45: continue
        if w[1]+w[2]>=0.28: out[j,i]=1 if w[1]>=w[2] else 2
        elif MODE=='stem': w[0]=0; out[j,i]=w.argmax()
        elif MODE=='fam':  # kleurgroep per blok bij meerderheid, dan middeling binnen die groep
            fw={f:sum(w[k] for k in ks) for f,ks in FAMS.items()}
            f=max(fw,key=fw.get)
            if w[6]>fw[f]: out[j,i]=6
            else:
                ks=FAMS[f]+[6]; c=sum(accs[k] for k in ks)/max(1e-9,sum(accws[k] for k in ks))
                out[j,i]=ks[int(((P[np.array(ks)-1]-c)**2).sum(1).argmin())]
        else:  # oppervlak-middeling van de echte (ontglitterde) modelkleuren, dan dichtstbijzijnde modelkleur
            c=acc/accw; dd=((P-c)**2).sum(1)
            if j<int((125*5.12+5.25-120)/12): dd[14]=1e9
            else: dd[2:5]=1e9
            if (OX+i*S+S/2)>=92: dd[2:5]=1e9
            out[j,i]=dd.argmin()+1
np.save('blok_w%s.npy'%('_dg' if DG else ''),WT); np.save('blok_gem%s.npy'%('_dg' if DG else ''),GEM)   # r2: per spritepixel de modelaandelen per kleur + gemiddelde vlakkleur
fn=('kaal_dg' if DG else 'kaal')+{'stem':'_stem','fam':'_fam','gem':''}[MODE]+'.png'
im=Image.fromarray(out,'P'); im.putpalette(sum(PAL,[])+[0]*(768-48)); im.save(fn,transparency=0)
json.dump(PAL,open('palet.json','w'))
print(fn,[(k,int((out==k).sum())) for k in range(16)])
