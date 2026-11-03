from PIL import Image
D='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/silicobra_uyuni/ronde1/'
n=Image.open(D+'silicobra_uyuni.png'); b=Image.open('/home/user/Pokemon-Fully-Ungrounded/graphics/pokemon/silicobra/anim_front.png').crop((0,0,64,64))
N=list(n.get_flattened_data()); B=list(b.get_flattened_data())
def zone(x,y):
    if y<=31: return 'kuif'          # kop: boven/achterkant (alle toegevoegde px liggen buiten het gezicht)
    if 32<=y<=43 and 18<=x<=41: return 'pekelzak'
    return 'rest'
cnt={}
for y in range(64):
    for x in range(64):
        a,c=N[y*64+x]!=0,B[y*64+x]!=0
        if a!=c:
            k=(zone(x,y),'erbij' if a else 'eraf'); cnt[k]=cnt.get(k,0)+1
print('alpha-diff per zone:',cnt)
print('pixels nieuw:',sum(v!=0 for v in N),'basis:',sum(v!=0 for v in B))
print('kleuren:',len(set(N)),'mode',n.mode,'transparency',n.info.get('transparency'))
# open randen: pixels naast transparant die geen randkleur zijn
pal=n.getpalette(); names='.OKedcbafgqrst'
rim=set('OKetsgd')
bad=[]
for y in range(64):
    for x in range(64):
        v=N[y*64+x]
        if v==0: continue
        if any((0<=x+dx<64 and 0<=y+dy<64 and N[(y+dy)*64+x+dx]==0) or not(0<=x+dx<64 and 0<=y+dy<64) for dx,dy in((1,0),(-1,0),(0,1),(0,-1))):
            if names[v] not in rim: bad.append((x,y,names[v]))
print('randpixels zonder randkleur:',bad)
# losse pixels: niet-transparante pixel zonder 4-buur
iso=[(x,y) for y in range(64) for x in range(64) if N[y*64+x] and not any(0<=x+dx<64 and 0<=y+dy<64 and N[(y+dy)*64+x+dx] for dx,dy in((1,0),(-1,0),(0,1),(0,-1)))]
print('losse pixels:',iso)
# eenzame kleurpixels (geen enkele 8-buur met dezelfde kleur), alleen ter info
lone=[(x,y,names[N[y*64+x]]) for y in range(1,63) for x in range(1,63) if N[y*64+x] and all(N[(y+dy)*64+x+dx]!=N[y*64+x] for dx in(-1,0,1) for dy in(-1,0,1) if dx or dy)]
print('eenzame kleurpixels (info):',lone)
