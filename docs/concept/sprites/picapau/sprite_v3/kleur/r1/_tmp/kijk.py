from PIL import Image
import sys
ims=[]
for f in sys.argv[2:]:
    p=Image.open(f); p.info['transparency']=0
    im=p.convert('RGBA'); bg=Image.new('RGBA',im.size,(255,255,255,255)); bg.alpha_composite(im)
    ims.append(bg.convert('RGB').crop((8,8,56,64)).resize((48*8,56*8),0))
W=Image.new('RGB',(len(ims)*(48*8+10),56*8),(180,180,180))
for i,im in enumerate(ims): W.paste(im,(i*(48*8+10),0))
W.save(sys.argv[1])
