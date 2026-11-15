# p5: Jordi over p4 (vier punten), alles met kleur/schaduw/lijnen binnen de bestaande vormen, niets hertekend.
import sys, numpy as np
from PIL import Image
P4=np.array(Image.open('../p4/welp_p4.png')); R=np.array(Image.open('../r11/welp_r11.png'))
PAL=Image.open('../r11/welp_r11.png').getpalette()
LIJN=np.isin(R,[1,2])
def maak(tong='A',kop='A',rug='A'):
    a=P4.copy()
    def zet(x,y,v):
        assert a[y,x]!=0, ('leeg',x,y); a[y,x]=v
    # 1 tong/poot: scheiding aan de pootkant (tongpixels blijven)
    if tong=='A':   # lijn: bovenrand van de poot onder de tong in donkerbruin 2
        for x in (11,12,13): zet(x,41,2)
    else:           # schaduw: slagschaduw van de tong op de poot (3/4), poot-hooglicht één rij lager blijft
        zet(11,41,3); zet(12,41,3); zet(13,41,4)
    # 2 rugband: band los van de buitenlijn (pixel tegen de zwarte rug-lijn wordt licht rugfacet 5),
    #   band 2 px: 8 boven, 7 onder; eindkrul: groef in lila 6 i.p.v. bruin, donkere balk ernaast naar bruin 4
    if rug=='A':   # band los van de buitenlijn (rugrand 5), band zelf 2 px helder 8
        for y in range(32,43):
            for x in range(31,43):
                if a[y,x] in (7,8) and (LIJN[y,x+1] or LIJN[y-1,x]) and (x,y)!=(41,40): a[y,x]=5
        for y in range(32,38):
            for x in range(31,41):
                if a[y,x]==7: a[y,x]=8
    for x,y in [(38,39),(39,39),(40,39),(40,40),(39,41),(40,41)]: zet(x,y,6)
    for x,y in [(36,39),(37,39),(37,40)]: zet(x,y,4)
    # 3 voorhoofdsband (haarspeld): buitenarm 8, binnenarm 7, bocht onder 7, groef lila 6 (variant A) of bruin 3 (B)
    binnen=[(20,21),(18,22),(19,22),(16,23),(17,23),(15,24),(16,24)]
    for p in binnen: zet(*p,7)
    for p in [(13,25),(15,25)]: zet(*p,7)
    if kop=='A':
        for p in [(18,21),(19,21),(16,22),(17,22),(14,23),(15,23),(14,24)]: zet(*p,6)
    # 4 staart: rechte crème streep (x52, y53-56) weg; gebogen ring om de staart (crème boven, lila eronder)
    for x,y,v in [(52,53,5),(52,54,4),(52,55,3),(52,56,3),(53,55,3),
                  (53,52,11),(54,52,11),(54,53,11),(55,53,9),
                  (53,53,8),(53,54,7),(54,54,7)]: zet(x,y,v)
    return a
def bewaar(a,naam):
    im=Image.fromarray(a.astype('uint8'),'P'); im.putpalette(PAL); im.save(naam+'.png',transparency=0)
    q=Image.open(naam+'.png').convert('RGBA'); bg=Image.new('RGBA',q.size,(255,255,255,255)); bg.alpha_composite(q)
    bg.resize((512,512),Image.NEAREST).save(naam+'_8x.png')
if __name__=='__main__':
    bewaar(maak('A','A','B'),'welp_p5')
    bewaar(maak('B','A','B'),'/tmp/claude-0/p5_tongB')
    bewaar(maak('B','B'),'/tmp/claude-0/p5_BB')
    bewaar(maak('A','A','B'),'/tmp/claude-0/p5_rugB')
