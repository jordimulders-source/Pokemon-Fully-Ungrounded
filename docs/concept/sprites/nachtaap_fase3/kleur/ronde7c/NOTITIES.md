# Nachtaap fase 3, ronde 7c: alleen de staartwortel (basis ronde 7 optie B)

Jordi (letterlijk):
- "b komt dichter in de buurt, geen idee weer wat je met matig en sterk aan het doen bent, matige en sterke hallucinaties? De staart lijkt nu net opgeplakt, dat moet geen streep zijn, de staart moet juist een beetje doorlopen op het lichaam met shading, kijk wederom naar andere sprites"
- "sterk en matig hebben allemaal willekeurige kringen en lijnen etc"

Matig en sterk (7b) vervallen. De romp van B blijft zoals hij is. Ik heb alleen de staartwortel aangeraakt, zonder nieuwe lijnen of ringen.

## Bestanden
- `nachtaap_fase3.png` + `normal.pal`
- `maak.py`: de rijen x42–47, r35–39, met de hand gezet
- `vel.py` maakt `vel.png`. Daarop staan B en 7c op 3× licht en donker, op 1× licht en donker, en een close-up op 8× van de staartwortel. Ernaast staan Zangoose, Furret en Mightyena op 8×.

## Studie (8×, front en back)
Ik heb deze sprites bekeken: Aipom, Zangoose, Linoone, Furret, Mightyena, Raticate, Sentret, Ninetales, Flareon, Absol, Seviper en Kecleon.

- **Geen lijn of kraag** waar de staart begint. Alleen in de inham van de omtrek staat één pixel omlijning.
- **De lichtkant van de staart loopt als band door** over de heup of rug en vervaagt na 3–5 px in de basistint van het lijf. Zangoose, Linoone en Mightyena laten dit het duidelijkst zien.
- **De schaduwkant van de staart loopt door** in de schaduw van het lijf.
- **De wortel is breder dan de staart** en vloeit uit. Bij Furret en Linoone lopen ook de strepen gewoon door op het lijf.

## Wat ik veranderd heb (14 px t.o.v. B, alleen x42–46 r35–39)
- **Plooi weg:** de donkere plooi in 2 aan de heupkant (x43–44, r35–37) en de schaduwkraag (x45, r38) zijn weg.
- **Inham:** alleen de inhampixel (x44, r35) blijft 2. Hij ligt tegen transparant, dus hij is omlijning en geen plooi.
- **Lichtband:** de lichtkant van de staart (5) wordt breder bij de wortel (x45–46 r36, x44 r37). Daarna loopt hij als band schuin naar linksonder de heup in en vervaagt via 4 in de basistint van de heup (r38, x42–45).
- **Schaduwkant:** de schaduwkant (x46–47, 3) loopt door in de heupschaduw onderaan (r38–40).
- **Dijschaduw:** de schaduwkolom van de dij (x42, r35–36) dooft nu uit in 4 in plaats van door te lopen naar de staart.

## Bewijs
- **Alpha-diff 0** t.o.v. B en t.o.v. ronde 6. Het palet is identiek.
- **Wijzigingen t.o.v. B:** alleen de 14 genoemde pixels, in x42–46 r35–39. Daarbuiten is alles gelijk aan B, dus ook de bevroren vakken zijn 0 px t.o.v. ronde 6: kop, vuistarm, healerhand en gloed, en beide voeten. De spiraal (x≥48) is gecontroleerd: 0 px t.o.v. ronde 6.
- **Open randen:** de 27 treffers zijn allemaal index 12 (de gloedrand van de healerhand), gelijk aan ronde 6. Er zijn 0 vachtpixels naast transparant.

## Eigen check (streng)
- **3×, licht en donker:** in B leest de wortel als een donkere streep. In 7c groeit de staart uit de heup: de lichtkant loopt door en vervaagt, en er staat geen streep of ring.
- **1×:** de staart en de heup lezen als één vorm. De rest van het lijf is gelijk aan B.
- **8×:** naast Zangoose en Mightyena is het dezelfde opbouw: een band van licht die doorloopt en dan vervaagt, met de schaduwkant in de lijfschaduw.

Ik lever één versie. Een tweede versie zou alleen een sterkte-variant zijn, en daar is niet om gevraagd.

## Lessen
- Een staartwortel krijgt nooit een plooi of kraag. De lichtkant loopt 3–5 px door op het lijf en vervaagt, en de schaduwkant loopt door in de lijfschaduw. Alleen de inhampixel tegen transparant blijft donker.
- Variant-reeksen (matig/sterk) zijn voor Jordi ruis. Lever één versie, tenzij een tweede echt een andere oplossing is.
- Werk alleen in de zone die Jordi noemt. Nieuwe banden of plooien elders in de romp lezen als "willekeurige kringen en lijnen".
