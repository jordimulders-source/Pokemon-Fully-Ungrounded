# Reparaties A (kopzone), per pixel naar het model (A-kopmodel: model/kop_opties/A_kopmodel_1024.png)
K,D,E,G,y,Y,L,B,W=1,2,3,4,5,6,7,8,9
FIX_A={(17,39):G,    # losse K in het nabije oor (model: 1 losse K natief (31,63)) -> oorrand G, zoals A0 (16,46)
       (20,48):W,    # gele pixel bovenin de witte krul (Gemini-ruis natief (34,71)) -> wit
       (12,62):B,
       # 2 px dikke zwarte lijnen (armbandrand + oorlijn liggen in het model naast elkaar; 1,13x maakt er 2 px van) -> 1 px:
       (15,35):D,(14,36):D,(14,37):D,      # linkerkant nabije oor: oorlijn blijft (16,34)-(16,35)-(15,36)-(15,37)-(14,38), band D
       (24,40):G,(23,42):G,(23,43):G}      # rechterkant nabije oor: oorlijn blijft, lichte streep G van de rechtervleugelband    # gele pixel aan de kin (Gemini-ruis natief (27,83)) -> B, zoals A0
