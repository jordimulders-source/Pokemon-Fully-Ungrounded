# Nachtaap fase 2: kleursprite ronde 13 (afwerking)

Basis is ronde 12. Ronde 12 had geen raster (de coördinator heeft hem rechtstreeks in de PNG bewerkt). Daarom zijn de wijzigingen nu expliciete pixelbewerkingen in `bron/bewerkingen.txt` (`x y letter`, met de hand). `bron/bouw.py` past ze toe op `ronde12/nachtaap.png` en controleert het resultaat.

Jordi: "een klein beetje meer ruimte [...] tussen de lijn, de staart en de buitenkant aan de rechterkant [...] de twee voorpoten zijn nog een beetje gek qua afwerking in kleur".

## Bewijs (`bron/bouw_uitvoer.txt`)
- **Alpha-diff:** 0.
- **Open randen:** 0 (ronde 12 had er ook 0).
- **Palet:** gelijk aan ronde 12.
- **Gewijzigd:**

| Zone | Pixels |
|---|---|
| A, achterste wig | 16 (11 oude wigpixels terug naar vacht + 6 nieuwe; 1 px valt samen) |
| B, armen en handen | 12 |
| buiten de zones | 0 |

- **Losse pixels:** 1 nieuw, (13,59) `s`. Dat is het begin van de vingerlijn op de handrug; hij gaat over in de crème lijn (13,60) `e`.

## Zone A: achterste wig
- De oude wig (x 43–46, y 34–38) raakte de staartwortel en de rechtercontour. Die pixels hebben de vachttint eronder teruggekregen, uit het raster van ronde 11 zonder wiggen.
- Nieuwe wig, vlak lila (idx 6, in de lijfschaduw), evenwijdig aan de middelste:

| Rij | x | Breedte |
|---|---|---|
| y 36 | 42–44 | 3 px |
| y 37 | 42–43 | 2 px |
| y 38 | 43 | 1 px |

- Tot de staartwortel (y 33) zit nu 2 rijen vacht. Tot de rechtercontour zit 2 px vacht (y 36: x 45–46; y 37: x 44–45).
- **Eerlijk:** tussen deze wig en de middelste zit nog maar 1 px vacht (x 41). Meer ruimte naar alle drie de kanten past niet met ≥ 3 px bovenaan, zo smal is het achterlijf daar. Jordi's ruimte naar staart en rand heeft voorrang gekregen. De wig is daardoor kort; hij is het kleinste van de drie, zoals in de projectie.

## Zone B: armen en handen
- **Verre hand:**
  - De crème vingertoppen in de schaduw (`e`) zijn nu rustig: één schuine vingerlijn (8,58)–(7,59) en één inkeping onderaan (5,59).
  - De onderrand aan de schaduwkant is zwart (was bruin `t`).
  - Een eerste poging met drie losse vingerlijnen las op 4× als dambord en is teruggedraaid.
- **Nabije onderarm:** twee losse lichte vlekjes zijn weg, (17,57) en (18,56) `l` → `b`. Zo leest de arm als een rustige cilinder (licht via de basis links, schaduw rechts en onder).
- **Nabije hand:** de vingerlijn bij de duim loopt nu door van de violette handrug (13,59) naar de crème top. Daarmee lopen alle drie de lijnen (x 13, 16, 19) van rug tot top.
- **Niet veranderd:** de vorm, de violette handrug met crème toppen, de verre voet en de kop.

## Lessen
- **Een ronde zonder raster:** schrijf de wijzigingen als `x y letter`-lijst en laat een script ze toepassen en tellen per zone. Dan blijven ze met de hand en controleerbaar.
- **Vingerlijnen op een kleine verre hand:** hooguit één lijn plus een inkeping. Meerdere korte lijnen in twee tinten worden op 4× een dambord.
