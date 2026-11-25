from build import zet
# 5 VUISTEN naar het model: rug van de hand linksboven licht, naad (x14) en wit glanspunt uit het model,
# vingerplooi als donkere lijn (model r13), daaronder de vingers als segmenten met korte scheidingen (model: zwarte strepen)
GESTREKT=(10,8,['_ _ _ _ _ _ _ _ _ _',
                '_ _ _ 5 5 3 _ _ _ _',   # r9
                '_ _ 5 5 5 2 3 _ _ _',   # r10
                '_ 5 5 5 2 5 3 _ _ _',   # r11
                '_ 5 3 3 2 7 3 3 _ _',   # r12
                '_ 3 3 3 1 1 1 1 _ _',   # r13 vingerplooi
                '_ _ 2 5 3 1 5 3 3 _',   # r14 vingers
                '_ _ _ 2 2 1 3 2 2 _',   # r15
                ])
BORST=(37,19,['_ _ _ _ _ _ _ _ _ _',
              '_ _ 5 5 5 3 3 _ _ _',     # r20
              '_ _ 5 7 5 2 3 2 _ _',     # r21
              '_ 5 5 5 2 5 3 2 _ _',     # r22
              '_ 3 3 3 1 1 1 1 _ _',     # r23 vingerplooi
              '_ _ 2 5 3 1 5 3 2 _',     # r24 vingers
              '_ _ 2 2 2 1 2 2 _ _',     # r25
              ])
def zet_vuisten(a):
    zet(a,*GESTREKT); zet(a,*BORST)
