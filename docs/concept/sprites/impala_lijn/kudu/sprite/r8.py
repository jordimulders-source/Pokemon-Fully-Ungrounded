# Ronde 8: manen = één vorm (r6-haar = model A3), los van het lijf, rand licht gerafeld met randstukken 1-op-1 uit
# Arcanine/Growlithe (anim_front_gba), vlak = vultinten van de Arcanine-rugpluk, omtrek per regel. Zie r8/NOTITIES.md.
import r8lib as L, sys
A_UP1=('arcanine',40,3,42,5); A_UP2=('arcanine',14,4,17,6); A_LEFT=('arcanine',4,37,7,42)
A_DOWN=('arcanine',19,47,23,51); A_RIGHT=('arcanine',54,16,59,23)
G_UP=('growlithe',25,12,29,14); G_UP2=('growlithe',20,13,24,15); G_LEFT=('growlithe',18,36,22,41)
G_DOWN=('growlithe',23,43,28,46)
A_BUMP=('arcanine',54,17,58,20)  # kleine bult van de rechterrand van de rugpluk
VELD=('arcanine',33,2,60,26,7,23)
VARIANTEN={
 'A':('pluizige kraag met puntjes (Arcanine)',[
   (A_UP2,22,25,'kampunt 1'),(A_UP2,26,26,'kampunt 2'),(A_UP2,29,28,'kampunt 3'),
   (A_LEFT,7,33,'franjepluk 1',2),(A_LEFT,7,38,'franjepluk 2',2),
   (A_LEFT,15,27,'nekrand-pluk 1'),(A_LEFT,15,32,'nekrand-pluk 2'),
   (A_DOWN,8,41,'onderpunt 1',2),(A_DOWN,12,42,'onderpunt 2',2),(A_DOWN,16,42,'onderpunt 3',2),
   (A_DOWN,25,27,'kampunt onder (over de rug)'),
   (A_RIGHT,21,31,'schouderpunten 1'),(A_RIGHT,19,36,'schouderpunten 2'),
   (A_BUMP,22,31,'schouderbult'),(A_BUMP,9,31,'franje rechts: inkeping'),(A_BUMP,7,37,'franje links: bult',1,True)]),
 'B':('lang hangend kapsel, licht gerafelde onderrand',[
   (A_UP2,26,26,'kampunt'),
   (A_DOWN,8,41,'onderpunt 1',2),(A_DOWN,11,42,'onderpunt 2',2),(A_DOWN,14,42,'onderpunt 3',2),(A_DOWN,17,42,'onderpunt 4',2),
   (A_RIGHT,19,36,'schouderpunt (onderste lok)'),(A_DOWN,25,27,'kampunt onder (over de rug)'),
   (A_BUMP,23,31,'schouderbult'),(A_BUMP,9,31,'franje rechts: inkeping'),(A_BUMP,8,31,'franje links: bult 1',1,True),
   (A_BUMP,8,37,'franje links: bult 2',1,True),(A_BUMP,15,29,'nekrand: inkeping',1,True)]),
 'C':('zachte plukken (Growlithe)',[
   (G_UP,21,25,'kampunt 1'),(G_UP,26,26,'kampunt 2'),
   (G_LEFT,7,32,'franjepluk 1',2),(G_LEFT,7,37,'franjepluk 2',2),(G_LEFT,15,29,'nekrand-pluk'),
   (G_DOWN,9,42,'onderpunt 1',2),(G_DOWN,14,42,'onderpunt 2',2),
   (A_RIGHT,21,31,'schouderpunten (Arcanine)'),(A_DOWN,25,27,'kampunt onder (Arcanine)'),
   (A_BUMP,22,31,'schouderbult (Arcanine)'),(A_BUMP,9,31,'franje rechts: inkeping (Arcanine)')]),
}
def bouw(k):
    naam,stamps=VARIANTEN[k]
    v=L.Vorm(); v.veld(*VELD,label='vlak: Arcanine-rugpluk (x33-60,y2-26) op (7,23)')
    for st in stamps:
        sn,dx,dy,lab=st[:4]; v.rand(*sn,dx,dy,(st[5] if len(st)>5 else False),label=lab,diepte=(st[4] if len(st)>4 else 1))
    return v,v.maak(slagschaduw=True)
if __name__=='__main__':
    from PIL import Image
    V=Image.new('RGB',(3*300,280),'white')
    for i,k in enumerate(VARIANTEN):
        v,g=bouw(k); print(k); L.toon(g,23,48,34); print('recht:',L.rechte(g,L.ZONE))
        V.paste(L.rgba8(g).crop((2,18,38,52)).resize((288,272),0),(i*300,0))
    V.save(sys.argv[1])
