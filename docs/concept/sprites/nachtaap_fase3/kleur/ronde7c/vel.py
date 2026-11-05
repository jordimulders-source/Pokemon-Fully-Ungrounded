# vel.png: B en 7c op 3x (licht/donker) en 1x, 8x close-up staartwortel, naast 3 GF-close-ups (8x)
from PIL import Image, ImageDraw
G='/home/user/Pokemon-Fully-Ungrounded/graphics/pokemon/'
cols=[('ronde 7 optie B','../ronde7_opties/optie_B.png'),('ronde 7c (staartwortel)','nachtaap_fase3.png')]
box=(34,24,52,44); k=8
W=Image.new('RGBA',(2*210+3*160+10,16+200+200+72+14+(box[3]-box[1])*k+8),(238,238,242,255)); d=ImageDraw.Draw(W)
for i,(lab,f) in enumerate(cols):
    im=Image.open(f).convert('RGBA'); x=i*210+8; y=4
    d.text((x,y),lab,fill=(0,0,0)); y+=14
    W.alpha_composite(im.resize((192,192),Image.NEAREST),(x,y)); y+=200
    dk=Image.new('RGBA',(192,192),(40,40,48,255)); dk.alpha_composite(im.resize((192,192),Image.NEAREST)); W.alpha_composite(dk,(x,y)); y+=200
    W.alpha_composite(im,(x,y)); dk=Image.new('RGBA',(64,64),(40,40,48,255)); dk.alpha_composite(im); W.alpha_composite(dk,(x+72,y)); y+=72
    d.text((x,y),'8x staartwortel x34-51 r24-43',fill=(0,0,0)); y+=14
    W.alpha_composite(im.crop(box).resize(((box[2]-box[0])*k,(box[3]-box[1])*k),Image.NEAREST),(x,y))
refs=[('Zangoose front 8x','zangoose/anim_front_gba.png',(36,28,54,46)),('Furret front 8x','furret/anim_front_gba.png',(14,22,32,40)),('Mightyena front 8x','mightyena/anim_front_gba.png',(38,16,56,34))]
for j,(lab,f,b) in enumerate(refs):
    x=2*210+10+j*160; y=4
    d.text((x,y),lab,fill=(0,0,0))
    W.alpha_composite(Image.open(G+f).convert('RGBA').crop(b).resize((152,152),Image.NEAREST),(x,y+14))
    W.alpha_composite(Image.open(G+f).convert('RGBA').crop((0,0,64,64)).resize((128,128),Image.NEAREST),(x,y+176))
W.save('vel.png'); print(W.size)
