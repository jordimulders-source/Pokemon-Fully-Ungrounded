# opzij lopen: voorpoot (lokaal x4-9, rij 20-21) 1 px naar voren, achtervoet (lokaal x10-18) 1 px naar achteren
f5=shift(f5, 28, 29, 7, 12, -1)
f5=shift(f5, 28, 29, 13, 21, +1)
# naad tussen de voeten dichtzetten waar het lijf erboven doorloopt
for x in range(7,23):
    if f5[28][x]=='.' and f5[27][x] not in '.o': f5[28][x]='o'
