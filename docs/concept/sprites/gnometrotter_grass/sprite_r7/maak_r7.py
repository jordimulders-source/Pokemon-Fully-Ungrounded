# maak_r7.py: Gnometrotter Grass r7 = r6, alleen de roze romp opnieuw: plankvlakken en naden uit het model
# (model op 12x: naad x ±30 boven -> ±29,5 onder, naad x 35; stippelnerven ±37,3 en ±43,3 weggelaten).
# Per plank één verdeling 15 (links boven) / 8 / 7 (rechts en onder), sikkel 6 boven de riem en rechts. Rest 0 px. Log: log_r7.txt.
import os, sys, numpy as np
from PIL import Image
from scipy import ndimage
HIER=os.path.dirname(os.path.abspath(__file__)); os.chdir(HIER)
bim=Image.open('../sprite_r6/gnometrotter_grass.png'); B=np.asarray(bim).astype(int); O=B.copy()
PINK=[6,7,8,15]
OVAAL={21:(41,44),22:(40,47),23:(40,48),24:(40,49),25:(40,49),26:(41,49),27:(42,49),28:(44,47)}
uit=np.zeros((64,64),bool)
for y,(a,b) in OVAAL.items(): uit[y,a:b+1]=True
uit[:,:26]=True; uit[:,50:]=True; uit[26:,48:]=True; uit[:20,:]=True
uit[19:22,40:44]=True    # bovenkant schouder (keuring_r5 punt A, r6) hoort niet bij de romp
L,_=ndimage.label(np.isin(B,PINK)&~uit); romp=L==L[30,33]

# Jordi (akkoord, via coördinator): maximaal twee plankennaden in een vloeiende, gelijkmatige bocht, hooguit één nerflijn;
# het hout komt verder uit het ronde tonvolume. Hier: de twee sterkste modelnaden (±30 en 35), geen nerf.
# Bocht = één pixel uitbuiging links van het tonmidden (duig van een ton): boven en onder 1 px naar rechts, midden 1 px naar links.
def naad1(y): return 29 if 24<=y<=32 else 30
def naad2(y): return 34 if 24<=y<=32 else 35
onder=np.zeros((64,64),bool)
for y,x in zip(*np.nonzero(romp)):
    if B[y+1,x] in (2,3,4) and x>=31: onder[y,x]=True
def tint(x,y):
    n1,n2=naad1(y),naad2(y)
    if x==n1 or x==n2: return 6
    if onder[y,x]: return 6                       # sikkel boven de riem
    if x<n1: return 7                             # plank 1: in de schaduw van de baard
    if x<n2:                                      # plank 2
        if x<=n1+2 and y<=25: return 15
        if y>=33 or (x==n2-1 and y>=27): return 7
        return 8
    # plank 3 (rechts van naad 2, tot de rugtak): licht links, sikkel rechts/onder als boog
    if x==n2+1 and 21<=y<=26: return 15
    if y>=29:
        rand=max(xx for xx in range(36,50) if romp[y,xx])
        if x==rand and x>=45: return 6            # lijf draait weg achter de schouder
        if y>=33 or x>=42-(y-29): return 7        # schaduwgrens loopt als boog naar linksonder
        return 8
    if x>=44: return 7
    return 8
for y,x in zip(*np.nonzero(romp)): O[y,x]=tint(x,y)

if __name__=='__main__':
    ver=O!=B
    assert not (ver&~romp).any()
    print('t.o.v. r6: romp',int(ver.sum()),'rest 0')
    with open('log_r7.txt','w') as f:
        for y,x in zip(*np.nonzero(ver)): f.write('romp x=%d y=%d %d->%d\n'%(x,y,B[y,x],O[y,x]))
    out=Image.new('P',(64,64)); out.putpalette(bim.getpalette()); out.putdata(O.astype('uint8').ravel().tolist())
    out.save('gnometrotter_grass.png'); out.resize((512,512),Image.NEAREST).save('gnometrotter_grass_8x.png')
    H='0123456789abcdef'
    for y in range(18,38): print('%2d '%y+''.join(('.' if O[y,x]==0 else H[O[y,x]]) if romp[y,x] else ' ' for x in range(24,51)))
    # vel: model | r5 | r6 | r7, 12x, alleen de romp (x 24-51, y 17-38)
    sys.path.insert(0,'../../gnometrotter_rock/sprite'); os.chdir('../../gnometrotter_rock/sprite')
    from kijk import sprite, model_op_schaal
    z=12; x0,y0,x1,y1=24,17,51,38
    m=model_op_schaal('../../gnometrotter_grass/hybride/model_hybride.png',64*z).crop((x0*z,y0*z,x1*z,y1*z)); os.chdir(HIER)
    ps=[m]+[sprite(p).crop((x0,y0,x1,y1)).resize(((x1-x0)*z,(y1-y0)*z),Image.NEAREST) for p in
        ('../sprite_r5/gnometrotter_grass.png','../sprite_r6/gnometrotter_grass.png','gnometrotter_grass.png')]
    w=(x1-x0)*z; W=Image.new('RGB',(4*(w+10),(y1-y0)*z),'white')
    for k,p in enumerate(ps): W.paste(p,(k*(w+10),0))
    W.save('vel.png')
