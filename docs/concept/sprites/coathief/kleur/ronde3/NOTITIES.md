# Coathief: kleursprite ronde 3 (de vier FAILs uit `../ronde2/KEURING.md`)

Basis: ronde 2. Studie, palet en checklist staan in `../ronde1/NOTITIES.md`, de zones van ronde 2 in `../ronde2/NOTITIES.md`.

## Bestanden
- `coathief.png`: 64×64, mode P, 16 kleuren (15 in gebruik), index 0 transparant, transparency=0.
- `vel.png`: hetzelfde vel als eerder.
- `r2_vs_r3_kop_klauwen.png`: kop en klauwen op 8×, ronde 2 naast ronde 3.
- `uitsnede.png`
- `bron/`:
  - de ronde-3-reparaties staan onderaan `reparaties.txt`, met twee paletwaarden in `bouw.py`;
  - `diff_r2.py` is de diff per zone tegen ronde 2;
  - `controle.py` is aangescherpt: lichte crème (n, c, w) mag niet meer naast transparant staan, alleen x of k. Alleen aan de klauwen is n als schaduwrand toegestaan.

## Bewijs
```
controle.py: pixels 1297 | silhouet 1297 | alpha-diff 0 | open randen 0 | losse pixels 0
diff_r2.py:
zone 1 oog (vlekglans)                        5 px   (2 glans → c, 3 oogpixels door de nieuwe r)
zone 2 mond                                   5 px
zone 3 naad kop-hals                         29 px
zone 4a randen staart en oren                24 px
zone 4b klauwen opgetilde poot               13 px
zone 4c voet (24,61)                          1 px
totaal 77 | buiten de zones: 0
```
Dat is binnen het budget van ±75 px: de 3 oogpixels komen alleen door de paletwaarde.

## Paletwijzigingen
- **Index 13 (r):** `6a1c14` → `8c2418`. De donkere iris (luma ±59) komt nu boven de kop (51) uit en blijft duidelijk donkerder dan i.
- **Index 15 (x, was reserve):** `7c6448` (luma 104). Dit is de crème selout naast transparant.

## Per zone
1. **Oog:**
   - De glans in beide vlekken is terug naar c: (20,36) en (21,43). Het oog (glans w) is nu het helderste punt van de kop.
   - Met de lichtere r leest het op 1× (licht en donker) als een klein kraaloog: zwart bovenlid, rode iris met een lichtere onderkant en een glans. Geen losse stip meer.
2. **Mond:**
   - een k-lijn van 4 px direct achter de neus (8–11,46);
   - een mondhoek van 1 px in m op (12,45): een licht opgetrokken hoek, sluw en geen grijns;
   - de kaak eronder blijft z/m plus de k-omlijning.
3. **Naad kop–hals:**
   - De m-kolom is weg; binnen de muts is alles z.
   - Eerste bruine pixel per rij, y 35–46: 26, 27, 28, 28, 27, 28, 27, 27, 26, 25, 25, 24.
   - De naad heen-en-weer kartelt bij y 38–41 (vachtplukjes van 1 px).
   - De schedel bolt bij y 37–40 1 px verder uit dan in ronde 2.
   - Er is geen nieuwe donkere lijn: aan de halskant staat één d-pixel als vachtselout.
4. **Open randen:**
   - **Staart en oren:** alle 24 n-pixels naast transparant zijn nu x: de ringselouts links en de krul, plus de oortoppen (17,33) en (21–23,33). De n binnenin is gebleven.
   - **Klauwen:**
     - de buitenrand (links, onder, de punt) is x;
     - de schaduwkant is n;
     - c staat waar de klauw aan de poot vastzit (geen rand);
     - één w-glans binnenin per klauw: (17,57) en (21,57).
     - De vorm van de twee haken is ongewijzigd.
     - Op 1× lezen ze nog als lichte klauwen. Ze zijn iets donkerder dan in ronde 2, maar staan scherper tegen de witte achtergrond.
   - **(24,61):** z → m.

## Zelf bekeken (1×, 2× en 8×, licht en donker, naast ronde 2)
- Het oog leest als een oog.
- De mond maakt het gezicht af, zonder grijns.
- De muts loopt via een vachtkartel over in de hals; het is geen helm meer.
- De staart en de klauwen hebben op wit een rand.
- Het gezicht oogt niet vreemder dan in ronde 2.

## Niet aangeraakt (ligt bij Jordi)
- de lijfkleur;
- extra klauwen;
- de kaaklijn;
- de pose;
- het eiland van 2 px op (21–22,62).

## Lessen
- **Een donkere iris op een donkere kop moet minstens ±8 luma lichter zijn dan de kop.** Anders blijft er op 1× alleen een glans met wat rood over.
- **Glans (w) alleen in het oog.** Witte pixels in de vlekken eromheen trekken de blik weg van het oog.
- **Lichte delen naast transparant krijgen een eigen donkere crème selout** (luma ±100), niet de lichte schaduwtint. Die selout is ook ruimte voor een extra paletindex waard.
- **Klauwen van 2 px:** buitenrand in de donkere crème, de root in c (geen rand) en één w-glans binnenin. Dan lezen ze als klauw en niet als spikkel.
