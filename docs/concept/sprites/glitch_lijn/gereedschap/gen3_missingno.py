"""Gen 3-MissingNo: wat als Emerald GEEN grenscontrole had op gMonFrontPicTable.
Mechanisme (zie fase1_glitch/STUDIE.md): ongeldige soort -> pointer naar willekeurige ROM-data
-> BIOS-LZ77 pakt die data uit als sprite (grootte uit de garbage-header, back-references
kopiëren eerdere stukken) -> 2048 bytes 4bpp in de spritebuffer (nibble 0 = doorzichtig)
-> palet van index 0 (SPECIES_NONE, het ?-palet: zwart/grijs/wit), zoals MissingNo in Gen 1
het palet van index 0 (Mew) kreeg.
Gebruik: python3 gen3_missingno.py UITMAP [aantal] [rom.gba] (met ROM: steekproef van 4-byte-uitgelijnde ROM-adressen)"""
import sys, os, random
from PIL import Image, ImageDraw
REPO=os.path.abspath(os.path.join(os.path.dirname(__file__),'../../../../..'))
BRONNEN=['data/mb_berry_fix.gba','data/mb_ereader.gba']
def pal_none():
    lines=open(os.path.join(REPO,'graphics/pokemon/question_mark/circled/normal.pal')).read().split('\n')[3:19]
    return [tuple(int(v) for v in l.split()) for l in lines]
def lz77(data,pos,buf_len=2048):
    out=bytearray(buf_len); n=0
    size=int.from_bytes(data[pos+1:pos+4],'little'); p=pos+4
    limit=min(size,buf_len)
    try:
        while n<limit:
            flags=data[p]; p+=1
            for bit in range(8):
                if n>=limit: break
                if flags&(0x80>>bit):
                    b0,b1=data[p],data[p+1]; p+=2
                    ln=(b0>>4)+3; disp=((b0&0xF)<<8|b1)+1
                    for _ in range(ln):
                        if n>=limit: break
                        out[n]=out[n-disp] if n-disp>=0 else 0; n+=1
                else:
                    out[n]=data[p]; p+=1; n+=1
    except IndexError: pass
    return out,size
def render(buf,pal):
    im=Image.new('RGBA',(64,64),(0,0,0,0)); px=im.load()
    for t in range(64):
        tx,ty=t%8,t//8
        for i in range(32):
            b=buf[t*32+i]
            for k,v in enumerate((b&0xF,b>>4)):
                if v: px[tx*8+(i*2+k)%8, ty*8+(i*2+k)//8]=pal[v]+(255,)
    return im
def score(im):
    a=[im.getpixel((x,y))[3]>0 for y in range(64) for x in range(64)]
    f=sum(a)/4096
    rows=[sum(a[y*64:(y+1)*64]) for y in range(64)]
    return f, len(set(rows))
if __name__=='__main__':
    uit=sys.argv[1]; aantal=int(sys.argv[2]) if len(sys.argv)>2 else 40
    os.makedirs(uit,exist_ok=True); pal=pal_none(); kand=[]
    rom=sys.argv[3] if len(sys.argv)>3 else None
    for bron in ([rom] if rom else BRONNEN):
        data=open(bron if rom else os.path.join(REPO,bron),'rb').read()
        r=random.Random(7)
        posities=sorted(r.randrange(0,len(data)-4096)//4*4 for _ in range(60000)) if rom else range(0,len(data)-8,4)
        if rom: bron=os.path.basename(rom)
        for pos in posities:
            buf,size=lz77(data,pos); im=render(buf,pal); f,v=score(im)
            if 0.12<f<0.6 and v>20: kand.append((bron,pos,size,f,im))
    random.Random(1).shuffle(kand); kand=kand[:aantal]
    cols=8; rows=(len(kand)+cols-1)//cols
    sheet=Image.new('RGB',(cols*76,rows*84),(255,255,255)); d=ImageDraw.Draw(sheet)
    for i,(bron,pos,size,f,im) in enumerate(kand):
        x,y=(i%cols)*76+6,(i//cols)*84+4
        sheet.paste(im,(x,y),im); d.text((x,y+66),str(i+1),fill=(200,0,0))
        im.save(f'{uit}/k{i+1:02d}.png')
    with open(f'{uit}/kandidaten.txt','w') as fh:
        for i,(bron,pos,size,f,im) in enumerate(kand): fh.write(f'{i+1}\t{bron}\t0x{pos:X}\tsize={size}\tvulling={f:.2f}\n')
    sheet.resize((sheet.size[0]*2,sheet.size[1]*2),Image.NEAREST).save(f'{uit}/vel.png')
    print(len(kand))
