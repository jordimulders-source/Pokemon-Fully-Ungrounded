# r20: V-vel op 16x (r18 | r19 | r20 | r20 sterk, rode hulplijn = kolom van de r18-punt x30) + 8x + vel.png
from PIL import Image, ImageDraw
G='../../../../../../graphics/pokemon/mr_mime/'
def L(p): return Image.open(p).convert('RGBA').crop((0,0,64,64))
bg=(200,230,200,255)
def plak(ims,z,crop=None,lijn=None,lab=None):
    ims=[i.crop(crop) if crop else i for i in ims]; w,h=ims[0].size
    W=Image.new('RGBA',(len(ims)*(w*z+8),h*z+(14 if lab else 0)),bg); d=ImageDraw.Draw(W)
    for k,i in enumerate(ims):
        X=k*(w*z+8); W.paste(i.resize((w*z,h*z),Image.NEAREST),(X,0),i.resize((w*z,h*z),Image.NEAREST))
        if lijn is not None: d.line([(X+(lijn-crop[0])*z+z//2,0),(X+(lijn-crop[0])*z+z//2,h*z)],fill=(220,0,0,160),width=1)
        if lab: d.text((X+4,h*z+2),lab[k],fill=(0,0,0,255))
    return W
r20,r19,r18,st=L('bokser.png'),L('../sprite_r19/bokser.png'),L('../sprite_r18/bokser.png'),L('var/var_sterk.png')
plak([r18,r19,r20,st],16,(16,18,46,38),30,['r18 V groot','r19','r20 (hoofd)','r20 sterk']).save('v_perspectief_16x.png')
r20.resize((512,512),Image.NEAREST).save('bokser_8x.png')
plak([r20,r19,r18,L(G+'anim_front_gba.png'),L(G+'galar/front.png')],6,None,None,['r20','r19','r18','Mr. Mime','Galar']).save('vel.png')
