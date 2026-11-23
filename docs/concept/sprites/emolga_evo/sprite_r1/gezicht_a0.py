# Gezicht A0: per pixel naar het model (raster f1: model per spritecel). Elke regel = (x,y): klasse, met de modelwaarde.
K,D,E,G,y,Y,L,B,W=1,2,3,4,5,6,7,8,9
def rij(y,x0,s):
    m={'K':K,'D':D,'E':E,'G':G,'B':B,'W':W}
    return {(x0+i,y):m[ch] for i,ch in enumerate(s) if ch!='_'}
FIX={}
# V1: modellezing per cel (model op het spriteraster, 40x)
FIX.update(rij(54,14,'W__K'))          # streep links van de krul tot boven; pupiltop
FIX.update(rij(55,10,'WG____E'))       # verre streep wit, pupil midden
FIX.update(rij(56,10,'WG_E_______G'))  # verre streep wit; kopvacht rechts van de krul
FIX.update(rij(57,9,'GW'))
FIX.update(rij(58,10,'GEE_DW'))        # onderkant verre wang, oogglans linksonder (model)
FIX.update(rij(59,15,'E___W'))
FIX.update(rij(60,13,'EEE__W_K'))      # (14,60) losse K in de donkere band -> E (buren)
FIX.update(rij(61,17,'W'))
FIX.update(rij(62,13,'B__W'))          # model: geen gele pixel aan de kin (Gemini-ruis)
