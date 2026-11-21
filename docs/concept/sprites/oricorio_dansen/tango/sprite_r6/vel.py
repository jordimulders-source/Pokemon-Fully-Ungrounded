# vel.png r6: r6 | r5 | model (8x, model op bbox geschaald); vleugels 12x (r6 | r5 | model), franje 12x; 1x/2x op licht/donker/gevechtsgroen (A en B)
import numpy as np; from PIL import Image, ImageDraw
G=(152,208,160)
def rgba(p): return Image.open(p).convert('RGBA')
def op(im,bg,z):
    b=Image.new('RGB',(im.width*z,im.height*z),bg); r=im.resize(b.size,Image.NEAREST); b.paste(r,(0,0),r); return b
A=rgba('tango.png'); B=rgba('tango_B_lichter.png'); R5=rgba('r5_ref.png')
m=Image.open('../model/gemini_r7.png').convert('RGB'); ma=np.asarray(m); ys,xs=np.where(ma.min(2)<200)
al=np.asarray(A)[:,:,3]>0; sy,sx=np.where(al)
def model(z):
    mc=m.crop((xs.min(),ys.min(),xs.max()+1,ys.max()+1)).resize(((sx.max()-sx.min()+1)*z,(sy.max()-sy.min()+1)*z),Image.LANCZOS)
    M=Image.new('RGB',(64*z,64*z),'white'); M.paste(mc,(sx.min()*z,sy.min()*z)); return M
M8=model(8); M12=model(12)
def raster(im,z):
    d=ImageDraw.Draw(im)
    for k in range(0,im.width,z): d.line([(k,0),(k,im.height)],fill=(205,205,205))
    for k in range(0,im.height,z): d.line([(0,k),(im.width,k)],fill=(205,205,205))
    return im
W=Image.new('RGB',(3*522,30+512+30+200+200+170),(230,230,230)); d=ImageDraw.Draw(W)
for k,(im,t) in enumerate([(op(A,'white',8),'r6 tango.png (palet A_donker)'),(op(R5,'white',8),'r5'),(M8,'model gemini_r7 (zelfde schaal)')]):
    W.paste(im,(k*522,30)); d.text((k*522+4,10),t,fill='black')
y=572
for (y0,y1,x0,x1),t,xo in (((26,41,0,26),'linkervleugel 12x: r6 | r5 | model',0),((2,29,44,64),'rechtervleugel 12x: r6 | r5 | model',0)):
    pass
d.text((4,y),'linkervleugel 12x: r6 | r5 | model',fill='black')
c=(0,26,26,41); x=0
for im in (raster(op(A.crop(c),'white',12),12),raster(op(R5.crop(c),'white',12),12),raster(M12.crop(tuple(v*12 for v in c)),12)):
    W.paste(im,(x,y+16)); x+=im.width+8
y2=y+16+190; d.text((4,y2),'franje 12x: r6 | r5 | model',fill='black')
c=(10,40,48,62); x=0
for im in (raster(op(A.crop(c),'white',8),8),raster(op(R5.crop(c),'white',8),8),raster(M12.crop(tuple(v*12 for v in c)).resize((38*8,22*8)),8)):
    W.paste(im,(x,y2+16)); x+=im.width+8
d.text((960,y),'rechtervleugel 12x: r6 | r5 | model',fill='black')
c=(44,2,64,29); x=960
for im in (raster(op(A.crop(c),'white',10),10),raster(op(R5.crop(c),'white',10),10)):
    W.paste(im,(x,y+16)); x+=im.width+6
y3=y+16+290; W.paste(raster(M12.crop((44*12,2*12,64*12,29*12)).resize((200,270)),10),(960+412,y+16))
y=y2+16+190; d.text((4,y),'1x en 2x: A op wit / donker / gevechtsgroen ; B op wit / donker / gevechtsgroen',fill='black')
for i,(im,bg) in enumerate([(A,'white'),(A,(40,40,48)),(A,G),(B,'white'),(B,(40,40,48)),(B,G)]):
    W.paste(op(im,bg,1),(i*70+(30 if i>2 else 0),y+20)); W.paste(op(im,bg,2),(470+i*136,y+16))
W.save('vel.png'); print(W.size)
