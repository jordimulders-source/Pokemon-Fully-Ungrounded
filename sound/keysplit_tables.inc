@ Due to the way mks4agb (Nintendo's tool) works, key split table labels can
@ appear before the actual start of the key split table data. If you look at
@ the first keysplit table (keysplit_piano), you'll notice it's offset backwards
@ by 36 bytes. This is because the key split tables don't map instruments
@ for the entire note range (0-127)--they only map subsets, and the upper
@ and lower ranges aren't necessarily 0 or 127.
@
@ For example if a key split table maps an note range of 10-20, then the key
@ split table label will be offset 10 bytes before the actual key split data
@ begins. Therefore, the notes naturally map to the key split table without
@ any extra offset calculation.

keysplit piano, 36
	split 0, 55
	split 1, 70
	split 2, 91
	split 3, 108

keysplit strings, 36
	split 0, 69
	split 1, 81
	split 2, 108

keysplit trumpet, 36
	split 0, 66
	split 1, 84
	split 2, 108

keysplit tuba, 24
	split 0, 42
	split 1, 108

keysplit french_horn, 36
	split 0, 66
	split 1, 108

@ Project Grounded: Battle! Heatran v6 (heatran_theme.py): een eigen sample per riffnoot C2 Db2 Eb2 F2 Gb2 G2 Ab2 Bb2 C3
@ (0-8), zodat niets ver getransponeerd wordt (spectrum blijft gelijk); heatran_lead: C4 (0) en G4 (1).
keysplit heatran, 36
	split 0, 37
	split 1, 38
	split 2, 40
	split 3, 42
	split 4, 43
	split 5, 44
	split 6, 45
	split 7, 47
	split 8, 108

keysplit heatran_lead, 48
	split 0, 64
	split 1, 108
