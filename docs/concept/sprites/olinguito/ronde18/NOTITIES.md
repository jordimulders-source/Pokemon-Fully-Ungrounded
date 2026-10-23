# Olinguito ronde 18: kop terug naar ronde 16, alleen de neuspunt opgeschoven

Jordi over ronde 17: "Helemaal verknald het hoofd. Het enige wat je hoeft te doen is de neus een héél klein beetje naar rechts te sturen zodat het perspectief lijkt alsof het ertussen zit." Ronde 17 verschoof neus, grijns en kaak 11 px en sloot de wang; dat was veel te veel.

**Opbouw** (`bron/bouw18.py`, rechtstreeks op de PNG's):
- Alles met x < 48 komt pixel voor pixel uit ronde 16 (kop, oren, masker, ogen, snuit, grijns, kaak, lijf, poten).
- De staartzone x ≥ 48 komt uit ronde 17 (de hangende J). Lijf, poten en armen zijn in 16 en 17 gelijk.
- `normal.pal` is byte voor byte gelijk aan ronde 16/17.
- Daarna verandert alleen de neuspunt (ronde 16: `0a0/000/050`, x9–11, y32–34 in frame 1, y31–33 in frame 2).

| versie | neus | wat er links van komt | hoofdpixels veranderd (per frame) |
|---|---|---|---|
| `ronde18/` (1 px) | x10–12 | x9 = bruine omlijning (1) in de boven- en onderrij, middenrij blijft zwart | 9 |
| `variant_2px/` (2 px) | x11–13 | x9 blijft zwarte omlijning, x10 = crème snuitvlak (5/6/6) | 9 |

- De rand van de snuit (x9) blijft in beide versies dicht en het silhouet is gelijk aan ronde 16. Er zijn geen open randen.
- In de 2 px-versie zit er crème tussen de rand en de neus. Daardoor zit de neus "op" de snuit in plaats van op de punt, en dat geeft het meeste perspectief. De 1 px-versie is subtieler: alleen een bruine rand in plaats van zwart.

compare.png: ronde 16 | 1 px | 2 px, telkens 1× (frame 1 en 2) en 6× de kop.
