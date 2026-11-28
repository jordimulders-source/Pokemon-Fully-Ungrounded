import sys; from PIL import Image
R='/home/user/Pokemon-Fully-Ungrounded/'
naam=sys.argv[1]; ic=Image.open(naam+'.png').convert('RGBA'); G=(110,190,160,255)
fr=Image.open(R+'docs/concept/sprites/banette_evo/af/shuppetto.png').convert('RGBA')
c=Image.new('RGBA',(256+20+2*270,272),G); c.alpha_composite(fr.resize((256,256),0),(0,8))
for i in range(2): c.alpha_composite(ic.crop((0,32*i,32,32*i+32)).resize((256,256),0),(276+i*270,8))
c.save(naam+'_8x.png')
bur=['banette','shuppet','dusclops','mismagius','drifblim','dragapult','gengar']
v=Image.new('RGBA',(36*(len(bur)+1)+8,40),G)
for i,b in enumerate(bur): v.alpha_composite(Image.open(R+f'graphics/pokemon/{b}/icon.png').convert('RGBA').crop((0,0,32,32)),(4+36*i,4))
v.alpha_composite(ic.crop((0,0,32,32)),(4+36*len(bur),4)); v.resize((v.width*3,v.height*3),0).save(naam+'_buren3x.png')
