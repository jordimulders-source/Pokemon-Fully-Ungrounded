# r1 Moonkey: kale reductie (kaal.npy) -> technische opschoning -> toegestane afwijkingen (ogen + maan uit de oude sprite)
# -> anim_front.png + normal.pal. Elke pixel die niet uit de kale reductie komt wordt gelogd met zone en reden.
import sys; sys.path.insert(0,'r1'); from pal import *
g=np.load('r1/kaal.npy').copy()
o=np.array(Image.open('referenties/oude_sprite.png')).astype(int)
oud=np.zeros_like(o); oud[1:,0:63]=o[:63,1:]      # oude sprite 1 px links, 1 px omlaag: ogen vallen precies op de oogplek van het model
log=[]
def zet(x,y,v,zone,reden):
    if g[y,x]!=v: log.append((zone,x,y,int(g[y,x]),v,reden)); g[y,x]=v
H=dict(zip('.123456789ABCDEF',range(16)))

# ===== 1) TECHNISCH =====
# staart: wit binnen de spiraal is ingesloten achtergrond van het model -> transparant
for y in range(9,21):
    for x in range(46,62):
        if g[y,x]==8: zet(x,y,0,'staart','ingesloten achtergrond in de krul -> transparant')
# kop links: gat in de buitenlijn van het model (cel (3,42) is wit) -> lijn dicht
zet(3,42,2,'kop L','open rand in het model -> buitenlijn')
# wit binnen de kop staat nu als wit (8) in de kale reductie (floodfill met het lijngat dicht); geen afwijking.
zet(6,53,2,'kin L','modelpixel 4 op de buitenrand (kin) -> buitenlijn 2, sluit aan op (5,52)')

zet(42,34,6,'rug/staartaanzet','losse 5 in het lavendel hooglicht -> 6 (een vlakje i.p.v. 3 tinten op 2 px)')
zet(43,34,6,'rug/staartaanzet','losse 4 tussen 6 en lijn -> 6 (idem)')
zet(46,38,1,'lijf R','2 op de rechterbuitenrand tussen 1-en -> 1 (geen zwart/donkerlila om en om)')
zet(7,57,2,'arm L','3 op de bovenrand -> selout 2 (zoals (8,57))')
zet(19,59,13,'voet midden','losse lavendel pixel (6) in de creme teen -> D zoals (18,59)')
zet(17,61,14,'voet midden','creme hoekpixel zonder lijn (open rand) -> bruin 14 zoals de teenrand (16,60)')

# ===== 2) TOEGESTANE AFWIJKINGEN (bovenlaag): ogen + maan uit de oude sprite =====
# a) Bovenkop y35-42: buitenrand = model (lijn, linkeroor, oor rechts). Maan = wit tot aan de buitenlijn
#    (zoals de oude maan de lijn raakt), rechterrand van de maan zoals in de oude sprite: rand 7, dan paarse band
#    (5/4) en een binnenlijn tegen het verre oor; onderrand (inham 77 boven het voorhoofd) uit de oude sprite.
#    De rechterrand loopt als in de oude sprite schuin van boven naar rechts (rand op x15,17,18,19,19,19,19,19 voor y35-42;
#    oud x15,17,18,19,19 voor y38-42) en dan recht omlaag langs het oog: volgt de grotere kop.
kop={35:(3,'??????22'+'8888'+'7555'+'11'),
     36:(3,'????22'+'8'*8+'7555'+'1'),
     37:(3,'?222'+'8'*11+'7551'),
     38:(3,'?253'+'8'*12+'7553'),
     39:(3,'252'+'8'*13+'7543'),
     40:(3,'25'+'8'*14+'7442'),
     41:(3,'2'+'8'*15+'74424'),
     42:(3,'2'+'8'*9+'77'+'8888'+'74423')}
for y,(x0,s) in kop.items():
    for i,c in enumerate(s):
        if c!='?': zet(x0+i,y,H[c],'maan (bovenkop)','oude maan aangepast aan de kop van r3')
# b) y43-52: rij voor rij uit de oude sprite (verschoven -1,+1): voorhoofd, wenkbrauwen, ogen, maanpunten
#    langs de ogen, snuit; buitenlijn en transparant blijven van het model.
for y in range(43,53):
    for x in range(4,25):
        if g[y,x]==0: continue
        if y==52 and x<6: continue                 # kin links: lijn van het model (1 px smaller dan oud)
        if x==24 and y>=44: continue               # rechterbuitenlijn van het model
        v=oud[y,x]
        if v==0: continue
        zone='ogen' if (y>=44 and y<=49 and (5<=x<=11 or 14<=x<=20) and v in (1,9,10,11) or (y==44 and v==2 and 6<=x<=18)) else 'maan/gezicht (oud)'
        zet(x,y,v,zone,'oude sprite')

np.save('r1/r1.npy',g)
full=np.zeros((128,64),'uint8'); full[:64]=g; full[64:]=g
im=Image.fromarray(full,'P'); flat=[]
for c in PAL: flat+=list(c)
im.putpalette(flat); im.save('r1/anim_front.png',transparency=0)
open('r1/normal.pal','w').write('JASC-PAL\r\n0100\r\n16\r\n'+''.join('%d %d %d\r\n'%c for c in PAL))
if __name__=='__main__':
    from collections import Counter
    for z,x,y,o_,n,r in log: print(z,(x,y),S[o_],'->',S[n],r)
    print(dict(Counter(z for z,*_ in log)),'totaal',len(log))
    toon(g,0,64,7,64)
