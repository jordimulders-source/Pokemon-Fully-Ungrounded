# Probeersels kop (op r9)

## Jordi letterlijk
- **"doe wat probeersels en toon me"**
- **"puur van hoofd"**

## Werkwijze
- Basis = r9 zonder snavel (`basis.png`). De rest is bevroren.
- Elke variant is met de hand ingetypt in `varianten.txt`.
- `probeer.py` maakt `P1.png`–`P6.png`, `vel.png` en `controle_uitvoer.txt`.
- `vel.png` toont alleen de koppen: 8× boven, 1× onder, met de r9-kop als vergelijking.
- Controle: alle zes zonder losse pixels en zonder lichte kleur op de buitenrand.
- Draaien: `python3.11 probeer.py`

## Per variant
- **P1**: de snavel van Picapau cel voor cel, 1,4× breder (11 px), licht open, in Picapau's grijs; hij leest als familie van Picapau, maar ligt nog tegen de donkere verre vleugel.
- **P2**: P1 met de verre vleugel achter de snavel weggehaald (vleugel alleen boven en naast de kop, zoals Pidgeot); de snavel staat nu tegen lucht en leest beter, maar onder de vleugel loopt een rechte zwarte afsluitlijn.
- **P3**: een lange spechtenbeitel van 12 px, dicht, in lichte hoorn (a/b met e als omlijning aan de lichtkant, G als onderrand); dit leest het meest als specht, maar de hoornkleur ligt dicht bij de crème keel.
- **P4**: P3 licht open, met een dunne zwarte spleet die naar een rode mondhoek zakt en een kortere ondersnavel; dit geeft het meeste karakter, maar de snavel is groot voor de kop.
- **P5**: de korte, stevige snavel van Staravia, omgekleurd naar grijs en 1,5× vergroot, tegen lucht; hij past het best bij de ronde kop, maar is geen specht meer.
- **P6 (eigen idee)**: een beitel van 10 px in Picapau-grijs met een hoge voet, tegen lucht; de spleet zakt naar een rode mondhoek die in de wang overloopt, als middenweg tussen P1 en P4.

## Zwak bij allemaal
- In P2-P6 sluit een rechte zwarte lijn van 5-8 px de verre vleugel af boven de lege plek (rij 9).
- De vleugelwortel onder de keel (rij 15) heeft geen bovenrand meer.
- Bij een gekozen variant moet ik die vleugelafsluiting netjes maken.

Er is niets gecommit en niets verwijderd.
