# Charlatan-Alakazam: kleur r10 (onderarm loopt door in de linkerhand)

Basis: `basis_L1.txt` (= `../kleur_r9/var_L1.txt`). Jordi: "bij beide sluit de hand niet aan op de onderarm. Links heeft in elk geval de kaart zeeer netjes vast, dus als je nog kan zorgen dat het een logisch geheel lijkt qua onderarm dan is die goed".

Bouwen: `python3 r10.py` (schrijft `var_A/B.txt/.png` en bewijst de diff), daarna `python3 vel.py`.

## Wijzigingen (alleen onderarm/pols, zone x12–21, y33–42; kaart, vingers en schoppen van L1 onveranderd)
- **A:**
  - De zwarte lijnen tussen onderarm en hand zijn weg: rij 38 x13–15, (15–16,39) en rij 40 x16–19 worden c. De grijze onderarm loopt nu als één vorm door in de rug van de hand, zoals in het model (daar loopt de zwarte onderarm zonder lijn over in de hand).
  - De losse schaduw (15–16,41) d is c geworden, want er hangt geen onderarm meer overheen.
  - Een schaduwsikkel d staat langs de rechterkant: (20,36–38) en (19,39). Licht van linksboven.
  - De pols is 1 px breder: (12,37) o erbij, (13,37) b. De linkercontour loopt nu recht door van onderarm naar hand, zonder knik.
- **B:** gelijk aan A, met een korte polsplooi in d op rij 40, x16–18 (geen zwarte lijn).

## Controle
- Pixeldiff buiten de zone: 0 (A en B, elk 17 px gewijzigd).
- Alpha-diff: 1 px erbij, (12,37). Er gaat niets af.
- Open randen 0, losse o 0. Clusters < 3 px: geen nieuwe; de 8 die er zijn stonden al in r9.

## Zwak punt
- In A is de onderarm met de rug van de hand een groot vlak in c, zonder binnenlijn. De vorm komt alleen uit de b-glans linksboven en de d-sikkel rechts.
