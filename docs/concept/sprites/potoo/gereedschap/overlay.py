# overlay.py ronde uit.png: model op 8x met de donkere spritepixels (lijnen) als magenta stippen erover, en sprite-silhouetrand in rood
import sys,json,numpy as np; from PIL import Image
P='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/potoo/'
k=json.load(open(P+'gereedschap/kader.json')); X0,Y0,s=k['x0'],k['y0'],k['s']
im=Image.open(P+'model/model_lijf_30.png'); bg=Image.new('RGBA',im.size,(64,160,64,255)); bg.alpha_composite(im)
o=np.asarray(bg.convert('RGB').crop((int(X0),int(Y0),int(X0+64*s),int(Y0+64*s))).resize((512,512),Image.LANCZOS)).copy()
sp=np.asarray(Image.open(P+sys.argv[1]+'/potoo.png').convert('RGBA')).astype(int)
dark=(sp[...,3]>0)&(sp[...,:3].mean(2)<70)
for y,x in zip(*np.where(dark)): o[y*8+3:y*8+5,x*8+3:x*8+5]=[255,0,255]
Image.fromarray(o.astype('uint8')).save(sys.argv[2])
