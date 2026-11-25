# close-up kop op 12x: sprite | kale reductie | Capybarrel-kop | model-kop
import sys,json; from PIL import Image
R='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/capykart/'
def crop(p,box,z=12): return Image.open(p).convert('RGBA').crop(box).resize(((box[2]-box[0])*z,(box[3]-box[1])*z),Image.NEAREST)
ims=[crop(p,(10,8,46,40)) for p in sys.argv[2:]]
ims.append(crop(R+'sprite/kaal.png',(10,6,46,38)))
ims.append(crop('/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/capybarrel/af/capybarrel.png',(4,22,40,54)))
m=Image.open(R+'referenties/model_r5.png').convert('RGBA').crop((133+10*12,112+6*12+12,133+46*12,112+38*12+12)).resize((432,384))
ims.append(m)
out=Image.new('RGBA',(sum(i.width+8 for i in ims),max(i.height for i in ims)),(235,235,235,255))
x=0
for i in ims: out.alpha_composite(i,(x,0)); x+=i.width+8
out.save(sys.argv[1])
