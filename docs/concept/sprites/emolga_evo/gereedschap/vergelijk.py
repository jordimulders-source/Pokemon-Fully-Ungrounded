# vergelijk(o, uit): sprite 4x | model op schaal 4x | sprite 1x | model 1x (wit) | sprite 1x op donker
import sys; sys.path.insert(0,'/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/emolga_evo/gereedschap')
from PIL import Image; import palet; from raster import modelcrop
def vergelijk(o,uit,S,OX,OY,model=None,z=4):
    v=Image.new('RGB',(64*z*2+8+220,64*z),'white')
    v.paste(palet.rgb(o,(255,255,255)).resize((64*z,64*z),Image.NEAREST),(0,0)); v.paste(modelcrop(S,OX,OY,0,0,64,64,z,model),(64*z+8,0))
    v.paste(palet.rgb(o,(255,255,255)),(128*z+16,0)); v.paste(modelcrop(S,OX,OY,0,0,64,64,1,model),(128*z+86,0))
    v.paste(palet.rgb(o,(40,48,56)),(128*z+156,0))
    v.save(uit)
