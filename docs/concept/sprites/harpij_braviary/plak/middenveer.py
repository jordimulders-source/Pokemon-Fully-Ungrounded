# Variant D + de middelste veer die Gemini in r6 toevoegde opnieuw in de stijl van de rest (banden, zelfde grijs, ronde punt).
import importlib.util, numpy as np
from PIL import Image
spec=importlib.util.spec_from_file_location('v','plak/veren.py')
src=open('plak/veren.py').read().split('V={')[0]
ns={}; exec(src,ns); feather=ns['feather']
D=np.asarray(Image.open('plak/variant_D.png')).astype(int)
def clear(a):
    a=a.copy()
    start={2:53,3:53,4:53,5:53,6:53,7:52,8:51,9:50,10:49,11:49,12:48,13:47,14:47,15:47}  # begin rechterpluk per rij
    for y,e in start.items():
        for x in range(41,e):
            if a[y,x].mean()<150: a[y,x]=(255,255,255)   # oude veer weg, kop (licht) blijft
    return a
def dicht(a):
    # witte gaatjes tussen veren en kop onder de kuif opvullen met lijnkleur
    for y in range(10,18):
        for x in range(41,50):
            if a[y,x].mean()>225:
                n=sum(a[y+dy,x+dx].mean()<=225 for dy,dx in((1,0),(-1,0),(0,1),(0,-1)))
                if n>=3: a[y,x]=(22,24,30)
    return a
out={}
for k,(base,ang,L,W) in {'E':((43,17),82,15,2.6),'F':((44,17),76,15,2.6),'G':((43,17),86,14,2.8)}.items():
    a=clear(D); feather(a,base,ang,L,W); a=dicht(a); out[k]=a
    Image.fromarray(a.astype('uint8')).save(f'plak/variant_D_{k}.png')
from PIL import ImageDraw
tiles=[Image.fromarray(D.astype('uint8'))]+[Image.fromarray(out[k].astype('uint8')) for k in 'EFG']
v=Image.new('RGB',(4*410,99*5+40),'white'); d=ImageDraw.Draw(v)
for i,(t,n) in enumerate(zip(tiles,['D','D+E','D+F','D+G'])):
    v.paste(t.crop((10,0,90,99)).resize((400,495),Image.NEAREST),(i*410,40)); d.text((i*410+180,10),n,fill=(0,0,0))
v.save('plak/varianten_midden.png')
v.crop((0,40,1640,240)).save('/tmp/claude-0/-home-user-Pokemon-Fully-Ungrounded/19dfe9e4-3efd-5231-a28d-9f6e305e37a4/scratchpad/mid.png')
