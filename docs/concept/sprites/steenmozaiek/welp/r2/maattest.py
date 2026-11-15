# Maattest-vel: model | per maat 46/50/54 de kale reductie op 6x en 1x; boven = puur vlakgemiddelde (red_), onder = met kenmerkregel (red2_)
from PIL import Image, ImageDraw
M=Image.open('natief_q.png').convert('RGBA'); mh=300
M2=M.resize((int(M.width*mh/M.height),mh),Image.NEAREST)
rows=[]
for pre,lab in (('red_','vlakgemiddelde'),('red2_','vlakgemiddelde + kenmerkregel')):
    tiles=[]
    for tw in (46,50,54):
        r=Image.open(f'{pre}{tw}.png').convert('RGBA')
        bg=Image.new('RGBA',(r.width*6,r.height*6),(235,235,225,255)); bg.alpha_composite(r.resize(bg.size,Image.NEAREST))
        one=Image.new('RGBA',(64,64),(235,235,225,255)); one.alpha_composite(r,((64-r.width)//2,63-r.height))
        t=Image.new('RGBA',(bg.width+80,mh+20),(255,255,255,255)); t.alpha_composite(bg,(0,0)); t.alpha_composite(one,(bg.width+8,0))
        ImageDraw.Draw(t).text((2,mh+5),f'{tw} px breed, {lab}',fill=(0,0,0)); tiles.append(t)
    rows.append(tiles)
W=M2.width+10+sum(t.width+10 for t in rows[0]); out=Image.new('RGBA',(W,2*(mh+20)+10),(255,255,255,255))
out.alpha_composite(M2,(0,0))
for k,tiles in enumerate(rows):
    x=M2.width+10
    for t in tiles: out.alpha_composite(t,(x,k*(mh+30))); x+=t.width+10
out.save('maattest_vel.png')
