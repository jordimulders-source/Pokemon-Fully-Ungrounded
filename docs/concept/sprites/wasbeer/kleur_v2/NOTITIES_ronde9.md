# Kleur ronde 9 (maker-agent, 3 nov)

Basis is ronde 8. Ik heb alleen de reparaties 1–8 uit `KEURING_ronde8.md` uitgevoerd, als (x, y): (oud, nieuw) in `rijen_ronde9.py`. Het script controleert bij elke pixel de oude waarde.

- **ronde9**: reparatie 1 zonder pupil. Het nabije oog is rond, in de lijn van olinguito en Coathief: e-a-e / f-f-f / 2-f-2. De grijze wallenbalk (20–22,13) is weg, en (21,13) is f, zodat de onderkant rond is. 27 px gewijzigd t.o.v. ronde 8.
- **ronde9b**: hetzelfde, plus de pupil (21,12) f→1 zoals de keuring voorstelt: e-a-e / f-1-f / 2-f-2. 28 px.
- R2–R8 zijn exact uitgevoerd: verre onderlid, verre oor, nabij oor als holte, staartpunt, onderarm, slagschaduw achter de kop, kaak en neus (R8 heb ik ook gedaan).
- **Afwijking bij R7:** de keuring noemt (28,18) en (29,18), maar die zijn in ronde 8 al 5. Het losse 6-vlak staat op (29,18) en (30,18); die twee heb ik naar 5 gezet.

## Controles (script)
- **Beide versies:**
  - alpha-diff 0, geen open randen;
  - bevroren zones gelijk: buidel, klauwen/handen, buikcrème en het verre oog (13,11–12).
- **ronde9:** 96 losse binnenpixels, evenveel als in ronde 8.
  - Weg: (12,16) 6, (13,13) 4 en (33,29) 4.
  - Nieuw: alleen de neusglans (12,16) 7 op dezelfde plek, plus (13,16) en (13,17) door de afgeronde neushoek uit R8.
- **ronde9b:** 100 losse binnenpixels. De pupil splitst de iris in losse pixels: (20,12), (22,12) en (21,13) f, en (21,12) 1. Dat hoort bij het voorstel van de keuring.

## Zwakke punten
- **Staarthaak op 1x:** nog steeds een donkere kop met een lichte vlek. Dit vraagt een silhouetwijziging; dat is aan Jordi.
- **Rechte randen in het silhouet** (borst x 15, kopzijde x 12): niet opgelost.
- **Pupil of niet** blijft een ontwerpkeuze voor Jordi:
  - 9b leest op 2x/4x als een rijker Pokémon-oog;
  - 9 sluit beter aan op de lijn.
- **Niet aangeraakt**, want buiten de opdracht: buidelplooi, bovenarmstreep, blokkige bovenrand van de onderarm, mond, buikband.

## Lessen
- Coördinaten uit een keuring altijd met een assert op de oude waarde uitvoeren: bij R7 zat de keurder op y 18 één pixel naast het vlak.
