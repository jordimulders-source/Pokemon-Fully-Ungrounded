from PIL import Image, ImageDraw
G=(152,208,160,255)
r9=Image.open('../sprite_r9/gnomad.png'); r10=Image.open('gnomad.png')
a,o=r9.load(),r10.load()
assert r9.getpalette()==r10.getpalette()
ch=[(x,y) for y in range(64) for x in range(64) if a[x,y]!=o[x,y]]
def on(im,bg,k):
    b=Image.new('RGBA',(64,64),bg); b.alpha_composite(im.convert('RGBA')); return b.resize((64*k,64*k),0).convert('RGB')
on(r10,G,8).save('gnomad_8x.png')
A,R=on(r9,G,8),on(r10,G,8); D=R.copy(); d=ImageDraw.Draw(D)
for x,y in ch: d.rectangle([x*8,y*8,x*8+7,y*8+7],outline=(255,0,255),width=2)
V=Image.new('RGB',(512*3+32,512+24),G[:3]); dv=ImageDraw.Draw(V)
for i,(im,t) in enumerate([(A,'r9'),(R,'r10'),(D,'r10, gewijzigd = magenta kader (%d px)'%len(ch))]):
    V.paste(im,(i*528,24)); dv.text((i*528+6,6),t,fill='black')
V.save('vergelijk_8x.png')
W=Image.new('RGB',(64+192+64+192+50,192+20),(128,128,128))
x=10
for bg in [(0,0,0,255),(255,255,255,255)]:
    W.paste(on(r10,bg,1),(x,10)); x+=74
    W.paste(on(r10,bg,3),(x,10)); x+=202
W.save('donker_1x.png')
print(len(ch))
