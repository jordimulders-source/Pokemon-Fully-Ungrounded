# maak_r9.py (vanuit kleur_r9/): ../kleur_r8/abra_r8.png       -> abra_r9.png
#                                ../kleur_r8/abra_r8_curve.png -> abra_r9_curve.png
# Jordi over r8: "nu zitten er rechts op de schouder een paar overbodige pixels, laat een agent daarnaar kijken tezamen met de laatste eindkeuring".
# Bevroren: ogen, pose, kleuren (A, modeltonen), vlekjes, rand-zwart ±40-45 %. Alleen pixels uit de lijsten hieronder (oude waarde = assert).
# spritepixel (x,y) = natief modelblok (2x-1, 2y-14) van ../kleur_r1/natief.png
import sys; import numpy as np; from PIL import Image
sys.dont_write_bytecode=True; sys.path.insert(0,'.'); from randmeting import rand
NM='.KL123TsmbhI'; V={c:i for i,c in enumerate(NM)}

# ---- 1. SCHOUDER RECHTS (beide versies). Modelrand rechts (natief, in sprite-eenheden): rij 28 44,75 | 29 45,75 | 30 46,25 |
#         31 46,5 | 32 46,25 | 33 45,75 | 34 44,75: een ronde bult van een halve pixel, geen punt.
SCHOUDER=[
 ((46,31),'K','.','spijkertje: 1-px-punt in de schouderbocht (model 46,5 = halve pixel); rand rij 29-33 nu één boog op x45'),
 ((45,31),'1','K','buitenlijn sluit waar de punt weg is (was plaatvulling op de rand)'),
 ((44,33),'L','K','losse lijnkleur-pixel tussen twee evenwijdige zwarte lijnen (plaatnaad (44,32)(43,33) en buitenlijn (45,32)(45,33)); model zwart (K1/KK): plaatnaad loopt nu in de buitenlijn'),
 ((44,32),'K','1','anders 2x2-zwartklont (44-45,32-33); plaatvulling 1 tot de buitenlijn (model 1K/KK: plaatnaad, hier één lijn)'),
 ((43,35),'K','1','(43,34) was een ingesloten 1-pixel (4 x K rondom); model 1K/1K = half vulling: donkere lijfstrook x43 loopt nu door tot de plaatnaad'),
]
# ---- 1b. alleen r8_curve: (45,34) was daar extra gezet (r8 LOG: "model 44,5/44,0 -> ~1 px buiten"); met 1. wordt de rand anders x45 rij 29-34 (6 recht)
CURVE_SCHOUDER=[
 ((45,34),'K','.','uitsteeksel onder de schouder (alleen in r8_curve; model rij 34 = 44,75, dus buiten het model)'),
 ((44,34),'1','K','buitenlijn terug naar x44, zoals r8'),
]
# ---- 2. EINDKEURING (KEURING.md): de schouderpunten hierboven zijn MOET 1-3; verder geen MOET, en de MAG-punten zijn bewust niet
#         uitgevoerd (model-trouw of herontwerp; reden per punt in KEURING.md). Lijst blijft leeg.
KEUR=[
]
def pas(arr,edits):
    for (x,y),old,new,why in edits:
        assert NM[arr[y,x]]==old, ((x,y),NM[arr[y,x]],old)
        arr[y,x]=V[new]
PAL=[(255,0,255),(14,13,22),(60,54,80),(49,48,61),(71,68,87),(89,88,103),(104,98,126),(130,126,150),(161,158,174),(180,179,191),(209,206,219),(92,86,114)]
def bewaar(arr,naam):
    im=Image.fromarray(arr.astype('uint8'),'P'); flat=[c for p in PAL for c in p]; im.putpalette(flat+[0]*(768-len(flat))); im.save(naam,transparency=0)
OGEN=[(22,28),(23,29),(24,30),(24,31),(30,27),(29,28),(28,29),(28,30)]
uit={}
for bron,doel,extra in (('../kleur_r8/abra_r8.png','abra_r9.png',[]),('../kleur_r8/abra_r8_curve.png','abra_r9_curve.png',CURVE_SCHOUDER)):
    a0=np.array(Image.open(bron)).astype(int); a=a0.copy()
    pas(a,SCHOUDER); pas(a,extra); pas(a,KEUR); bewaar(a,doel); uit[doel]=a
    assert all(a[y,x]==a0[y,x] for x,y in OGEN), 'ogen gewijzigd'
    sil=np.argwhere((a>0)!=(a0>0)); r=rand(a); r0=rand(a0)
    kl=sorted(NM[v] for v in np.unique(a[a>0]))
    print(f'{doel}: {len(np.argwhere(a!=a0))} px gewijzigd t.o.v. {bron[3:]}, silhouet {len(sil)} px {[(int(x),int(y)) for y,x in sil]}')
    print(f'   kleuren {kl}; figuur {int((a>0).sum())} px; rand {int(r.sum())} px, rand-zwart {100*(a[r]==1).mean():.1f} % (was {100*(a0[r0]==1).mean():.1f} %); zwart totaal {100*(a==1).sum()/(a>0).sum():.1f} % (was {100*(a0==1).sum()/(a0>0).sum():.1f} %)')
d=np.argwhere(uit['abra_r9.png']!=uit['abra_r9_curve.png'])
print('r9 vs r9_curve verschillen op', [(int(x),int(y)) for y,x in d])
