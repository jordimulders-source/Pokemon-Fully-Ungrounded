# Kolibrie pre-evo – kleur ronde 1 (maker, 2 nov)

Jordi, letterlijk: "fluweel als kleur" · "deze pre evo mag wel een veel mildere kleur hebben, veel minder mysterieus" · "ja beetje het idee zoals dat fletchling nog niet fire is" · "Moet echt cute zijn".
Basis: silhouet r2 (bevroren). Puur Flying, geen Ghost-kenmerken.

## Bestanden
- `rijen_r1.txt`: de met de hand geschreven rijen (`y x: tekens`, één teken per paletindex, per onderdeel).
- `bouw.py` maakt er `raster.txt` van (64×64) en meet de alpha-diff.
- `palet.py` maakt `kolibrie_pre.png` (geïndexeerd, index 0 transparant) en `normal.pal` (JASC, CRLF zoals in `graphics/pokemon/`).
- `controle.py` controleert alpha-diff, open randen, losse pixels en kleurgebruik.
- `vel.png` (`vel.py`): de sprite 4× en 1× op licht en donker, naast Fletchling, Taillow, Natu en de eindvorm (2× en 1×, licht en donker) en foto 1.

## Game Freak-studie (op 8× bekeken als indexraster)
| sprite | kleurgroepen (tinten) | omlijning | licht/schaduw | oog en snavel |
|---|---|---|---|---|
| Fletchling | kop grijs 3 (+zwart), borst oranje 3, buik wit/grijs 3, staart zwart/wit | donkergrijs rond de kop, zwart rond oranje en wit aan de schaduwkant | hooglicht linksboven op kop en borst, schaduw rechtsonder in de buik | oog = zwart blok met witte glans; snavel 2–3 px met donkere omlijning |
| Taillow | blauw 3, rood 2, crème 3, staart blauw | gekleurde donkerblauwe omlijning aan de lichtkant, zwart aan de onderkant | kop licht linksboven, buik crème met schaduw die de bolling volgt | oog met glans en donker bovenlid; korte gele snavel |
| Natu | groen 4, geel/rood accenten | zwart/donkergrijs, op de rug een gekleurde donkergroene rand | volume met 4 groentinten in banden die de bol volgen | grote ogen; snavel geel met donkere rand |
| Starly | grijs 3, wit 3, oranje snavel 2 | zwart aan de schaduwkant, grijs aan de lichtkant | witte buik met grijze schaduw onderaan | klein oog met glans; snavel met hooglicht |
| Eindvorm kolibrie | violet 4, lavendel 3, blauwgroen 2, donker 3 | diep violet in plaats van zwart | licht linksboven | klein oog; donkere snavel |

Wat ik overnam:
- Per groep 3–4 tinten.
- Gekleurde omlijning (lila 3) aan de lichtkant en diep violet (1) aan de schaduwkant, nergens puur zwart.
- Schaduw die de bolling volgt: buikhooglicht linksboven, buikschaduw rechtsonder.
- Oog met donker bovenlid, iris donker boven en licht onder, en een glans.
- Snavel: donker met een lichte middenpixel, plus de gele mondhoek uit foto 3.

## Palet (16, index 0 transparant)
| index | kleur | gebruik |
|---|---|---|
| 0 | 152,208,160 | transparant |
| 1 | 44,32,62 | omlijning schaduwkant, ooglid |
| 2 | 88,72,118 | donkere omlijning, scheiding vleugel, diepe schaduw |
| 3 | 126,110,160 | lila schaduw en omlijning lichtkant |
| 4 | 164,150,200 | lila basis |
| 5 | 200,190,228 | lila licht, buikschaduw |
| 6 | 226,222,242 | buik lavendelwit |
| 7 | 250,248,255 | buik hooglicht |
| 8 | 74,150,160 | blauwgroene glans |
| 9 | 142,208,200 | blauwgroene glans licht |
| A | 70,62,84 | snavel en pootjes |
| B | 122,114,140 | snavel hooglicht |
| C | 248,208,82 | gele mondhoek |
| D | 214,150,52 | mondhoek schaduw |
| E | 96,80,146 | iris onder |
| F | 255,255,255 | glans |

Kleurfamilie van de eindvorm (violet, lavendel, blauwgroen), maar licht en grijsviolet: geen fluweelzwarte kop.

## Per onderdeel
- **Kop:** lila 4 met hooglicht 5 linksboven op de kruin, schaduw 3 aan de achterkant en onder het achterhoofd (scheiding kop/lijf). Kruin- en achterrand in 2; geen harde kapgrens, dus geen helm.
- **Oog (x24–27, y14–17):** bovenlid 1 met zachte hoekjes 2, glans F linksboven, iris 1 → E (licht onder), onderrand 3. Groot (4×4) en glanzend, maar geen witte stip.
- **Bek:**
  - Bovensnavel: rand 1, midden B/A (blijft ook op donker zichtbaar).
  - Ondersnavel: bovenrij A/C, onderrand 1.
  - Gele mondhoek C/D vormt aan de basis van beide snavelhelften en in de hoek één "⊐", zoals de open bedelbek in foto 3.
- **Keel en buik:** lavendelwit 6, hooglicht 7 op de bolle borst linksboven, schaduw 5 naar rechtsonder en onderaan; omlijning 3 links, 2 onderaan.
- **Vleugel (ingeklapt, nabije):** gebogen voorrand (scheidingslijn 2, geen zwart), hooglichtrand 4 alleen bij de schouder, basis 3, schaduw 2 en omlijning 1 aan de rugkant.
- **Blauwgroen accent:** 4 pixels glans (9/8) schuin op de schouder, als enige hint naar de eindvorm.
- **Staartstompje:** 3/2 met omlijning 1.
- **Pootjes:** nabij A met omlijning 1; verre poot helemaal donker (1, in de schaduw).
- **Verre vleugel:** valt in deze houding achter het lijf (zoals in foto 1), dus niet zichtbaar.

## Checks
- **Alpha-diff tegen silhouet r2: 0** (`controle.py`).
- **Open randen: 0.** Elke pixel naast transparant is 1, 2, 3 (omlijning), A (snavel) of C/D (gele mondrand).
- **Losse pixels:** alleen bewuste accenten (ooglidhoekjes, glans, mondhoek D, kinpunt, einden van de omlijning), geen ruis.
- **Aandeel zeer donkere pixels (1 + A):** 0,109, aan de onderkant van de Gen 3-band (±0,10–0,25). Dat past bij "veel mildere kleur".
- 15 van de 16 kleuren gebruikt, plus index 0. Totaal 732 px.
- Zelf bekeken op 1× en 4× op licht en donker, naast Fletchling, Taillow, Natu, de eindvorm en foto 1:
  - Leest als een rond, lief lila vogeltje met een open gele bedelbek.
  - Duidelijk familie van de eindvorm, maar mild.
  - Geen Ghost-kenmerken.

## Wat nog niet klopt / voor Jordi
- Ik zie geen open fouten.
- **Smaakkeuze voor Jordi:** de kop kan een iets diepere violette kruin krijgen als voorbode van de fluweelkap van de eindvorm (zoals Fletchling een grijze kop heeft). Nu is de kop even licht als het lijf om het mild en cute te houden. Een donkere kap riskeert de "helm"; daarom niet gedaan zonder zijn keuze.
- Naast de felle Gen 3-vogels oogt hij bewust zachter (minder contrast). Wil Jordi meer pit, dan kan de omlijning aan de schaduwkant een stap donkerder.

## Lessen
- Een donkere snavel met alleen omlijningskleur verdwijnt op een donkere achtergrond. Eén lichtere middenpixel (B) per kolom houdt hem zichtbaar.
- Een blauwgroen accent als 2×3-blok leest als een geplakt label. Een schuine streep van 4 pixels langs de vleugelrand leest als glans.
- Een vleugelrand met een constante helling leest als touw of streep. De voorrand gebogen laten lopen (bol bij de schouder, dan naar achteren) en het hooglicht alleen bij de schouder houden lost dat op.
