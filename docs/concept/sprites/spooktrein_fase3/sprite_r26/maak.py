import colorsys,sys
from PIL import Image
sys.path.insert(0,'.')
from opt import pc,L0
def kleur(h,s,lum):
    lo,hi=0,1
    for _ in range(40):
        l=(lo+hi)/2; r,g,b=colorsys.hls_to_rgb(h/360,l,s)
        if .299*r+.587*g+.114*b<lum/255: lo=l
        else: hi=l
    return tuple(max(0,min(255,round(v*255))) for v in colorsys.hls_to_rgb(h/360,(lo+hi)/2,s))
V={
'A':{7:(28,.42,196),10:(38,.10,170),14:(25,.50,146),8:(18,.42,120),11:(45,.05,120),12:(250,.07,78),9:(6,.38,56),
     2:(112,.62,200),4:(122,.36,178),3:(128,.50,158),5:(136,.34,135),6:(150,.36,98)},
'B':{7:(28,.42,192),10:(38,.10,165),14:(26,.52,138),8:(20,.45,110),11:(45,.05,112),12:(255,.08,56),9:(12,.42,86),
     2:(112,.62,200),4:(122,.36,178),3:(128,.50,158),5:(136,.34,132),6:(152,.36,64)},
'C':{7:(30,.45,196),10:(34,.14,170),14:(24,.55,146),8:(17,.45,120),11:(30,.10,120),12:(20,.14,78),9:(355,.30,56),
     2:(112,.62,200),4:(122,.36,178),3:(128,.50,158),5:(136,.34,135),6:(150,.36,98)},
}
lum=lambda c:.299*c[0]+.587*c[1]+.114*c[2]
M={7,8,9,10,11,12,14};G={2,3,4,5,6,13}
def meet(pal):
    out={}
    for naam,test in [('metaal',lambda a,b:a in M and b in M),('groen',lambda a,b:a in G and b in G),('groen-metaal',lambda a,b:(a in G)!=(b in G) and a in G|M and b in G|M)]:
        tot=w=0
        for (a,b),n in pc.items():
            if test(a,b):
                tot+=n
                if abs(lum(pal[a])-lum(pal[b]))<20: w+=n
        out[naam]=(w,tot,round(100*w/tot,1))
    return out
if __name__=='__main__':
    im=Image.open('../sprite_r25/sprite.png'); p=im.getpalette()
    pal0=[tuple(p[3*i:3*i+3]) for i in range(16)]
    print('r25',meet(pal0))
    for k,v in V.items():
        pal=list(pal0)
        for i,(h,s,l) in v.items(): pal[i]=kleur(h,s,l)
        q=im.copy(); q.putpalette([c for t in pal for c in t]+p[48:])
        q.save(f'sprite_{k}.png'); q.resize((512,512),Image.NEAREST).save(f'sprite_{k}_8x.png')
        print(k,meet(pal),{i:pal[i] for i in v})
