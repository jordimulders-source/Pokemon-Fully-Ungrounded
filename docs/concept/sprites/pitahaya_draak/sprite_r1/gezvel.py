# gezicht-vergelijking: sprite (crop) op z x naast natief model op dezelfde plek (elke spritepixel = 3x3 natief)
import sys,numpy as np; from PIL import Image, ImageDraw
def paar(sp,info,X0,Y0,X1,Y1,z=10):
    OY,OX,ymin,xmin,y0,x0=np.load(info)['geo']
    n=Image.open('natief.png').convert('RGB'); s=Image.open(sp)
    b=Image.new('RGBA',(64,64),(214,222,214,255)); b.alpha_composite(s.convert('RGBA'))
    gs=b.convert('RGB').crop((X0,Y0,X1,Y1)).resize(((X1-X0)*z,(Y1-Y0)*z),Image.NEAREST)
    nx=OX+3*(xmin-x0); ny=OY+3*(ymin-y0)
    gm=n.crop((nx+3*X0,ny+3*Y0,nx+3*X1,ny+3*Y1)).resize(gs.size,Image.NEAREST)
    return gs,gm
if __name__=='__main__':
    X0,Y0,X1,Y1=17,20,47,40; z=8
    fs=sys.argv[1:]; rows=[]
    for f in fs: rows.append(paar(f,f[:-4]+'_info.npz',X0,Y0,X1,Y1,z))
    W,Hh=rows[0][0].size; v=Image.new('RGB',(2*W+30,len(rows)*(Hh+16)),'white'); d=ImageDraw.Draw(v)
    for k,(a,b) in enumerate(rows):
        v.paste(a,(0,k*(Hh+16)+14)); v.paste(b,(W+10,k*(Hh+16)+14)); d.text((0,k*(Hh+16)),fs[k],fill='black')
    v.save('/tmp/claude-0/-home-user-Pokemon-Fully-Ungrounded/cfff8772-8395-516e-9e06-8a26124b2eaf/scratchpad/gez.png')
