# na de buitenlijn: onderrand verre vleugel (10-12,36) in selout i.p.v. donker streepje
for x in (10,11,12):
    if r[36][x]!='.': r[36][x]='4'
r[53][16]='2'
r[20][56]='A'
# drie losse pixels tussen krul en rand horen bij de krullijn
extra=[(56,20),(59,34),(54,44),(57,35),(58,35)]
for x,y in extra[:3]: r[y][x]='6'
for x,y in extra[3:]: r[y][x]='9'
open('krul_lijnen.txt','a').write(''.join(f'{x},{y}\n' for x,y in extra[:3]))
