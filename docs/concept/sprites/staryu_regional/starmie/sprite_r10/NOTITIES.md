# Regionale Starmie r10: twee omcirkelde plekken netjes afgewerkt

Opdracht (Jordi, omcirkeld op `referenties/jordi_starmie_omcirkeld.png`): "omcirkeld is nog niet netjes afgewerkt".
Basis: `sprite_r9/starmie_r9.png` (= af-versie). Bouw: `python3 sprite_r10/bouw.py` (vanuit `starmie/`).
- Alleen tinten binnen het bestaande silhouet, met bestaande paletkleuren. Het palet is ongewijzigd.
- Het script toetst met asserts: elke pixel ligt in een zonemasker, het silhouet is gelijk (alpha-diff 0) en de diff buiten de maskers is 0.
- Zonemaskers: zone 1 = x36–46, y10–20; zone 2 = x44–57, y20–26.

## Uitkomst
- **`starmie_r10.png`**: 42 px gewijzigd, 0 buiten de zones, **0 silhouetwijzigingen**.
- **`starmie_r10_B.png`** (variant ernaast): hetzelfde, maar de lijn waar de voorste ster over de achterpunt valt is selout 2 in plaats van zwart. Daardoor 46 px gewijzigd.

## Zone 1: achterpunt rechtsboven (35 px, waarvan 3 net buiten de genoemde x37–46/y10–19)
**Vlakken.**
- Er zijn twee vlakken. Het lichte vlak ligt linksboven: tint 4, met een rand van tint 5 langs de selout-lijn linksboven (rij 11–14).
- Het donkere vlak ligt rechts/onder: tint 3.
- Ze worden gescheiden door één nette trap van voet naar tip: rij 11–12 x45, rij 13–15 x44–45, rij 16 x43–45, rij 17–18 x43–44.
- Volgt de modelhelderheid: links ±140–167, de rechterstrook ±100–130.

**Weg.**
- De schuine lijntjes in tint 2 en 3 dwars door de punt: (39,14), (40,15), (41,16), (40,17), (41,18) en (39–40,16–19).
- De losse chip (39,13).

**Chips.**
- Het model heeft twee chips, op ±(42–43,14) en ±(42,17–18). Ze waren al zo geplaatst. Nu zijn het twee heldere vormen op het lichte vlak:
  - liggend paar (41–42,14);
  - staand paar (41,17–18).
- Ze liggen 1 px naar links ten opzichte van r9, zodat er tint 4 tussen de chip en het donkere vlak blijft.

**Binnenlijn van de voorste ster.**
- Eén diagonaal van 1 px: (36,12–13) [ongewijzigd], (37,14–15), (38,16–17), (39,18–19). Daarna loopt hij als selout 2 verder over de voet (40–44,19), met één wissel op de hoek (39,19).
- In A is die lijn zwart. Het is de buitenlijn van de voorste ster aan de schaduwkant: dezelfde lijn als (36,12–13) erboven, en hetzelfde als bij de achterpunt rechtsonder (44,36–38). Ook het model heeft daar zwart.
- B zet (37,14–15), (38,16–17) en (39,18) in 2. Jordi kiest.

**Voorrand opgeschoond.**
- (37,16) was zwart en is nu rand 4.
- De rand (36–38,17–19) is nu één doorlopende band van tint 4 tussen glazuur en lijn.

**Buiten de letterlijke zone, wel in de omcirkeling.**
- (36,18), (36,19) en (37,20) waren zwart midden in de binnenhoek. Ze zijn nu glazuurlijn 7.
- Daarmee loopt de glazuurlijn netjes door: (35,16–17) → (36,18–19) → (37,20) → (38–39,21).
- Dit telt mee in de 35 px.

## Zone 2: tip rechter voorarm (7 px)
- **Silhouet:** het was al vrijwel het spiegelbeeld van de linker voorarm. Nu:
  - platte tip van 3 px zwart in kolom 56 (rij 22–24) plus de hoek (55,21);
  - selout 2 op de bovenrand (rij 21);
  - zwart aan de schaduwkant.
- **Weg:** de zwarte pixels (52,22) en (53,22) midden in de bovenrand. Dat was een kartel uit het model. Ook weg: de losse 3 op (54,22) en de losse 2 op (54,24).
- (55,24) was zwart en is nu 3. Hij blijft ondoorzichtig, dus het silhouet verandert niet. Bij de linker arm is (5,24) ook rand (4) en geen lijn.
- **Koekrand rond het glazuur:**
  - rij 22 is 5 (licht) tot x54;
  - daaronder 5 → 4 (midden), zoals de rest van de rechterrand (5 5 4 4 1);
  - het tipeinde is 4/3/3 (donker) op x55, rij 22–24.
- Rij 21 blijft een selout-lijn van 1 px. De linker arm heeft precies dezelfde lijn (x5–13). Hij oogt nu niet meer dun, omdat rij 22 eronder weer een volle lichte rand is.
- Het glazuur en de glazuurlijn 7 van de arm zijn niet aangeraakt.

## Niet gedaan
- Geen slagschaduw 3 langs de voorste ster in de achterpunt, al hebben LB en LO die wel. De opdracht vroeg precies twee vlakken. Mogelijk punt voor de keurder.
- Niets gladgestreken buiten de zones (diff 0, ge-assert).

## Vel
`vel.png`:
- r10 | r9 op 8×, met de wijzigingen blauw omkaderd;
- zone 1 op 16×: r9 | r10 | r10_B | achterpunt linksboven;
- zone 2 op 16×: r9 | r10 | linker voorarm gespiegeld;
- 2× en 1× op wit en donker: r10 | r10_B | r9.
