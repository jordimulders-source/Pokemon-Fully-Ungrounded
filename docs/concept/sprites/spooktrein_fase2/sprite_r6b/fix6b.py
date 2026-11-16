# r6b: flank weer planken (8, glans 7) met ijzeren banden (9) op de modelplek. Alleen hout/ijzerpixels binnen de flank;
# groen, omlijning op de buitenrand, gezicht en onderkant (y>=44) onaangeroerd. Keuze per pixel uit de modelklassen.
import numpy as np, sys; from PIL import Image
TH=float(sys.argv[1]) if len(sys.argv)>1 else 0.6
src=Image.open('r6.png'); pal=src.getpalette(); o=np.asarray(src).astype(int).copy(); r6=o.copy()
C=np.load('../sprite_r6/clsfrac.npy'); MS=np.load('../sprite_r6/modelstats.npy'); MG=MS[0]; P15=MS[1]
FACE=np.zeros((64,64),bool); FACE[9:27,25:42]=True
FL=np.zeros((64,64),bool); FL[23:43,24:56]=True   # onderkant (y>=43, schaduw/onderzijde, model 55-68) blijft
def fg(y,x): return 0<=y<64 and 0<=x<64 and o[y,x]>0
def edge(y,x): return any(not fg(y+dy,x+dx) for dy,dx in ((-1,0),(1,0),(0,-1),(0,1)))
iron=C[13]+C[1]+C[9]; wood=C[8]+C[10]+C[7]
log=[]
for y,x in zip(*np.where(FL&~FACE)):
    if o[y,x] not in (7,8,9) or edge(y,x): continue
    t=iron[y,x]+wood[y,x]
    if t<0.2: continue
    # band = ijzeren strook: donkere lijn in het blok (p15<45) en vlak donker (gem<TH); anders plank (8, glans 7)
    nv=9 if iron[y,x]/t>=TH else (7 if MG[y,x]>=123 else 8)   # ijzeraandeel in het modelblok
    if nv!=o[y,x]: log.append((x,y,o[y,x],nv)); o[y,x]=nv
# banden smal: per rij elke 9-reeks (binnen, y<=42) breder dan BW px terug naar de BW donkerste modelpixels; rest plank
BW=int(sys.argv[2]) if len(sys.argv)>2 else 3
nar=[]
for y in range(23,43):
    x=24
    while x<56:
        if o[y,x]==9 and not edge(y,x) and not FACE[y,x]:
            x1=x
            while x1+1<56 and o[y,x1+1]==9 and not edge(y,x1+1): x1+=1
            n=x1-x+1
            if n>BW:
                best=min(range(x,x1-BW+2),key=lambda a:MG[y,a:a+BW].sum())
                for xx in range(x,x1+1):
                    if not(best<=xx<best+BW):
                        nv=7 if MG[y,xx]>=123 else 8; nar.append((xx,y,9,nv)); o[y,xx]=nv
            x=x1+1
        else: x+=1
log+=nar
# opschonen: losse pixels (<3, 4-verbonden) van 8/9 in de flank opgaan in de buren
def comps(mask):
    seen=np.zeros((64,64),bool); out=[]
    for y,x in zip(*np.where(mask)):
        if seen[y,x]: continue
        st=[(y,x)]; seen[y,x]=True; cur=[]
        while st:
            cy,cx=st.pop(); cur.append((cy,cx))
            for dy,dx in ((-1,0),(1,0),(0,-1),(0,1)):
                yy,xx=cy+dy,cx+dx
                if 0<=yy<64 and 0<=xx<64 and mask[yy,xx] and not seen[yy,xx]: seen[yy,xx]=True; st.append((yy,xx))
        out.append(cur)
    return out
cl=[]
for it in range(3):
    for v in (7,8,9):
        for cp in comps((o==v)&FL&~FACE):
            if len(cp)>=3: continue
            for (y,x) in cp:
                if edge(y,x): continue
                nb=[o[y+dy,x+dx] for dy,dx in ((-1,0),(1,0),(0,-1),(0,1)) if o[y+dy,x+dx] in (7,8,9) and o[y+dy,x+dx]!=v]
                if nb:
                    u,c=np.unique(nb,return_counts=True); cl.append((x,y,o[y,x],int(u[c.argmax()]))); o[y,x]=int(u[c.argmax()])
im=Image.fromarray(o.astype('uint8'),'P'); im.putpalette(pal); im.save('sprite.png',transparency=0)
d=o!=r6
print('modelklasse',len(log),'opschoning',len(cl),'totaal diff',int(d.sum()),'gezicht diff',int(d[FACE].sum()),'buiten flank',int((d&~FL).sum()))
L=np.array([0 if i==0 else 0.3*pal[3*i]+0.59*pal[3*i+1]+0.11*pal[3*i+2] for i in range(14)])
z=np.zeros((64,64),bool); z[30:45,36:51]=True; z&=o>0
print('rechterflank sprite %.0f model %.0f (r6 %.0f)'%(L[o][z].mean(),MG[z].mean(),L[r6][z].mean()))
w=z&np.isin(o,(7,8,9)); print('flank hout/ijzer sprite %.0f model %.0f'%(L[o][w].mean(),MG[w].mean()))
open('telling.txt','w').write('modelklasse %d: %s\nopschoning %d: %s\n'%(len(log),[(int(a),int(b),int(c),int(e)) for a,b,c,e in log],len(cl),[(int(a),int(b),int(c),int(e)) for a,b,c,e in cl]))
