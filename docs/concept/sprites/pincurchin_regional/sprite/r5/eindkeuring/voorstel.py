# Alleen ter vergelijking: past de voorgestelde tint-/lijnreparaties toe op een KOPIE (sprite zelf blijft ongewijzigd)
from PIL import Image
R='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/pincurchin_regional/sprite/r5/'
im=Image.open(R+'V1_oog4x5_mond+1+2.png').copy()
fix={(10,31):2,(13,40):2,(14,46):1,(15,48):1,
     (14,43):4,(14,44):3,(15,44):3,(14,45):3,(15,45):3,(16,45):3,(15,46):3,(16,46):3,(15,47):3,(16,47):3,
     (50,43):6,(52,44):6,(38,59):6,(39,61):6,
     (39,45):4,(40,45):4,(41,45):4,(42,45):4,(32,47):4,(33,47):4,(34,47):4,(45,43):2,
     (36,12):6,(10,18):6,(9,19):6}
for (x,y),v in fix.items():
    print((x,y),im.getpixel((x,y)),'->',v); im.putpixel((x,y),v)
im.save(R+'eindkeuring/voorstel.png')
im2=im.copy(); p=im2.getpalette(); p[21:24]=[156,38,42]; im2.putpalette(p); im2.save(R+'eindkeuring/voorstel_rood7.png')
S=8; W=Image.new('RGB',(64*S*3,64*S),'white')
for i,f in enumerate(['V1_oog4x5_mond+1+2.png','eindkeuring/voorstel.png','eindkeuring/voorstel_rood7.png']):
    a=Image.open(R+f).convert('RGBA'); src=Image.open(R+f); px=a.load()
    for y in range(64):
        for x in range(64):
            if src.getpixel((x,y))==0: px[x,y]=(255,255,255,255)
    W.paste(a.resize((64*S,64*S),Image.NEAREST),(64*S*i,0))
W.save(R+'eindkeuring/voor_na_8x.png')
