# r21: keuring r20, vier punten (gemeten met px.py/grid.py, zie NOTITIES)
F={(43,29):'4',(42,30):'4',(41,31):'4',(40,32):'4',(40,33):'4',   # linkerrand voorvleugel langs de spleet
   (54,36):'4',                                                    # gat in de naad voor-/achtervleugel
   (35,50):'4', (36,50):'4', (39,33):'A',                                                  # bovenrand middenpoot
   (18,35):'1'}                                                    # glans linkeroog alleen (18,34)
W={}
for (x,y),c in F.items(): W.setdefault(y,[]).append((x,c))
