# r9 = r8 A + kleine reparaties uit de eindkeuring (Claude, 11 px)
from PIL import Image
a=Image.open('sprite/r8/mate2_A.png'); p=a.copy()
fix={(21,34):1,            # zwarte scheiding yerba/zilver terug (r4 (23,34))
     (58,30):4,            # geen lichtste tan op de buitenrand
     (52,28):5,(53,28):5,(54,28):5,(55,28):5,(52,29):4,(53,29):4,  # rand achtersteven: één lichte band, middentint eronder
     (56,32):13,(58,34):14,(59,35):14}  # losse waterpixels bij hun vlak
for xy,c in fix.items(): p.putpixel(xy,c)
p.save('sprite/r9/mate2.png',transparency=0)
def big(im):
    im.save('/tmp/claude-0/-home-user-Pokemon-Fully-Ungrounded/eb59fc12-e21e-54d5-9c31-b287c86808be/scratchpad/t.png',transparency=0)
    t=Image.open('/tmp/claude-0/-home-user-Pokemon-Fully-Ungrounded/eb59fc12-e21e-54d5-9c31-b287c86808be/scratchpad/t.png').convert('RGBA').resize((512,512),0)
    b=Image.new('RGBA',(512,512),(235,240,235,255)); b.alpha_composite(t); return b.convert('RGB')
v=Image.new('RGB',(1034,512),'white'); v.paste(big(a),(0,0)); v.paste(big(p),(522,0)); v.save('sprite/r9/r8A_r9.png')
big(p).save('sprite/r9/mate2_8x.png')
