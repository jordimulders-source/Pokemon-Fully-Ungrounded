# Ronde 1 v16: technisch opschonen van brok_<VAR>.npy (model v16 verkleind + rechterkant rond + brokkels uit r5).
# Niets getekend: alleen (1) buitenlijn 1 px: selout (2) aan de lichtkant linksboven, zwart (1) aan de schaduwkant,
# per stuk één scheiding op de normaalrichting; (2) steentint-vlekjes < 3 px -> buurtint; (3) losse zwarte pixels
# binnenin (< 3 px, raken geen rand/oog/lijn) -> buurtint.
import sys, numpy as np; from PIL import Image, ImageDraw; from scipy import ndimage; import tool
VAR=sys.argv[1] if len(sys.argv)>1 else 'A'; OUT=sys.argv[2] if len(sys.argv)>2 else '.'
o=np.load(f'brok_{VAR}.npy').copy(); kaal=np.load('groot_model.npy'); rondz=np.load('groot_zone.npy'); g=np.load('groot.npy')
J,I=np.mgrid[0:64,0:64]
STEEN=[3,4,5,7]; RK={3:0,4:1,5:2,7:3}
# 0. uitsteeksels van 1 px die door het knippen ontstonden (niet in het model): weg
spk=0
for _ in range(2):
    f=o>0; nb=sum(np.roll(f,s,a) for s in (1,-1) for a in (0,1))
    m=f&(nb<=1)&(o!=g); spk+=int(m.sum()); o[m]=0
fig=o>0
# oogmasker (binnen + ring) en neus
ring=(o==1)&(I>=24)&(I<=40)&(J>=20)&(J<=38)
eyein=ndimage.binary_fill_holes(ring)&~ring
eye=ndimage.binary_dilation(eyein,iterations=2)&fig
neus=(I<=24)&(J>=23)&(J<=34)&fig&~eye
# 1. buitenlijn
# lokale normaal van de rand (gladgestreken silhouet), zodat ook de wanden van de happen goed belicht zijn
rim=fig&~ndimage.binary_erosion(fig,structure=[[0,1,0],[1,1,1],[0,1,0]])
sm=ndimage.gaussian_filter(fig.astype(float),1.6); gy,gx=np.gradient(sm)
lijn=0
for y,x in zip(*np.where(rim)):
    nx,ny=-gx[y,x],-gy[y,x]; L=np.hypot(nx,ny)+1e-6
    v=2 if (-nx-ny)/(np.sqrt(2)*L)>0.30 else 1
    if o[y,x]!=v: o[y,x]=v; lijn+=1
# 2. steentint-vlekjes < 3 px
vlek=0
for _ in range(3):
  for v in STEEN:
    L,nl=ndimage.label(o==v)
    for c in range(1,nl+1):
        m=L==c
        if m.sum()>=3 or (m&(eye|neus)).any(): continue
        rr=ndimage.binary_dilation(m,structure=np.ones((3,3)))&~m
        st=[x for x in o[rr] if x in STEEN and x!=v]
        if not st: continue
        kv=kaal[m]; t=int(np.bincount(kv).argmax()); t=t if t in RK else v
        best=min(set(st),key=lambda x:(abs(RK[x]-RK[t]),-st.count(x)))
        o[m]=best; vlek+=int(m.sum())
# 3. losse zwarte pixels binnenin
rim=fig&~ndimage.binary_erosion(fig,structure=[[0,1,0],[1,1,1],[0,1,0]])
inner=(o==1)&~rim&~eye
L,nl=ndimage.label(inner,structure=np.ones((3,3))); los=0
for c in range(1,nl+1):
    m=L==c
    touch=(ndimage.binary_dilation(m,structure=np.ones((3,3)))&~m&(rim|eye)&(o<=2)).any()
    if m.sum()<3 and not touch:
        rr=ndimage.binary_dilation(m,structure=np.ones((3,3)))&~m; st=[x for x in o[rr] if x in STEEN]
        if st: o[m]=max(set(st),key=st.count); los+=int(m.sum())
np.save(f'{OUT}/idx.npy',o); tool.save(o,f'{OUT}/sprite.png'); tool.save(o,f'{OUT}/sprite_8x.png',8)
# ---- vel
M=Image.open('../../referenties/model_v16.png').convert('RGB')
W=512*2+16*3+ 12*20*2 +16
vel=Image.new('RGB',(W,560),(230,230,230)); d=ImageDraw.Draw(vel)
vel.paste(tool.rgba(o,sc=8),(16,32)); d.text((16,12),f'v16 r2{VAR} 8x',fill=(0,0,0))
vel.paste(M.resize((512,512),Image.LANCZOS),(544,32)); d.text((544,12),'model v16 (verkleind)',fill=(0,0,0))
# close-up gezicht: oog + neus, 12x, naast model op dezelfde uitsnede
bx=(2,20,42,38)
cs=tool.rgba(o[bx[1]:bx[3],bx[0]:bx[2]],sc=12)
# zelfde uitsnede in het model via de natieve coördinaten (rek: kolommen 14,25 dubbel; offset -4,-2)
vel2=Image.new('RGB',(cs.width*2+48,cs.height+40),(230,230,230)); d2=ImageDraw.Draw(vel2)
vel2.paste(cs,(8,30)); d2.text((8,10),'gezicht sprite 12x',fill=(0,0,0))
# model-uitsnede: groot-coördinaten -> natief: x_n ~ x+4-(#dubbele kolommen links), simpel: natief kader 5..41, 22..39
mc=M.crop((16*5,16*21,16*41,16*38)).resize((cs.width,int(cs.width*17/36)),Image.NEAREST)
vel2.paste(mc,(cs.width+40,30)); d2.text((cs.width+40,10),'model (zelfde uitsnede)',fill=(0,0,0))
for x0,bg in ((1072,(232,232,232)),(1072+80,(40,40,48))):
    pass
vel_full=Image.new('RGB',(max(W,vel2.width+16),560+vel2.height+100),(230,230,230))
vel_full.paste(vel,(0,0)); vel_full.paste(vel2,(16,560))
y1=560+vel2.height+10
for k,bgc in enumerate([(240,240,240),(48,48,56),(120,160,120)]):
    vel_full.paste(tool.rgba(o,bgc=bgc),(16+k*80,y1))
vel_full.paste(tool.rgba(o,bgc=(240,240,240),sc=2),(16+3*80,y1-10))
vel_full.save(f'{OUT}/vel.png')
# ---- rapport
Z=np.full((64,64),'lijf',dtype=object)
lg,ng=ndimage.label(kaal>0); sg=np.bincount(lg.ravel()); sg[0]=0
Z[(lg!=np.argmax(sg))&(lg>0)]='puin'
Z[rondz]='rechterkant (rond)'
br=(np.load(f'brok_{VAR}.npy')!=g); Z[br]='brokkels (r5)'
Z[neus|((kaal>0)&(I<=24)&(J>=23)&(J<=34))]='neus'; Z[eye]='oog'
dif=(o!=kaal)
rap=[f'Ronde 2{VAR} (model v16); t.o.v. r1: randkleur met lokale normaal (wanden van de happen), brokkels.py zet de rand niet meer zwart']
rap.append('Pipeline: natief.py (Gemini-raster 16 px, fase 15, 1-op-1) -> kwant.py (r4-palet; oog binnen de ring met irispalet)')
rap.append('  -> rond.py (rechterkant rond) -> rek.py (4 kolommen + 4 rijen verdubbeld zodat de groep het vak vult) -> brokkels.py -> bouw.py')
rap.append('Pixels afwijkend van de kale reductie (natief raster, gekwantiseerd, zelfde vergroting) per zone:')
for z in ['oog','neus','lijf','rechterkant (rond)','brokkels (r5)','puin']:
    m=(Z==z)&((kaal>0)|(o>0)); rap.append(f'  {z:20s}: {int((dif&m).sum()):4d} van {int(m.sum())}')
rap.append(f'  totaal: {int(dif.sum())}')
rap.append(f'Uitsteeksels van het knippen weg: {spk} px'); rap.append(f'Opschonen: buitenlijn {lijn} px (selout linksboven / zwart schaduwkant), steenvlekjes {vlek} px, losse zwarte pixels {los} px')
ys,xs=np.where(o>0); rap.append(f'bbox x{xs.min()}-{xs.max()} y{ys.min()}-{ys.max()}; kleuren gebruikt: {sorted(set(o.ravel())-{0})}')
open(f'{OUT}/wijzigingen.txt','w').write('\n'.join(rap)+'\n'+open(f'brokkels_{VAR}.txt').read())
print('\n'.join(rap))
