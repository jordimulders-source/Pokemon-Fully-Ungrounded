"""Salticonda kleurronde 3: alleen een nieuwe kop (3/4, Silicobra-kop als skelet, ~1,2x) op kleur1-E.
Kopzone = rechthoek x 0-47, y 0-23; daarbuiten 0 pixels anders dan E (zie check_kleur3.py).
In de kopzone: E-pixels van rij 0-19 eerst weg; rij 20-23 blijven staan waar de kop ze niet bedekt.
Tekens: . transparant | O K h omlijning | e d c b a zout | f g gezicht | q r s t pekel. ' ' = laat E staan."""
from PIL import Image
D='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/salticonda/'
CH='.OKhedcbafgqrst'
OX,OY=4,0
KOP = [
"...............hhhhhh..hhhhK..............",  # 0
".............hhaaaabbhhaabbbhhK...........",  # 1
"...........hhaaaabbbbbdabbbbbbbhK",  # 2
"..........haaabbbbbbbbbdabbbbbbcbK",  # 3
".........haabbbbbbbbbbbbdabbbbbbccK",  # 4
".........heeeeeedbbbbdddbdabbbbbccdK",  # 5
".....hhh..heaaafeeeddaaadcdabbbbbceK",  # 6
"....haaah.haaaaaaedbaaaaabcddabcdceeK",  # 7
"...haaaabhbeaaaaaebaaaabbbcccddcdccdeK",  # 8
"..haaaabbaaaaaaaaheecccccccceecdcccdeKO...",  # 9
"..haabaaaaaaaaaaarOOddddddOOtshcdcccdeO...",  # 10
"..hOOaaKOOaaaaaarttOOOOOOOttshcccdcccdeO...",  # 11
"..hOaaaaKOaaaaaarrrastOOttsssfhccdcccdeO...",  # 12
"..KaaaaaaaaaaaaafrqqrrOOrrssfhccccdccdeO..",  # 13
"...haageeeffaaaffrrrrrrssssfhcccccdccdeO..",  # 14
"...KeeffffeefffffffrsssssffhccccccdccdeO..",  # 15
"....KeffffffeeeffffffffffffhccccccdccdeO..",  # 16
"....KeffffffeeeffffffffffffhccccccdccdeO..",  # 17
".....KfffffffffegggfffffffhcccccccdccdeO..",  # 18
"......KOgffffffffggggggffKOccccccdcccdeO...",  # 19
"........KKOgggggggggggKKOOtrrrrrssssstdO..",  # 20
"..........KKKOOOOOOOOOtqqqqaaaqqrrrrssstK.",  # 21
"........ttrqqqaaaaqqqqqqqqqrrrrrrssssstt..",  # 22
"........trqqqqqaaqqqqqrrrrrrrrrrsssssst...",  # 23
"........tsrrrrrrrrrrrrrrrrrssssssssst.....",  # 24
".........ttsssssrrrrrrssssssssttt........",  # 25
]
def build():
    E=Image.open(D+'kleur1/salticonda_E.png'); P=E.load()
    out=E.copy(); Q=out.load()
    for y in range(0,22):
        for x in range(0,48): Q[x,y]=0
    for j,row in enumerate(KOP):
        for i,ch in enumerate(row):
            x,y=OX+i,OY+j
            if ch=='.':
                if y<22: Q[x,y]=0
                continue
            Q[x,y]=CH.index(ch)
    return out
if __name__=='__main__':
    im=build(); im.save(D+'kleur3/salticonda.png',transparency=0)
    Q=im.load()
    open(D+'kleur3/salticonda_raster.txt','w').write('\n'.join(''.join(CH[Q[x,y]] for x in range(64)) for y in range(64))+'\n')
