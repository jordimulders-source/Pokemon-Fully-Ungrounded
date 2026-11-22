import sys; from PIL import Image
def wb(p,s):
    im=Image.open(p).convert('RGBA'); bg=Image.new('RGB',im.size,(255,255,255)); bg.paste(im,mask=im.split()[3]); return bg.resize((im.width*s,im.height*s),Image.NEAREST)
a=wb(sys.argv[1],12); b=Image.open('natief.png').crop((74,12,149,165)).resize((75*4,153*4),Image.NEAREST)
S=Image.new('RGB',(a.width+b.width+10,max(a.height,b.height)),'white'); S.paste(a,(0,0)); S.paste(b,(a.width+10,0)); S.save(sys.argv[2])
