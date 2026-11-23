# vel(rijen, uit): per sprite een rij: sprite 8x | model op dezelfde schaal 8x | gezicht 12x (sprite | model) | 1x op licht en donker
import sys; sys.path.insert(0,'/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/emolga_evo/gereedschap')
from PIL import Image, ImageDraw; import numpy as np; import palet; from raster import modelcrop, grid
def rij(o,naam,S,OX,OY,model,gez):
    x0,y0,x1,y1=gez
    sp=palet.rgb(o,(255,255,255)).resize((512,512),Image.NEAREST)
    mc=modelcrop(S,OX,OY,0,0,64,64,8,model)
    z=12
    gs=grid(palet.rgb(o[y0:y1,x0:x1],(255,255,255)).resize(((x1-x0)*z,(y1-y0)*z),Image.NEAREST),x0,y0,z,(220,220,220))
    gm=grid(modelcrop(S,OX,OY,x0,y0,x1,y1,z,model),x0,y0,z,(255,180,180))
    W=512*2+16+gs.width*2+8+16+64*2+24; H=max(512,gs.height)+20
    v=Image.new('RGB',(W,H),'white'); d=ImageDraw.Draw(v)
    d.text((2,2),naam+' 8x | model op dezelfde schaal 8x | gezicht 12x (sprite | model) | 1x licht, donker',fill=(0,0,0))
    v.paste(sp,(0,18)); v.paste(mc,(528,18)); x=1056; v.paste(gs,(x,18)); v.paste(gm,(x+gs.width+8,18)); x+=gs.width*2+24
    for i,bg in enumerate([(232,232,216),(40,48,56)]): v.paste(palet.rgb(o,bg),(x+i*72,18))
    return v
def vel(rijen,uit):
    ims=[rij(*r) for r in rijen]; W=max(i.width for i in ims); H=sum(i.height for i in ims)
    v=Image.new('RGB',(W,H),'white'); y=0
    for i in ims: v.paste(i,(0,y)); y+=i.height
    v.save(uit); return v.size
