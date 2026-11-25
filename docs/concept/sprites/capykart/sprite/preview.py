# snelle preview: sprite(s) op 8x naast model verkleind
import sys; from PIL import Image
R='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/capykart/'
ims=[Image.open(p).convert('RGBA') for p in sys.argv[2:]]
m=Image.open(R+'referenties/model_r5.png').convert('RGBA').resize((512,512),Image.LANCZOS)
out=Image.new('RGBA',(520*(len(ims)+1),520),(235,235,235,255))
for i,im in enumerate(ims): out.alpha_composite(im.resize((512,512),Image.NEAREST),(i*520,0))
out.alpha_composite(m,(len(ims)*520,0)); out.save(sys.argv[1])
