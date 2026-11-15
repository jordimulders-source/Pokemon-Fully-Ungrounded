# v7-kandidaten. Linkeroog = gespiegeld rechteroog (v6), kolommen geschrapt, pupil verschoven.
# Mond = Haunters eigen mondpixels, wang- en kinomtrek (Haunter-lijf) geschrapt, linkerdeel verkort, verplaatst.
from gezicht import *
import haunter_mond as HM
def verplaats_pupil(g,rij,van,naar):
    g=[list(r) for r in g]
    for j in (rij,rij+1):
        p=g[j][van]; g[j][van]=g[j][naar]; g[j][naar]=p
    return g
def oog(schrap,pupil_naar,rijschrap=()):
    g=schrap_kol(spiegel(RECHTEROOG),schrap)
    pv=[i for i,v in enumerate(g[5]) if v==1 and i<len(g[5])-2][0]
    if pupil_naar is not None: g=verplaats_pupil(g,5,pv,pupil_naar)
    if rijschrap: g=schrap_rij(g,rijschrap)
    return g
# Haunter-mond (x15-34, y38-45). Lijf-specifiek en dus weg: wangomtrek (15,38),(15,39),(16,39),
# kinomtrek (20,45) en Haunters linker kaaklijn (19,44).
WEG=[(15,38),(15,39),(16,39),(20,45),(19,44)]
def mond(kolschrap_x,rijschrap_y=(),tong=10):
    g=HM.kern(tong)
    for x,y in WEG: g[y-HM.Y0][x-HM.X0]=None
    ks=[x-HM.X0 for x in kolschrap_x]+[0,1]      # x15-16 zijn na het schrappen leeg
    rs=[y-HM.Y0 for y in rijschrap_y]
    g=schrap_kol(g,ks); g=schrap_rij(g,rs)
    # lege kolommen rechts weg
    while all(r[-1] is None for r in g): g=[r[:-1] for r in g]
    return g
OGEN={
 'A':dict(schrap=[3,5,8,10],pupil_naar=4),             # 12->8 kolommen
 'B':dict(schrap=[2,4,6,8,10],pupil_naar=3),           # 12->7: ook de buitenste witkolom weg (punt smaller)
 'C':dict(schrap=[3,5,8,10],pupil_naar=4,rijschrap=(2,)),  # 12->8 en één rij uit de punt: minder steil
}
MONDEN={
 'M1':dict(kol=[18,20],rechts=35,boven=31),            # wangomtrek weg, 2 kolommen uit het verre deel (x18 = hoektand-kolom, x20); 4 links, 1 lager dan v6
 'M2':dict(kol=[18,20],rij=[42],rechts=35,boven=32),   # idem + openingsrij y42 weg (onderste helft van de bol draait weg): 4 links, 2 lager
}
KANDIDATEN={   # naam: (oog, mond, tongkleur)  5 = tong in donkerroze (Haunters tweekleurige mond), 10 = alles donkerrood (zoals v6)
 'A':('A','M1',5),
 'C':('C','M2',5),
 'C_donker':('C','M2',10),
}
def bouw(ok,mk,tong=10,oogplek=(23,28)):
    a=basis()
    o=OGEN[ok]; g=oog(o['schrap'],o['pupil_naar'],o.get('rijschrap',()))
    w=len(g[0]); witrij=5-len([r for r in o.get('rijschrap',()) if r<5])
    plak(a,g,oogplek[0]-(w-1),oogplek[1]-witrij)
    m=MONDEN[mk]; mg=mond(m['kol'],m.get('rij',()),tong)
    plak(a,mg,m['rechts']-(len(mg[0])-1),m['boven'])
    # opruimen: losse bolpixel (1 px eigen tint, 8-buren) op een VRIJGEKOMEN plek -> meest voorkomende boltint
    # van zijn buren (herkleuren, niets getekend). Tanden (bolpixels binnen de mond) blijven.
    nieuw=np.zeros((64,64),bool)
    for (gg,x0,y0) in ((g,oogplek[0]-(w-1),oogplek[1]-witrij),(mg,m['rechts']-(len(mg[0])-1),m['boven'])):
        for j,r in enumerate(gg):
            for i,v in enumerate(r):
                if v is not None: nieuw[y0+j,x0+i]=True
    global OPGERUIMD; OPGERUIMD=[]
    b=a.copy()
    for y in range(64):
        for x in range(64):
            if F[y,x] and not nieuw[y,x] and a[y,x] in (6,7,8,9):
                nb=[a[yy,xx] for yy in range(y-1,y+2) for xx in range(x-1,x+2) if (yy,xx)!=(y,x)]
                if a[y,x] not in nb:
                    bol=[n for n in nb if n in (6,7,8,9)]
                    if bol:
                        b[y,x]=max(set(bol),key=bol.count); OPGERUIMD.append((x,y,int(a[y,x]),int(b[y,x])))
    return b
if __name__=='__main__':
    for k in OGEN: print('oog',k); print(toon(oog(OGEN[k]['schrap'],OGEN[k]['pupil_naar'],OGEN[k].get('rijschrap',()))))
    for k in MONDEN: print('mond',k); print(toon(mond(MONDEN[k]['kol'],MONDEN[k].get('rij',()))))
    import glob,os
    for f in glob.glob(D+'/kandidaat_*.png'): os.remove(f)
    for n,(o,m,t) in KANDIDATEN.items(): bewaar(bouw(o,m,t),D+'/kandidaat_%s.png'%n); print(n,'opgeruimd',OPGERUIMD)
