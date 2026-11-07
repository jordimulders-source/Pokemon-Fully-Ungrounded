# nabij oog: glanzend zwart amandeloog, iets schuin (bovenrechts hoog, linksonder laag), zwarte pupil,
# glans als schuin ovaal linksboven, zwakke donker-olijf reflectie onderin; tan ring blijft uit k_kop3
EYE={32:(30,"222"),33:(28,"21111 2".replace(' ','')),34:(26,"21AA1112"),35:(26,"1AA11112"),
     36:(25,"211111112"),37:(25,"211111112"),38:(25,"21BBB112"),39:(25,"21B1112"),40:(26,"22222")}
for y,(x0,s) in EYE.items():
    for i,c in enumerate(s): r[y][x0+i]=c
r[35][25]='2'; r[33][27]='6' if r[33][27]=='.' else r[33][27]
# ver oog: reflectie ook olijf, pupil zwart
r[38][17]='B'
r[32][33]='A'
