# Gedeelde hulpjes guarana fase 2 r1: schaal natief -> sprite, overlap, palet (basis = fase 1 af/normal.pal), opslaan.
import numpy as np; from PIL import Image
# natief raster 199x199 (cel 5,12 px), figuur x11-186, y25-170 (176x146). Schaal 62/176: 62 breed (x1-62), onderkant op y51 zoals fase 1.
S=62/176; U0,V0=11,25; X0=1.0; Y0=52.0-146*S
NATIEF='sprite_r1/natief_model.png'
# palet = fase 1 (af/normal.pal) indexen 0-11 ongewijzigd; 12-13 erbij (r2), 14-15 vrij
PAL=[(152,208,160),(16,16,16),
     (120,28,32),(176,56,48),(224,80,56),(240,136,104),
     (58,86,46),(84,122,64),(122,160,80),(166,198,108),
     (248,248,248),(196,200,204),
     (248,184,148),(104,146,86),
     (140,36,40),(70,102,56)]   # r3: 12 = glans (was oranjerood), 14 diep rood (achterste vruchten), 15 diep groen (schaduwkant strengen/achterblad)
# r2: 12 = oranjerood, 13 = middengroen: modeltinten die in het fase 1-palet ontbreken (k-means-mediaan van het vruchtvlees/groen in het natieve model:
# rood 178,54,47 | 223,86,59 | 236,113,79 | 249,144,112 ; groen 55,87,45 | 76,115,67 | 105,148,89 | 123,167,101)
ROOD=[2,14,3,4,12,5]; GROEN=[6,15,7,13,8,9]; WIT=[10,11]
def overlap(X,Y,W=199,H=199):
    ua=(X-X0)/S+U0; ub=ua+1/S; va=(Y-Y0)/S+V0; vb=va+1/S
    for v in range(int(np.floor(va)),int(np.ceil(vb))):
        for u in range(int(np.floor(ua)),int(np.ceil(ub))):
            w=max(0,min(ub,u+1)-max(ua,u))*max(0,min(vb,v+1)-max(va,v))*S*S
            if w>1e-9 and 0<=u<W and 0<=v<H: yield u,v,w
def naar_sprite(u,v): return (u-U0)*S+X0,(v-V0)*S+Y0
def model_op_schaal():
    a=np.asarray(Image.open(NATIEF).convert('RGB')).astype(float); out=np.full((64,64,3),255.)
    for Y in range(64):
        for X in range(64):
            acc=np.zeros(3); tw=0
            for u,v,w in overlap(X,Y): acc+=w*a[v,u]; tw+=w
            if tw: out[Y,X]=acc/tw
    return Image.fromarray(out.astype('uint8'))
def rgb(o,bg=None,pal=None):
    pal=pal or PAL; img=np.zeros((64,64,3),'uint8'); img[:]=bg if bg else pal[0]
    for k in range(1,len(pal)): img[o==k]=pal[k]
    return Image.fromarray(img)
def opslaan(o,path,pal=None):
    pal=pal or PAL
    p=Image.fromarray(o.astype('uint8'),'P'); fl=[v for c in pal for v in c]; p.putpalette(fl+[0]*(768-len(fl))); p.save(path,transparency=0)
def pal_schrijven(path,pal=None):
    pal=(pal or PAL)+[(0,0,0)]*(16-len(pal or PAL))
    open(path,'w').write('JASC-PAL\r\n0100\r\n16\r\n'+''.join('%d %d %d\r\n'%c for c in pal))
