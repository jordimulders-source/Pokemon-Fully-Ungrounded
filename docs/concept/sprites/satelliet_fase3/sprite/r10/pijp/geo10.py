# r10: paneelgeometrie consistent in grootte, met perspectief (Jordi over r9: "de panelen mogen nog iets consistenter qua
#   grootte, houd rekening met de hoek he").
# - Alle vier de liggende panelen (PA, PC, PD, PE) zijn in de ruimte even groot (4 vakken); in beeld alleen verkleind met een
#   perspectieffactor f. f uit de modelgeometrie: achter/voor langs de hoofdas (voorste bol -> achterbol) ~0,75 over de hele
#   arm (bollen 14,8/20,6 = 0,72; kragen ~0,78), dus tussen het voorste en het achterste paneelpaar ~0,89; links/rechts langs de
#   dwarsarm (linker/rechter oogbol 10,75/11,98) 0,90. PE (voor, rechts) = 1.
# - Maat bij f=1 = PE (nabij): lengte 50,0, breedte 30,8 modelpx (r9). Richtingen per paneel blijven die van het model.
# - Het binnen-einde (vast aan de romp/staafje) blijft staan, het lengteverschil zit aan het buiteneinde; alleen PD houdt zijn
#   buiteneinde (anders buiten het modelkader). Het kader (schaal) blijft dat van r8/r9 (kaal.py).
# - Mast PB/PF: zelfde maat (lengte 47 = PB, 3 vakken), breedte 24,2 = dezelfde breedte:lengte als de liggende panelen in de
#   ruimte (kijkhoek uit de bovenring van de knoopbol: ellips 17x6 -> elevatie ~21 graden; verticaal x0,94, dwarsas x0,78).
import numpy as np
GEO0={'PA':((86,24),(137,40),(71,36)),'PC':((176,58),(227,72),(163,70)),'PD':((20,86),(61,101),(3,96)),
      'PF':((123,100),(123,136),(133,104)),'PE':((102,117),(149,134),(88,132)),'PB':((123,3),(123,50),(132,8))}
F={'PE':1.0,'PD':0.90,'PC':0.89,'PA':0.80}
L0,W0=50.0,30.8
MAAT={k:(L0*f,W0*f) for k,f in F.items()}
MAAT['PB']=(47.0,24.2); MAAT['PF']=(36.0,24.2)
# PF: in de ruimte gelijk aan PB (vak 47/3 = 15,7), maar zoals in het model (Jordi: "zal in de sprite onder een ander paneel
#   vallen, maar je ziet hem net nog afkappen") afgekapt op 36: de rest valt onder PE. Volle lengte 47 zou rechts naast PE
#   tot y 156 uitsteken. Vakgrenzen PF daarom op 15,7 en 31,3 van boven (u = 0,435 / 0,870), dezelfde vakmaat als PB.
LIJNU={'PB':[1/3,2/3],'PF':[15.667/36,31.333/36]}
AU={'PA':1.0,'PD':0.0,'PC':0.0,'PE':0.0,'PB':0.0,'PF':0.0}    # binnen-einde (staafje aan de romp) blijft staan; PD: buiteneinde (anders buiten het kader; +1,3 px valt achter de bol)
AV={'PA':0.5,'PE':0.5,'PD':1.0,'PC':0.0,'PB':0.0,'PF':0.0}    # breedte-anker zoals r9
def nieuw(k):
    T,R,L=map(lambda p:np.array(p,float),GEO0[k]); u=R-T; v=L-T
    su=MAAT[k][0]/np.linalg.norm(u); sv=MAAT[k][1]/np.linalg.norm(v)
    T2=T+AU[k]*(1-su)*u+AV[k]*(1-sv)*v
    return (tuple(T2),tuple(T2+su*u),tuple(T2+sv*v))
GEO10={k:nieuw(k) for k in GEO0}
if __name__=='__main__':
    for k in GEO0:
        T,R,L=map(np.array,GEO0[k]); print(k,'r13b L %.1f W %.1f'%(np.linalg.norm(R-T),np.linalg.norm(L-T)),'r10 L %.1f W %.1f'%MAAT[k],np.round(np.array(GEO10[k]),1).tolist())
