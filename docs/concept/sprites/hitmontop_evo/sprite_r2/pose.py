# Ronde 2, stap A: POSE als silhouet, per rij met de hand opgegeven bereiken (x_van, x_tot) per onderdeel.
# Coördinaten = eindcoördinaten van ronde 2. Bevroren delen komen uit bevroren.txt.
# Letters: H haar, K hoorn, G gezicht/kin, N nek, S schouder, T romp, W vrije arm, Q vrije hand, P broek (heup),
#          L nabije been, R verre been, F nabije voet, E verre voet, A steunarm (bevroren), C cordão (bevroren)
PARTS = {
 'F': {1:[(27,33)],2:[(26,35)],3:[(27,35)],4:[(26,35)],5:[(27,35)],6:[(29,31)]},
 'L': {1:[(35,37)],2:[(34,38)],3:[(35,39)],4:[(34,40)],5:[(34,41)],6:[(35,42)],7:[(36,43)],8:[(37,45)],9:[(38,46)],
       10:[(39,47)],11:[(40,49)],12:[(41,50)],13:[(42,51)],14:[(43,51)],15:[(44,51)],16:[(46,51)],17:[(47,50)]},
 'E': {1:[(59,61)],2:[(58,62)],3:[(57,62)],4:[(57,62)],5:[(56,62)],6:[(56,61)]},
 'R': {7:[(57,61)],8:[(57,60)],9:[(56,60)],10:[(56,59)],11:[(55,59)],12:[(54,58)],13:[(54,58)],14:[(53,57)],15:[(52,57)]},
 'P': {14:[(51,52)],15:[(51,56)],16:[(50,57)],17:[(49,57)],18:[(48,58)],19:[(47,58)],20:[(46,58)],21:[(46,58)],
       22:[(46,57)],23:[(47,56)],24:[(48,55)],25:[(49,54)],26:[(50,53)],27:[(51,52)]},
 'T': {23:[(43,45)],24:[(42,46)],25:[(41,47)],26:[(41,48)],27:[(40,49)],28:[(39,49)],29:[(38,50)],30:[(38,50)],
       31:[(37,51)],32:[(36,50)],33:[(35,49)],34:[(34,48)],35:[(33,47)],36:[(32,48)],37:[(31,47)],38:[(32,46)],
       39:[(33,45)],40:[(34,44)],41:[(35,43)],42:[(36,43)]},
 'S': {41:[(33,41)],42:[(32,42)],43:[(32,41)],44:[(32,39)]},
 'N': {38:[(29,31)],39:[(29,32)],40:[(27,33)],41:[(26,33)],42:[(25,32)],43:[(25,31)]},
 'W': {17:[(41,43)],18:[(40,44)],19:[(40,45)],20:[(39,46)],21:[(38,46)],22:[(38,45)],
       23:[(38,41)],24:[(37,40)],25:[(37,40)],26:[(37,40)],27:[(36,39)],28:[(36,39)],29:[(35,38)],30:[(35,38)],
       31:[(35,37)],32:[(34,37)],33:[(34,37)]},
 'Q': {21:[(44,47)],22:[(43,48)],23:[(42,49)],24:[(42,49)],25:[(42,49)],26:[(42,49)],27:[(43,48)],28:[(44,47)]},
 'H': {25:[(13,25)],26:[(11,28)],27:[(10,29)],28:[(9,33)],29:[(9,33)],30:[(9,33)],31:[(10,17),(26,32)],
       32:[(28,32)],33:[(29,31)],34:[(29,30)]},
 'G': {42:[(10,24)],43:[(12,22)],44:[(14,20)]},
}
ORDER='RELFPTSNWQHG'
def silhouet():
    g=[['.']*64 for _ in range(64)]
    for p in ORDER:
        for y,rs in PARTS[p].items():
            for a,b in rs:
                for x in range(a,b+1): g[y][x]=p
    fr=[r.rstrip('\n') for r in open('bevroren.txt')]
    for y in range(64):
        for x in range(64):
            if fr[y][x]!='.':
                g[y][x]='A' if y>=45 else ('C' if x>=48 else ('K' if y<27 else 'G'))
    # gezicht: alles binnen de gezichtsomtrek van de bevroren rijen 31-41 is G (ook waar haar zou vallen)
    return g
COL={'.':(255,255,255),'H':(120,80,40),'K':(240,200,140),'G':(222,189,131),'N':(200,160,110),'S':(205,165,115),
     'T':(215,175,120),'W':(170,120,70),'Q':(250,220,160),'P':(70,110,200),'L':(98,156,222),'R':(60,90,160),
     'F':(139,189,238),'E':(110,150,210),'A':(230,190,130),'C':(197,74,49)}
if __name__=='__main__':
    from PIL import Image, ImageDraw
    g=silhouet()
    open('pose_silhouet.txt','w').write('\n'.join(''.join(r) for r in g)+'\n')
    sil=Image.new('RGB',(64,64),(255,255,255)); kl=Image.new('RGB',(64,64),(255,255,255))
    for y in range(64):
        for x in range(64):
            if g[y][x]!='.': sil.putpixel((x,y),(20,20,20)); kl.putpixel((x,y),COL[g[y][x]])
    foto=Image.open('../referenties/pose_eenhandsstand.webp').convert('RGB').transpose(Image.FLIP_LEFT_RIGHT)
    foto=foto.crop((0,0,foto.width,int(foto.height*0.93)))
    fh=512; fw=int(foto.width*fh/foto.height); foto=foto.resize((fw,fh))
    W=Image.new('RGB',(fw+512*2+40+200,560),(235,235,240)); d=ImageDraw.Draw(W)
    W.paste(foto,(0,40)); W.paste(sil.resize((512,512),Image.NEAREST),(fw+20,40)); W.paste(kl.resize((512,512),Image.NEAREST),(fw+40+512,40))
    for i,im in enumerate([sil,kl]): W.paste(im,(fw+40+1024+20,40+i*80)); W.paste(im.resize((128,128),Image.NEAREST),(fw+40+1024+20+70,40+i*150) if False else (fw+40+1024+40+64,40+i*140))
    d.text((4,8),'posefoto, gespiegeld',fill=(0,0,0)); d.text((fw+24,8),'silhouet 8x',fill=(0,0,0)); d.text((fw+44+512,8),'onderdelen 8x',fill=(0,0,0)); d.text((fw+40+1024+20,8),'1x / 2x',fill=(0,0,0))
    W.save('pose_silhouet.png')
