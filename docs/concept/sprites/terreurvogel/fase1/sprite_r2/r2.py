# Ronde 2: vorm van r1 + oog D bevroren; alleen tinten (paletten), 2 restpixels, snavelvarianten a/b/c.
import numpy as np, colorsys; from PIL import Image
BASIS=np.array(Image.open('../sprite_r1/oog_D.png'))      # r1 met Jordi's oog D
P=BASIS.copy()
# restpixels (vlekjes <3 px die geen lijn/selout/oog zijn) -> meerderheid van de buren
REP={(31,29):10,(33,49):10}
for (x,y),v in REP.items(): P[y,x]=v
# facetranden (b, c): lichte rand = index 8 (snavel facet), schaduwlijn eronder = snavel donker (2); op modelhelderheidsgrenzen in de snavel
FACET={(15,28):8,(16,28):8,(16,29):2,(17,29):2,(17,30):8,(18,30):8,(15,32):8,(15,33):8,(15,34):2}
PF=P.copy()
for (x,y),v in FACET.items(): PF[y,x]=v
Z=(16,16,16); T=(255,255,255)
OOG=[(248,248,240),(236,200,64)]
BRUIN={'M':[(78,48,44),(122,84,62),(166,126,92)],'sA':[(52,52,70),(86,84,96),(132,124,120)],'sD':[(102,42,42),(156,74,52),(204,124,80)]}
CREME=[(210,180,136),(246,236,206)]
POTEN={'M':[(120,56,40),(186,96,60),(240,152,96)],'sA':[(104,76,60),(160,126,92),(222,188,140)],'sD':[(104,76,60),(160,126,92),(222,188,140)]}
SNAVEL={'a':[(66,62,52),(118,110,86),(200,190,150),None],          # oker steen, mat
        'b':[(66,62,52),(118,110,86),(200,190,150),(164,154,118)],  # a + facetranden
        'c':[(44,48,60),(84,90,104),(224,216,190),(140,146,156)]}  # VOORSTEL Claude: vuursteen (blauwzwarte kern, krijtwitte cortex) + facetten
def pal(sch,sn):
    s=SNAVEL[sn]; b=BRUIN[sch]; p=POTEN[sch]
    return [T,Z,s[0],s[1],s[2],b[0],b[1],b[2],s[3] or (128,128,128),CREME[0],CREME[1],p[0],p[1],p[2],OOG[0],OOG[1]]
def opslaan(S,pad,pal):
    im=Image.fromarray(S.astype('uint8'),'P'); fl=[]
    for c in pal: fl+=list(c)
    im.putpalette(fl+[0]*(768-len(fl))); im.save(pad,transparency=0)
if __name__=='__main__':
    for sch in BRUIN:
        for sn in SNAVEL:
            opslaan(P if sn=='a' else PF,'kuiken_r2_%s_%s.png'%(sch,sn),pal(sch,sn))
    # bewijs: vorm bevroren
    R1=np.array(Image.open('../sprite_r1/kuiken_r1.png'))
    print('alpha-diff t.o.v. r1:',int(((P>0)!=(R1>0)).sum()),'/',int(((PF>0)!=(R1>0)).sum()))
    d=[(x,y,int(BASIS[y,x]),int(PF[y,x])) for y,x in zip(*np.where(PF!=BASIS))]
    print('indexwijzigingen t.o.v. r1+oog D (b/c):',d)
    snavelbox=lambda x,y: 10<=x<=23 and 26<=y<=41
    print('buiten snavel:',[t for t in d if not snavelbox(t[0],t[1])])
    # helderheidsstappen
    def L(c): return sum(c)/3
    def hs(c):
        h,l,s=colorsys.rgb_to_hls(*[v/255 for v in c]); return '%d/%.2f'%(h*360,s)
    oud=[(60,60,57),(104,100,94),(222,212,188)],[(60,50,47),(90,75,67),(132,113,95)],[(200,182,150),(239,229,204)],[(92,66,52),(150,104,80),(214,136,100)]
    for nm,r in zip(('snavel r1','bruin r1','creme r1','poten r1'),oud): print(nm,[int(L(c)) for c in r],[hs(c) for c in r])
    for nm,r in [('snavel a/b',SNAVEL['b']),('snavel c',SNAVEL['c'])]+[('bruin '+k,v) for k,v in BRUIN.items()]+[('creme',CREME)]+[('poten '+k,v) for k,v in POTEN.items()]+[('oog',OOG)]:
        print(nm,[int(L(c)) for c in r],[hs(c) for c in r])
