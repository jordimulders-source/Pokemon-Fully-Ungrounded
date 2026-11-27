# vel_oog.png: oog zonder glans (hoofdversie) | met de modelglans op (18,15), 16x close-up + kop op 1x (4x vergroot)
import sys,os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); from gemeen import *
from kijk import groot
o=np.array(Image.open(HIER+'/hoatzin_r1.png')); g=o.copy(); g[15,18]=12
W=(255,255,255); box=(12,8,28,22)
ims=[groot(rgb(x,W).crop(box),16,False) for x in (o,g)]+[rgb(x,W).crop((0,0,40,30)).resize((160,120),0) for x in (o,g)]+[model_op_schaal().crop(box).resize((256,224),0)]
w=sum(i.width for i in ims)+8*len(ims); out=Image.new('RGB',(w,max(i.height for i in ims)),(220,220,220)); x=0
for i in ims: out.paste(i,(x,0)); x+=i.width+8
out.save(HIER+'/vel_oog.png')
