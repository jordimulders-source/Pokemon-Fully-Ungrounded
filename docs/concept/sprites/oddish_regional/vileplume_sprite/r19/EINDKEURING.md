# Eindkeuring Dragonfly Cave: Vileplume-regional r19 (21 nov)

Getoetst op 1×, 2× en 8× naast Vileplume, Gloom, Bellossom, Tentacruel, Lileep en Cradily (anim_front, bovenste 64×64), licht en donker. Alleen uitvoering; Jordi's toegestane afwijkingen (geklonterde tentakels, gezicht uit de game, middelste anemoon naar links, voorste anemonen uit r3, poten per rij) niet ter discussie.

## Oordeel: PASS
De reparaties hieronder zijn klein (samen 10 pixels) en mogen, maar hoeven niet; geen ervan verandert de vorm.

| Toets | Uitkomst |
|---|---|
| Kleuren | 16 inclusief transparant, index 0 = transparant (152,208,160) |
| Past in 64×64 | bbox x2–60, y1–62; voeten onderaan (rechtervoet y62, linkervoet y59, perspectief) |
| Gaatjes in het silhouet | geen ingesloten gaten; 2 inkepingen van 1 px (zie 3) |
| Aandeel zwart | 15,2 % (echte: Lileep 15,9, Vileplume 17,6, Cradily 18,1, Gloom 20,2, Tentacruel 24,9): goed |
| Lichte kleuren op de buitenrand | geen in de kroon en het lijf (rand = 2/3 rood of 1 zwart); op de poten alleen index 7 als selout aan de lichtkant (bedoeld) |
| Belichting | linksboven klopt: kroon licht links/boven, rode selout linksboven, zwart rechtsonder; lijf A links, 9/8 rechts en onder de kroon |
| Losse pixels/ruis | de losse zwarte en rode pixels in de kroon zijn de tentakeltextuur (zoals de vlekken van de echte Vileplume) en lezen op 1× als anemonen; geen losse pixels in lijf en poten |
| Leesbaarheid 1× | goed: kroon met krater, wit lijf, gezicht, armpjes en twee steltpoten lezen naast de echte Vileplume |

## Reparaties (optioneel, alleen pixels)
1. **Rechterarm, bovenrand wisselt zwart en donkergroen** (`1,6,1,6,1`): (42,35) en (44,36) van 6 → 1; ook (40,31) van 6 → 1 (enige donkergroene pixel in de zwarte rechterrand van het lijf). Schaduwkant = zwart, consequent.
2. **Selout op de linkerrand van de poten wisselt licht/donker** (linkerpoot 7 y42–46, 6 y47–48, 7 y49–51; rechterpoot 6 y45–48, 7 y49–51): (23,47), (23,48) van 6 → 7 en (35,45)–(35,48) van 6 → 7. Daarna beide poten: lichte selout bovenaan tot y51, donker eronder.
3. **Twee inkepingen van 1 px onder de armen:** (20,36) en (41,38) transparant → 1 (sluit de onderlijn van arm op het lijf aan).

## Ter info voor Jordi (telt niet mee)
- De kroon is op 1× drukker dan bij de echte Vileplume (die grote rustige vlakken met vlekken heeft); dat is het gevolg van de anemoonstructuur, geen uitvoeringsfout.
- De gele ogen (2 px) lezen op 1× net; ze zitten zoals besloten net onder de kroon.
