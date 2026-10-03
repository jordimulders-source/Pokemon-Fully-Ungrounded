"""Bouwt de layouts voor Raikou en Entei (kopieen van vanilla grotten):
- NewMauville_ThunderCave: kapot ondergronds datacenter onder New Mauville (Raikou): rotsgrot in de stijl van
  NewMauville_Entrance (Facility-tileset) met tanks en computers uit AquaHideout_B2F; ingang = de deur bovenin (11,1).
- MtChimney_EnteiPassage / MtChimney_EnteiLair: kopie van TerraCave_Entrance / TerraCave_End.
Gebruik: python3 tools/grounded/maptools/beasts_maps.py"""
import json, os, shutil, struct
REPO=os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','..'))
os.chdir(REPO)
L={l['name']:l for l in json.load(open('data/layouts/layouts.json'))['layouts'] if 'name' in l}
def load(n):
    l=L[n+'_Layout']; W=l['width']; v=list(struct.unpack('<%dH'%(W*l['height']),open(l['blockdata_filepath'],'rb').read()))
    return [v[y*W:(y+1)*W] for y in range(l['height'])]
ent=load('NewMauville_Entrance'); aqua=load('AquaHideout_B2F')
W,H=22,16
C=0xc00
FLOOR=0x3d0|(3<<12)
g=[[FLOOR]*W for _ in range(H)]
for y in range(H):
    g[y][0]=ent[3][0]; g[y][1]=ent[3][1]; g[y][W-2]=ent[3][7]; g[y][W-1]=ent[3][8]
for x in range(1,W-1):
    g[0][x]=ent[0][1]; g[1][x]=ent[1][2]
    g[H-2][x]=ent[7][2] if 2<=x<W-2 else g[H-2][x]
    g[H-1][x]=ent[8][1]
g[0][0]=ent[0][0]; g[0][W-1]=ent[0][8]; g[1][0]=ent[1][0]; g[1][1]=ent[1][1]; g[1][W-2]=ent[1][7]; g[1][W-1]=ent[1][8]
g[H-2][1]=ent[7][1]; g[H-2][W-2]=ent[7][7]; g[H-1][0]=ent[8][0]; g[H-1][W-1]=ent[8][8]
# deur bovenin (x 10-12): de ingang van NewMauville_Entrance
for dy in range(2):
    for dx in range(3): g[dy][10+dx]=ent[dy][3+dx]
# vloervarianten (scheuren) uit de ingang
import random
rnd=random.Random(110)
for _ in range(14):
    x,y=rnd.randint(2,W-3),rnd.randint(2,H-3); g[y][x]=rnd.choice((ent[2][3],ent[2][5],ent[6][4]))
def paste(sx,sy,w,h,dx,dy):
    for yy in range(h):
        for xx in range(w):
            t=aqua[sy+yy][sx+xx]
            if (t&0x3ff) in (0x228,0x2a1,0x2a9,0x22a,0x230,0x238,0x232,0x23a): continue  # Aqua-vloer en schaduwen -> grotvloer
            g[dy+yy][dx+xx]=t
# twee tanks tegen de achterwand (rij 0-6 van de Aqua-tank, inclusief voet en schaduw)
paste(20,0,4,7,3,0); paste(26,0,4,7,15,0)
# computerclusters (3x4: scherm, kast, kast, schaduw)
for (dx,dy) in ((2,9),(6,11),(14,11),(17,8),(9,7)):
    paste(17,6,3,4,dx,dy)
open('data/layouts/NewMauville_ThunderCave/map.bin','wb').write(struct.pack('<%dH'%(W*H),*[t for r in g for t in r]))
shutil.copy('data/layouts/NewMauville_Entrance/border.bin','data/layouts/NewMauville_ThunderCave/border.bin')

for src,dst in (('TerraCave_Entrance','MtChimney_EnteiPassage'),('TerraCave_End','MtChimney_EnteiLair')):
    os.makedirs('data/layouts/'+dst,exist_ok=True)
    for f in ('map.bin','border.bin'): shutil.copy('data/layouts/%s/%s'%(src,f),'data/layouts/%s/%s'%(dst,f))
print('klaar')
