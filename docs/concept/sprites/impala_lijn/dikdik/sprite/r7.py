# r7: oogvarianten op r6 (donker brons). Alleen oogzone abs x21-29, y24-32 (lokaal x11-19, y18-26); diff 0 erbuiten.
import json, numpy as np
from PIL import Image, ImageDraw
src=json.load(open('r6/grid.json')); OX,OY=src['OX'],src['OY']; R=src['grid']; H=len(R); W=len(R[0])
G='/home/user/Pokemon-Fully-Ungrounded/graphics/pokemon/'
def gen3(naam,x0,y0,kaart):   # 4x4 oog 1-op-1 uit anim_front_gba.png, index -> ons palet
    a=np.asarray(Image.open(G+naam+'/anim_front_gba.png'))
    return [''.join(kaart[int(a[y0+j,x0+i])] for i in range(4)) for j in range(4)]
# Pichu oog x32-35 y27-30: 15 zwart->0, 1 wit->C, 13 grijs->D (iris), 3 huid (hoeken)->0 (donkere binnenkant van onze ring)
PICHU=gen3('pichu',32,27,{15:'0',1:'C',13:'D',3:'0',2:'0',4:'0'})
# Igglybuff oog x33-36 y29-32: 15 zwart->0, 1 wit->C, 13 donkerrood->D, 6 roodbruin->S, 2/4/9 huid/blos (hoeken)->0
IGGLY=gen3('igglybuff',33,29,{15:'0',1:'C',13:'D',6:'S',2:'0',4:'0',9:'0',10:'0'})
VAR={'A':[], 'B':[(15,22,'0'),(14,23,'C')], 'C':[(15,22,'0'),(16,23,'C')],
     'D':[(14,21,'C'),(15,21,'C'),(14,22,'C'),(15,22,'C')],
     'E':[(14+i,21+j,PICHU[j][i]) for j in range(4) for i in range(4)],
     'F':[(14+i,21+j,IGGLY[j][i]) for j in range(4) for i in range(4)]}
print('Pichu',PICHU,'Igglybuff',IGGLY)
PAL={'.':(0,0,0),'0':(24,16,20),'D':(66,34,18),'S':(108,58,26),'M':(160,92,40),'L':(194,120,56),'C':(244,221,190),'c':(212,174,132),
     'N':(106,76,64),'n':(140,110,94),'H':(132,102,70),'h':(184,148,106),'I':(62,66,78),'J':(86,92,104),'K':(110,116,128),'w':(92,68,44)}
ORDER=list(PAL); sprites={}
for v,ch in VAR.items():
    g=[list(r) for r in R]; n=0
    for x,y,c in ch:
        assert 11<=x<=19 and 18<=y<=26
        if g[y][x]!=c: g[y][x]=c; n+=1
    buiten=sum(1 for y in range(H) for x in range(W) if g[y][x]!=R[y][x] and not (11<=x<=19 and 18<=y<=26))
    traan=g[24][13] in 'D0' and g[24][12]=='D'
    print(v,'gewijzigd',n,'diff buiten oogzone',buiten,'traanvlek sluit aan',traan)
    for y in range(19,26): print('    %2d '%(y+OY)+''.join(g[y][11:20]))
    img=np.zeros((64,64),'uint8')
    for y in range(H):
        for x in range(W): img[OY+y,OX+x]=ORDER.index(g[y][x])
    pal=[]; [pal.extend(PAL[k]) for k in ORDER]
    im=Image.fromarray(img,'P'); im.putpalette(pal); im.save(f'r7/dikdik_r7_{v}.png',transparency=0)
    s=Image.open(f'r7/dikdik_r7_{v}.png').convert('RGBA'); s.resize((512,512),Image.NEAREST).save(f'r7/dikdik_r7_{v}_8x.png'); sprites[v]=s
# vel: kop 8x per variant met letter, daaronder alle varianten 1x op licht en donker
kx0,ky0,kx1,ky1=OX+2,OY+10,OX+26,OY+34; Z=8; tw=(kx1-kx0)*Z
V=Image.new('RGBA',(max(3*(tw+12)+10,6*146+20),2*(tw+30)+110),(236,236,236,255)); d=ImageDraw.Draw(V)
for i,(v,s) in enumerate(sprites.items()):
    t=s.crop((kx0,ky0,kx1,ky1)).resize((tw,tw),Image.NEAREST); x=10+(i%3)*(tw+12); y=10+(i//3)*(tw+30)
    V.paste(t,(x,y),t); d.text((x+tw//2,y+tw+6),v,fill=(0,0,0))
y=10+2*(tw+30); x=10
for v,s in sprites.items():
    for bg in [(248,248,248,255),(40,40,48,255)]:
        t=Image.new('RGBA',(68,68),bg); t.paste(s,(2,2),s); V.paste(t,(x,y)); x+=70
    d.text((x-80,y+70),v,fill=(0,0,0)); x+=6
V.save('r7/oog_varianten.png')
