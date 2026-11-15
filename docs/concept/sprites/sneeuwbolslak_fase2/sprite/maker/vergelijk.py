# python3 maker/vergelijk.py r.png uit.png : sprite 8x | model 8x
import sys; from PIL import Image
s=Image.open(sys.argv[1]); s=s.convert('RGBA')
bg=Image.new('RGBA',(64,64),(255,255,255,255)); bg.alpha_composite(s)
m=Image.open('meet/model_1x.png').convert('RGB')
o=Image.new('RGB',(1040,512),(255,255,255)); o.paste(bg.convert('RGB').resize((512,512),Image.NEAREST),(0,0)); o.paste(m.resize((512,512),Image.NEAREST),(528,0)); o.save(sys.argv[2])
