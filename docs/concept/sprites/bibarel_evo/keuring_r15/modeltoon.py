# Model-tonen binnen de vachtmasker van r15, gekwantiseerd naar c/d/f op rangorde (zelfde aantallen als r15)
from laad import *
from PIL import ImageDraw
ch='.KbcdfSCeLMogWwD'; I={c:i for i,c in enumerate(ch)}
a,p=ons('docs/concept/sprites/bibarel_evo/sprite_r15/sprite.png')
P=np.load('model_proj.npy'); Lm=P@[0.299,0.587,0.114]
fur=np.isin(a,[I['c'],I['d'],I['f']])
v=Lm[fur]; order=np.argsort(np.argsort(v)); n=len(v)
nc,nd=(a==I['c']).sum(),(a==I['d']).sum()
q=np.where(order<nc,I['c'],np.where(order<nc+nd,I['d'],I['f']))
mq=a.copy(); mq[fur]=q
np.save('model_q.npy',mq)
z=10; box=(8,5,58,62)
def big(img): return img.crop(box).resize(((box[2]-box[0])*z,(box[3]-box[1])*z),Image.NEAREST)
W=Image.new('RGB',(3*(50*z+10),57*z+20),'white'); d=ImageDraw.Draw(W)
for i,(img,t) in enumerate([(rgb(a,p),'r15'),(rgb(mq,p),'modeltonen in c/d/f (rang)'),(Image.fromarray(P.astype('uint8')),'model geprojecteerd')]):
    W.paste(big(img),(i*(50*z+10),18)); d.text((i*(50*z+10),2),t,fill='black')
W.save('/tmp/claude-0/-home-user-Pokemon-Fully-Ungrounded/7bc2735f-b867-5692-94ea-d6711f144b87/scratchpad/mq.png')
