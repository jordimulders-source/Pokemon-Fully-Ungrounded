import sys; sys.path.insert(0,'gereedschap'); from r4lib import rgba
from PIL import Image, ImageDraw
L=sys.argv[1:] or list('ABC')
ims=[rgba(Image.open(f'sprite_r9/baltoy_r9{k}.png')) for k in L]
crop=(15+2,27,15+33,27+37)  # figuur
W=(crop[2]-crop[0]); H=crop[3]-crop[1]; z=8
vel=Image.new('RGB',(len(ims)*(W*z+20)+20, H*z+40+H*3+20),(255,255,255)); d=ImageDraw.Draw(vel)
for i,(k,im) in enumerate(zip(L,ims)):
    c=im.crop(crop); x=20+i*(W*z+20)
    b=Image.new('RGBA',c.size,(255,255,255,255)); b.alpha_composite(c); vel.paste(b.convert('RGB').resize((W*z,H*z),Image.NEAREST),(x,30)); d.text((x,8),k,fill=(0,0,0))
    for j,bg in enumerate([(255,255,255),(48,48,56)]):
        for zz,off in ((1,0),(2,40)):
            b=Image.new('RGBA',c.size,bg+(255,)); b.alpha_composite(c); b=b.convert('RGB').resize((W*zz,H*zz),Image.NEAREST)
            vel.paste(b,(x+off+j*110,H*z+40))
vel.save(sys.argv[0].replace('kijk_r9.py','')+'../sprite_r9/werk.png' if False else '/tmp/claude-0/-home-user-Pokemon-Fully-Ungrounded/cc339c8a-c402-5a74-878a-f7e0da92c812/scratchpad/werk.png')
