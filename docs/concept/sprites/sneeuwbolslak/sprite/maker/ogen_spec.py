# Oogprobeersels op r2: alleen voelspriettoppen (lokaal rij 8-13, kolom 0-13; abs x9-22, y31-36).
# Elk oog pixel voor pixel uit een echte sprite, kleuren naar het palet van r1_B.
# '.' = transparant. Kolom 0-5 linker top, 8-13 rechter top.
V = {
# magcargo (anim_front_gba): oogbal 7 boven/8 onder, kleine grijze pupil d boven e (2 px verticaal)
# 7->7, 8->6, d->d(13), e->2, schaduw 3->4
'magcargo': [
".222.....2222.",
".2771....27761",
"277761..277761",
"277d61..277d61",
".16241...16241",
".11641...1461.",
],
# surskit (anim_front_gba): kraaloog 181/111 (donker, witte glinster boven midden), c-rand links -> lijntint 2
'surskit': [
".222.....2222.",
".2761....27761",
"218161..218161",
"211141..211141",
".26641...26441",
".11441...1441.",
],
# gastrodon (anim_front): linkeroog .22/2b2/2b2/227 -> zwart ovaal met witte verticale streep; 2->1, b->8
'gastrodon': [
".222.....2222.",
".2111....21161",
"218161..218161",
"218141..218141",
".11641...11441",
".11441...1441.",
],
# sliggoo (anim_front): vlak oog zonder pupil .6./676/676/.6. ; 6->1, 7->2
'sliggoo': [
".222.....2222.",
".2161....21761",
"212161..212161",
"212141..212141",
".21641...21441",
".11441...1441.",
],
}
