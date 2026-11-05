# Coathief: kleursprite ronde 3b (alleen de klauwen van de opgetilde poot)

Basis: ronde 3, die verder bevroren is: oog, mond, naad, randen van staart en oren, en (24,61). Zie `../ronde3/NOTITIES.md`.

## Bestanden
- `coathief.png`
- `vel.png`
- `uitsnede.png`
- `klauwen_r2_r3_r3b.png`: de klauwen op 8× en 1×, op wit en op donker, van links naar rechts ronde 2, ronde 3, ronde 3b en de olinguito.
- `bron/`:
  - het blok "ronde 3b" staat onderaan `reparaties.txt`;
  - `diff_r3.py` is de diff tegen ronde 3.

## Bewijs
```
controle.py: pixels 1297 | silhouet 1297 | alpha-diff 0 | open randen 0 | losse pixels 0
diff_r3.py:  zone klauwen opgetilde poot (x 15-22, y 55-61)  13 px | buiten de zone: 0
```
De vorm van de twee haken is gelijk (alpha-diff 0).

## Wat er veranderd is (13 px)
| | Klauw A | Klauw B |
|---|---|---|
| Crème kern c over de volle lengte, aan de lichtkant | (17–18,56), (16,57–59) | (20–21,56), (20,57), (19–20,58), (20,59) |
| Glans w (1 per klauw) | (17,57) | (21,57) |
| Donkere crème x aan de schaduwkant | (18,57), (17,58–59) | (22,57), (21,58–59) |
| Punt x | (17,60) | (21,60) |
| n als schaduw waar de klauw aan de poot vastzit | – | (22,56) |

- Deze opbouw volgt de olinguito-klauwen: een licht vlak met een donkere schaduwrand.
- Een tussenversie met n als selout aan de lichtkant oogde nog te bruin. Daarom staat de kern c nu op de lichte rand. `controle.py` staat dat alleen in de klauwzone toe, aan de lichtkant (zoals Linoone en Sneasel).

## Zelf bekeken (8× en 1×, wit en donker)
- Op 1× zijn het weer twee heldere crème klauwen, minstens zo licht als in ronde 2, en scherper begrensd door de donkere schaduwrand.
- Ze staan even opvallend als de klauwen van de olinguito.
- Op donker vallen ze duidelijk op.

## Les
- Een klauw van 2 px leest als licht kenmerk als de lichte kolom de volle lengte loopt en alleen de schaduwkant donker is.
- Een donkere rand rondom, of n aan de lichtkant, maakt er bruine haakjes van.
