# naast.py: sprite 8x naast het natieve model op dezelfde schaal (8/3). python3 sprite_r8/naast.py sprite.png uit.png
import sys; sys.path.insert(0,'gereedschap'); sys.path.insert(0,'sprite_r5')
from PIL import Image; import basis as B
im=Image.open(sys.argv[1]).convert('RGBA'); bg=Image.new('RGBA',(64,64),'white'); bg.alpha_composite(im)
s=bg.convert('RGB').resize((512,512),Image.NEAREST)
u0,v0=B.blok(0,0)
m=Image.new('RGB',(192,192),'white'); m.paste(Image.fromarray(B.a.astype('uint8')),(-u0,-v0))
m=m.resize((512,512),Image.NEAREST)
out=Image.new('RGB',(1032,512),'white'); out.paste(s,(0,0)); out.paste(m,(520,0)); out.save(sys.argv[2])
