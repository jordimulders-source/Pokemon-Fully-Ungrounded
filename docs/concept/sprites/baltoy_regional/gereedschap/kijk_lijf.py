import sys; sys.path.insert(0,'gereedschap'); from r4lib import rgba
from PIL import Image
L=sys.argv[1:] or list('ABC'); z=14
crop=(15+5,27+16,15+25,27+31)
out=Image.new('RGB',(len(L)*((crop[2]-crop[0])*z+10),(crop[3]-crop[1])*z),(255,255,255))
for i,k in enumerate(L):
    c=rgba(Image.open(f'sprite_r9/baltoy_r9{k}.png')).crop(crop); b=Image.new('RGBA',c.size,(255,255,255,255)); b.alpha_composite(c)
    out.paste(b.convert('RGB').resize((c.width*z,c.height*z),Image.NEAREST),(i*(c.width*z+10),0))
out.save('/tmp/claude-0/-home-user-Pokemon-Fully-Ungrounded/cc339c8a-c402-5a74-878a-f7e0da92c812/scratchpad/lijf.png')
