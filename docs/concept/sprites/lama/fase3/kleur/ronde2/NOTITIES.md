# Lama fase 3: kleur ronde 2 (verse maker, 5 nov)

Gemaakt vanaf `ronde1b/ronde1b.txt` + `normal.pal` (palet ongewijzigd). Alle wijzigingen zijn met de hand getypt in `bron/wijzigingen.txt` (per rij `y x0 pixels`). `bron/bouw.py` plaatst ze alleen en controleert ze.
Silhouet en model zijn niet aangeraakt.
- **Alpha-diff met `silhouet/ronde2.txt`: +4 / −0.** De 4 pixels zijn alle van de bombín en gemeld:
  - x22 y4 en x23 y4: bol, 1 px boven het silhouet, tussen de oren;
  - x17 y9 en x18 y9: rand, 2 px links buiten het silhouet.
  - Zie `alpha_diff.txt`.
- **Gewijzigd t.o.v. 1b: 92 px.** Kop, bombín en vlecht (y0–23): 80. Poten: 12. Lijf, cape, ruches en pompons: 0.

## Per punt van Jordi
1. **"het hoofd is nu wat te klein ook" / "kijk vooral naar hoe het origineel het doet":** ik heb de onderlaag per pixel naast `labels.txt` gelegd (4×4-blokken).
   - In 1b stond de mondlijn op y17 (`ddd`) met een donkere onderkaak eronder (y18 `SSSS`, y19 `kk`). Daardoor eindigde de kop optisch op y16.
   - In de onderlaag loopt de snuit door tot y19 en ligt de kinlijn op y20.
   - Nu is de snuit tot y19 licht crème. Alleen de lip-schaduw volgt de mondlijn. De kinlijn ligt op y20 (`kkkd`), zoals de onderlaag.
   - In het gezicht zitten geen donkere vlakken meer. Wat er donker is: het oog, het neusgat en de lijnen.
2. **Snuit-binnenlijn ("meer een lijn naar binnen toe"):**
   - De mondlijn `d` loopt schuin van de voorkant naar binnen en omhoog: y18 x17–19, y17 x20–21, y16 x22–23. Dat is de diagonaal van de onderlaag (x17 y19 → x22 y16), zoals bij Girafarig en Stantler.
   - Onder de mondlijn ligt een lip-schaduw `S`.
   - De kin-onderlijn loopt ook naar binnen (y20 x16–19), waarna de crème hals volgt.
   - Neusgat `k` op x17 y15, zoals in de onderlaag.
3. **Oog duidelijk:** recept van fase 2 (goedgekeurd), op de plek van de labels (x21–24, y13–15).
   - Zwaar vlak lid `dkkk` (y13).
   - Daaronder `d H k k`: glans laag vóór, iris donker (y14), met de onderkant van de iris in `dd` (y15).
   - Achter het oog blijft 1 kolom crème-schaduw over (x25) vóór de vlecht.
4. **Bombín "ietsje meer aan de linkerkant uitsteken en iets groter":**
   - De bol is 1 rij hoger (top x22–23 y4, tussen de oren) en 1 kolom breder naar links (x20–24 met omlijning x19, y6–8).
   - Glans `S`/`d` linksboven en een rode band `RRrrm` van 5 px.
   - De rand is 8 px breed (x17–24 y9) en steekt 2 px links uit, met een glans `dd`. Aan de rechterkant zakt hij naar y10 (x23–26), zoals in de onderlaag.
   - **De oren blijven zichtbaar:** het linkeroor y1–5 (x19–21) en het rechteroor y1–9 (x25–27). Geen enkele oorpixel is weggevallen boven y5.
5. **"De vlechten zijn onzichtbaar":**
   - Bovenaan (y12–17, x26–28) ligt de vlecht op de rand van het silhouet, zoals in het model. Daar is hij een donkere streng met knotten: lichtjes `S`/`d` die per knot van kant wisselen en `k`-inkepingen.
   - Onderaan (y18–22) zwaait hij 1–2 px naar voren over de hals (x24–27). Erachter blijft een strookje crème hals zichtbaar (x28, y19–21), zodat hij als losse hangende streng leest en niet als omlijning. In het model liggen de knotten daar ook over de hals.
   - Hij eindigt in de rode tullma `kRrm` (y22) tegen de halsband.
   - Alles valt binnen het silhouet.
6. **"de poten zijn wel oke, dat is puur controle en afwerking":**
   - De knie van de nabije voorpoot was een losse vlek (`SSCS`, y47). Nu is het een zachte schaduw aan de rechterkant (`CCCCSS`).
   - Het verre windsel had rood en geel bijna geheel in de donkerste tint (`rmmm`). Nu heeft het dezelfde volgorde en opbouw als het nabije, één tint donkerder: `yyyd`, `rrrm`, `BBBD`, `gggD`, `yyyd`, `rrrm`, `yydd`, met `k` aan de buitenkant.
   - De scheiding tussen de voorpoten (donkere rechterkolom van het verre windsel/de verre poot tegen `d`/`H` van de nabije) is ongemoeid gelaten. Die klopte al.

## Controle (§0 / norm)
- Licht linksboven, omlijning `d` aan de lichtkant en `k` aan de schaduwkant en onderkant: ok.
- **Open randen: 4, alle in de oren van 2 px** (x20 y2–3, x25 y3–4). Overgenomen uit 1b: een oor van 2 px kan niet zowel omlijning als crème hebben. Niet veranderd.
- 15 kleuren gebruikt; palet ongewijzigd.
- `lama3.png` is 64×64, geïndexeerd, index 0 transparant.

## Eerlijke zwakke punten
1. **Op 1× is het verschil met 1b klein.** De mondlijn en de lichte onderkaak maken de kop op 4×–8× duidelijk groter en leesbaarder, maar op 1× blijft de kop smal naast het brede lijf. Dat komt door de verhouding in het silhouet (W3); kleur haalt dat niet weg.
2. **Op 1× leest de bombín als een klein donker petje met rand.** De bol is 5×5 binnen de oren. Groter kan alleen door een oor af te dekken, of door verder buiten het silhouet te gaan dan de toegestane 1–2 px.
3. **Het bovenste deel van de vlecht (y12–17) ligt op de silhouetrand** en leest op 1× nog als een donkere rand achter de kop. Alleen het onderste deel (over de hals, met de tullma) leest als losse streng.
4. **Het oog en de bovenkant van de vlecht liggen dicht bij elkaar** (1 kolom crème ertussen). Op 1× vormen ze samen een donkere vlek rechts in de kop.
5. **De vlecht is onderaan 1–2 px naar voren geschoven** t.o.v. de labels (`p` x26–27 → x24–27 op y19–21). Dat is binnen het silhouet, maar een interpretatie; Jordi moet het zien.

## Bestanden
- `ronde2.txt`, `lama3.png`, `normal.pal`, `alpha_diff.txt`.
- `vel_ronde2.png`: onderlaag | 4× licht/donker | 1× licht/donker; op 2×/1× naast ronde 1b, fase 2, Girafarig, Stantler, Entei en Tauros; onderaan de kop op 8× naast dezelfde uitsnede van de onderlaag en ronde 1b.
- `bron/`: `wijzigingen.txt` (het handwerk), `bouw.py`, `vel.py`.

## Lessen
- Een kop leest "te klein" als de mondlijn te hoog staat en de onderkaak donker is. Leg de mond- en kinlijn op de rijen van de onderlaag (blokgemiddelde 4×4 per spritepixel), dan krijgt de snuit zijn volle hoogte terug.
- Een vlecht die op de silhouetrand ligt, leest als omlijning. Laat hem, waar het model hem over de hals legt, 1–2 px van de rand af hangen, met een streepje crème erachter.
