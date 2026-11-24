import sys; sys.path.insert(0,'/tmp/claude-0/-home-user-Pokemon-Fully-Ungrounded/df5125ac-9381-5d71-af17-ce82baab011f/scratchpad')
from PIL import Image
import ronde
src='sprite_r9/A0.png'
a=Image.open(src); P=a.getpalette(); P[30:33]=[140,152,172]
tmp='/tmp/claude-0/-home-user-Pokemon-Fully-Ungrounded/df5125ac-9381-5d71-af17-ce82baab011f/scratchpad/r9_pal.png'
b=a.copy(); b.putpalette(P); b.save(tmp,transparency=0)
E={(8,9):[(42,36),(43,36),(41,37),(42,37),(43,37),(40,38),(41,38),(42,38),(39,39),(40,39),(41,39),(39,40),(40,40)],
(8,10):[(45,33),(46,33),(47,33),(46,34),(46,35)],
(6,5):[(47,21),(46,22),(45,23),(45,24),(44,25),(43,26),(43,27),(42,28),(42,29),(42,30),(41,31),(41,32),(40,33),(39,34),(39,35),(38,36),(37,37),(36,37),(35,38),(34,39),(33,40)],
(9,8):[(35,46),(33,47),(34,47),(32,48),(31,49),(30,50)],(7,6):[(20,45),(20,46)],(3,2):[(28,46)]}
zone={(8,9):'buik',(8,10):'buik',(6,5):'vleugel',(9,8):'buikrand',(7,6):'flap',(3,2):'lijf'}
R=[]
for (o,n),ps in E.items():
    for x,y in ps:
        assert b.getpixel((x,y))==o
        R.append((zone[(o,n)],y,x,'%x'%n))
ronde.run(tmp,'sprite_r10',R)
