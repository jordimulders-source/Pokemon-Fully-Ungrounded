# Hoatzin r5 = r4 + DC-eindkeuring (dc.py: belijning) + tinten (hue shift/contrast). Silhouet: alpha-diff 0 (bewezen hieronder).
import sys,os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from dc import *
def lum(c): return 0.299*c[0]+0.587*c[1]+0.114*c[2]
# Tinten: lijf schaduw koeler/blauwer, licht warmer (DC: "slightly in the blue direction for shadows"); stappen vanaf zwart 15:
# 42 -> 70 -> 110 (was 42 -> 64 -> 97; Taillow-stappen ±30-40). Zuur: schaduw groener, licht geler; zelfde helderheden.
NIEUW={2:(35,42,48),3:(60,70,72),4:(100,112,102),
       5:(82,104,42),6:(150,170,46),7:(214,224,90)}
def palet(im):
    p=im.getpalette()[:48]
    for i,c in NIEUW.items(): p[3*i:3*i+3]=list(c)
    return p
def maak(bron,doel):
    im=Image.open(R4+bron); a=np.array(im); o,tel=bewerk(a)
    p=palet(im)
    out=Image.fromarray(o.astype('uint8'),'P'); out.putpalette(p+[0]*(768-len(p))); out.save(HIER+'/'+doel,transparency=0)
    alpha=int(((a==0)!=(o==0)).sum())
    print(doel,tel,'px gewijzigd (index):',int((o!=a).sum()),'alpha-diff:',alpha,'kleuren:',len(set(o.flatten())-{0}))
    return o,p
if __name__=='__main__':
    o,p=maak('hoatzin_r4.png','hoatzin_r5.png')
    ov,_=maak('hoatzin_r4_variant_teken.png','hoatzin_r5_variant_teken.png')
    for i in sorted(NIEUW): print(i,NIEUW[i],round(lum(NIEUW[i])))
