# Studie Gen 3 rots (anim_front_gba frame 1) op 5x: geodude, graveler, golem, onix, nosepass, regirock, lunatone, solrock, relicanth
from PIL import Image
G='../../../../../../graphics/pokemon/'
L=['geodude','graveler','golem','onix','nosepass','regirock','lunatone','solrock','relicanth']
o=Image.new('RGB',(64*5*5,64*5*2),'white')
for i,s in enumerate(L):
    im=Image.open(G+s+'/anim_front_gba.png').crop((0,0,64,64)); im.info['transparency']=0
    im=im.convert('RGBA'); bg=Image.new('RGBA',im.size,(255,255,255,255)); bg.alpha_composite(im)
    o.paste(bg.convert('RGB').resize((320,320),Image.NEAREST),((i%5)*320,(i//5)*320))
o.save('studie.png')
