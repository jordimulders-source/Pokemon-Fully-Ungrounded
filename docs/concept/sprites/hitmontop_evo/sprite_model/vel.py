from PIL import Image, ImageDraw
src=Image.open('../referenties/model_gemini_pose_v3.png').convert('RGB')
m=src.resize((int(765*512/1024),512),Image.LANCZOS)
sp=Image.open('sprite.png'); ta=Image.open('../../../../../graphics/pokemon/hitmontop/anim_front_gba.png').crop((0,0,64,64))
pl=[int(v) for l in open('../../../../../graphics/pokemon/hitmontop/normal_gba.pal').read().split('\n')[3:19] for v in l.split()]
ta.putpalette(pl); ta=ta.convert('RGB')
V=Image.new('RGB',(m.width+512+512+70,560),'white'); d=ImageDraw.Draw(V)
V.paste(m,(10,30)); V.paste(sp.resize((512,512),Image.NEAREST),(m.width+20,30))
V.paste(ta.resize((256,256),Image.NEAREST),(m.width+542,30)); V.paste(sp.resize((256,256),Image.NEAREST),(m.width+542+256,30))
V.paste(ta,(m.width+542,300)); V.paste(sp,(m.width+542+70,300))
d.text((10,10),'model v3 (bron)',fill='black'); d.text((m.width+20,10),'sprite ronde 1 (8x), silhouet D',fill='black')
d.text((m.width+542,10),'Hitmontop | evolutie (4x, 1x)',fill='black')
V.save('vel_r1.png')
