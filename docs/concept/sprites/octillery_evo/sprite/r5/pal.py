# r3: roodtinten herverdeeld naar stappen ±30-38, tint dicht bij het model
# lum 2/3/4/5/6 = 46/70/102/140/179 (r2: 53/74/100/133/177); binnenlijn f iets donkerder (35 -> 28)
import sys,os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))+'/..')
import cfg
cfg.PAL[2]=(102,22,30); cfg.PAL[3]=(144,38,40); cfg.PAL[4]=(190,66,60); cfg.PAL[5]=(224,106,92); cfg.PAL[6]=(246,154,132)
cfg.PAL[15]=(68,12,20)
