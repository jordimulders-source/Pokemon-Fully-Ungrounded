# Lama fase 2: silhouetvariant "jonger" (maker-agent, 2 nov)

Jordi over 2c (letterlijk): "de vacht is idd te klonterig. Daarnaast lijkt die nu iets te volwassen denk ik?"
Fase 2 is een tussenvorm: "marshtomp, charmeleon, monferno, prinplup idee". Fase 3 wordt de zware volwassen kampioen.
Dit is alleen een silhouet in één kleur. Jordi kiest eerst; daarna volgt de kleur.

## Analyse: wat maakt een tussenvorm "tiener"
Gemeten in `graphics/pokemon/` (pixels, frame 1):

| tussenvorm | px | eindvorm | px |
|---|---|---|---|
| Charmeleon | 1160 | Charizard | 2514 |
| Marshtomp | 1120 | Swampert | 2058 |
| Monferno | 1121 | Infernape | 1452 |
| Prinplup | 1224 | Empoleon | 1825 |
| Combusken | 1136 | Blaziken | 1579 |
| Grovyle | 1368 | Sceptile | 1783 |

- **Massa:** tussenvormen zitten rond 1100–1370 px. Eindvormen zijn 1,3–2,2× zo zwaar, met brede schouders en borst.
- **Kop en lijf:** de tussenvorm heeft naar verhouding een grotere kop, ±38–45% van de hoogte; de eindvorm ±25–30%. Ook de ogen zijn naar verhouding groter (Charmeleon, Prinplup).
- **Ledematen:** bij de tussenvorm korter en dunner. De lange benen en lange armen komen pas in de eindvorm (Blaziken, Infernape, Sceptile).
- **Vorm:** de tussenvorm is ronder en compacter, met minder versiering en een minder dominante houding (Marshtomp, Prinplup). De eindvorm is hoekiger en heeft meer uitsteeksels.

## Toegepast (zo weinig mogelijk ingrepen)
Pose, kleding, banaanoren, stompe snuit, wolhals en de rechte rustige lamastand blijven.
1. **Kortere poten, lijf lager.** Rijen 47, 50 en 53 van `ronde2.txt` (rechte schachtstukken in alle vier de poten) zijn weg, en alles erboven zakt 3 rijen (`stap1_korterepoten.txt`). Knie, hak, wolmouwen en handschoenen blijven zoals ze waren.
2. **Kop naar verhouding groter** (niet herschaald):
   - de kop meet nu 22 van 58 rijen, ±38% (was 36%);
   - het achterhoofd is opnieuw getekend als ronding (x22 op y13–15, x23 op y16–17) in plaats van de rechte rand op x21; de kop is +6 px.
3. **Minder zware wolhals:** de achterkant van de hals is 1 px slanker op y23–27 (−5 px). De plukinham op y22 blijft.
4. Formaat: **1208 px** (ronde 2: 1278), box 44×58.

Bestanden:
- `variant_jonger.txt` (`#` = pixel) en `variant_jonger_1x.png`;
- `vel.png`:
  - 4×: ronde 2, de variant, de alpaca en het ontwerp van fase 3Y;
  - 1×: ronde 2, de variant, kleur 2c, kleur ronde 3 en de alpaca;
- `vel.py` (bouwt de png en het vel).

Handmatige spans: kop y13–17 (x12–22, x12–22, x12–22, x12–23, x13–23), hals y23–27 (x10–26, x11–27, x12–27, x13–15 + x18–27, x17–29).

## Eerlijk: wat nog niet werkt
- **De kop:** die is alleen relatief groter, door de kortere poten, plus 6 px achterhoofd. Op 1× zie je vooral een korter, compacter dier; de kop zelf oogt nauwelijks groter. Voor een echt "jonger" gezicht moet het oog groter en ronder. Dat gebeurt in de kleur, binnen de kop, als Jordi deze richting kiest.
- **Ronder en zachter:** behalve het achterhoofd is de omtrek niet ronder gemaakt. Romp, borst en achterwerk zijn die van ronde 2.
- **De opgetilde handschoen** (x19–28, y52–56) staat nu dichter bij de grond en dichter bij de verre handschoen. Er zit nog lucht tussen, maar de opgetilde poot leest minder opgetild.
- **Rijen weghalen is een mechanische stap**, geen nieuwe tekening. De poten houden hun vorm, maar zijn niet opnieuw ontworpen op de kortere maat.

## Lessen
- "Jonger" zit vooral in de verhoudingen (kortere poten, relatief grote kop en ogen, minder massa), niet in de kleur. Rechte schachtrijen weghalen kort de poten in zonder knie, hak of handschoen te raken.
