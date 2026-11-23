# mg.py: modeluitsnede met spriteraster (gedeelde geometrie) naast de sprite, voor metingen. mg.py sprite.png X0 Y0 X1 Y1 uit.png [model]
import sys; from PIL import Image, ImageDraw
sys.path.insert(0,'../sprite'); from kijk import sprite
P=8.1; S=4
def mg(sp,X0,Y0,X1,Y1,out,model='../r3/gemini_r3_lijf.png'):
    a=Image.open(model).convert('RGB')
    x0=512+(X0-32)*P; y0=523-(60-Y0)*P; x1=512+(X1-32)*P; y1=523-(60-Y1)*P
    W=int((X1-X0)*P*S); H=int((Y1-Y0)*P*S)
    c=a.crop((int(round(x0)),int(round(y0)),int(round(x1)),int(round(y1)))).resize((W,H),Image.LANCZOS)
    s=sprite(sp).crop((X0,Y0,X1,Y1)).resize((W,H),Image.NEAREST)
    V=Image.new('RGB',(2*W+8,H),'white'); V.paste(s,(0,0)); V.paste(c,(W+8,0)); d=ImageDraw.Draw(V)
    for off in (0,W+8):
        for X in range(X0,X1+1):
            x=off+(X-X0)*P*S; d.line([(x,0),(x,H)],fill=(255,0,0) if X%5==0 else (255,190,190))
        for Y in range(Y0,Y1+1):
            y=(Y-Y0)*P*S; d.line([(off,y),(off+W,y)],fill=(255,0,0) if Y%5==0 else (255,190,190))
    V.save(out)
if __name__=='__main__':
    mg(sys.argv[1],*map(int,sys.argv[2:6]),sys.argv[6],*(sys.argv[7:8]))
