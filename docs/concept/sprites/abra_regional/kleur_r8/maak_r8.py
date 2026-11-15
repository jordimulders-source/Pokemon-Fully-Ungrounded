# maak_r8.py (vanuit kleur_r8/): ../kleur_r7/abra_r7_A.png -> abra_r8.png (rand + curven die het model draagt)
#                                                       -> abra_r8_curve.png (r8 + lichte curven waar het model recht is; Jordi beslist)
# Jordi (15 nov): "de zwarte belijning aan de buitenkant is meer dan bij andere gen 3 sprites of niet? Daarnaast zijn er nog steeds
#  best veel rechte lijnen, rechterkant van de staart, rechterkant van het lichaam, beide armen, linkerkant hoofd."
# Bevroren: ogen, pose, kleuren (A), vlekjes. Alleen pixels uit de lijsten hieronder veranderen (elk met oude waarde = assert).
# spritepixel (x,y) = natief modelblok (2x-1, 2y-14) van ../kleur_r1/natief.png
import sys; import numpy as np; from PIL import Image
sys.dont_write_bytecode=True; sys.path.insert(0,'.'); from randmeting import rand
NM='.KL123TsmbhI'; V={c:i for i,c in enumerate(NM)}
src=Image.open('../kleur_r7/abra_r7_A.png'); a0=np.array(src).astype(int)

# ---- 1. BUITENRAND: K -> L naar het recept van Abra/Kadabra (lichtkant en rechterkant van grote huidvlakken = donkere huidtint,
#         zwart blijft onder (bodem/grond), tegen de donkere platen/kaak, in het gat arm/lijf, in de oorkerf en op scherpe punten)
RAND=[
 # A staart bovenkant rechts (loopt van het lijf weg, naar boven/rechts gekeerd; Abra/Kadabra: staart boven E)
 ((50,47),'K','L','A staart boven-rechts'),((51,48),'K','L','A'),((52,49),'K','L','A'),((53,50),'K','L','A'),((54,51),'K','L','A'),
 # G staart rechterkant (Kadabra: rechterkant huid = E, zwart pas waar hij naar de bodem draait)
 ((55,53),'K','L','G staart rechts'),((55,54),'K','L','G'),((55,55),'K','L','G'),((54,57),'K','L','G laatste rechts-pixel vóór de bocht naar de bodem'),
 # F kop rechterkant onder de kerf tot de plaat (Kadabra kop rechts E/F; oorpunt + kerf blijven K = snede)
 ((34,19),'K','L','F kop rechts'),((35,20),'K','L','F'),((35,21),'K','L','F'),((35,22),'K','L','F'),((35,23),'K','L','F'),((36,24),'K','L','F'),
 # H rechterkant onderlijf (huid s, tussen plaat en staartaanzet)
 ((43,43),'K','L','H onderlijf rechts'),((43,44),'K','L','H'),
 # L binnenrand staartlus (naar linksboven gekeerd; loopt door in L/T eronder)
 ((50,52),'K','L','L binnenrand staartlus'),((51,53),'K','L','L'),
 # B linkervoet: hele linker-/onderlinkerkant licht (Abra: voeten E links, F rechts/onder); bodem (16-17,57) en rechterkant blijven K
 ((8,50),'K','L','B teen links (Abra: linker teenpunt E)'),((9,51),'K','L','B'),((10,51),'K','L','B'),((11,51),'K','L','B'),((12,51),'K','L','B'),
 ((13,52),'K','L','B'),((14,53),'K','L','B'),((15,56),'K','L','B scheen links, sluit aan op L (15,54-55)'),
 ((19,52),'K','L','B hoek scheen/hand: anders losse K tussen L (18,53),(20,51),(21,52)'),((18,53),'K','L','B rechterkant scheen (zijkant huid = lijntint; onderkant (16-18,56-57) blijft K)'),((18,54),'K','L','B'),((18,55),'K','L','B'),
 # C linkerhand: vinger linkerkant + onderkant handpalm boven het gaatje (licht vlak b erboven)
 ((21,53),'K','L','C vinger links, sluit aan op L (21,52)'),
 ((24,51),'K','L','C vinger rechterkant (Abra: handen bijna helemaal E; zwart alleen de onderkant (22-25,54))'),((25,52),'K','L','C'),((25,53),'K','L','C'),((25,50),'K','L','C palm-onderkant, b erboven'),((26,50),'K','L','C'),
 ((28,50),'K','L','C vingerrand: K tussen L (27,50) en L (29,50)'),((27,51),'K','L','C vingertop: anders losse K tussen L (26,50)/(28,50)'),
 # E staartpunt onderkant (dunne lichte punt; links = lichtkant)
 ((22,61),'K','L','E staartpunt'),((23,61),'K','L','E'),((24,61),'K','L','E'),((25,61),'K','L','E'),
]
# ---- 2a. CURVEN DIE HET MODEL DRAAGT (op natieve resolutie gemeten; silhouet verandert, elke pixel gemeld)
CURVE=[
 # staart rechts: model (natief) 1,1,1 diagonaal -> 1,5 rij half, 4 rijen vol, 1,5 half -> sprite 1,2,3,2,1 (was 1,1,5,1,1)
 ((55,52),'K','.','staart rechts: rij 52 naar x54 (model rij 51-52: 55,0 = halve pixel)'),
 ((54,52),'s','L','staart rechts: nieuwe buitenrand'),
 ((55,56),'K','.','staart rechts: rij 56 naar x54 (model rij 56-57: 55,5/55,0)'),
 ((54,56),'s','L','staart rechts: nieuwe buitenrand'),
 ((53,56),'b','s','staart: schaduwband langs de rechterrand loopt door (rij 55 s s, rij 57 s)'),
 # linkerarm buitenkant: 24,24 | 23 | 22,22 | 21 | 20 (2,1,2,1,1 heen en weer) -> 24,24 | 23,23 | 22 | 21 | 20 (2,2,1,1,1);
 # model natief 24,0 / 23,5 / 22,5 / 22,0 / 21,3 / 19,8: versnelt naar de hand toe (bol), rij 41 = 22,5 (halve pixel)
 ((22,41),'L','.','linkerarm buiten: rij 41 naar x23'),
 ((23,41),'s','L','linkerarm: nieuwe buitenrand (lijntint lichtkant)'),
]
# ---- 2b. VARIANT: lichte curve waar het model op natieve resolutie recht is (afwijking <= 1 px van het model)
VARIANT=[
 # kop links: model 20,0-20,5 (jitter) rij 25-33 = recht; sprite 2,9,1,1 -> 3,6,3,1 (holte onder het oor, bolle wang naar de kin)
 ((19,25),'.','L','kop links: rij 25 naar x19 (model 19,94)'),((20,25),'L','b','kop links: was rand, nu huid zoals (21,25)'),
 ((20,32),'K','.','kop links: kaak 1 px in (model 19,94)'),((21,32),'1','K','kaakrand'),
 ((20,33),'K','.','kop links: kaak 1 px in'),((21,33),'1','K','kaakrand'),
 # lijf rechts: model 44,5 (rij 36-39) en 43,5 (rij 40-45) = twee rechte stukken; sprite 2,1,2,6,6 -> 2,1,3,4,6 (oplopend)
 ((45,34),'.','K','lijf rechts: rij 34 naar x45 (model 44,5/44,0)'),((44,34),'K','1','plaat loopt door tot de nieuwe rand'),
 ((44,39),'K','.','lijf rechts: rij 39 naar x43 (model 44,5/44,0)'),
 # linkerarm binnenkant (rand van het gat): model 27,0 / 26,5 / 26,0 = vrijwel recht; boven een pixel breder (schouder)
 ((27,39),'.','K','linkerarm binnen: rij 39 naar x27 (model 27,0)'),((26,39),'K','s','arm: was rand, nu huid'),
 # rechterarm (binnenlijnen x38 en x41, rij 36-40, model recht): linkerlijn knikt een rij eerder naar de elleboog: 3,3,2,1,1 i.p.v. 5,1,2,1,1
 ((37,39),'1','K','rechterarm linkerlijn'),((37,40),'1','K','rechterarm linkerlijn'),((38,39),'K','b','arm verbreedt naar de elleboog'),((38,40),'K','b','idem'),
]
def pas(arr,edits):
    for (x,y),old,new,why in edits:
        assert NM[arr[y,x]]==old, ((x,y),NM[arr[y,x]],old)
        arr[y,x]=V[new]
PAL=[(255,0,255),(14,13,22),(60,54,80),(49,48,61),(71,68,87),(89,88,103),(104,98,126),(130,126,150),(161,158,174),(180,179,191),(209,206,219),(92,86,114)]
def bewaar(arr,naam):
    im=Image.fromarray(arr.astype('uint8'),'P'); flat=[c for p in PAL for c in p]; im.putpalette(flat+[0]*(768-len(flat))); im.save(naam,transparency=0)
a=a0.copy(); pas(a,RAND); pas(a,CURVE); bewaar(a,'abra_r8.png')
b=a.copy(); pas(b,VARIANT); bewaar(b,'abra_r8_curve.png')
# ---- controle
OGEN=[(22,28),(23,29),(24,30),(24,31),(30,27),(29,28),(28,29),(28,30)]
for arr,nm in ((a,'r8'),(b,'r8_curve')):
    assert all(arr[y,x]==a0[y,x] for x,y in OGEN), 'ogen gewijzigd'
    sil=np.argwhere((arr>0)!=(a0>0)); r=rand(arr)
    kl=sorted(NM[v] for v in np.unique(arr[arr>0]))
    print(f'{nm}: {len(np.argwhere(arr!=a0))} px gewijzigd, silhouet {len(sil)} px {[(int(x),int(y)) for y,x in sil]}, kleuren {kl}')
    print(f'   rand {r.sum()} px, zwart {100*(arr[r]==1).mean():.1f} %  (r7 A: {100*(a0[rand(a0)]==1).mean():.1f} %)')
