# Ogen uit r8: oogzone van het natieve r8-raster (5,12-pitch) verkleind met factor 2, per blok het materiaal dat in het model domineert
# (zwart pupil, wit oogwit, donkerbruin ooglid, anders zandtint). Geen getekende pixels.
import numpy as np; import materiaal as mt; import bewerk, kleur
R8=bewerk.R8.astype(float)
def oog(box, fase=(0,0), f=2):
    x0,y0,x1,y1=box; L=R8@[0.299,0.587,0.114]; h,s,v=mt.hsv(R8)
    out=[]
    for y in range(y0+fase[1],y1,f):
        row=[]
        for x in range(x0+fase[0],x1,f):
            l=L[y:y+f,x:x+f].ravel(); ss=s[y:y+f,x:x+f].ravel()
            zw=(l<60).sum(); wi=((l>195)&(ss<0.25)).sum(); db=(l<125).sum()
            if zw>=1 and zw>=wi: row.append(1)
            elif wi>=2 or (wi>=1 and zw==0 and db==0): row.append(23)
            elif db>=2: row.append(10)
            else: row.append(10+kleur.band(l.mean(),kleur.ZAND))
        out.append(row)
    return np.array(out)
