# Hoatzin fase 2, r16 (20 nov): vanaf r15, kuif terug van r14

Jordi op r15: "beter maar er is geen scheidingslijn bij de nek, de linksepoot is nog even en de linkervleugel ook" ·
"14 is de kuif beter dan 15" · "maar nog niet perfect" · "linksonderin mag iets beter aansluiten op het hoofd, de kuif" · "de dikte is nu wel goed".

`sh alles.sh`: bouw16.py → check → diff → vel (r16 | r15 | model, plus 12x nek, linker poot en linker vleugel naast het model).
Pixeldiff t.o.v. r15: 203 px, **0 buiten de zones** (kuif/verre vleugel/kruin 142, nek 29, linker poot 32). Silhouet: 34 px.
Kuif y8-21 wijkt 11 px af van r14 (alleen de aansluiting linksonder en de kruinonderrand). check.py: dambord 0, om-en-om 0, klonten 0. 16 kleuren, palet ongewijzigd.

| punt | r16 |
|---|---|
| kuif | plukken + kruin = r14 (plukdikte 2 px ongewijzigd). Verre-vleugeltoppen y2-7 = r15 (4 ronde toppen 4/3, scheidingen 2, geen zwart binnenin), behalve waar r14-bruin ligt. |
| aansluiting linksonder | harde 2-rand tussen kruin en blauw vlak/snavel (9-10,20), (8-9,21) → 6; vleugelpaars-gaatje (8,15-16) en donkere stip (8,17) → 7: de plukbasis loopt door tot op de kop. Kruinonderrand: het rechte 2-stuk (13-16,19) → 6, zodat de sikkel gebogen blijft. |
| nek | doorlopende binnenlijn 1 van (28,23) tot (24,35) langs de grens uit het model; slagschaduw 2 links ervan (2 px y23-30, 1 px y31-35: taps); lichte voorrand 5 van de vleugel rechts ervan (y24-31). |
| linker (verre) poot | scheen 2/D/D/2/2/1 schuin omlaag naar links (x22-29, y50-54); voet met twee tenen naar links zoals het model (bovenste teen D/2 tot x16, onderste D/2 tot x18) en twee klauwen 2 px diagonaal (15,57)-(14,58), (16,59). Grijs D/2 = een stap donkerder dan de nabije voet (E/D/2). |
| linker (verre) vleugel | toppen van r15 (zie kuif); verder r14-kuif erover. |

Zwak: de verre vleugel onder de kuif is r14 (3 met bruine plukken); de nekscheiding is een 1-px lijn met 5-rand, het model heeft een breder zwart nekvlak.
