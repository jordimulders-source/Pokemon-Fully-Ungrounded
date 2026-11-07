from PIL import Image
base=Image.open('../../kleur/ronde7c/nachtaap_fase3.png'); b=base.load()
for f in ['optie_A.png','optie_B.png']:
    im=Image.open(f); a=im.load()
    assert im.getpalette()==base.getpalette()
    alpha=sum((a[x,y]==0)!=(b[x,y]==0) for x in range(64) for y in range(64))
    ch=[(x,y) for x in range(64) for y in range(64) if a[x,y]!=b[x,y]]
    xs=[c[0] for c in ch]; ys=[c[1] for c in ch]
    buiten=[c for c in ch if not (23<=c[0]<=42 and 30<=c[1]<=46) or (c[0]>=32 and c[1]>=45) or (c[0]>=37 and c[1]>=44)]
    nieuw={a[x,y] for x,y in ch}
    open_=[(x,y) for x,y in ch if any(not(0<=x+dx<64 and 0<=y+dy<64) or a[x+dx,y+dy]==0 for dx,dy in((1,0),(-1,0),(0,1),(0,-1)))]
    # losse pixels: bandpixel zonder bandburen (4-buren)
    los=[(x,y) for x,y in ch if not any((x+dx,y+dy) in set(ch) for dx,dy in((1,0),(-1,0),(0,1),(0,-1)))]
    print(f,'gewijzigd',len(ch),'x',min(xs),max(xs),'r',min(ys),max(ys),'alpha-diff',alpha,'buiten romp-zone',len(buiten),'tinten',nieuw,'open randen',len(open_),'losse px',len(los))
