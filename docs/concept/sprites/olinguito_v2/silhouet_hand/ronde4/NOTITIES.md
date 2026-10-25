# Olinguito v2: silhouet ronde 4 (gerichte reparaties op de direct verkleinde B2-render)

**Basis (bevroren massa):** `../../silhouet_kolibriemethode/silhouet_ontwerp_direct_1x.png` (1131 px), door Jordi gekozen ("3 is veel beter"). Ronde 1–3 zijn losgelaten; die waren te dun ("veel te dun", "waarom is dat lichaam zo ingedund").

**Resultaat:** `silhouet.txt`, `silhouet_1x.png` en `vel.png`. Op het vel staan:
- de onderlaag;
- de basis en ronde 4 op 4×;
- ronde 4 over de onderlaag (zelfde coördinaten, geen verschuiving);
- ronde 4 met de toegevoegde pixels lichter;
- de basis en ronde 4 op 1× (grijs en wit), naast Linoone en Zigzagoon (1× en 4×).

**Pixels:** 1131 → **1188** (+57). Er is geen massa weggehaald: alleen trapjes, de stomp en de inkeping kostten pixels, en die zijn elders ruim teruggezet.

## Diff per zone (script, basis → ronde 4)
| zone | gebied | + px | − px |
|---|---|---|---|
| 1 klauwen | x 14–23, y 53–60 | 21 | 5 |
| 2 oor | x 22–31, y 13–19 | 21 | 0 |
| 3 kop (voorkant + kin) | x 5–13, y 20–41 en x 6–20, y 41 | 10 | 0 |
| 4 achterpoten | x 32–46, y 42–53 | 5 | 4 |
| 5 staart | x 40–58, y 4–30 | 22 | 13 |

**Buiten de zones: 0 pixels gewijzigd** (lege lijst in de diff). Kleine afwijking van de opgegeven zones:
- de klauwzone loopt tot x 23 (de bestaande pootrand), maar daar is niets veranderd;
- de kin (rij 41) valt net buiten "y 20–41, x 6–13". Die hoort bij punt 3 (kin en keel).

## Per punt
1. **Klauwen:**
   - De stomp (y 54–58) is vervangen door 2 Linoone-haakjes van 6 rijen (y 54–59).
   - Elk haakje is aan de basis 3 px breed, loopt schuin naar linksonder en heeft een punt die terugbuigt (licht gebogen).
   - Tussen de haakjes zit 1 kolom lucht bovenaan, oplopend tot 2 kolommen onderaan.
   - De pootbasis (y 53) is 2 px naar voren verbreed, zodat beide haakjes vastzitten.
2. **Oor:** het vlakke plateau is nu één ronde bult op de kruin (rijen 14–18: 3, 5, 7, 7, 8 px breed) met een inkeping eronder aan de achterkant. In de overlay steekt hij ±1 px hoger uit dan het oor van de onderlaag; dat houdt de bult op 1× leesbaar. Het nopje van het verre oor (x 17–19, y 18) zat buiten de zones en is ongewijzigd.
3. **Kop:**
   - De voorkant loopt nu als één vloeiende curve van voorhoofd naar neus. Linkerrand per rij (y 20–40): 15, 14, 13, 12, 12, 11, 11, 10, 10, 10, 9, 9, 8, 8, 8, 7, 7, 7, 7, 7, 8. Geen terugspringende trapjes meer.
   - De ronde neus zit bij x 7, y 35–39.
   - Onder de kop is een rij kin toegevoegd (y 41, x 10–17). Daardoor is de rechte onderlijn van 11 px nu een lichte bolling: neus → kin → keel. De keelinham naar de voorpoot (x 19–22, y 40–41) is gebleven.
4. **Achterpoten:** twee poten met 1 kolom lucht tussen de voeten (x 38, y 47–49).
   - De verre achterpoot is de voet linksboven (x 33–37, y 47–49), hoger.
   - De nabije achterpoot is het blok rechts met een platte voet tot y 52 (tenen naar voren op x 38).
   - De massa is gelijk gebleven (+5 −4).
5. **Staart:**
   - De buitenrand is een gladde boog (x 56, 57, 57, 57, 58 ×5, 57 ×4, 56 ×2 van y 9 tot y 23) zonder het uitstulpje bij y 15–18. De dikte is overal 5 px.
   - De top is afgerond (y 4: 3 px).
   - De punt is een ronde krul die naar binnen buigt (y 13: x 42–45, y 14: x 43–45) in plaats van een blokje.

## Toets op 1×
Naast de basis oogt ronde 4 even vol (ook iets meer pixels). De kop leest als ronde druppel met een stompe neus, het oor als bult, de voorpoot met twee haakjes, en twee achtervoeten. De staartboog leest glad.

## Eerlijk
- **Het oor** zit ±1 px hoger dan op de onderlaag.
- **De verre voorpoot** is in de basis niet zichtbaar (hij valt achter de nabije); die stond niet in de opdracht en is niet toegevoegd.
- **De inkeping tussen de achtervoeten** is 1 kolom. In één kleur leest dat op 1× net; in kleur helpt de schaduwtint op de verre voet.

## Lessen
- **Werk op een massa die Jordi goedkeurt** (de direct verkleinde render) en repareer alleen randen; een eigen pose als lijnen tekenen leverde steeds een te dun lijf op.
- **Diff per zone met + en − apart** bewijst meteen dat er geen massa verdwijnt.
