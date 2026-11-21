# Eindkeuring onweerswolk-Swablu r8 (Dragonfly Cave-stijl, 21 nov)

Getoetst: `swablu_r8.png` naast het model (verkleind 38×34, BOX-reductie) en Swablu, Altaria, Castform, Wingull, Taillow (8× en 1× op wit, lichtgrijs, donkergrijs, zwart, groen, blauw). Alleen uitvoering; Jordi's keuzes (grijze snavel, staartje, zit op de wolk, zachte gekleurde selout, oog, mondlijn) niet aangekaart.

## Algemeen
- **Wazig/hard:** niet wazig (heldere tintstappen ±30–40, gelijk aan Taillow) en niet hard (zwart alleen aan de onderkant/schaduwkant, binnenlijnen in selout-donker 46,60,78). Eén uitzondering: de rechte balk onder de vogel (zie M1), op 1× het hardste element.
- **Palet:** 15 kleuren + transparant (index 15 ongebruikt). OK.
- **Licht linksboven:** OK (linkerwolk en vogelkop licht, rechterkant en onderwolk donker).
- **Leesbaarheid 1×:** leest als Swablu op een wolk op alle achtergronden; op zwart valt de zwarte onderrand weg (normaal voor Gen 3).
- **Trouw aan het model:** silhouet, wolkverdeling, antennes, snavel en staart kloppen; afwijking alleen bij M1.

## MOETEN
- **M1 – onderkant vogel/bovenrand onderwolk (trouw + "geen rechte buikrand"):** de lijn (23–33,37) is 11 px kaarsrecht. In het model zit daar een V-inkeping tussen twee wolkbultjes (donker op x=28–29, rij 38; de losse index 2 op (28,38) is er een restant van). Reparatie (overnemen uit het model): (28,37) en (29,37) → index 7 (vogel donker); (28,38) en (29,38) → index 12 (selout donker). Daarna twee bogen met een inkeping, zoals het model. Proef gemaakt: werkt.
- **M2 – linker buitenrand onderwolk (geen zwart en donker om en om):** van boven naar onder nu C,2,2,C,C,**1**,2,**1**. Reparatie: (14,38), (13,39), (13,42), (14,43) → index 12. De rand is dan één lijn in selout donker tot (14,44); vanaf daar zwart langs de onderkant (zoals nu).
- **M3 – korrel in de naad rechtsonder:** losse index 12-stippen (40,40) en (43,40) in een naad van index 3 → index 3. De naad wordt één rustige tint (zachter, past bij "niet hard").

Totaal 10 px, alleen in de onderwolk; vogel, oog, snavel, antennes en bovenwolken diff 0.

## ZOU KUNNEN
- (16,28) index 2 is één donkere pixel in de lichte rand (index 4) van de linkerwolk (restant van de inkeping tussen twee bolletjes in het model); → index 3 maakt hem zachter.
- Korrel in de onderwolk: (18,43) index 3 los in index 2, (34–35,43) index 2 in index 3. Mag, staat ook zo in het model; netter als vlak.
- (48,35) index 12 los tussen index 3 op de rechterrand → index 3.
- Bovenwolken zijn licht in het midden met een donkerder rand rondom (licht pillow); de linkerbovenkant van de rechterwolk (40–41,26–29, index 5) is donkerder dan zijn middenkant terwijl daar licht valt. Kleur mag van het model afwijken; optioneel 2–3 px index 5 → 6.
- Onderwolk is horizontaal getint (4 → 3 → 2, licht banding); het model doet hetzelfde, dus geen moet.

## Ter info voor Jordi (geen uitvoering)
- Geen.

## Oordeel
**FAIL (bijna):** na M1–M3 (10 px) **PASS** zonder nieuwe keuring nodig, mits diff buiten deze 10 px = 0.
