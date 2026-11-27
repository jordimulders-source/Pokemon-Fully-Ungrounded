# Ronde 3: r2 (vorm, oog D) bevroren; gezicht krijgt een eigen kleurgroep (indexen 8 en 14). Alleen indextoewijzing + paletten.
import numpy as np, colorsys; from PIL import Image
R2=np.array(Image.open('../sprite_r2/kuiken_r2_M_a.png'))     # r2 zonder facetten
ML=np.load('../sprite_r1/ml.npy')                              # modelhelderheid per spritepixel (kale reductie r1)
P=R2.copy()
P[28,29]=10        # oogglans: index 14 -> crème licht (10), vrijwel gelijke kleur; maakt 14 vrij
# gezichtszone uit het model: kop voor de lichtere/grijsbruine modelzone; kuif (y<=20) en nek/achterhoofd (donker in het model) blijven lijf
FACE=np.zeros((64,64),bool)
for y in range(64):
    for x in range(64):
        if R2[y,x] in (5,6,7) and ((21<=y<=39 and x<=33) or (y<=38 and x<=36 and ML[y,x]>=100)):
            FACE[y,x]=True
P[FACE&(R2==7)]=14     # gezicht licht
P[FACE&(R2==6)]=8      # gezicht midden ; 5 blijft gedeelde donkere tint/lijn
Z=(16,16,16); T=(255,255,255)
OOG=(236,200,64)
BRUIN={'M':[(78,48,44),(122,84,62),(166,126,92)],'sA':[(52,52,70),(86,84,96),(132,124,120)],'sD':[(92,36,38),(138,58,48),(180,96,70)]}
CREME=[(210,180,136),(246,236,206)]
POTEN={'M':[(120,56,40),(186,96,60),(240,152,96)],'sA':[(104,76,60),(160,126,92),(222,188,140)],'sD':[(104,76,60),(160,126,92),(222,188,140)]}
GEZICHT={'i':[(146,124,104),(190,166,134)],     # warm lichtbruin/grijsbeige zoals het model, laag verzadigd
         'ii':[(160,108,86),(206,140,98)]}      # roest-tan zoals de kop van fase 2 r4 (160,108,86)
SNAVEL={'a':[(66,62,52),(118,110,86),(200,190,150)],'c':[(44,48,60),(84,90,104),(224,216,190)]}   # c = VOORSTEL vuursteen (zonder facetten)
def pal(sch,gz,sn):
    s=SNAVEL[sn]; b=BRUIN[sch]; p=POTEN[sch]; g=GEZICHT[gz]
    return [T,Z,s[0],s[1],s[2],b[0],b[1],b[2],g[0],CREME[0],CREME[1],p[0],p[1],p[2],g[1],OOG]
def opslaan(S,pad,pal):
    im=Image.fromarray(S.astype('uint8'),'P'); fl=[]
    for c in pal: fl+=list(c)
    im.putpalette(fl+[0]*(768-len(fl))); im.save(pad,transparency=0)
if __name__=='__main__':
    for sch in BRUIN:
        for gz in GEZICHT:
            for sn in SNAVEL: opslaan(P,'kuiken_r3_%s_%s_%s.png'%(sch,gz,sn),pal(sch,gz,sn))
    np.save('face.npy',FACE)
    print('alpha-diff t.o.v. r2:',int(((P>0)!=(R2>0)).sum()),' gezichtspixels:',int(FACE.sum()),'(licht %d, midden %d, donker gedeeld %d)'%((FACE&(R2==7)).sum(),(FACE&(R2==6)).sum(),(FACE&(R2==5)).sum()))
    ch=[(x,y,int(R2[y,x]),int(P[y,x])) for y,x in zip(*np.where(P!=R2))]
    print('indexwijzigingen die geen gezicht-hertoewijzing zijn:',[c for c in ch if not FACE[c[1],c[0]]])
    print('gebruikte indices',sorted(set(P.ravel())-{0}))
    L=lambda c:int(sum(c)/3)
    def hs(c): h,l,s=colorsys.rgb_to_hls(*[v/255 for v in c]); return '%d/%.2f'%(h*360,s)
    for k,v in list(GEZICHT.items())+[('lijf '+a,b) for a,b in BRUIN.items()]: print(k,[L(c) for c in v],[hs(c) for c in v])
