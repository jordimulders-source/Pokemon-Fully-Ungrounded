# Bandolingo variant B: tintzones lijf/staart/poten, met de hand als segmenten (x_start, tekst).
# L=5 licht (nieuw: lichter), G=4 grondtint, S=3 schaduw/selout/plooilijn, 1=lijn. Kop wordt niet aangeraakt.
from PIL import Image
import os
H=os.path.dirname(os.path.abspath(__file__))
im=Image.open(os.path.join(H,'../../../olinguito_v2/af/olinguito.png')); px=im.load()
M={'L':5,'G':4,'S':3,'1':1,'2':2}
SEG={
 # staart: lichtkant 1 px licht, schaduwkant donker
 3:[(45,'LLL')],
 4:[(43,'LLLGGS')],
 5:[(42,'LLS'),(48,'GS')],
 6:[(41,'LGS'),(48,'LGS')],
 7:[(41,'LS'),(48,'LS')],
 8:[(40,'LS'),(49,'LGS')], 9:[(40,'LS'),(49,'LGS')],
 10:[(49,'LGS')],11:[(49,'LGS')],12:[(50,'LS')],13:[(50,'LS')],14:[(50,'LS')],15:[(50,'LS')],16:[(50,'LS')],
 17:[(49,'LGS')],18:[(49,'LGS')],19:[(49,'LGS')],20:[(49,'LGS')],21:[(49,'LGS')],22:[(49,'LGS')],
 23:[(49,'LS')],24:[(48,'LGGS')],25:[(48,'LGS')],
 # lijf: lichtzone op de bolling linksboven (harde diagonale grens), grondtint midden, schaduwsikkel rechts/onder
 26:[(41,'LLL'),(49,'GS')],
 27:[(38,'LLLLLLLL'),(46,'GGGGS')],
 28:[(36,'LLLLSLLLL'),(45,'GGGGS')],
 29:[(35,'LLLLLLSLL'),(44,'GGGGG'),(49,'S')],
 30:[(34,'LLLLLLLLL'),(43,'GGGGG'),(48,'S')],
 31:[(34,'LLLLLLL'),(41,'GGGGGGG'),(48,'SS')],
 32:[(34,'LLLLL'),(39,'GGSS'),(43,'GGGG'),(47,'SSS')],
 33:[(34,'LLLL'),(38,'GGS'),(41,'LLL'),(44,'GG'),(46,'SSSS')],
 34:[(34,'LLL'),(37,'GGS'),(40,'LLL'),(43,'GG'),(45,'SSSSS')],
 35:[(34,'LL'),(36,'GGGS'),(40,'LLL'),(43,'SG'),(45,'SSSSS')],
 36:[(34,'L'),(35,'GGGGS'),(40,'LL'),(42,'GS'),(44,'SSSSS')],
 37:[(34,'GGGGGS'),(40,'L'),(41,'GG'),(43,'SSSSSS')],
 38:[(33,'LLL'),(36,'SGGS'),(40,'GG'),(42,'SSSSSS')],
 39:[(32,'LLL'),(35,'SGGGS'),(40,'GG'),(42,'SSSSS')],
 40:[(31,'LL'),(33,'GGG'),(36,'SSSSSS'),(42,'GG'),(44,'SSS')],
 # nabije voorpoot: licht aan de voorkant (1 px), grond, schaduw achter
 41:[(29,'LGGGG'),(42,'LGGS')],
 42:[(29,'LGGGS'),(42,'LGSS')],
 43:[(29,'LGGGS'),(42,'LGSS')],
 44:[(29,'LGGSS'),(42,'LGSS')],
 45:[(29,'LGGSS'),(42,'LGGSS')],
 46:[(29,'LGGSS'),(42,'LGGSS')],
 47:[(29,'LGGSS'),(42,'SLGGSS')],
 48:[(29,'LGGS'),(42,'SLGSSS')],
 49:[(29,'LGGS')],
 50:[(29,'LGS')],
}
n=0
for y,segs in SEG.items():
    for x0,s in segs:
        for i,ch in enumerate(s):
            x=x0+i; assert px[x,y]!=0,(x,y)
            if px[x,y]!=M[ch]: n+=1
            px[x,y]=M[ch]
pal=im.getpalette(); pal[15:18]=[186,136,88]; im.putpalette(pal)
im.save(os.path.join(H,'na_B.png'),transparency=0)
print('gewijzigd',n)
