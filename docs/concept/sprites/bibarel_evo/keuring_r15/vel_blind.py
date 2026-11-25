from laad import *
from PIL import ImageDraw
items=[('r15',ons('docs/concept/sprites/bibarel_evo/sprite_r15/sprite.png'))]
for n in ['bibarel','ursaring','linoone','furret','swampert','sentret','teddiursa']: items.append((n,gen3(n)))
for f,n in [('mightyena_evo/af/alphyena.png','alphyena'),('dundragoon/af/dundragoon.png','dundragoon'),('gnomad/af/gnomad.png','gnomad'),('coathief/af/coathief.png','coathief'),('alpaca/af/palpaca.png','palpaca')]:
    items.append((n,ons('docs/concept/sprites/'+f)))
z=4; W=Image.new('RGB',(6*(64*z+8),2*(64*z+20)),'white'); d=ImageDraw.Draw(W)
for i,(n,(a,p)) in enumerate(items):
    X=(i%6)*(64*z+8); Y=(i//6)*(64*z+20)
    W.paste(rgb(a,p).resize((64*z,64*z),Image.NEAREST),(X,Y+16)); d.text((X,Y+2),n,fill='black')
W.save('blind_4x.png')
