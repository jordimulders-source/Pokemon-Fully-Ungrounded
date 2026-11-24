from PIL import Image, ImageDraw
src='tempel.png'; K9='../k9/tempel.png'; K8='../k8/tempel.png'
M=Image.open('../../referenties/model.webp').convert('RGB'); s=(983-46)/62
def mcrop(x0,y0,x1,y1,z):
    return M.crop((int(46+(x0-1)*s),int(57+(y0-3)*s),int(46+(x1-1)*s),int(57+(y1-3)*s))).resize(((x1-x0)*z,(y1-y0)*z),Image.LANCZOS)
def op(p,bg,box=(0,0,64,64),z=8):
    im=Image.open(p).convert('RGBA').crop(box); b=Image.new('RGBA',im.size,bg+(255,)); b.alpha_composite(im)
    return b.convert('RGB').resize(((box[2]-box[0])*z,(box[3]-box[1])*z),Image.NEAREST)
WB=(44,14,63,60); FB=(6,34,32,62)
wW=(WB[2]-WB[0])*12; hW=(WB[3]-WB[1])*12; wF=(FB[2]-FB[0])*12; hF=(FB[3]-FB[1])*12
W=4*(wW+10)+10
V=Image.new('RGB',(max(3*522+10,W, 2*(wF+10)+10),24+512+40+hW+40+hF+40+160),(236,236,236)); d=ImageDraw.Draw(V)
for i,(p,t) in enumerate([(src,'k10 (nieuw)'),(K9,'k9')]): V.paste(op(p,(255,255,255)),(10+i*522,24)); d.text((10+i*522,6),t+' 8x',fill=(0,0,0))
V.paste(mcrop(0,0,64,64,8),(1054,24)); d.text((1054,6),'model 8x',fill=(0,0,0))
y=24+512+30
d.text((10,y-16),'bergwand 12x (x44-62,y14-59): k10 | k9 | k8 | model',fill=(0,0,0))
for i,im in enumerate([op(src,(255,255,255),WB,12),op(K9,(255,255,255),WB,12),op(K8,(255,255,255),WB,12),mcrop(*WB,12)]): V.paste(im,(10+i*(wW+10),y))
y+=hW+30
d.text((10,y-16),'gezicht + poort 12x (x6-31,y34-61): k9 | k10 (latei steekt rechts 2 px uit) | model',fill=(0,0,0))
for i,im in enumerate([op(K9,(255,255,255),FB,12),op(src,(255,255,255),FB,12),mcrop(*FB,12)]): V.paste(im,(10+i*(wF+10),y))
y+=hF+30
d.text((10,y-16),'1x op licht en donker: k10 | k9 ; rechts k10 2x',fill=(0,0,0))
for j,c in enumerate([(255,255,255),(232,232,224),(40,40,48),(16,16,20)]):
    V.paste(op(src,c,z=1),(10+j*70,y)); V.paste(op(K9,c,z=1),(300+j*70,y)); V.paste(op(src,c,z=2),(600+j*136,y))
V.save('vel.png'); print(V.size)
