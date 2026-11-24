from PIL import Image, ImageDraw
src='sprite_r10/A0.png'; a=Image.open(src); im=a.copy()
R={33:(41,'8888aaa'),34:(41,'889aa'),35:(41,'899aa'),36:(40,'89998aa'),37:(39,'8999888a'),
   38:(39,'899888a'),39:(38,'898888a'),40:(37,'88888a'),41:(36,'888a'),42:(35,'888 a'.replace(' ','8')),
   43:(34,'88988'),44:(33,'89988'),45:(32,'99998')}
# kolom-check: alleen zilver/wit (8,9,10) mag veranderen
n=0
for y,(x0,s) in R.items():
    for k,ch in enumerate(s):
        x=x0+k; cur=a.getpixel((x,y)); assert cur in (8,9,10),(x,y,cur)
        new=int(ch,16)
        if cur!=new: im.putpixel((x,y),new); n+=1
# zone-check: geen pixel buiten x32-47,y33-45 veranderd
for y in range(64):
    for x in range(64):
        if a.getpixel((x,y))!=im.getpixel((x,y)): assert 32<=x<=47 and 33<=y<=45
M=lambda i,v:[i.getpixel((x,y))==v for y in range(64) for x in range(64)]
assert M(a,0)==M(im,0) and M(a,1)==M(im,1)
im.save('sprite_r11/A0.png',transparency=0); print(n,'pixels gewijzigd; masker+omlijning identiek; alles binnen x32-47,y33-45')
z=16; box=(28,28,52,52)
W=Image.new('RGBA',(2*24*z+16+300,24*z),(236,236,236,255)); d=ImageDraw.Draw(W)
for i,f in enumerate([src,'sprite_r11/A0.png']):
    c=Image.open(f).convert('RGBA').crop(box).resize((24*z,24*z),0); W.paste(c,(i*(24*z+16),0),c)
x0=2*24*z+32
for j,(bg,f) in enumerate([((248,248,248),src),((248,248,248),'sprite_r11/A0.png'),((24,24,32),src),((24,24,32),'sprite_r11/A0.png')]):
    bx=x0+(j%2)*130; by=10+(j//2)*130
    d.rectangle([bx,by,bx+119,by+119],fill=bg); s1=Image.open(f).convert('RGBA'); W.paste(s1,(bx+28,by+28),s1)
d.text((x0,280),'1x: r10 | r11 (licht/donker)',fill=(0,0,0)); d.text((x0,300),'links r10, rechts r11 (16x)',fill=(0,0,0))
W.save('sprite_r11/closeup.png'); W.save('/tmp/claude-0/-home-user-Pokemon-Fully-Ungrounded/df5125ac-9381-5d71-af17-ce82baab011f/scratchpad/c11.png')
