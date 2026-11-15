# Ronde 2 (eenmalig): oude manen wissen, met de hand getekende maangrids plaatsen, wervel opnieuw (handwerk; geen inkleuring per script)
R=[list(l.rstrip('\n')) for l in open('raster.txt')]
# bolrand (spans uit ronde 1): x-links/x-rechts per rij
SP={13:(25,35),14:(22,38),15:(20,40),16:(18,42),17:(17,43),18:(16,44),19:(15,45),20:(14,46),21:(13,47),22:(12,48),23:(11,49),24:(11,49),25:(10,50),26:(10,50),27:(9,51),28:(9,51),29:(9,51),
    41:(9,51),42:(9,51),43:(9,51),44:(10,50),45:(10,50),46:(11,49),47:(11,49),48:(12,48),49:(13,47),50:(14,46),51:(15,45),52:(16,44),53:(17,43),54:(18,42),55:(20,40),56:(22,38),57:(25,35)}
for y in range(30,41): SP[y]=(8,52)
def inbol(x,y): return y in SP and SP[y][0]<=x<=SP[y][1]
LOB={(x,y) for y,(a,b) in {19:(47,55),20:(46,56),21:(47,54),22:(48,53),23:(49,52),24:(49,51),25:(50,51)}.items() for x in range(a,b+1)}
# wissen: grijs overal; omlijning '1' buiten bol en gaslob in de maangebieden
for y in range(64):
    for x in range(64):
        c=R[y][x]
        maan=(y<=11 and 23<=x<=38) or (20<=y<=32 and x>=50) or (40<=y<=52 and x<=13) or (y>=49 and x>=40)
        if c in 'def' or (maan and c=='1' and not inbol(x,y) and (x,y) not in LOB): R[y][x]='.'
# bol herstellen onder de oude hand rechtsonder (lijfrijen ronde 1)
for x,y,c in [(44,50,'2'),(45,50,'2'),(46,50,'1'),(43,51,'2'),(44,51,'2'),(45,51,'1'),(42,52,'3'),(43,52,'2'),(44,52,'1'),(41,53,'4'),(42,53,'4'),(43,53,'1'),(40,54,'4'),(41,54,'1'),(42,54,'1')]:
    R[y][x]=c
def plaats(x0,y0,grid,mode):
    for j,row in enumerate(grid):
        for i,c in enumerate(row):
            if c=='.': continue
            x,y=x0+i,y0+j
            if mode=='onder' and R[y][x]!='.': continue
            R[y][x]=c
A=["....fff.....",
   "...fdddfff..",
   "...fdddddd1.",
   ".ff111ddddd1",
   "fddddddddde1",
   "fdddddddffe1",
   ".1111edddee1",
   "...fdddddee1",
   "..fdddddeee1",
   "..1ddeeeeee1",
   "...111eeee1.",
   "......1111.."]
C=["..11fffff...",
   ".1ddddddd1..",
   "1dddddddde1.",
   "1dddffddde1.",
   "fdddfeddde1.",
   "fdddddddeee1",
   ".fdddedd1ee1",
   ".fdde1de1ef1",
   ".1de11de1f1.",
   "..11.1de11..",
   ".....1ee1...",
   "......11...."]
B=["..111111..",
   ".1eeeeee1.",
   "1eeeeeeef1",
   "1eeeeffef1",
   "1eeeefeff1",
   "1eefeefef1",
   "1ee1ee1ef1",
   ".11.11.11."]
D=[".11111..",
   "1eeeee1.",
   "1eeeffe1",
   ".1fefee1",
   "1eeeeee1",
   "1eeeeef1",
   ".1feeff1",
   "1eeefff1",
   "1eefff1.",
   ".11111.."]
plaats(24,0,A,'voor'); plaats(43,51,C,'voor'); plaats(50,21,B,'onder'); plaats(3,41,D,'onder')
W={32:(37,'55553335544'),33:(37,'55335553355'),34:(37,'53555555535'),35:(37,'53553335535'),
   36:(37,'53535553535'),37:(37,'53535555534'),38:(37,'55535553354'),39:(37,'5555333544')}
for y in range(33,39):
    for x in range(33,38): R[y][x]='5'
for y,(x,s) in W.items():
    for i,c in enumerate(s): R[y][x+i]=c
open('raster.txt','w').write('\n'.join(''.join(r) for r in R)+'\n')
