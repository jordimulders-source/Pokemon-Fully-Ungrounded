# Ronde 1: kale reductie van r3b + manenvarianten A/B/C (lokken uit het model verschoven/verlengd, op modelniveau,
# daarna dezelfde reductie) + groottevariant (rijen in het hoornstuk geschrapt). Uit: r1/*.png, r1/telling.txt
import numpy as np, json
from PIL import Image
from scipy import ndimage as nd
from reduce import fgmask, palet, reduceer, opslaan, buitenlijn
Ld=lambda n:np.asarray(Image.open(n).convert('RGB')).astype(int)
M=Ld('../referenties/model_r3b.png'); C3=Ld('../gemini/r3c/kudu_r3c.png')
fg=fgmask(M); C=palet(M,fg); np.save('model_pal.npy',C)
hb=np.load('haar_r3b.npy'); hc=np.load('haar_r3c.npy')
ys,xs=np.nonzero(fg); y0,y1,x0,x1=ys.min(),ys.max()+1,xs.min(),xs.max()+1
H=64; p=(y1-y0)/H; W=int(np.ceil((x1-x0)/p))
def plak(dst,src,mask,dx,dy,sy=1.0,ankery=370,alleen_fg=True):
    """lok-asset (src[mask]) verschuiven met (dx,dy); sy>1 = verlengen door rijen te herhalen vanaf ankery (bovenkant manen)."""
    out=dst.copy(); hh,ww=mask.shape
    yy,xx=np.nonzero(mask)
    ny=(ankery+(yy-ankery)*sy).astype(int)+dy
    for k in range(int(np.ceil(sy))):   # rijen herhalen: elke bronrij vult de rijen tot de volgende
        t=ny+k; ok=(t<(ankery+(yy+1-ankery)*sy).astype(int)+dy)|(k==0)
        t=t[ok]; x=xx[ok]+dx; s=(yy[ok],xx[ok])
        v=(t>=0)&(t<hh)&(x>=0)&(x<ww)
        if alleen_fg: v&=fg[np.clip(t,0,hh-1),np.clip(x,0,ww-1)]
        out[t[v],x[v]]=src[s[0][v],s[1][v]]
    return out
var={}
var['kaal']=M
# A: r3b-manen als geheel 70 px naar rechts en 30 naar beneden over de schouder gelegd (origineel blijft eronder)
var['A']=plak(M,M,hb,70,30)
# B: r3b-manen 30% verlengd (rijen herhalen vanaf de bovenkant achter de oren) en 40 px naar rechts: lokken vallen lager over de schouder
var['B']=plak(M,M,hb,40,0,sy=1.3)
# C: grotere lokken van r3c (alleen het halsdeel rechts van de keelfranje, x>=380) 90 px naar rechts, 20 naar beneden
hc2=hc.copy(); hc2[:,:380]=False
var['C']=plak(M,C3,hc2,90,20)
for k,v in var.items(): Image.fromarray(v.astype('uint8')).save(f'r1/model_{k}.png')
red={k:reduceer(v,fg,C,y0,x0,p,H,W) for k,v in var.items()}
# groottevariant: reduceer op 72 rijen, schrap 8 rijen uit het hoornstuk (rijen boven de oren) waar de buurrijen het meest op elkaar lijken
H2=72; p2=(y1-y0)/H2; W2=int(np.ceil((x1-x0)/p2))
for k in ['kaal','A']:
    r=reduceer(var[k],fg,C,y0,x0,p2,H2,W2)
    if k=='kaal':
        top=int(260/p2)   # bovenkant oren in het model ±y260 -> rijen 0..top zijn alleen hoorn
        sc=[((r[j-1]>=0)!=(r[j+1]>=0)).sum()+((r[j-1]!=r[j+1])).sum()*0.3 for j in range(2,top-1)]
        cand=sorted(range(2,top-1),key=lambda j:sc[j-2]); weg=[]
        for j in cand:
            if all(abs(j-w)>1 for w in weg): weg.append(j)
            if len(weg)==8: break
        for j in cand:                       # te weinig niet-aangrenzende rijen: vul aan met de volgende beste
            if len(weg)==8: break
            if j not in weg: weg.append(j)
        weg=sorted(weg)
    red['groot_'+k]=np.delete(r,weg,0)
json.dump({'pitch':p,'W':W,'pitch_groot':p2,'W_groot':W2,'geschrapt_rijen_van_72':[int(w) for w in weg]},open('r1/meta.json','w'))
bl={}
for k in list(red):
    opslaan(red[k],C,f'r1/kaalpuur_{k}.png'); red[k],bl[k]=buitenlijn(red[k])   # pure reductie bewaard; daarna buitenlijn dicht
imgs={k:opslaan(v,C,f'r1/kudu_r1_{k}.png') for k,v in red.items()}
# telling per zone t.o.v. de kale reductie
hz=np.zeros((H,W),bool)   # manenzone = cellen die in een variant van kaal verschillen (alleen daar is iets veranderd)
with open('r1/telling.txt','w') as f:
    for k in ['A','B','C']:
        d=red[k]!=red['kaal']; ys_,xs_=np.nonzero(d)
        f.write(f'{k}: {d.sum()} px anders dan kaal, alle in rij {ys_.min()}-{ys_.max()}, kolom {xs_.min()}-{xs_.max()} (manenzone); buiten de manenzone 0\n')
    f.write('buitenlijn dicht (technisch, alle varianten): '+str(bl)+' px\n')
    f.write(f"groot: 8 van 72 rijen in het hoornstuk geschrapt ({weg}); verder kaal\n")
# hoornhoogte
kol=(red['kaal']>=0); 
print(open('r1/telling.txt').read(), 'W',W,'p',p, 'kleuren',len(C)+0)
