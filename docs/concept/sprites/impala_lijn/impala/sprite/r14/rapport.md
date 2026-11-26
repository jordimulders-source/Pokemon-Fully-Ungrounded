# Impala r14: poten naar Kirlia (Jordi, 26 nov: "doe kirlia maar na idd")
Basis r12 (niet r13). Script `sprite/r14.py`, vel `r14/vel.py` → `r14/vel.png` (r14 | r12 | model op 8×; poten op 12× naast Kirlia x26–37).

## Kirlia gemeten (`anim_front_gba.png`, nabije poot x29–32, verre x33–34, y46–57)
- Nabije poot, vulling 1 px, van boven naar onder: 73BD73 (y46–47), 94E694 (y48), CDFFAC (y49–56), 73BD73 (y57).
- Linkerlijn 317B4A (donker eigen), op y48/52/56–57 middentint; rechterlijn zwart (101010) of 317B4A.
- Verre poot: 94E694 met 73BD73, één stap donkerder; lijn 317B4A.

## Toegepast (46 px, alleen vulpixels; lijnen, hoeven en silhouet ongewijzigd)
| poot | middentint (heup / gewricht / boven de hoef) | lichte tint (scheen) | px |
|---|---|---|---|
| nabije voorpoot | L: y48–49, 52–53 (knie; in het model 167–176), 59–60 | H: y50–51, 54–58 | 8 |
| nabije achterpoot | L: y46–48 (dij/heup), 53–54 (hiel), 58–59 | H: y49–52, 55–56 | 27 |
| verre voorpoot | M: y48–49, 52–53 (knik), 57–58 | N: y50–51, 54–56 | 5 |
| verre achterpoot | M: y46–48, 52–53 (hiel), 56 | N: y49–51, 54–55 | 6 |
Stukken van 2–5 rijen (één stuk van 1 rij: verre achterpoot y56 boven de hoef, 2 px breed). Gewrichten liggen op de knikken in de pootvorm, de knie van de nabije voorpoot ook op de modelplek. Linkerlijn D, rechterlijn zwart (al zo in r12). Kleuren 12 + transparant.

Bevroren met assert (diff 0): alles buiten de vier pootvakken, silhouet, oog B3, strepen, witte borst/buik + grens, alle lijn- en hoefpixels.

## Ter info voor Jordi
- De nabije achterpoot is nu licht (L/H). Het model geeft hem dezelfde grijswaarde als de verre poten (±145), maar de opdracht wilde voor nabije poten de lichte tint. Daardoor zie je nu nabij/ver beter. Ook de onderste dijrij (y46) is van M naar L gegaan, zodat er geen donkere streep tussen lijf en poot blijft.
- De linkerlijn heb ik overal D gelaten. Kirlia zet op een paar rijen een middentint in de lijn, maar de opdracht zei belijning ongewijzigd.
