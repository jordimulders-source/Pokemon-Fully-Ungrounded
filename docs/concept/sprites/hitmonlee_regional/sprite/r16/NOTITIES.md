# r16 – getapete benen (gladde omtrek, ringen alleen binnenin) + groene plekken

Jordi over r15/ek3 (letterlijk): "nee kijk eens goed naar de hitmonlee sprite, daar zijn de benen gewoon een normale vorm alsof ze getaped zijn, dus alleen binnen de lijnen zie je die golven" · "naar dat betekent dat je alleen de buitenste lijn hoeft te fixen" · krabbel `jordi/krabbel_benen.png`: "met geel heb ik getoond hoe je dan een beenvorm kan maken, dan hoef je deze alleen nog op te vullen qua kleur en de groene lijnen twijfel ik of die niet te recht zijn" · "nee de gele lijnen zijn een indicatie" · "maak het netjes". Plus groene plek (f) (beschreven door Claude: L-lijn bij de overgang ring → doorschijnend deel).

Basis = r15 (= ek3). Bestanden: `r16.png` (64×64 geïndexeerd, palet ek2, 15 kleuren + 0), `r16_8x.png`, `diff_ek2_r16.png`, `vel.png` (ek2 | r16 | model | Gen 3-Hitmonlee op 8×, diff, 1×/2× licht/donker), `overlay_krabbel.png` (r16 op de schaal van de krabbel met Jordi's gele en groene lijnen erover), `log.txt` (alle 156 px die van ek2 afwijken, met reden), `bouw.py`, `vel.py`, `krabbel.py`, `overlay_krabbel.py`.
Krabbel gemeten: 10,02 px per spritepixel, offset (8, 3) (gefit op ek3, kleurfout 2,8).

## Benen
- Omtrek: glad, 1 px, selout 2 links (lichtkant), zwart rechts; geen bolletjes of inkepingen meer. Ligging/breedte uit het model (uniform gefit, subpixelrand per rij), de buiging gelijkmatig zoals Jordi's gele indicatie:
  - trapbeen links kol 42 (rij 10–15), 41 (16–20), 40 (21–23), daarna 39, 38, 37 van ek2: runs 6-5-3-2-2-2; rechts 48 (9–16), 47 (17–21), 46 (22–25), 45: runs 8-5-4-2. Model en indicatie verschillen hier ≤ ~0,8 px; het model alleen is in rij 11–19 vrijwel verticaal (subpixel 41,6–42,4), wat een recht stuk van 9 gaf.
  - standbeen links kol 51 (rij 44–51), 50 (52–54), 49 (voet); rechts 56 (42–47), 57 (48–55), 58 (voet). Rij 54 (bovenkant voet) 1 px breder zodat de rechterrand niet meer deukt (model 57,6).
- Binnenin: de ringen van r15 (zelfde tabellen en kleuren), per rij opnieuw op de nieuwe breedte gelegd: per ring een rij met de boog-uiteinden (die raken de omtrek), een rij met de middenlijn (boog 1 rij lager) en een gewone rij met het verloop licht → donker. Waar het been 6 breed is, is de tabel met 1 middentint verlengd (log).

## Groene plekken (gemeten in het model)
| plek | meting | gedaan |
|---|---|---|
| (a) lijn binnen de trapvoet | donkerrode plooi in het model: bovenrand rij 4 (kol 37–40), rij 5 (41–43), rij 6 (44–48) = schuin. ek3 had hem recht op rij 5/6 en stopte op kol 43 | plooi schuin gemaakt: 9 px naar tint 3, bovenrand trapjes 2-3-4 |
| (b) voet → trapbeen | model rij 10 donker op kol 41–43 en 46–48, licht in het midden; rij 11 donker over de hele breedte = boog | enkellijn als boog zoals de ringen: uiteinden rij 10, midden rij 11 (4 px) |
| (c) onderrand romp boven de verre hand | model onderrand 44,8 → 47,3 (kol 22–34) = ek3 (runs 3-4-6, goede curve). De zwarte lijn liep daarna 2 px door in de naad met de verre arm (8 px recht) | naad kol 35–36 donkerrood (binnenlijn), linkerrand verre arm 1-1-1 trap (+1 px op (36,48), model 48,8) |
| (d) romp → standbeen | model onderrand 43,4 / 43,2 / 43,0 / 42,8 / 42,8 / 43,2 (kol 45–50): een boog van maar 0,7 px | kol 45 een rij lager (model 43,41): boog 4-5 i.p.v. 3-6; meer laat het model niet toe |
| (e) pols nabije arm | model-ringlijn loopt schuin (rij 50 kol 10–11, rij 49 kol 13) | lijn schuin: (49,12) lijn, (50,12) crème |
| (f) ring → doorschijnend deel | modellijn (natief rij 59–63) loopt van (41; 25,6) schuin naar rechts en dan vlak tot kol 45,6; geen verticaal stuk omlaag | verticaal stuk kol 41 rij 26–27 weg (beige); de lijn is nu een boog (24,40) → (25,41–45) |

## Check
Rechte-lijnencheck: in de benen alleen nog runs van 5–8 waar het model zelf vrijwel recht is (trapbeen boven, standbeen); geen sprongen, geen losse pixels. Elders over: zool trapvoet, koepeltop 5, linkerwand romp (model recht, zie r14). Bekeken op 8×, 2× en 1× naast de Gen 3-Hitmonlee: de benen lezen als gladde getapete poten met de golven binnenin, zoals bij de Gen 3-Hitmonlee.

## Twijfelpunten
1. Trapbeen: de buiging begint hoger dan in het model (op Jordi's indicatie), afwijking ≤ ~0,8 px.
2. Standbeen wordt naar de voet toe 1 px breder (6 → 8); het model is in het midden ±6 breed.
3. (d) blijft vrij vlak: het model heeft daar maar 0,7 px boog.
4. Nog niet onafhankelijk gekeurd.
