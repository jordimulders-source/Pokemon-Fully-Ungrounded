import sys
sys.path.insert(0,'.')
from PIL import Image
import palet
H='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/kolibrie_pre/blender/A/kleur_r4/'
im=palet.build(H+'raster.txt',H+'kolibrie_pre.png').convert('RGBA')
c=im.crop((8,10,50,48)).resize((42*10,38*10),Image.NEAREST)
out=Image.new('RGBA',(42*10*2+20+84*2,38*10),(200,200,200,255))
bg=Image.new('RGBA',c.size,(235,235,235,255)); bg.alpha_composite(c); out.paste(bg,(0,0))
r3=Image.open(H+'../kleur_r3/kolibrie_pre.png').convert('RGBA').crop((8,10,50,48)).resize((420,380),Image.NEAREST)
bg=Image.new('RGBA',r3.size,(235,235,235,255)); bg.alpha_composite(r3); out.paste(bg,(430,0))
s=im.crop((8,10,50,48)).resize((84,76),Image.NEAREST); bg=Image.new('RGBA',s.size,(235,235,235,255)); bg.alpha_composite(s); out.paste(bg,(860,0))
s1=im.crop((8,10,50,48)); bg=Image.new('RGBA',s1.size,(235,235,235,255)); bg.alpha_composite(s1); out.paste(bg,(860,100))
out.save(sys.argv[1])
