import sys
from PIL import Image
R='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/capybarrel/'
ims=[]
for v in sys.argv[2:]:
    im=Image.open(R+f'sprite/r1/capybarrel_{v}.png').convert('RGBA')
    bg=Image.new('RGBA',(64,64),(235,235,235,255)); bg.alpha_composite(im); ims.append(bg.convert('RGB').crop((9,26,55,60)).resize((46*10,34*10),Image.NEAREST))
m=Image.open(R+'referenties/model_r3.png').convert('RGB').crop((143,254,881,799)).resize((460,340),Image.LANCZOS)
W=Image.new('RGB',(460*(len(ims)+1)+10*len(ims),340),(255,255,255))
W.paste(m,(0,0))
for i,im in enumerate(ims): W.paste(im,((i+1)*470,0))
W.save(sys.argv[1])
