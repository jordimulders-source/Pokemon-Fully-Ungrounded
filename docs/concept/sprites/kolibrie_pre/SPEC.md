# Kolibrie pre-evo: SPEC

**Status (2 nov): stap 1 (ontwerp).** Nog niets bevroren. Ontwerp en vragen: `ONTWERP.md`. Werkwijze: `docs/lessen/SPRITE_WERKWIJZE.md`.

## Onderdelen
| onderdeel | bron / referentie | Jordi's woorden | status |
|---|---|---|---|
| richting/concept | `ONTWERP.md` (A jong vogeltje, B nestje, C kantuta) | "laten we met de pre-evo van de kolibrie beginnen" | besloten: A (jonge kolibrie) |
| type | puur Flying; eindvorm Ghost/Flying | "pure flying type die pas per evolutie ghost wordt" | besloten |
| pose | foto van Jordi (nog nodig) | — | open |
| kleurfamilie | eindvorm `kolibrie/af/kolibrie.png` | — | volgt de eindvorm |
| formaat | ±450–650 px (eindvorm ±1000 px) | — | richtlijn |

## Afgekeurd (niet herhalen)
- Losse bloem als rekwisiet (kantuta-capuchon): bij Cherrim/Flabébé is de bloem een deel van de Pokémon, hier niet (Jordi, 2 nov).
- Alles wat bij de eindvorm is afgekeurd (`kolibrie/SPEC.md`): modeltekeningen uit cirkels/driehoeken, ronde kop, groot oog, kuifveertjes recht omhoog (oren), slierten onder het lijf (lezen als poten).

## Pose (Jordi, 2 nov)
"ik wil deze eigenlijk zittend met de vleugels ingeklapt, misschien snavel open omdat die gevoed wil worden. Moet echt cute zijn". Foto's: `referenties/jordi_1..5` (1 zittend jong, 2 jong met vleugel, 3 nestjongen met open bek, 4 voeren, 5 uitvlieger in de hand).
- Silhouet v1 (foto 1 recht verkleind): te lang/stijf, open bek viel weg. v2 (foto 5): bek 1 px.
- **Silhouet v3 (voor Jordi):** `silhouet/vel_v3.png`. A = foto 1 met korter lijf (×0,78) en kop ×1,45, B = foto 5 als bolletje; beide met een open bedelbekje met de hand (2 px dik, gaap 3 px), kop links. Advies Claude: A (leest als vogeltje, kop als eigen onderdeel); B is ronder maar leest eerder als bal.

## 3D-poppetje (Jordi, 2 nov: "a veel beter uiteraard, maak een 3d model"; "met een script van coathief, of bijv de lama/alpaca")
- `pop3d/pop3d.py` (op basis van `lama/ontwerp/pop3d_lama.py`, branch `claude/blissful-sagan-4f6hqj`): gekleurd, donsbobbels op buik en kop, open bedelbek met gele mondhoeken, donsplukje als voorbode van de jeguaka, ingeklapte vleugels, staartstompje. Hoek van foto 1 (lijf 22° naar de kijker).
- Vel `pop3d/vel_ronde1.png`: kop A/B/C (45/49/53% van de hoogte) en kleur (fluweel / dons-doffer / hillstar+violet); `pop3d/lijn_ronde1.png`: op schaal naast de eindvorm. Advies Claude: B + fluweel.
- Daarna (werkregel Coathief, 2 nov): het goedgekeurde poppetje direct verkleind als onderlaag; de **maker-agent** tekent silhouet en kleur met de hand, niet Claude. Silhouet v3A geldt alleen als posekeuze.

## Ronde 2 (Jordi, 2 nov: "waarom wijkt dit zo immens veel af van het silhouet?" · "welke werkwijze gebruik je, toch niet olinguito?" · "dat zou verklaren waarom het zo fout gaat")
- Fout in ronde 1: twee werkwijzen door elkaar. Eerst een handsilhouet uit de foto (kolibriemethode), daarna een los poppetje uit vrije vormen (59% overlap met het silhouet). Silhouet A was bovendien zelf al vervormd (lijf geplet, kop ×1,45), waardoor het poppetje ernaar passen een pinguïn gaf.
- Nu de Coathief-volgorde: **foto → poppetje → silhouet**. `pop3d/pas_foto.py` past de grote vormen van het poppetje op de omtrek van foto 1 (88% overlap, `pop3d/overlay_foto.png`, parameters `pas_foto_params.json`); daarna pas cute in 3D (`vel_ronde2.py`: stand 1 foto-getrouw 40% kop, stand 2 50%, stand 3 58%). Vel: `pop3d/vel_ronde2.png`. Advies Claude: stand 2 (fase 1-maat D2 40–55%).
- Silhouet v3A vervalt als bron; het silhouet komt straks uit het gekozen poppetje (direct verkleind, maker-agent repareert met de hand).

## Ronde 3: gestopt met het poppetje (Jordi, 2 nov: "gaat weer fout he, lijkt totaal niet op de silhouet" · "dat zie je zelf ook wel toch")
- Ook het poppetje dat het best op silhouet A past (`pop3d/vel_ronde3_A.png`, 79% overlap, parameters gezocht) lijkt er niet op: gladde ellipsoïden worden een ei/pinguïn; de schuine houding, de rugbult, de kop die laag in het lijf zit en het staartstompje van A komen er niet uit.
- Werkregel "twee rondes zonder voortgang = stoppen": het 3D-poppetje werkt niet voor deze vogel (net als bij de wasbeer). Stap terug: **silhouet A (Jordi: "a veel beter") is de vorm**; de maker-agent tekent de sprite met de hand op A, met foto 1/3/5 als bron. Wacht op Jordi.
- **Herzien (Jordi: "79% overlap is waarom het fout gaat"):** niet stoppen met het model, maar het model uit silhouet A zelf maken. `pop3d/opblazen.py` blaast A op tot 3D (omtrek = A, 98% overlap op 1×; het verschil zit alleen in de gladde bek), met kop, buik, vleugel, staart, bek met gele mondhoek, oog en pootjes als delen; drie kleuren. Vel: `pop3d/vel_ronde3.png`. Wacht op Jordi (kleur, en of dit model de bron wordt voor de maker-agent).
