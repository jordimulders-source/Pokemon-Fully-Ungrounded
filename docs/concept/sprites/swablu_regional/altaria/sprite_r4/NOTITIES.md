# Onweerswolk-Altaria frontsprite, ronde 4 (vanaf r3)

Opdracht (Claude, na het r3-vel): kop/ogen/snavel/hals blijven zoals r3; 1. static subtieler, 1 px, alleen de langere modelstukken (boog buiten de rechtervleugel weg, vonk links blijft); 2. kuif: twee gladde hoofdstrengen, alleen de grootste modelvorken (≥2 px, vast), geen losse pixels; 3. wolk: vleugels donkerder zoals het model, kappen alleen op de bollen, ronder (3 tinten met tussenstap); 4. vleugelrand mag het model volgen via een andere alpha-drempel.

Bestanden: `altaria_r4.png` (13 kleuren incl. transparant), `altaria_r4_8x.png`, `vel.png` (r4 | r3 | model op schaal | game-Altaria 8× / kuif 16× naast het natieve model / linkervleugel 16× naast het model / 1× op licht en donker), `bouw.py`, `basis.py`, `basis_kop15.png`, `controle.py`, `vel4.py`. Bouwen vanuit `altaria/`: `python3 sprite_r4/bouw.py && python3 sprite_r4/vel4.py`.

## Wat er t.o.v. r3 veranderde
- **Silhouet (basis.py), alpha-diff r4 ↔ r3 = 16 px weg, 0 erbij** (figuur 1937 px):
  - vleugels (`vleugel()`: Y13–32, X6–21 en X39–61 buiten de kuif): figuur bij ≥ 6/9 modeldekking i.p.v. ≥ 5/9 (`WT=6`); de halfbedekte randpixels bij de inhammen tussen twee bollen vallen weg: (8,16) (60,16) (55,17) (60,20) (43,22) (39,25) (6,28) (8,30). Static telt in de vleugelzone niet meer als figuur: de boog buiten de rechtervleugel (61,23) (61,24) (60,25) (60,26) is weg; de vonk links (x3–5) blijft.
  - kuif: twijgjes van 1 px aan een vertakkingspunt en groepjes < 3 px weg (alleen weghalen): (37,8) (46,10) (45,14) (50,14).
- **Static:** tint (150,206,230) L190, tussen het wolkhooglicht (136,192,214) en het r3-cyaan in; uitgedund tot 1 px (Zhang-Suen), daarna stukken < 10 px weg. 76 px in 6 stukken (6, 6, 11, 11, 13, 29), was 115.
- **Wolk:** kapvolume 1 px aan de rechteronderrand i.p.v. 2 (kleine kappen hielden anders geen hooglicht); kaphoeken: bolle hoekpixels van kappen ≥ 8 px → midden (tussenstap), hooglicht dat aan de onder/rechterrand van de kap komt → licht (hooglicht | licht | midden); waar de buitenlijn een kap opeet schuift de kaptint 1 px naar binnen.
- Kop, ogen, snavel, wang en hals: zelfde regels als r3 (`KOPGRID` ongewijzigd).

## Controle
13 kleuren incl. transparant; alpha = basis; zwart alleen in de pupillen; geen lichte kleur op de buitenrand; geen static-stuk < 4 px. Pixels zonder 8-buur van dezelfde tint: kuif-takpunten (31,7) (36,8) (35,9), oogglans, wang/snavelschaduw, vonkpixel (3,26), 2 static-hoekjes, halsrand (22,32) (21,34) (20,36).

## Eerlijke twijfels
- **Vleugelrand:** een hogere drempel maakt alleen kleine inhammen (8 px); het blijft een trap met hier en daar een inham, geen duidelijke bolletjesrand. ≥7 haalt 22 px weg maar verschuift vooral de traptreden.
- **Vleugelkappen:** de modelkappen liggen direct onder de modelomlijning; op 1/3 valt hun bovenste rij in de buitenlijn, dus de kappen zijn klein (bol 1 alleen licht, bol 2 en 3 met 2–3 px hooglicht). De vleugels zijn nu donkerder dan in r3 en dichter bij het model, maar de bollen lezen er zwakker dan in het model.
- Grote voorste kap (X21–34, Y40–45): hoeken afgerond, maar de bovenrand is nog vrij recht.
- Kuif: losse groepjes zijn weg; drie takpunten blijven 1 px van kleur (de vorken zelf zijn ≥ 2 px).
