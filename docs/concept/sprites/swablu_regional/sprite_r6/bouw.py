# Swablu r6: Jordi over r5: "de originele swablu heeft nog heel subtiel een iets lichtere tint om de zwarte pixels in het oog heen, probeer hetzelfde
# te doen. wat betreft de mond, de lijn is te hard en 1 pixel te veel naar links, het zijn ook net teveel 2 lijnen, dat kan misschien iets netter,
# kijk ook naar hoe de originele swablu met tinten en schaduw speelt". Alleen oog en snavel; diff elders 0. Draaien vanuit swablu_regional/.
import sys, numpy as np; from PIL import Image
sys.path.insert(0,'gereedschap'); import gemeen as G
r5=Image.open('sprite_r5/swablu_r5.png'); o=np.asarray(r5).astype(int); start=o.copy()
G.PAL=[tuple(r5.getpalette()[3*i:3*i+3]) for i in range(15)]
# Oog. Echte Swablu: zwart (32,34) (31,35) + glans (31,34); recht ernaast donker blauwgroen (2) links van de glans, boven, en rechts van het onderste zwart:
# een tint tussen zwart en lijf. Hier hetzelfde met vogel donker (68,90,110) op de overeenkomstige plekken: links van de glans (27,28),
# rechtsboven het zwart (29,27), rechts van het onderste zwart (30,29). Subtiel: 3 px, geen volle ring.
for X,Y in ((27,28),(29,27),(30,29)): assert o[Y,X]==8; o[Y,X]=7
# Mond. Echte Swablu: geen harde lijn; wit boven, dan lichtlila/lila (schaduw) en grijs onderaan, de bek leest uit de tintstap.
# - lijn begint 1 px naar rechts: (21,31) selout -> wolk midden (zoals de snavelrand erboven);
# - lijn zachter: (22,31) (23,31) (24,30) (25,30) selout donker -> wolk donker (96,108,126), sluit rechts aan op de rechterrand (wolk donker);
# - geen tweede lijn: onderrand (22-25,32) wolk donker -> wolk midden (schaduw onder de onderkaak i.p.v. lijn); onderkaak (24,31) (25,31) blijft wolk licht.
for X,Y,k in ((21,31,4),(22,31,3),(23,31,3),(24,30,3),(25,30,3),(22,32,4),(23,32,4),(24,32,4),(25,32,4)): o[Y,X]=k
d=np.argwhere(o!=start); assert all(21<=x<=30 and 27<=y<=32 for y,x in d)
G.opslaan(o,'sprite_r6/swablu_r6.png'); G.rgb(o,(255,255,255)).resize((512,512),Image.NEAREST).save('sprite_r6/swablu_r6_8x.png')
print('anders dan r5:',len(d),[(int(x),int(y),int(start[y,x]),int(o[y,x])) for y,x in d])
