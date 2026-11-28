import sys; from PIL import Image
R='/home/user/Pokemon-Fully-Ungrounded/'
naam=sys.argv[1]; ic=Image.open(naam+'.png').convert('RGBA')
nat=Image.open('natief.png').convert('RGBA').crop((10,8,54,52))
G=(110,190,160,255)
c=Image.new('RGBA',(44*6+20+2*270,280),G)
c.paste(nat.resize((264,264),0),(0,8))
for i in range(2): c.alpha_composite(ic.crop((0,32*i,32,32*i+32)).resize((256,256),0),(284+i*270,12))
c.save(naam+'_8x.png')
bur=['pikachu','dedenne','pachirisu','jigglypuff','clefairy','togedemaru','marill']
v=Image.new('RGBA',(36*(len(bur)+1)+8,40),G)
for i,b in enumerate(bur): v.alpha_composite(Image.open(R+f'graphics/pokemon/{b}/icon.png').convert('RGBA').crop((0,0,32,32)),(4+36*i,4))
v.alpha_composite(ic.crop((0,0,32,32)),(4+36*len(bur),4))
v.resize((v.width*3,v.height*3),0).save(naam+'_buren3x.png')
