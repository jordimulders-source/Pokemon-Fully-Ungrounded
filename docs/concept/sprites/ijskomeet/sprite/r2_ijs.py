# r2: ogen (rond, lichtere ring, gloed), voet loopt langs de linkeronderrand op tot onder de kop,
# naad bovenkant middenplaat zachter en gebroken (geen kaak/mond), voetnaad een rij hoger (r53).
IJS2={
32:None,
42:(1,"SWWLLLDDDMDW"+"L"*13+"MMMKKLLK"),
43:(1,"SWWLLLSLLDL"+"L"*11+"M"*5+"DKLLLK"),
44:(1,"SWLLLLSLLLLLDD"+"L"*6+"M"*6+"DDDWLLK"),
45:(1,"SWLLLMSLLLLLLLDDDD"+"M"*7+"DDWWLLMK"),
46:(2,"SWLLMMS"+"LL"+"L"*8+"D"*7+"LLLLMMDK"),
47:(2,"KWLLMMS"+"L"*11+"M"*5+"D"+"LLLMMMDK"),
48:(2,"KLLLMMS"+"L"*8+"M"*9+"D"+"LLMMMDK"),
49:(3,"KLLMMMS"+"L"*4+"M"*12+"D"+"LMMMDDK"),
50:(3,"KLLMMMS"+"M"*16+"DD"+"MMMDK"),
51:(3,"KLMMMMDS"+"M"*12+"DDDDD"+"MDDK"),
52:(4,"KLMMMMS"+"M"*10+"D"*10+"K"),
53:(5,"KMMMMMS"+"S"*18+"K"),
54:(7,"KMMLLLLWW"+"LLLLL"+"D"+"WW"+"LLLL"+"D"+"WLL"+"K"),
55:(7,"KMMMLL"+"M"*9+"D"+"M"*6+"D"+"MMM"+"K"),
56:(8,"KMMMM"+"M"*10+"D"+"M"*6+"D"+"M"+"K"),
57:(9,"K"+"M"*14+"D"+"M"*5+"K"),
58:(10,"KKK"+"D"*14+"KK"),
59:(13,"KKK"+"D"*9+"KK"),
}
del IJS2[32]
OGEN={  # (x0,y): rij
 'L':{32:(5,"rrr"),33:(4,"rcccr"),34:(4,"rcCcr"),35:(4,"rcCcr"),36:(4,"rcccr"),37:(5,"rrr")},
 'R':{32:(12,"rrrr"),33:(11,"rccccr"),34:(11,"rcCCcr"),35:(11,"rcCCcr"),36:(11,"rccccr"),37:(12,"rrrr")},
}
GLOED=[(17,34),(17,35),(6,38),(13,38),(14,38),(4,33),(8,33),(4,36),(8,36),(11,33),(16,33),(11,36),(16,36)]
