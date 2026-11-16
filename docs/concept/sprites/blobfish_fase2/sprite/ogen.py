# Ogen herstellen naar het model: in de oogvensters wordt een spritepixel zwart als >= 30% van zijn modeloppervlak oogzwart (lum<90) is,
# anders de gekwantiseerde vulkleur van de kale reductie. Niets getekend: alleen de lijnregel vervangen door oppervlakdekking.
import json; import numpy as np; from PIL import Image
o=np.load('r1.npy'); P=json.load(open('kaal_palet.json')); cols=np.array(P['cols'],float); grp=P['grp']['0']
a=np.asarray(Image.open('model_natief.png').convert('RGBA')).astype(float)
l=a[...,:3]@[.299,.587,.114]; d=(l<90)&(a[...,3]>0); C=np.load('kaal_rgb.npy')
def feat(X): return np.c_[X@[.299,.587,.114], 2.0*(X[:,0]-X[:,1]), 2.0*(X[:,2]-X[:,1])]
F=1.5;x0,y0=11,21
def cov(i,j):
    sx,sy=x0+(i-1)*F,y0+(j-17)*F; s=0
    for y in range(int(sy),int(np.ceil(sy+F))):
        for x in range(int(sx),int(np.ceil(sx+F))):
            w=max(0,min(sx+F,x+1)-max(sx,x))*max(0,min(sy+F,y+1)-max(sy,y)); s+=w*d[y,x]
    return s/2.25
n=0
for (i0,i1,j0,j1) in [(12,18,29,34),(27,33,29,34)]:   # linker en rechter oog
    for j in range(j0,j1):
        for i in range(i0,i1):
            if cov(i,j)>=0.3: v=1
            elif o[j,i]!=1: continue
            else: v=grp[int(np.argmin(((feat(cols[grp])-feat(C[j-17,i-1][None]))**2).sum(1)))]
            if o[j,i]!=v: n+=1; print('oogpixel',(i,j),o[j,i],'->',v)
            o[j,i]=v
# laatste ruisronde: tintvlakjes < 3 px (niet glans/zwart, niet de buitenlijn) nemen de meest voorkomende buurtint uit dezelfde groep
G={c:g for g,vs in P['grp'].items() for c in vs}
op=o>0; p=np.pad(op,1); rand=op&~(p[:-2,1:-1]&p[2:,1:-1]&p[1:-1,:-2]&p[1:-1,2:])
for c in [c for c in range(3,len(cols)) if c!=9]:   # 9 = donkere binnenlijn, mag dun
    m=(o==c)&~rand; seen=np.zeros_like(m)
    for y,x in zip(*np.where(m)):
        if seen[y,x]: continue
        st=[(y,x)]; cl=[]; seen[y,x]=1
        while st:
            a,b=st.pop(); cl.append((a,b))
            for aa,bb in ((a-1,b),(a+1,b),(a,b-1),(a,b+1)):
                if m[aa,bb] and not seen[aa,bb]: seen[aa,bb]=1; st.append((aa,bb))
        if len(cl)<3:
            bu=[o[aa,bb] for a,b in cl for aa,bb in ((a-1,b),(a+1,b),(a,b-1),(a,b+1)) if o[aa,bb]>1 and o[aa,bb]!=c and G.get(o[aa,bb])==G[c]]
            if bu:
                v=max(set(bu),key=bu.count)
                for a,b in cl: o[a,b]=v; n+=1; print('ruis',(b,a),c,'->',v)
# losse donkere binnenlijnpixels (index 9 zonder 8-buur in zwart/9, niet op de buitenlijn) = ruis -> vulkleur van de kale reductie
for y,x in zip(*np.where((o==9)&~rand)):
    if not any(o[y+dy,x+dx] in (1,9) for dy in (-1,0,1) for dx in (-1,0,1) if (dy or dx)):
        g2=[c for c in grp if c!=9]; v=g2[int(np.argmin(((feat(cols[g2])-feat(C[y-17,x-1][None]))**2).sum(1)))]; o[y,x]=v; n+=1; print('losse 9',(x,y),'->',v)
np.save('r1.npy',o); print('gewijzigd',n)
im=Image.fromarray(o.astype(np.uint8),'P'); pl=sum(P['cols'],[]); im.putpalette(pl); im.save('r1.png',transparency=0)
rgb=np.array(P['cols'],'uint8')[o]; rgb[o==0]=255; Image.fromarray(rgb).resize((512,512),Image.NEAREST).save('r1_8x.png')
