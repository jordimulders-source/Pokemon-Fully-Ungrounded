# Kadabra-model uit ronde 10 B: beide handen van 4 naar 3 vingers, op het eigen 100x100-raster van het plaatje (cel 10,24 px).
# Open hand: de onderste vinger weg, rand van de handpalm rond gesloten (duim links, vinger omhoog, vinger schuin rechts; Gemini's eigen pixels).
# Kaarthand: Gemini's eigen hand, alleen de vinger linksonder weg en de onderrand van de vinger erboven gesloten (Jordi: "deze linkerhand ... met 1 vinger minder").
from PIL import Image
import numpy as np, sys
sys.path.insert(0,'model'); from grid10 import P,O,load,cell,cls
src='gemini/ronde10_B_kadabra_pose.png'
a0=load(src); a=a0.astype('uint8').copy()
samp={}
for j in range(22,50):
    for i in list(range(1,34))+list(range(68,100)):
        c=cell(a0,i,j); samp.setdefault(cls(c),[]).append(c)
COL={k:tuple(int(v) for v in np.median(np.array(v),0)) for k,v in samp.items()}
COL['.']=(255,255,255); COL['W']=(255,255,255); COL['o']=(14,13,20)
def px(i,j,ch):
    x0,y0,x1,y1=int(round(O+i*P)),int(round(O+j*P)),int(round(O+(i+1)*P)),int(round(O+(j+1)*P)); a[max(y0,0):y1,max(x0,0):x1]=COL[ch]
def row(j,c0,s):
    for k,ch in enumerate(s):
        if ch!='=': px(c0+k,j,ch)
# open hand (kolom 68 = positie 0)
row(37,88,'o.......')
row(38,88,'o.......')
row(39,88,'o........')
row(40,87,'o.........')
row(41,86,'o..........')
# kaarthand (kolom 1 = positie 0; strings beginnen op positie 5 = kolom 6)
row(41,6,'..oooo')
row(42,6,'....')
row(43,6,'.....')
row(44,6,'.....')
for j,c in ((37,89),(38,89),(39,89),(40,88),(41,87)):
    a[int(round(O+j*P))-1:int(round(O+(j+1)*P))+1, int(round(O+c*P)):]=(255,255,255)
a[int(round(O+36.6*P)):int(round(O+42.4*P)), int(round(O+89*P)):]=(255,255,255)
a[int(round(O+42*P))-1:int(round(O+45*P))+2, int(round(O+5*P)):int(round(O+10*P))]=(255,255,255)
a[int(round(O+43*P))-1:int(round(O+45*P))+2, int(round(O+10*P)):int(round(O+11*P))]=(255,255,255)
a[int(round(O+44*P))+1:int(round(O+46*P)), int(round(O+5*P)):int(round(O+11*P))+3]=(255,255,255)
out=Image.fromarray(a); out.save('model/model_B_hand3.png')
z1=out.crop((700,230,1010,470)).resize((620,480),Image.NEAREST); z2=out.crop((20,250,330,520)).resize((620,540),Image.NEAREST)
o=Image.new('RGB',(1250,540),'white'); o.paste(z2,(0,0)); o.paste(z1,(630,0)); o.save('model/model_B_handen_closeup.png')
