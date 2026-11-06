# Keuring poedelmot sprite ronde 7 (achterpoten), door de maker
- Bron: graphics/pokemon/giratina/anim_front.png, foto_tak_katoen_2.webp, vilt_poten_LEIDRAAD.png; ronde 6 als startpunt
- Bekeken op 8× en 1× (licht/donker), de poten op 16× naast het Giratina-vak en de tak-foto, ronde 6 naast ronde 7
- Controle: pixeldiff tegen ronde 6 is 103 px, waarvan 0 buiten de achterpootzone en 0 in de voorpoten; 0 lichte pixels op de buitenrand; 13 kleuren

## Jordi's punten
- "losse aanhangels zonder verbinding" / "maak ze vast aan het lichaam ook": links loopt de flank zonder naad door in P en komt Q uit de onderrand van de buik. Rechts loopt een heup door in S en R1. OK.
- "links zitten ze meer aan de onderkant dan rechts" / "kijk bijv naar giratina": links staan P recht onder het lijf en Q onder de buik. Rechts komen S en R1 hoger uit de zijkant (heup vanaf y48), zoals bij Giratina. OK, maar zie zwak punt 1 (vijf poten op een rij).
- "niet overdreven groot in beeld": S is smaller dan in ronde 6, R1 is 2 px en P is 5 px. OK.
- Puntig met minimale klauwtjes: P, Q en S lopen af naar een punt met 2 klauwtjes van 1 px; R1 heeft er 1. Ze zweven niet: P staat op y58 en S op y59, op de grond van de voorpoot aan hun kant. OK.
- Voorpoten: diff 0. OK.

- Oordeel: PASS (draft). Open vraag: de plek van Q onder de buik. Een onafhankelijke keurder moet nog kijken.
