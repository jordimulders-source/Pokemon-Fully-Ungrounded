// Project Grounded: lichte trainerklasse-intro's (Jordi: "misschien kunnen we specifieke trainer class intros bouwen, wel
// allemaal licht") en de gedeelde runner voor de rivaal-intro's (src/data/rival_intros.h).
// Geen nieuwe graphics: alles is code (paletrekenwerk, scroll/vensters per beeldlijn, tiles en tekst die tijdens het spelen
// worden getekend) plus gevechtsanimatie-art en item-iconen die al in de ROM staan.
// Wordt onderaan src/battle_transition.c ingevoegd. Timing: echte VBlanks vanaf de start van de transitie (= start van de
// muziek, Tapu_Elapsed); het tempo komt uit de BGM-speler zelf (tempoD), dus elke thema van ROTATE valt op de tel.
//
//   klasse                                   intro
//   Swimmer M/F, Tuber M/F                   het water komt omhoog, spetters, een fontein, kopje onder
//   Hiker                                    rotsblokken rollen het beeld in, het scherm barst
//   Bug Catcher, Bug Maniac                  een net (web) zwiept twee keer, het beeld spartelt drie keer en zit vast
//   Psychic                                  een lepel buigt, de wereld buigt mee
//   Fisherman                                lijn uitgooien, dobber, beet!, het beeld wordt opgehaald
//   Bird Keeper                              een veren-storm
//   Kindler                                  vlammen van onderen, hitte-trilling
//   Guitarist                                versterker-dreun op elke tel, podiumlicht, noten
//   Ruin Maniac                              zandwand met hiërogliefen schuift over het beeld
//   Hex Maniac                               een kaars in het donker flakkert, gaat uit, twee ogen
//   Black Belt, Battle Girl                  karateslag: het beeld splijt in tweeën
//   Cooltrainer                              het wordt koud: rijp kruipt vanaf de randen naar binnen
//   Triathlete                               zwemmen, fietsen, hardlopen in drie banen, dan de finishvlag
//   Expert                                   inktwas: alles grijs, een penseelstreek, een rood zegel
//   Sailor                                   het schip schommelt, zeeziek groen, een golf
//   Picnicker, Camper                        het picknickkleed valt, bessen erop
//   Youngster, School Kid                    het beeld stuitert als een trampoline en knapt
//   Pkmn Ranger                              de Capture Styler trekt drie lussen: CAPTURED.
//   Beauty, Aroma Lady, Parasol Lady,
//   Lass, Lady                               bloemblaadjes en een glimlicht
//   Ninja Boy                                rookbom: het beeld is er niet meer, één blaadje valt
//   Pkmn Breeder, Pokéfan                    hartjes en een Lucky Egg dat uitkomt
//   Rich Boy, Gentleman                      muntenregen

// (includes staan bovenaan src/battle_transition.c: "battle_anim.h" zou hier src/data/battle_anim.h vinden)

#define TI_MAX_TILES 760
#define TI_MAX_SPR   56
#define TI_MAX_PART  40
#define TI_MAX_TAGS  20
#define TI_FX(bpm)   (3600 * 256 / (bpm))

enum { TIB_BG0X, TIB_WX, TIB_WY, TIB_WIN0, TIB_N };
#define TIF_BG0X (1 << TIB_BG0X)   // BG0HOFS per beeldlijn
#define TIF_WX   (1 << TIB_WX)     // BG1-3 HOFS per beeldlijn (relatief: de buffer bevat de echte waarde)
#define TIF_WY   (1 << TIB_WY)     // BG1-3 VOFS per beeldlijn
#define TIF_WIN0 (1 << TIB_WIN0)   // WIN0H per beeldlijn

enum { TIK_NONE, TIK_SPRITE, TIK_TRAINER, TIK_MON, TIK_ITEM };

struct TIPart
{
    s32 x, y;           // 1/16 pixel
    s16 vx, vy, ax, ay; // 1/16 pixel per frame (per frame^2)
    s16 life;
    u8 slot;            // index in spr[]
    bool8 on;
    bool8 bounce;
};

struct TIntro
{
    void (*init)(void);
    bool32 (*update)(s32 t);
};

struct TIState
{
    u16 dma[2][DISPLAY_HEIGHT * 6] ALIGNED(4);     // DMA-buffers (gebouwd na de update, gekopieerd in de VBlank)
    u16 back[TIB_N][DISPLAY_HEIGHT];    // wat de intro per beeldlijn schrijft
    u16 base[PLTT_SIZE / 2];            // de kleuren zoals ze na de init te zien waren (met dag/nacht en weer); elke
                                        // frame begint daarmee, alle effecten zijn dus per frame
    u16 *bg0map, *bg0tiles;
    s32 start, last, beat0;
    u32 rng, ours;
    u16 beatFx, nextTile, reserved, lineFlags;
    u16 winin, winout, win0h, win1h, win0v, win1v, bldcnt, bldalpha, bldy;
    s16 camX, camY, wx, wy, bg0x, bg0y;
    bool8 regs, scroll;
    u8 nspr, ntags, nfield;
    u8 spr[TI_MAX_SPR];
    u8 kind[TI_MAX_SPR];
    u16 monSpr;                         // CreateMonPicSprite geeft een u16
    u16 tags[TI_MAX_TAGS];
    u8 field[MAX_SPRITES];              // sprites van de kaart (met hun oorspronkelijke x2/y2)
    s16 fieldY2[MAX_SPRITES];
    struct TIPart part[TI_MAX_PART];
    s32 v[24];
    u8 extra[16];                       // nog een paar sprite-ids (weer in de rivaal-finales)
    u16 trainer, species;
    u8 kindIdx, stage, elem;
    const struct TIntro *intro;
};

static EWRAM_DATA struct TIState *sTI = NULL;
static EWRAM_DATA u8 sTI_PendingElem = 0;   // rivaal-intro: starter van de rivaal, gezet vóór de init

// ---------------------------------------------------------------------------------------------------------------------
// VBlank/HBlank

// Per-beeldlijn-effecten gaan via HBlank-DMA (kanaal 0), niet via een HBlank-interrupt: de mixer draait in de
// VCount-interrupt en houdt de HBlank-interrupts een groot deel van het beeld tegen (zie CLAUDE.md, filmtransities).
// Eén DMA per frame: óf WIN0H (1 waarde per lijn), óf het scrollblok BG1HOFS..BG3VOFS (6 waarden per lijn; BG0
// scrolt alleen per frame).
#define TI_DMA_WIN    (1 | ((DMA_SRC_INC | DMA_DEST_FIXED | DMA_REPEAT | DMA_16BIT | DMA_START_HBLANK | DMA_ENABLE) << 16))
#define TI_DMA_SCROLL (3 | ((DMA_SRC_INC | DMA_DEST_RELOAD | DMA_REPEAT | DMA_32BIT | DMA_START_HBLANK | DMA_ENABLE) << 16))

// na elke update: de lijnbuffers van de intro omzetten naar de DMA-buffer
static void TI_BuildLines(struct TIState *s)
{
    u32 f = s->lineFlags, y;
    u16 *d = s->dma[0];
    if (f & TIF_WIN0)
    {
        CpuCopy16(s->back[TIB_WIN0], d, DISPLAY_HEIGHT * 2);
        return;
    }
    for (y = 0; y < DISPLAY_HEIGHT; y++, d += 6)
    {
        u16 x = (f & TIF_WX) ? s->back[TIB_WX][y] : (u16)(s->camX + s->wx);
        u16 v = (f & TIF_WY) ? s->back[TIB_WY][y] : (u16)(s->camY + s->wy);
        d[0] = d[2] = d[4] = x;
        d[1] = d[3] = d[5] = v;
    }
}

// Registers via SetGpuReg: de kaart zet elke frame zijn eigen scroll in de buffer, en die buffer wordt na deze
// callback naar de registers gekopieerd (CopyBufferedValuesToGpuRegs); direct schrijven zou dus overschreven worden.
static void VBlankCB_TI(void)
{
    struct TIState *s = sTI;
    DmaStop(0);
    LoadOam();
    ProcessSpriteCopyRequests();
    TransferPlttBuffer();
    if (s == NULL)
        return;
    if (s->scroll)
    {
        u16 x = s->camX + s->wx, y = s->camY + s->wy;
        SetGpuReg(REG_OFFSET_BG1HOFS, x);
        SetGpuReg(REG_OFFSET_BG2HOFS, x);
        SetGpuReg(REG_OFFSET_BG3HOFS, x);
        SetGpuReg(REG_OFFSET_BG1VOFS, y);
        SetGpuReg(REG_OFFSET_BG2VOFS, y);
        SetGpuReg(REG_OFFSET_BG3VOFS, y);
        SetGpuReg(REG_OFFSET_BG0HOFS, s->bg0x);
        SetGpuReg(REG_OFFSET_BG0VOFS, s->bg0y);
    }
    if (s->regs)
    {
        SetGpuReg(REG_OFFSET_WININ, s->winin);
        SetGpuReg(REG_OFFSET_WINOUT, s->winout);
        SetGpuReg(REG_OFFSET_WIN0H, s->win0h);
        SetGpuReg(REG_OFFSET_WIN1H, s->win1h);
        SetGpuReg(REG_OFFSET_WIN0V, s->win0v);
        SetGpuReg(REG_OFFSET_WIN1V, s->win1v);
        SetGpuReg(REG_OFFSET_BLDCNT, s->bldcnt);
        SetGpuReg(REG_OFFSET_BLDALPHA, s->bldalpha);
        SetGpuReg(REG_OFFSET_BLDY, s->bldy);
    }
    if (s->lineFlags)
    {
        u16 *fr = s->dma[1];
        u32 i;
        DmaCopy16(3, s->dma[0], fr, sizeof(s->dma[1]));
        if (s->lineFlags & TIF_WIN0)
        {
            SetGpuReg(REG_OFFSET_WIN0H, fr[0]);
            DmaSet(0, &fr[1], &REG_WIN0H, TI_DMA_WIN);
        }
        else
        {
            for (i = 0; i < 6; i++)
                SetGpuReg(REG_OFFSET_BG1HOFS + i * 2, fr[i]);
            DmaSet(0, &fr[6], &REG_BG1HOFS, TI_DMA_SCROLL);
        }
    }
}

// per-beeldlijn-buffers aanzetten (de buffers beginnen op de huidige scroll). Óf TIF_WIN0, óf de scroll-vlaggen.
static void TI_Lines(u16 flags)
{
    u32 y;
    for (y = 0; y < DISPLAY_HEIGHT; y++)
    {
        sTI->back[TIB_BG0X][y] = sTI->bg0x;
        sTI->back[TIB_WX][y] = sTI->camX + sTI->wx;
        sTI->back[TIB_WY][y] = sTI->camY + sTI->wy;
        sTI->back[TIB_WIN0][y] = 0;
    }
    sTI->lineFlags |= flags;
    TI_BuildLines(sTI);
}

// vensters/blend: de VBlank schrijft ze elke frame. win: welke vensters aan (DISPCNT_WIN0_ON/WIN1_ON)
static void TI_Windows(u16 win, u16 winin, u16 winout)
{
    sTI->regs = TRUE;
    sTI->winin = winin;
    sTI->winout = winout;
    sTI->win0v = WIN_RANGE(0, DISPLAY_HEIGHT);
    sTI->win1v = WIN_RANGE(0, DISPLAY_HEIGHT);
    ClearGpuRegBits(REG_OFFSET_DISPCNT, DISPCNT_WIN0_ON | DISPCNT_WIN1_ON | DISPCNT_OBJWIN_ON);
    SetGpuRegBits(REG_OFFSET_DISPCNT, win);
}

static void TI_Blend(u16 bldcnt, u32 eva, u32 evb)
{
    sTI->regs = TRUE;
    sTI->bldcnt = bldcnt;
    sTI->bldalpha = BLDALPHA_BLEND(eva, evb);
}

#define TI_WIN_ALL (WININ_WIN0_ALL | WININ_WIN1_ALL)
#define TI_NO_BG0  (WINOUT_WIN01_BG1 | WINOUT_WIN01_BG2 | WINOUT_WIN01_BG3 | WINOUT_WIN01_OBJ)

// ---------------------------------------------------------------------------------------------------------------------
// tijd, toeval, kleur

static u32 TI_Rand(void)
{
    sTI->rng = sTI->rng * 1103515245 + 12345;
    return sTI->rng >> 16;
}

static s32 TI_RandRange(s32 lo, s32 hi)
{
    return lo + (s32)(TI_Rand() % (u32)(hi - lo + 1));
}

// frame (vanaf de start van de intro) van de n-de tel
static s32 TI_Beat(u32 n)
{
    return (s32)(((sTI->beat0 + n) * sTI->beatFx) >> 8) - sTI->start;
}

static s32 TI_Beat2(u32 n2)
{
    return (s32)(((sTI->beat0 * 2 + n2) * sTI->beatFx) >> 9) - sTI->start;
}

#define TI_AT(x) (sTI->last < (x) && t >= (x))

// 0..256 over [a, b]
static s32 TI_Ramp(s32 t, s32 a, s32 b)
{
    if (t <= a)
        return 0;
    if (t >= b || b <= a)
        return 256;
    return (t - a) * 256 / (b - a);
}

// paletten van de wereld (kaart-BG 0-12 + kaartsprites), zonder onze eigen sprites
static u32 TI_World(void)
{
    return (0x1FFF | 0xFFFF0000) & ~sTI->ours;
}

// getoonde kleuren = origineel gemengd met 'to' (k 0-16)
static void TI_Tint(u32 mask, s32 k, u16 to)
{
    u32 i, j;
    for (i = 0; i < 32; i++)
    {
        if (!((mask >> i) & 1))
            continue;
        if (k <= 0)
        {
            CpuCopy16(&sTI->base[i * 16], &gPlttBufferFaded[i * 16], PLTT_SIZE_4BPP);
            continue;
        }
        for (j = 0; j < 16; j++)
            gPlttBufferFaded[i * 16 + j] = Tapu_Blend(sTI->base[i * 16 + j], to, k);
    }
}

// stapelbaar: getoonde kleuren verder naar 'to'
static void TI_TintMore(u32 mask, s32 k, u16 to)
{
    u32 i, j;
    if (k <= 0)
        return;
    for (i = 0; i < 32; i++)
    {
        if (!((mask >> i) & 1))
            continue;
        for (j = 0; j < 16; j++)
            gPlttBufferFaded[i * 16 + j] = Tapu_Blend(gPlttBufferFaded[i * 16 + j], to, k);
    }
}

static s32 TI_Lum(u16 c)
{
    return ((c & 31) * 77 + ((c >> 5) & 31) * 150 + ((c >> 10) & 31) * 29) >> 8;
}

// de wereld naar grijs (k 0-16), daarna eventueel een kleurzweem
static void TI_Gray(u32 mask, s32 k)
{
    u32 i, j;
    for (i = 0; i < 32; i++)
    {
        if (!((mask >> i) & 1))
            continue;
        for (j = 0; j < 16; j++)
        {
            u16 c = sTI->base[i * 16 + j];
            s32 l = TI_Lum(c);
            gPlttBufferFaded[i * 16 + j] = Tapu_Blend(c, RGB(l, l, l), k);
        }
    }
}

// kort flitsen: k van 'from' naar 0 in len frames
static void TI_Flash(s32 t, s32 at, s32 len, s32 from, u32 mask, u16 color)
{
    if (t < at || t >= at + len)
        return;
    TI_TintMore(mask, from - (t - at) * from / len, color);
}

static void TI_SetCol(u32 pal, u32 idx, u16 c)
{
    gPlttBufferUnfaded[pal * 16 + idx] = gPlttBufferFaded[pal * 16 + idx] = sTI->base[pal * 16 + idx] = c;
}

static void TI_SetPal(u32 pal, const u16 *cols, u32 n)
{
    u32 i;
    for (i = 0; i < n; i++)
        TI_SetCol(pal, i, cols[i]);
}

// ---------------------------------------------------------------------------------------------------------------------
// de kaart: schudden/verschuiven (kaartsprites schuiven mee)

static void TI_WorldMove(s32 dx, s32 dy)
{
    u32 i;
    sTI->wx = dx;
    sTI->wy = dy;
    for (i = 0; i < sTI->nfield; i++)
    {
        struct Sprite *sp = &gSprites[sTI->field[i]];
        sp->x2 = -dx;
        sp->y2 = sTI->fieldY2[i] - dy;
    }
}

static void TI_Shake(s32 amp)
{
    if (amp <= 0)
        TI_WorldMove(0, 0);
    else
        TI_WorldMove(TI_RandRange(-amp, amp), TI_RandRange(-amp, amp));
    sTI->bg0x = sTI->bg0y = 0;
    if (amp > 0)
    {
        sTI->bg0x = sTI->wx;
        sTI->bg0y = sTI->wy;
    }
}

static void TI_HideField(void)
{
    u32 i;
    for (i = 0; i < OBJECT_EVENTS_COUNT; i++)
        if (gObjectEvents[i].active)
            gObjectEvents[i].invisible = TRUE;   // anders zet de kaart ze elke frame weer zichtbaar
    for (i = 0; i < sTI->nfield; i++)
        gSprites[sTI->field[i]].invisible = TRUE;
}

// ---------------------------------------------------------------------------------------------------------------------
// BG0 als tekenvel (palet 15; tiles worden aangemaakt waar getekend wordt)

static u32 TI_NewTile(void)
{
    u32 n = sTI->nextTile;
    if (n >= TI_MAX_TILES)
        return 0;
    sTI->nextTile++;
    CpuFill16(0, &sTI->bg0tiles[n * 16], 32);
    sTI->reserved = sTI->nextTile;
    return n;
}

static void TI_SolidTile(u32 n, u32 c)
{
    CpuFill32(c * 0x11111111, &sTI->bg0tiles[n * 16], 32);
}

static void TI_TilePixel(u32 n, u32 x, u32 y, u32 c)
{
    u16 *p = &sTI->bg0tiles[n * 16 + y * 2 + (x >> 2)];
    u32 sh = (x & 3) * 4;
    *p = (*p & ~(0xF << sh)) | (c << sh);
}

static void TI_FillMap(u16 entry)
{
    CpuFill16(entry, sTI->bg0map, 32 * 32 * 2);
}

static void TI_Put(s32 x, s32 y, u16 entry)
{
    if ((u32)x < 32 && (u32)y < 32)
        sTI->bg0map[y * 32 + x] = entry;
}

static void TI_Plot(s32 x, s32 y, u32 c)
{
    u16 *e, *p;
    u32 idx, sh;

    if ((u32)x >= DISPLAY_WIDTH || (u32)y >= DISPLAY_HEIGHT)
        return;
    e = &sTI->bg0map[(y >> 3) * 32 + (x >> 3)];
    idx = *e & 0x3FF;
    if (idx == 0 || idx < sTI->reserved)
    {
        u32 n;
        if (sTI->nextTile >= TI_MAX_TILES)
            return;
        n = sTI->nextTile++;
        if (idx == 0)
            CpuFill16(0, &sTI->bg0tiles[n * 16], 32);
        else
            CpuCopy16(&sTI->bg0tiles[idx * 16], &sTI->bg0tiles[n * 16], 32);
        idx = n;
        *e = idx | (*e & 0xF000 ? *e & 0xF000 : (15 << 12));
    }
    p = &sTI->bg0tiles[idx * 16 + (y & 7) * 2 + ((x & 7) >> 2)];
    sh = (x & 3) * 4;
    *p = (*p & ~(0xF << sh)) | (c << sh);
}

static void TI_Stamp(s32 x, s32 y, s32 r, u32 c)
{
    s32 i, j;
    for (j = -r; j <= r; j++)
        for (i = -r; i <= r; i++)
            if (i * i + j * j <= r * r + r)
                TI_Plot(x + i, y + j, c);
}

// lijn, alleen het stuk tussen from en to (0-256)
static void TI_Line(s32 x0, s32 y0, s32 x1, s32 y1, s32 from, s32 to, s32 r, u32 c)
{
    s32 dx = x1 - x0, dy = y1 - y0, n = max(abs(dx), abs(dy)), i, i0, i1;
    if (n == 0)
        return;
    i0 = n * from >> 8;
    i1 = n * to >> 8;
    for (i = i0; i <= i1; i++)
    {
        if (r == 0)
            TI_Plot(x0 + dx * i / n, y0 + dy * i / n, c);
        else
            TI_Stamp(x0 + dx * i / n, y0 + dy * i / n, r, c);
    }
}

static void TI_Rect(s32 x0, s32 y0, s32 x1, s32 y1, u32 c)
{
    s32 x, y;
    for (y = y0; y < y1; y++)
        for (x = x0; x < x1; x++)
            TI_Plot(x, y, c);
}

// vulling vanaf de onderkant: tiles base+k (k = 1..8 onderste rijen gevuld, bovenste gevulde rij = rand 'edge'),
// base+9 = vol zonder rand, base+0 leeg (niet gebruikt)
static u32 TI_MakeFillTiles(u32 fill, u32 edge)
{
    u32 base = sTI->nextTile, k, x, y;
    for (k = 0; k < 10; k++)
        TI_NewTile();
    for (k = 1; k <= 9; k++)
    {
        u32 n = base + k, rows = k > 8 ? 8 : k;
        for (y = 8 - rows; y < 8; y++)
            for (x = 0; x < 8; x++)
                TI_TilePixel(n, x, y, (k <= 8 && y == 8 - rows) ? edge : fill);
    }
    return base;
}

// kolommen (31 stuks, 8 px breed) vullen vanaf top[c] (pixel-y) naar beneden; flip = van boven naar beneden
static void TI_DrawColumns(const s16 *top, u32 base, u32 pal, bool32 flip)
{
    s32 c, r;
    for (c = 0; c < 31; c++)
    {
        s32 tp = top[c];
        for (r = 0; r < 21; r++)
        {
            s32 y0 = flip ? (160 - (r + 1) * 8) : r * 8, filled;
            u16 e = 0;
            if (!flip)
                filled = y0 + 8 - tp;
            else
                filled = (tp) - y0;   // flip: tp = onderkant van de vulling van boven
            if (filled >= 8)
                e = (!flip && tp == y0) || (flip && tp == y0 + 8) ? base + 8 : base + 9;
            else if (filled > 0)
                e = base + filled;
            if (e != 0)
                e |= (pal << 12) | (flip ? 0x800 : 0);
            sTI->bg0map[(flip ? 19 - r : r) * 32 + c] = e;
        }
    }
}

// ---------------------------------------------------------------------------------------------------------------------
// tekst: via een tijdelijk venster in een buffer renderen (FONT_NORMAL: kleur 0 = achtergrond)

static void TI_TextBuf(void *dst, const u8 *str, u32 w, u32 h, s32 x, s32 y, u8 bg, u8 fg, u8 sh, u8 font)
{
    struct WindowTemplate tmpl = {.bg = 0, .tilemapLeft = 0, .tilemapTop = 0, .width = w, .height = h, .paletteNum = 15, .baseBlock = 1};
    u8 colors[3];
    u32 win;

    colors[0] = bg;
    colors[1] = fg;
    colors[2] = sh;
    win = AddWindow(&tmpl);
    if (win == WINDOW_NONE)
    {
        CpuFill32(bg * 0x11111111, dst, w * h * 32);
        return;
    }
    FillWindowPixelBuffer(win, PIXEL_FILL(bg));
    if (x < 0) // gecentreerd
        x = ((s32)w * 8 - GetStringWidth(font, str, 0)) / 2;
    AddTextPrinterParameterized3(win, font, x, y, colors, TEXT_SKIP_DRAW, str);
    CpuCopy16(gWindows[win].tileData, dst, w * h * 32);
    RemoveWindow(win);
}

// tekst als BG0-blok (w x h tiles) op tile-positie (tx, ty) met palet pal
static void TI_TextBg(const u8 *str, s32 tx, s32 ty, u32 w, u32 h, s32 x, s32 y, u8 bg, u8 fg, u8 sh, u8 font, u32 pal)
{
    u32 first = sTI->nextTile, i, j;
    if (first + w * h > TI_MAX_TILES)
        return;
    sTI->nextTile += w * h;
    sTI->reserved = sTI->nextTile;
    TI_TextBuf(&sTI->bg0tiles[first * 16], str, w, h, x, y, bg, fg, sh, font);
    for (j = 0; j < h; j++)
        for (i = 0; i < w; i++)
            TI_Put(tx + i, ty + j, (first + j * w + i) | (pal << 12));
}

// ---------------------------------------------------------------------------------------------------------------------
// sprites (alles wordt aan het eind opgeruimd)

static u32 TI_PalBit(u8 id)
{
    return 1 << (16 + gSprites[id].oam.paletteNum);
}

static u8 TI_Track(u8 id, u8 kind)
{
    if (id >= MAX_SPRITES)
        return MAX_SPRITES;
    gSprites[id].oam.priority = 0;
    if (sTI->nspr < TI_MAX_SPR)
    {
        sTI->spr[sTI->nspr] = id;
        sTI->kind[sTI->nspr] = kind;
        sTI->nspr++;
    }
    sTI->ours |= TI_PalBit(id);
    return id;
}

static void TI_AddTag(u16 tag)
{
    if (sTI->ntags < TI_MAX_TAGS)
        sTI->tags[sTI->ntags++] = tag;
}

static void TI_AffineInit(u8 id)
{
    if (gSprites[id].oam.affineMode != ST_OAM_AFFINE_OFF)
    {
        gSprites[id].affineAnimPaused = TRUE;
        SetOamMatrixRotationScaling(gSprites[id].oam.matrixNum, 256, 256, 0);
    }
}

// gevechtsanimatie-sprite (ANIM_TAG_*); tileOfs = eerste tile van het frame
static u8 TI_Anim(u16 tag, const struct OamData *oam, s16 x, s16 y, u16 tileOfs)
{
    struct SpriteTemplate tmpl = {
        .tileTag = tag, .paletteTag = tag, .oam = oam, .anims = gDummySpriteAnimTable, .images = NULL,
        .affineAnims = gDummySpriteAffineAnimTable, .callback = SpriteCallbackDummy,
    };
    u32 i = tag - ANIM_SPRITES_START;
    u8 id;
    if (GetSpriteTileStartByTag(tag) == 0xFFFF)
    {
        LoadCompressedSpriteSheet(&gBattleAnimPicTable[i]);
        TI_AddTag(tag);
    }
    if (IndexOfSpritePaletteTag(tag) == 0xFF)
        LoadSpritePalette(&gBattleAnimPaletteTable[i]);
    id = CreateSprite(&tmpl, x, y, 1);
    if (id >= MAX_SPRITES)
        return MAX_SPRITES;
    gSprites[id].oam.tileNum += tileOfs;
    TI_AffineInit(id);
    return TI_Track(id, TIK_SPRITE);
}

// sprite uit een buffer (procedureel getekend of tekst)
static u8 TI_BufSprite(const void *gfx, u32 size, u16 tag, const u16 *pal, const struct OamData *oam, s16 x, s16 y)
{
    struct SpriteSheet sheet = {gfx, size, tag};
    struct SpritePalette spal = {pal, tag};
    struct SpriteTemplate tmpl = {
        .tileTag = tag, .paletteTag = tag, .oam = oam, .anims = gDummySpriteAnimTable, .images = NULL,
        .affineAnims = gDummySpriteAffineAnimTable, .callback = SpriteCallbackDummy,
    };
    u8 id;
    if (GetSpriteTileStartByTag(tag) == 0xFFFF)
    {
        LoadSpriteSheet(&sheet);
        TI_AddTag(tag);
    }
    if (IndexOfSpritePaletteTag(tag) == 0xFF)
        LoadSpritePalette(&spal);
    id = CreateSprite(&tmpl, x, y, 0);
    if (id >= MAX_SPRITES)
        return MAX_SPRITES;
    TI_AffineInit(id);
    return TI_Track(id, TIK_SPRITE);
}

// tekst-sprite: w x h tiles (64x32 = 8x4), kleuren 1 (letter) en 2 (schaduw) uit pal
static u8 TI_TextSprite(const u8 *str, u32 w, u32 h, s32 y, u16 tag, const u16 *pal, const struct OamData *oam, s16 sx, s16 sy)
{
    u8 *buf = Alloc(w * h * 32), id;
    if (buf == NULL)
        return MAX_SPRITES;
    TI_TextBuf(buf, str, w, h, -1, y, 0, 1, 2, FONT_NORMAL);
    id = TI_BufSprite(buf, w * h * 32, tag, pal, oam, sx, sy);
    Free(buf);
    return id;
}

static u8 TI_Item(u16 tag, u16 item, s16 x, s16 y)
{
    u8 id = AddItemIconSprite(tag, tag, item);
    if (id >= MAX_SPRITES)
        return MAX_SPRITES;
    gSprites[id].x = x;
    gSprites[id].y = y;
    TI_AddTag(tag);
    return TI_Track(id, TIK_ITEM);
}

static u8 TI_Trainer(u16 pic, s16 x, s16 y, bool32 affine)
{
    u8 id = CreateTrainerSprite(pic, x, y, 0, NULL);
    if (id >= MAX_SPRITES)
        return MAX_SPRITES;
    if (affine)
    {
        struct Sprite *sp = &gSprites[id];
        sp->oam.affineMode = ST_OAM_AFFINE_DOUBLE;
        sp->oam.matrixNum = AllocOamMatrix();
        CalcCenterToCornerVec(sp, SPRITE_SHAPE(64x64), SPRITE_SIZE(64x64), ST_OAM_AFFINE_DOUBLE);
        SetOamMatrixRotationScaling(sp->oam.matrixNum, 256, 256, 0);
    }
    return TI_Track(id, TIK_TRAINER);
}

// schaal als matrixwaarde: 256 = normaal, 128 = 2x zo groot, -256 = gespiegeld (SetOamMatrixRotationScaling wil de zoom zelf)
static void TI_Scale(u8 id, s32 sx, s32 sy, u16 rot)
{
    if (id < MAX_SPRITES && gSprites[id].oam.affineMode != ST_OAM_AFFINE_OFF)
    {
        if (sx == 0)
            sx = 1;
        if (sy == 0)
            sy = 1;
        SetOamMatrixRotationScaling(gSprites[id].oam.matrixNum, 65536 / sx, 65536 / sy, rot);
    }
}

static void TI_Pos(u8 id, s32 x, s32 y)
{
    if (id >= MAX_SPRITES)
        return;
    gSprites[id].x = x;
    gSprites[id].y = y;
}

static void TI_Show(u8 id, bool32 on)
{
    if (id < MAX_SPRITES)
        gSprites[id].invisible = !on;
}

// ---------------------------------------------------------------------------------------------------------------------
// deeltjes (een sprite met snelheid en zwaartekracht)

static struct TIPart *TI_Part(u8 id, s32 x, s32 y, s32 vx, s32 vy, s32 ay, s32 life)
{
    u32 i;
    if (id >= MAX_SPRITES)
        return NULL;
    for (i = 0; i < TI_MAX_PART; i++)
    {
        struct TIPart *p = &sTI->part[i];
        if (p->on)
            continue;
        p->on = TRUE;
        p->slot = id;
        p->x = x * 16;
        p->y = y * 16;
        p->vx = vx;
        p->vy = vy;
        p->ax = 0;
        p->ay = ay;
        p->life = life;
        p->bounce = FALSE;
        TI_Pos(id, x, y);
        TI_Show(id, TRUE);
        return p;
    }
    return NULL;
}

static void TI_UpdateParts(void)
{
    u32 i;
    for (i = 0; i < TI_MAX_PART; i++)
    {
        struct TIPart *p = &sTI->part[i];
        if (!p->on)
            continue;
        p->vx += p->ax;
        p->vy += p->ay;
        p->x += p->vx;
        p->y += p->vy;
        if (p->bounce && p->y > 150 * 16 && p->vy > 0)
        {
            p->y = 150 * 16;
            p->vy = -p->vy / 2;
            p->vx = p->vx * 3 / 4;
        }
        if (p->life > 0 && --p->life == 0)
        {
            p->on = FALSE;
            TI_Show(p->slot, FALSE);
            continue;
        }
        TI_Pos(p->slot, p->x >> 4, p->y >> 4);
    }
}

// ---------------------------------------------------------------------------------------------------------------------
// de runner

#define tTiState data[0]
#define tTiDelay data[1]

static void TI_Free(void)
{
    u32 i;
    for (i = 0; i < sTI->nspr; i++)
    {
        struct Sprite *sp = &gSprites[sTI->spr[i]];
        if (!sp->inUse)
            continue;
        switch (sTI->kind[i])
        {
        case TIK_TRAINER:
            if (sp->oam.affineMode != ST_OAM_AFFINE_OFF)
                FreeSpriteOamMatrix(sp);
            DestroySpriteAndFreeResources(sp);
            break;
        case TIK_MON:
            break;
        default:
            if (sp->oam.affineMode != ST_OAM_AFFINE_OFF)
                FreeSpriteOamMatrix(sp);
            DestroySprite(sp);
            break;
        }
    }
    if (sTI->monSpr != 0xFFFF)
        FreeAndDestroyMonPicSprite(sTI->monSpr);
    for (i = 0; i < sTI->ntags; i++)
    {
        FreeSpriteTilesByTag(sTI->tags[i]);
        FreeSpritePaletteByTag(sTI->tags[i]);
    }
}

static void TI_Run(u8 taskId, const struct TIntro *in)
{
    struct Task *task = &gTasks[taskId];
    s32 t;
    bool32 done;
    u32 i;

    switch (task->tTiState)
    {
    case 0:
        sTI = AllocZeroed(sizeof(*sTI));
        if (sTI == NULL)
        {
            FadeScreenBlack();
            DestroyTask(taskId);
            return;
        }
        InitTransitionData();
        ScanlineEffect_Clear();
        sTI->intro = in;
        sTI->monSpr = 0xFFFF;
        sTI->start = Tapu_Elapsed();
        sTI->last = -1;
        // tempo uit de BGM-speler (tempoD = BPM); ROTATE wisselt thema's, zo valt elke intro op de tel van zijn thema
        i = gMPlayInfo_BGM.tempoD;
        if (i < 60 || i > 300)
            i = 150;
        sTI->beatFx = TI_FX(i);
        sTI->beat0 = ((sTI->start + 8) * 256 + sTI->beatFx - 1) / sTI->beatFx;
        sTI->rng = 0x7E57 ^ (gMain.vblankCounter1 * 2654435761u);
        sTI->trainer = TRAINER_BATTLE_PARAM.opponentA;
        sTI->elem = sTI_PendingElem;
        sTI->camX = sTransitionData->cameraX;
        sTI->camY = sTransitionData->cameraY;
        sTI->scroll = TRUE;
        for (i = 0; i < MAX_SPRITES; i++)
        {
            if (gSprites[i].inUse && !gSprites[i].invisible)
            {
                sTI->fieldY2[sTI->nfield] = gSprites[i].y2;
                sTI->field[sTI->nfield++] = i;
            }
        }
        GetBg0TilesDst(&sTI->bg0map, &sTI->bg0tiles);
        CpuFill16(0, sTI->bg0map, BG_SCREEN_SIZE);
        CpuFill16(0, sTI->bg0tiles, 32);
        sTI->nextTile = sTI->reserved = 1;
        SetGpuRegBits(REG_OFFSET_DISPCNT, DISPCNT_BG0_ON | DISPCNT_OBJ_ON);
        TI_Windows(0, WININ_WIN0_ALL | WININ_WIN1_ALL, WINOUT_WIN01_ALL);   // geen vensters, alles zichtbaar
        sTI->bldcnt = 0;
        in->init();
        CpuCopy16(gPlttBufferFaded, sTI->base, PLTT_SIZE);
        SetVBlankCallback(VBlankCB_TI);
        task->tTiState++;
        break;
    case 1:
        t = Tapu_Elapsed() - sTI->start;
        gPaletteFade.bufferTransferDisabled = TRUE;
        CpuCopy16(sTI->base, gPlttBufferFaded, PLTT_SIZE);
        done = in->update(t);
        TI_UpdateParts();
        if (sTI->lineFlags)
            TI_BuildLines(sTI);
        gPaletteFade.bufferTransferDisabled = FALSE;
        sTI->last = t;
        if (done)
        {
            task->tTiDelay = 2;
            task->tTiState++;
        }
        break;
    case 2:
        if (--task->tTiDelay == 0)
        {
            CpuCopy16(gPlttBufferFaded, gPlttBufferUnfaded, PLTT_SIZE);
            BeginNormalPaletteFade(PALETTES_ALL, 0, 0, 16, RGB_BLACK);
            task->tTiState++;
        }
        break;
    case 3:
        if (!gPaletteFade.active)
        {
            DmaStop(0);
            SetVBlankCallback(VBlankCB_BattleTransition);
            ClearGpuRegBits(REG_OFFSET_DISPCNT, DISPCNT_WIN0_ON | DISPCNT_WIN1_ON | DISPCNT_OBJWIN_ON);
            SetGpuReg(REG_OFFSET_BLDCNT, 0);
            SetGpuReg(REG_OFFSET_BLDY, 0);
            SetGpuReg(REG_OFFSET_BG0HOFS, 0);
            SetGpuReg(REG_OFFSET_BG0VOFS, 0);
            for (i = 0; i < sTI->nspr; i++)
                gSprites[sTI->spr[i]].invisible = TRUE;
            TI_Free();
            FREE_AND_SET_NULL(sTI);
            DmaStop(0);
            FadeScreenBlack();
            DestroyTask(taskId);
        }
        break;
    }
}

#undef tTiState
#undef tTiDelay

// gedeelde kleine sprites: een "!" (16x32, met de hand getekend) en een dobber (8x8)
static const u16 sTI_BangPal[4] = {0, RGB(31, 31, 31), RGB(4, 4, 6), RGB(31, 6, 4)};
#define TI_TAG_BANG   0x7A01
#define TI_TAG_BOBBER 0x7A02
#define TI_TAG_TEXT1  0x7A03
#define TI_TAG_TEXT2  0x7A04
#define TI_TAG_TEXT3  0x7A05
#define TI_TAG_ITEM   0x7A06

static void TI_BufPixel(u8 *buf, u32 wTiles, u32 x, u32 y, u32 c)
{
    u8 *p = &buf[((y >> 3) * wTiles + (x >> 3)) * 32 + (y & 7) * 4 + ((x & 7) >> 1)];
    if (x & 1)
        *p = (*p & 0x0F) | (c << 4);
    else
        *p = (*p & 0xF0) | c;
}

static u8 TI_Bang(s16 x, s16 y)
{
    u8 buf[2 * 4 * 32], id;
    s32 px, py;
    memset(buf, 0, sizeof(buf));
    for (py = 2; py < 30; py++)
        for (px = 3; px < 13; px++)
        {
            bool32 bar = (py >= 3 && py < 21 && px >= 5 + (py > 15) && px < 11 - (py > 15));
            bool32 dot = (py >= 24 && py < 29 && px >= 5 && px < 11);
            bool32 in = (py >= 2 && py < 22 && px >= 4 + (py > 15) && px < 12 - (py > 15)) || (py >= 23 && py < 30 && px >= 4 && px < 12);
            if (bar || dot)
                TI_BufPixel(buf, 2, px, py, 3);
            else if (in)
                TI_BufPixel(buf, 2, px, py, 2);
        }
    id = TI_BufSprite(buf, sizeof(buf), TI_TAG_BANG, sTI_BangPal, &gOamData_AffineDouble_ObjNormal_16x32, x, y);
    TI_Show(id, FALSE);
    return id;
}

// ---------------------------------------------------------------------------------------------------------------------
// de klasse-intro's

enum
{
    CI_NONE, CI_SWIM, CI_HIKER, CI_BUG, CI_PSYCHIC, CI_FISH, CI_BIRD, CI_KINDLER, CI_GUITAR, CI_RUIN, CI_HEX, CI_CHOP,
    CI_COOL, CI_TRI, CI_EXPERT, CI_SAILOR, CI_PICNIC, CI_BOUNCE, CI_RANGER, CI_PETAL, CI_NINJA, CI_HEART, CI_COINS,
    CI_COUNT
};

static u32 ClassIntro_ForClass(u32 trainerClass)
{
    switch (trainerClass)
    {
    case TRAINER_CLASS_SWIMMER_M: case TRAINER_CLASS_SWIMMER_F: case TRAINER_CLASS_TUBER_M: case TRAINER_CLASS_TUBER_F:
        return CI_SWIM;
    case TRAINER_CLASS_HIKER:
        return CI_HIKER;
    case TRAINER_CLASS_BUG_CATCHER: case TRAINER_CLASS_BUG_MANIAC:
        return CI_BUG;
    case TRAINER_CLASS_PSYCHIC:
        return CI_PSYCHIC;
    case TRAINER_CLASS_FISHERMAN:
        return CI_FISH;
    case TRAINER_CLASS_BIRD_KEEPER:
        return CI_BIRD;
    case TRAINER_CLASS_KINDLER:
        return CI_KINDLER;
    case TRAINER_CLASS_GUITARIST:
        return CI_GUITAR;
    case TRAINER_CLASS_RUIN_MANIAC:
        return CI_RUIN;
    case TRAINER_CLASS_HEX_MANIAC:
        return CI_HEX;
    case TRAINER_CLASS_BLACK_BELT: case TRAINER_CLASS_BATTLE_GIRL:
        return CI_CHOP;
    case TRAINER_CLASS_COOLTRAINER: case TRAINER_CLASS_COOLTRAINER_2:
        return CI_COOL;
    case TRAINER_CLASS_TRIATHLETE:
        return CI_TRI;
    case TRAINER_CLASS_EXPERT:
        return CI_EXPERT;
    case TRAINER_CLASS_SAILOR:
        return CI_SAILOR;
    case TRAINER_CLASS_PICNICKER: case TRAINER_CLASS_CAMPER:
        return CI_PICNIC;
    case TRAINER_CLASS_YOUNGSTER: case TRAINER_CLASS_SCHOOL_KID:
        return CI_BOUNCE;
    case TRAINER_CLASS_PKMN_RANGER:
        return CI_RANGER;
    case TRAINER_CLASS_BEAUTY: case TRAINER_CLASS_AROMA_LADY: case TRAINER_CLASS_PARASOL_LADY: case TRAINER_CLASS_LASS:
    case TRAINER_CLASS_LADY:
        return CI_PETAL;
    case TRAINER_CLASS_NINJA_BOY:
        return CI_NINJA;
    case TRAINER_CLASS_PKMN_BREEDER: case TRAINER_CLASS_POKEFAN:
        return CI_HEART;
    case TRAINER_CLASS_RICH_BOY: case TRAINER_CLASS_GENTLEMAN:
        return CI_COINS;
    }
    return CI_NONE;
}

bool32 ClassIntro_HasIntro(u32 trainerClass)
{
    return ClassIntro_ForClass(trainerClass) != CI_NONE;
}

// ---------------- Swimmer/Tuber: het water komt omhoog, spetters, op de 2e tel een fontein, dan kopje onder
static const u16 sCI_WaterPal[4] = {0, RGB(5, 13, 27), RGB(26, 30, 31), RGB(9, 19, 30)};

static void CISwim_Init(void)
{
    u32 i;
    TI_SetPal(15, sCI_WaterPal, 4);
    sTI->v[0] = TI_MakeFillTiles(1, 2);
    TI_Blend(BLDCNT_TGT1_BG0 | BLDCNT_EFFECT_BLEND | BLDCNT_TGT2_BG1 | BLDCNT_TGT2_BG2 | BLDCNT_TGT2_BG3 | BLDCNT_TGT2_OBJ, 9, 7);
    for (i = 0; i < 10; i++)
        sTI->v[4 + i] = TI_Anim(ANIM_TAG_SMALL_BUBBLES, &gOamData_AffineOff_ObjNormal_16x16, 0, 200, (i & 1) * 4), TI_Show(sTI->v[4 + i], FALSE);
    sTI->v[1] = TI_Anim(ANIM_TAG_SPLASH, &gOamData_AffineDouble_ObjNormal_64x64, 120, 220, 0);
    TI_Scale(sTI->v[1], 128, 128, 0);
    TI_Show(sTI->v[1], FALSE);
    PlaySE(SE_M_SURF);
}

static bool32 CISwim_Update(s32 t)
{
    s16 top[31];
    s32 end = TI_Beat(4), lvl, c, k;
    lvl = 176 - (TI_Ramp(t, 0, end) * 196 >> 8);
    for (c = 0; c < 31; c++)
        top[c] = lvl + Sin((c * 20 + t * 7) & 0xFF, 5) + Sin((c * 47 - t * 4) & 0xFF, 3);
    TI_DrawColumns(top, sTI->v[0], 15, FALSE);
    k = 9 + (TI_Ramp(t, TI_Beat(2), end) * 7 >> 8);
    sTI->bldalpha = BLDALPHA_BLEND(k, 16 - k);
    if ((t & 7) == 0 && lvl < 168 && lvl > 0)
    {
        u32 i = 4 + ((t >> 3) % 10);
        TI_Part(sTI->v[i], TI_RandRange(8, 232), lvl, TI_RandRange(-12, 12), -TI_RandRange(30, 48), 3, 30);
    }
    if (TI_AT(TI_Beat(2)))
    {
        PlaySE(SE_M_WATERFALL);
        TI_Part(sTI->v[1], 120, lvl + 8, 0, -40, 2, end - t);
    }
    TI_Flash(t, TI_Beat(2), 8, 8, TI_World(), RGB_WHITE);
    return t >= end + 2;
}

static const struct TIntro sCI_Swim = {CISwim_Init, CISwim_Update};

// ---------------- Hiker: rotsblokken rollen van boven het beeld in en stuiteren; elke tel barst het scherm verder
static const u16 sCI_CrackPal[4] = {0, RGB(2, 2, 3), RGB(20, 20, 22), RGB(31, 31, 31)};
#define HK_ROCKS 6

static void CIHiker_Init(void)
{
    u32 i;
    TI_SetPal(15, sCI_CrackPal, 4);
    for (i = 0; i < HK_ROCKS; i++)
    {
        sTI->v[i] = TI_Anim(ANIM_TAG_ROCKS, &gOamData_AffineNormal_ObjNormal_32x32, -40, -40, (i % 6) * 16);
        TI_Show(sTI->v[i], FALSE);
    }
}

// barst vanaf (x, y): een paar zigzaggende takken (deterministisch per seed)
static void CIHiker_Crack(s32 x0, s32 y0, u32 seed, s32 grow)
{
    u32 b, j, r = seed;
    for (b = 0; b < 4; b++)
    {
        s32 x = x0, y = y0, ang = (b * 64 + (r & 31)) & 0xFF;
        for (j = 0; j < 5; j++)
        {
            s32 len = 10 + (r >> 8) % 12, nx, ny;
            r = r * 1103515245 + 12345;
            ang = (ang + ((s32)((r >> 16) & 63) - 32)) & 0xFF;
            nx = x + Cos(ang, len);
            ny = y + Sin(ang, len);
            if ((s32)j * 51 > grow)
                break;
            TI_Line(x, y, nx, ny, 0, 256, 0, 1);
            TI_Line(x + 1, y + 1, nx + 1, ny + 1, 0, 256, 0, 3);
            x = nx;
            y = ny;
        }
    }
}

static bool32 CIHiker_Update(s32 t)
{
    s32 n, end = TI_Beat(4);
    static const s16 sImpact[3][2] = {{70, 110}, {170, 60}, {120, 90}};
    for (n = 0; n < 3; n++)
    {
        s32 at = TI_Beat(n + 1);
        if (TI_AT(at - 22))
        {
            struct TIPart *p = TI_Part(sTI->v[n], n == 1 ? 260 : -20, -30, n == 1 ? -40 : 40, 0, 4, 0);
            if (p != NULL)
            {
                // landt rond 'at' op het inslagpunt
                p->vx = (sImpact[n][0] * 16 - p->x) / 22;
                p->vy = (sImpact[n][1] * 16 - p->y) / 22 - 2 * 22;
            }
        }
        if (TI_AT(at))
        {
            PlaySE(SE_M_ROCK_THROW);
            CIHiker_Crack(sImpact[n][0], sImpact[n][1], 0x1234 + n * 777, 256);
            sTI->v[10] = 6;
        }
    }
    // kleine rolsteentjes
    if (TI_AT(4))
    {
        struct TIPart *p = TI_Part(sTI->v[3], 250, 140, -36, -20, 3, 0);
        if (p)
            p->bounce = TRUE;
    }
    if (TI_AT(14))
    {
        struct TIPart *p = TI_Part(sTI->v[4], -10, 120, 30, -30, 3, 0);
        if (p)
            p->bounce = TRUE;
    }
    for (n = 0; n < HK_ROCKS; n++)
        TI_Scale(sTI->v[n], 256, 256, t * (n & 1 ? 9 : -7));
    if (sTI->v[10] > 0)
        sTI->v[10]--;
    TI_Shake(sTI->v[10]);
    if (t >= TI_Beat(4) - 6)
        TI_Tint(TI_World(), TI_Ramp(t, end - 6, end) * 12 >> 8, RGB(2, 2, 3));
    TI_Flash(t, TI_Beat(3), 6, 10, TI_World(), RGB_WHITE);
    return t >= end;
}

static const struct TIntro sCI_Hiker = {CIHiker_Init, CIHiker_Update};

// ---------------- Bug Catcher: het net (een web) zwiept heen en terug, dan zit het beeld vast en spartelt het drie keer
static void CIBug_Init(void)
{
    sTI->v[0] = TI_Anim(ANIM_TAG_SPIDER_WEB, &gOamData_AffineDouble_ObjNormal_64x64, -100, 80, 0);
}

static bool32 CIBug_Update(s32 t)
{
    s32 b1 = TI_Beat(1), b2 = TI_Beat(2), b3 = TI_Beat(3), end = TI_Beat(6), x, y, sc, k, a;
    u8 web = sTI->v[0];
    if (t < b2)
    {
        // zwaai over een boog rond een draaipunt onder het scherm
        s32 r = TI_Ramp(t, 0, b1);
        if (t >= b1)
            r = 256 - TI_Ramp(t, b1, b2);
        a = 160 - (r * 96 >> 8);   // hoek in 256-stappen
        x = 120 + Cos(a & 0xFF, 150);
        y = 230 - Sin(a & 0xFF, 190);
        TI_Pos(web, x, y);
        TI_Scale(web, 128, 128, (a - 192) << 8);
        if (TI_AT(4) || TI_AT(b1))
            PlaySE(SE_M_STRING_SHOT);
        TI_Tint(TI_World(), 0, 0);
    }
    else
    {
        // het net valt over het beeld: groot, in het midden; het beeld spartelt (zoals een Poké Ball)
        sc = 160 - (TI_Ramp(t, b2, b2 + 6) * 32 >> 8);   // hoogstens 2x (groter knipt de dubbele affine-box af)
        TI_Pos(web, 120, 80);
        k = 0;
        if (t >= b3)
        {
            s32 w = ((t - b3) * 256 / max(1, (TI_Beat(4) - b3))) & 0xFF;
            s32 n = (t - b3) / max(1, (TI_Beat(4) - b3));
            if (n < 3)
                k = Sin(w, 14);
            if (TI_AT(TI_Beat(3)) || TI_AT(TI_Beat(4)) || TI_AT(TI_Beat(5)))
                PlaySE(SE_BALL_BOUNCE_1);
        }
        if (TI_AT(TI_Beat(6) - 4))
            PlaySE(SE_RG_BALL_CLICK);
        TI_Scale(web, sc, sc, (k * 64) & 0xFFFF);
        TI_WorldMove(k, 0);
        TI_Tint(TI_World(), 5, RGB(4, 10, 2));
    }
    return t >= end;
}

static const struct TIntro sCI_Bug = {CIBug_Init, CIBug_Update};

// ---------------- Psychic: een lepel buigt op de tel, de wereld golft steeds harder mee, paars
static void CIPsychic_Init(void)
{
    sTI->v[0] = TI_Anim(ANIM_TAG_BENT_SPOON, &gOamData_AffineDouble_ObjNormal_16x32, 120, 78, 0);
    TI_Scale(sTI->v[0], 96, 96, 0);
    TI_Lines(TIF_WX);
    PlaySE(SE_M_PSYBEAM);
}

static bool32 CIPsychic_Update(s32 t)
{
    s32 end = TI_Beat(4), amp, y, f;
    u16 base = sTI->camX;
    f = 0;
    for (y = 1; y <= 4; y++)
        if (t >= TI_Beat(y))
            f = y;
    if (t >= end - 4)
        f = 5;
    gSprites[sTI->v[0]].oam.tileNum = GetSpriteTileStartByTag(ANIM_TAG_BENT_SPOON) + f * 8;
    amp = 1 + (TI_Ramp(t, 0, end) * 14 >> 8);
    for (y = 0; y < DISPLAY_HEIGHT; y++)
        sTI->back[TIB_WX][y] = base + Sin((y * 4 + t * 6) & 0xFF, amp);
    TI_Tint(TI_World(), TI_Ramp(t, 0, end) * 9 >> 8, RGB(18, 6, 26));
    TI_Scale(sTI->v[0], 96 - f * 4, 96 + f * 3, Sin((t * 8) & 0xFF, 6) << 8);
    if (TI_AT(TI_Beat(2)))
        PlaySE(SE_M_TELEPORT);
    TI_Flash(t, end - 4, 6, 12, PALETTES_ALL, RGB(31, 26, 31));
    return t >= end + 2;
}

static const struct TIntro sCI_Psychic = {CIPsychic_Init, CIPsychic_Update};

// ---------------- Fisherman: lijn uitgooien, dobber, "!", en het beeld wordt opgehaald
static const u16 sCI_LinePal[4] = {0, RGB(28, 28, 26), RGB(10, 10, 10), RGB(31, 6, 4)};
static const u16 sCI_BobberPal[4] = {0, RGB(31, 5, 4), RGB(31, 31, 31), RGB(4, 4, 4)};

static void CIFish_Init(void)
{
    u8 buf[32];
    s32 x, y;
    TI_SetPal(15, sCI_LinePal, 4);
    memset(buf, 0, sizeof(buf));
    for (y = 1; y < 7; y++)
        for (x = 1; x < 7; x++)
            if ((2 * x - 7) * (2 * x - 7) + (2 * y - 7) * (2 * y - 7) < 32)
                TI_BufPixel(buf, 1, x, y, y < 4 ? 1 : 2);
    sTI->v[0] = TI_BufSprite(buf, 32, TI_TAG_BOBBER, sCI_BobberPal, &gOamData_AffineOff_ObjNormal_8x8, -20, -20);
    sTI->v[1] = TI_Bang(150, 40);
    sTI->v[2] = TI_Anim(ANIM_TAG_SMALL_BUBBLES, &gOamData_AffineOff_ObjNormal_16x16, 0, 200, 0);
    TI_Show(sTI->v[2], FALSE);
    TI_Windows(DISPCNT_WIN0_ON, WININ_WIN0_ALL, 0);
    sTI->win0h = WIN_RANGE(0, DISPLAY_WIDTH);
    PlaySE(SE_M_FLY);
}

static bool32 CIFish_Update(s32 t)
{
    s32 b1 = TI_Beat(1), b2 = TI_Beat(2), b3 = TI_Beat(3), end = TI_Beat(4) + 6, r, x, y, i, off = 0;
    // boog van de hengeltop (0, 150) naar (150, 70)
    if (t <= b1)
    {
        r = TI_Ramp(t, 0, b1);
        x = 4 + (146 * r >> 8);
        y = 150 - (80 * r >> 8) - (Sin((r >> 1) & 0xFF, 50));
        TI_Pos(sTI->v[0], x, y);
        for (i = sTI->v[3]; i <= r; i += 8)
        {
            s32 px = 4 + (146 * i >> 8), py = 150 - (80 * i >> 8) - Sin((i >> 1) & 0xFF, 50);
            TI_Plot(px, py, 1);
        }
        sTI->v[3] = r & ~7;
    }
    if (TI_AT(b1))
    {
        PlaySE(SE_M_BUBBLE);
        TI_Part(sTI->v[2], 146, 66, 0, -10, 1, 16);
    }
    if (t > b1 && t < b3)
        TI_Pos(sTI->v[0], 150, 70 + (Sin((t * 12) & 0xFF, 2)) + (t >= b2 ? 4 : 0));
    if (TI_AT(b2))
    {
        PlaySE(SE_PIN);
        TI_Show(sTI->v[1], TRUE);
        TI_Scale(sTI->v[1], 128, 128, 0);
    }
    if (t >= b3)
    {
        // ophalen: de wereld gaat omhoog, eronder is het zwart
        s32 dt = t - b3;
        off = dt * dt / 3 + dt * 2;
        if (off > 160)
            off = 160;
        TI_Show(sTI->v[1], FALSE);
        TI_WorldMove(0, off);
        sTI->bg0y = off;
        TI_Pos(sTI->v[0], 150, 70 - off);
        sTI->win0v = WIN_RANGE(0, 160 - off);
        if (TI_AT(b3))
            PlaySE(SE_M_STRENGTH);
    }
    gPlttBufferFaded[0] = RGB_BLACK;
    return t >= end;
}

static const struct TIntro sCI_Fish = {CIFish_Init, CIFish_Update};

// ---------------- Bird Keeper: een verenstorm van rechts, steeds dichter, op de 3e tel alles wit
#define BD_N 14
static void CIBird_Init(void)
{
    u32 i;
    for (i = 0; i < BD_N; i++)
    {
        sTI->v[i] = TI_Anim(ANIM_TAG_WHITE_FEATHER, i < 6 ? &gOamData_AffineNormal_ObjNormal_32x32 : &gOamData_AffineOff_ObjNormal_32x32, -50, -50, (i & 1) * 16);
        TI_Show(sTI->v[i], FALSE);
    }
    PlaySE(SE_M_GUST);
}

static bool32 CIBird_Update(s32 t)
{
    s32 end = TI_Beat(4), i;
    for (i = 0; i < BD_N; i++)
    {
        s32 t0 = i * TI_Beat(2) / BD_N, dt = t - t0;
        if (dt < 0)
            continue;
        if (dt == 0 || TI_AT(t0))
        {
            struct TIPart *p = TI_Part(sTI->v[i], 260, TI_RandRange(10, 150), -TI_RandRange(70, 110), TI_RandRange(-8, 8), 0, 0);
            if (p)
                p->ax = -1;
        }
        TI_Scale(sTI->v[i], 256, 256, (t * (5 + i)) << 7);
        gSprites[sTI->v[i]].y2 = Sin((t * 9 + i * 40) & 0xFF, 6);
    }
    if (TI_AT(TI_Beat(2)))
        PlaySE(SE_M_WING_ATTACK);
    TI_Tint(TI_World(), TI_Ramp(t, TI_Beat(1), end) * 14 >> 8, RGB(31, 31, 30));
    TI_WorldMove(-(TI_Ramp(t, 0, end) * 10 >> 8) + Sin((t * 20) & 0xFF, 2), 0);
    return t >= end;
}

static const struct TIntro sCI_Bird = {CIBird_Init, CIBird_Update};

// ---------------- Kindler: vlammen komen van onderen, de lucht trilt van de hitte
#define KD_N 8
static const u16 sCI_FirePal[4] = {0, RGB(29, 9, 2), RGB(31, 27, 8), RGB(31, 18, 4)};

static void CIKindler_Init(void)
{
    u32 i;
    TI_SetPal(15, sCI_FirePal, 4);
    sTI->v[20] = TI_MakeFillTiles(1, 2);
    for (i = 0; i < KD_N; i++)
        sTI->v[i] = TI_Anim(ANIM_TAG_FIRE, &gOamData_AffineOff_ObjNormal_32x32, 16 + i * 30, 200, 0);
    TI_Lines(TIF_WX);
    PlaySE(SE_M_FLAME_WHEEL);
}

static bool32 CIKindler_Update(s32 t)
{
    s32 end = TI_Beat(4), i, y, rise = TI_Ramp(t, 0, end), lvl;
    s16 top[31];
    u16 base = sTI->camX;
    for (i = 0; i < KD_N; i++)
    {
        s32 fy = 190 - (rise * (120 + (i % 3) * 20) >> 8) + Sin((t * 6 + i * 50) & 0xFF, 4);
        TI_Pos(sTI->v[i], 16 + i * 30 + Sin((t * 3 + i * 30) & 0xFF, 3), fy);
        gSprites[sTI->v[i]].oam.tileNum = GetSpriteTileStartByTag(ANIM_TAG_FIRE) + (((t >> 2) + i) & 7) * 16;
    }
    // hitte: onderste beeldlijnen trillen het hardst
    for (y = 0; y < DISPLAY_HEIGHT; y++)
        sTI->back[TIB_WX][y] = base + Sin((y * 10 + t * 12) & 0xFF, (y * (1 + (rise >> 6))) >> 7);
    lvl = 200 - (TI_Ramp(t, TI_Beat(2), end) * 220 >> 8);
    for (i = 0; i < 31; i++)
        top[i] = lvl + Sin((i * 40 + t * 11) & 0xFF, 6) + ((i * 7 + t) & 7);
    TI_DrawColumns(top, sTI->v[20], 15, FALSE);
    TI_Tint(TI_World(), rise * 8 >> 8, RGB(31, 12, 2));
    if (TI_AT(TI_Beat(2)))
        PlaySE(SE_M_SACRED_FIRE);
    return t >= end + 2;
}

static const struct TIntro sCI_Kindler = {CIKindler_Init, CIKindler_Update};

// ---------------- Guitarist: op elke tel een versterker-dreun (het beeld springt), podiumlicht wisselt, noten vliegen
#define GT_N 8
static const u16 sCI_StageCols[4] = {RGB(31, 4, 22), RGB(4, 24, 31), RGB(31, 26, 4), RGB(10, 31, 8)};

static void CIGuitar_Init(void)
{
    u32 i;
    for (i = 0; i < GT_N; i++)
    {
        sTI->v[i] = TI_Anim(ANIM_TAG_MUSIC_NOTES, &gOamData_AffineOff_ObjNormal_16x16, -20, -20, (i % 6) * 4);
        TI_Show(sTI->v[i], FALSE);
    }
}

static bool32 CIGuitar_Update(s32 t)
{
    s32 end = TI_Beat(5), n, since = 99, k;
    for (n = 0; n <= 4; n++)
    {
        s32 at = TI_Beat(n);
        if (t >= at)
            since = t - at;
        if (TI_AT(at))
        {
            u32 i;
            PlaySE(n == 4 ? SE_M_HYPER_BEAM : SE_M_BELLY_DRUM);
            for (i = 0; i < 2; i++)
                TI_Part(sTI->v[(n * 2 + i) % GT_N], i ? 230 : 10, 150, i ? -TI_RandRange(20, 40) : TI_RandRange(20, 40), -TI_RandRange(40, 60), 2, 40);
            sTI->v[12] = n;
        }
    }
    k = since < 10 ? (10 - since) : 0;
    TI_WorldMove((since < 10 ? Sin((since * 80) & 0xFF, k) : 0), since < 4 ? -k / 2 : 0);
    TI_Tint(TI_World(), t >= TI_Beat(0) ? 4 + (since < 6 ? 6 - since : 0) : 0, sCI_StageCols[sTI->v[12] & 3]);
    TI_Flash(t, TI_Beat(4), 10, 16, PALETTES_ALL, RGB_WHITE);
    return t >= end;
}

static const struct TIntro sCI_Guitar = {CIGuitar_Init, CIGuitar_Update};

// ---------------- Ruin Maniac: een zandwand vol hiërogliefen schuift van rechts over het beeld (rafelige rand)
static const u16 sCI_SandPal[4] = {0, RGB(27, 22, 13), RGB(19, 13, 6), RGB(30, 27, 18)};

static void CIRuin_Init(void)
{
    u32 g, n, j, x, y, r = 0xC0FFEE;
    u32 sand = TI_NewTile();
    TI_SetPal(15, sCI_SandPal, 4);
    TI_SolidTile(sand, 1);
    // 6 tegels met een "glief" (willekeurige streepjes binnen een kader)
    for (g = 0; g < 6; g++)
    {
        n = TI_NewTile();
        TI_SolidTile(n, 1);
        for (j = 0; j < 5; j++)
        {
            r = r * 1103515245 + 12345;
            x = 1 + ((r >> 16) % 6);
            y = 1 + ((r >> 20) % 6);
            if ((r >> 24) & 1)
            {
                u32 l = 1 + ((r >> 26) & 3);
                for (; l && x < 7; l--, x++)
                    TI_TilePixel(n, x, y, 2);
            }
            else
            {
                u32 l = 1 + ((r >> 26) & 3);
                for (; l && y < 7; l--, y++)
                    TI_TilePixel(n, x, y, 2);
            }
        }
        TI_TilePixel(n, 0, 0, 3);
    }
    for (y = 0; y < 21; y++)
        for (x = 0; x < 32; x++)
            TI_Put(x, y, (((x + y * 3) % 5 == 0 || (x * 7 + y) % 9 == 0) ? sand + 1 + ((x * 3 + y * 5) % 6) : sand) | (15 << 12));
    TI_Lines(TIF_WIN0);
    TI_Windows(DISPCNT_WIN0_ON, WININ_WIN0_ALL, TI_NO_BG0 | WINOUT_WIN01_CLR);
    PlaySE(SE_M_SAND_ATTACK);
}

static bool32 CIRuin_Update(s32 t)
{
    s32 end = TI_Beat(4), y, edge = 240 - (TI_Ramp(t, 0, end) * 260 >> 8);
    for (y = 0; y < DISPLAY_HEIGHT; y++)
    {
        s32 e = edge + Sin((y * 5 + t * 3) & 0xFF, 6) + ((y * 37 + t * 5) % 7);
        e = max(0, min(240, e));
        sTI->back[TIB_WIN0][y] = WIN_RANGE(e, 240);
    }
    sTI->bg0x = (-edge) & 0x1FF;   // de wand schuift mee naar links
    TI_Tint(TI_World(), TI_Ramp(t, 0, end) * 6 >> 8, RGB(27, 20, 10));
    if (TI_AT(TI_Beat(2)))
        PlaySE(SE_M_SAND_ATTACK);
    return t >= end + 2;
}

static const struct TIntro sCI_Ruin = {CIRuin_Init, CIRuin_Update};

// ---------------- Hex Maniac: alles donker, alleen een kaars; die flakkert op de tel en gaat uit. Twee ogen.
static const u16 sCI_EyePal[4] = {0, RGB(31, 31, 31), RGB(26, 6, 30), 0};

static void CIHex_Init(void)
{
    TI_SetPal(15, sCI_EyePal, 4);
    sTI->v[0] = TI_Anim(ANIM_TAG_WISP_FIRE, &gOamData_AffineOff_ObjNormal_32x32, 120, 96, 0);
    TI_Lines(TIF_WIN0);
    // binnen de cirkel: alles; erbuiten: alles behalve BG0, en donkerder (blend 'darken')
    TI_Windows(DISPCNT_WIN0_ON, WININ_WIN0_BG1 | WININ_WIN0_BG2 | WININ_WIN0_BG3 | WININ_WIN0_OBJ, TI_NO_BG0 | WINOUT_WIN01_CLR);
    sTI->bldcnt = BLDCNT_TGT1_BG1 | BLDCNT_TGT1_BG2 | BLDCNT_TGT1_BG3 | BLDCNT_TGT1_OBJ | BLDCNT_EFFECT_DARKEN;
    PlaySE(SE_M_NIGHTMARE);
}

static bool32 CIHex_Update(s32 t)
{
    s32 b3 = TI_Beat(3), end = TI_Beat(5), r, y, cx = 120, cy = 88, flick;
    flick = (t / 3) % 5;
    r = 46 + flick * 2 + ((t >> 1) & 1);
    if (t >= TI_Beat(1) && t < TI_Beat(1) + 4)
        r -= 14;
    if (t >= TI_Beat(2) && t < TI_Beat(2) + 4)
        r -= 20;
    if (t >= b3)
        r = max(0, 30 - (t - b3) * 6);
    for (y = 0; y < DISPLAY_HEIGHT; y++)
    {
        s32 dy = y - cy, h;
        if (r <= 0 || dy * dy >= r * r)
            sTI->back[TIB_WIN0][y] = 0;
        else
        {
            h = Sqrt(r * r - dy * dy);
            sTI->back[TIB_WIN0][y] = WIN_RANGE(max(0, cx - h), min(240, cx + h));
        }
    }
    sTI->bldy = min(16, TI_Ramp(t, 0, 12) * 14 >> 8);
    gSprites[sTI->v[0]].oam.tileNum = GetSpriteTileStartByTag(ANIM_TAG_WISP_FIRE) + ((t >> 3) & 3) * 16;
    TI_Show(sTI->v[0], t < b3 + 2);
    TI_Tint(TI_World(), 4, RGB(10, 2, 14));
    if (TI_AT(b3))
        PlaySE(SE_M_HAZE);
    if (TI_AT(TI_Beat(4)))
    {
        // twee ogen in het donker
        TI_Rect(104, 70, 112, 74, 2);
        TI_Rect(128, 70, 136, 74, 2);
        TI_Rect(106, 71, 110, 73, 1);
        TI_Rect(130, 71, 134, 73, 1);
        sTI->winout |= WINOUT_WIN01_BG0;
        sTI->bldcnt &= ~BLDCNT_TGT1_BG0;
        PlaySE(SE_M_FAINT_ATTACK);
    }
    if (t >= TI_Beat(4) + 10 && t < TI_Beat(4) + 14)
        sTI->winout &= ~WINOUT_WIN01_BG0; // knipperen
    if (t >= TI_Beat(4) + 14)
        sTI->winout |= WINOUT_WIN01_BG0;
    return t >= end;
}

static const struct TIntro sCI_Hex = {CIHex_Init, CIHex_Update};

// ---------------- Black Belt/Battle Girl: een hand komt neer, witte snee, de bovenkant schuift naar links, de onderkant
// naar rechts
static void CIChop_Init(void)
{
    TI_SetPal(15, sCI_CrackPal, 4);
    sTI->v[0] = TI_Anim(ANIM_TAG_HANDS_AND_FEET, &gOamData_AffineDouble_ObjNormal_32x32, 260, -40, 3 * 16);
    TI_Scale(sTI->v[0], 128, 128, 0);
    TI_Lines(TIF_WX);
}

static bool32 CIChop_Update(s32 t)
{
    s32 b1 = TI_Beat(1), b2 = TI_Beat(2), end = TI_Beat(4), y, split, r;
    u16 base = sTI->camX;
    if (t < b1)
    {
        r = TI_Ramp(t, b1 - 14, b1);
        TI_Pos(sTI->v[0], 260 - (r * 160 >> 8), -40 + (r * 120 >> 8));
        TI_Scale(sTI->v[0], 128, 128, (-r * 40) & 0xFFFF);
    }
    if (TI_AT(b1))
    {
        PlaySE(SE_M_MEGA_KICK);
        TI_Rect(0, 77, 240, 83, 1);           // de spleet: zwart met witte randen
        TI_Line(0, 76, 240, 76, 0, 256, 0, 3);
        TI_Line(0, 83, 240, 83, 0, 256, 0, 3);
    }
    split = t < b1 ? 0 : (TI_Ramp(t, b1 + 2, end) * 90 >> 8) + (t >= b1 ? 3 : 0);
    if (t >= b1)
    {
        TI_Pos(sTI->v[0], 100 - split, 80);
        TI_Show(sTI->v[0], t < b1 + 6);
    }
    for (y = 0; y < DISPLAY_HEIGHT; y++)
        sTI->back[TIB_WX][y] = base + (y < 80 ? split : -split);
    sTI->bg0x = 0;
    if (TI_AT(b2))
        PlaySE(SE_M_VITAL_THROW);
    TI_Flash(t, b1, 6, 14, TI_World(), RGB_WHITE);
    if (t >= b1)
        TI_Tint(TI_World(), TI_Ramp(t, b2, end) * 8 >> 8, RGB(31, 31, 31));
    return t >= end;
}

static const struct TIntro sCI_Chop = {CIChop_Init, CIChop_Update};

// ---------------- Cooltrainer: het wordt koud. Rijp kruipt vanaf de randen naar binnen (vignet), ijskristallen
static const u16 sCI_FrostPal[4] = {0, RGB(25, 29, 31), RGB(31, 31, 31), RGB(18, 24, 31)};
#define CL_N 8

static void CICool_Init(void)
{
    u32 n, x, y, i, r = 0xF00D;
    TI_SetPal(15, sCI_FrostPal, 4);
    for (i = 0; i < 4; i++)
    {
        n = TI_NewTile();
        TI_SolidTile(n, 1);
        for (y = 0; y < 8; y++)
            for (x = 0; x < 8; x++)
            {
                r = r * 1103515245 + 12345;
                if (((r >> 16) & 7) == 0)
                    TI_TilePixel(n, x, y, 2);
                else if (((r >> 16) & 7) == 1)
                    TI_TilePixel(n, x, y, 3);
            }
    }
    for (y = 0; y < 21; y++)
        for (x = 0; x < 32; x++)
            TI_Put(x, y, (1 + ((x * 5 + y * 3) & 3)) | (15 << 12));
    for (i = 0; i < CL_N; i++)
    {
        sTI->v[i] = TI_Anim(ANIM_TAG_ICE_CRYSTALS, &gOamData_AffineOff_ObjNormal_8x8, -20, -20, 0);
        TI_Show(sTI->v[i], FALSE);
    }
    TI_Lines(TIF_WIN0);
    // binnen de cirkel de wereld, erbuiten de rijp (BG0) half doorzichtig over de wereld
    TI_Windows(DISPCNT_WIN0_ON, WININ_WIN0_BG1 | WININ_WIN0_BG2 | WININ_WIN0_BG3 | WININ_WIN0_OBJ, WINOUT_WIN01_ALL);
    TI_Blend(BLDCNT_TGT1_BG0 | BLDCNT_EFFECT_BLEND | BLDCNT_TGT2_BG1 | BLDCNT_TGT2_BG2 | BLDCNT_TGT2_BG3 | BLDCNT_TGT2_OBJ, 12, 6);
    PlaySE(SE_M_ICY_WIND);
}

static bool32 CICool_Update(s32 t)
{
    s32 end = TI_Beat(4), r, y, i;
    r = 150 - (TI_Ramp(t, 0, TI_Beat(3)) * 150 >> 8);
    for (y = 0; y < DISPLAY_HEIGHT; y++)
    {
        s32 dy = (y - 80) * 3 / 2, h, rr = r + Sin((y * 13 + t * 2) & 0xFF, 4);
        if (rr <= 0 || dy * dy >= rr * rr)
            sTI->back[TIB_WIN0][y] = 0;
        else
        {
            h = Sqrt(rr * rr - dy * dy);
            sTI->back[TIB_WIN0][y] = WIN_RANGE(max(0, 120 - h), min(240, 120 + h));
        }
    }
    for (i = 0; i < CL_N; i++)
        if (TI_AT(i * 7 + 2) || TI_AT(TI_Beat(2) + i * 3))
            TI_Part(sTI->v[i], TI_RandRange(10, 230), TI_RandRange(10, 150), 0, 0, 0, 20);
    TI_Tint(TI_World(), TI_Ramp(t, 0, end) * 8 >> 8, RGB(20, 27, 31));
    if (TI_AT(TI_Beat(3)))
        PlaySE(SE_M_BLIZZARD);
    TI_Flash(t, TI_Beat(3), 8, 12, PALETTES_ALL, RGB_WHITE);
    return t >= end;
}

static const struct TIntro sCI_Cool = {CICool_Init, CICool_Update};

// ---------------- Triathlete: drie banen (zwemmen golft, fietsen raast, lopen stuitert), dan een finishvlag
static const u16 sCI_FlagPal[4] = {0, RGB(31, 31, 31), RGB(2, 2, 2), RGB(31, 31, 31)};

static void CITri_Init(void)
{
    u32 a, b, x, y;
    TI_SetPal(15, sCI_FlagPal, 4);
    a = TI_NewTile();
    b = TI_NewTile();
    for (y = 0; y < 8; y++)
        for (x = 0; x < 8; x++)
        {
            TI_TilePixel(a, x, y, ((x >> 2) ^ (y >> 2)) & 1 ? 2 : 1);
            TI_TilePixel(b, x, y, (y == 0 || y == 7) ? 1 : 0);
        }
    sTI->v[0] = a;
    sTI->v[1] = b;
    // scheidingslijnen tussen de banen (rij 6/7 en 13/14)
    for (x = 0; x < 32; x++)
    {
        TI_Put(x, 6, b | (15 << 12));
        TI_Put(x, 13, b | (15 << 12));
    }
    TI_Lines(TIF_WX | TIF_WY);
    PlaySE(SE_M_SURF);
}

static bool32 CITri_Update(s32 t)
{
    s32 end = TI_Beat(5), y, fx;
    u16 bx = sTI->camX, by = sTI->camY;
    for (y = 0; y < DISPLAY_HEIGHT; y++)
    {
        s32 dx = 0, dy = 0;
        if (y < 52 && t >= TI_Beat(0))
            dx = Sin((y * 12 + t * 8) & 0xFF, 4);
        else if (y >= 52 && y < 108 && t >= TI_Beat(1))
            dx = (t - TI_Beat(1)) * 9;
        else if (y >= 108 && t >= TI_Beat(2))
            dy = -abs(Sin(((t - TI_Beat(2)) * 12) & 0xFF, 6)), dx = (t - TI_Beat(2)) * 3;
        sTI->back[TIB_WX][y] = bx + dx;
        sTI->back[TIB_WY][y] = by + dy;
    }
    if (TI_AT(TI_Beat(1)))
        PlaySE(SE_M_SWIFT);
    if (TI_AT(TI_Beat(2)))
        PlaySE(SE_M_DOUBLE_SLAP);
    // finishvlag: twee kolommen dambord die van rechts naar links schuiven
    if (t >= TI_Beat(3))
    {
        s32 col = 31 - (TI_Ramp(t, TI_Beat(3), end - 6) * 33 >> 8);
        for (fx = 0; fx < 32; fx++)
            for (y = 0; y < 20; y++)
                if (y != 6 && y != 13)
                    TI_Put(fx, y, (fx == col || fx == col + 1) ? (sTI->v[0] | (15 << 12)) : 0);
        if (TI_AT(TI_Beat(3)))
            PlaySE(SE_M_STAT_INCREASE);
    }
    TI_Flash(t, end - 6, 6, 14, PALETTES_ALL, RGB_WHITE);
    return t >= end;
}

static const struct TIntro sCI_Tri = {CITri_Init, CITri_Update};

// ---------------- Expert: inktwas (alles wordt grijs), een penseelstreek, een rood zegel met een klap
static const u16 sCI_InkPal[4] = {0, RGB(2, 2, 3), RGB(27, 3, 3), RGB(31, 29, 24)};

static void CIExpert_Init(void)
{
    TI_SetPal(15, sCI_InkPal, 4);
    PlaySE(SE_M_SKETCH);
}

static bool32 CIExpert_Update(s32 t)
{
    s32 b1 = TI_Beat(1), b2 = TI_Beat(2), b3 = TI_Beat(3), end = TI_Beat(4) + 4, r;
    TI_Gray(TI_World(), TI_Ramp(t, 0, b2) * 16 >> 8);
    if (t >= TI_Beat(0) && t <= b2)
    {
        // penseelstreek in stukjes: van linksboven naar rechtsonder, dikker in het midden
        r = TI_Ramp(t, TI_Beat(0), b2);
        if (r > sTI->v[0])
        {
            s32 i;
            for (i = sTI->v[0]; i <= r; i += 4)
            {
                s32 x = 20 + (200 * i >> 8), y = 30 + (90 * i >> 8) + Sin((i >> 1) & 0xFF, 10);
                s32 w = 2 + Sin((i >> 1) & 0xFF, 5);
                TI_Stamp(x, y, w, 1);
            }
            sTI->v[0] = r;
        }
    }
    if (TI_AT(b1))
        PlaySE(SE_M_SKETCH);
    if (TI_AT(b3))
    {
        // het zegel (rood vierkant met een licht teken)
        TI_Rect(184, 108, 212, 136, 2);
        TI_Rect(190, 114, 206, 116, 3);
        TI_Rect(197, 114, 199, 132, 3);
        TI_Rect(190, 123, 206, 125, 3);
        TI_Rect(190, 130, 206, 132, 3);
        PlaySE(SE_M_COMET_PUNCH);
        sTI->v[1] = 6;
    }
    if (sTI->v[1] > 0)
        sTI->v[1]--;
    TI_Shake(sTI->v[1]);
    return t >= end;
}

static const struct TIntro sCI_Expert = {CIExpert_Init, CIExpert_Update};

// ---------------- Sailor: het schip schommelt (scheefgetrokken beeld), zeeziek groen, dan een golf over het dek
static void CISailor_Init(void)
{
    TI_SetPal(15, sCI_WaterPal, 4);
    sTI->v[0] = TI_MakeFillTiles(1, 2);
    TI_Lines(TIF_WX | TIF_WY);
    PlaySE(SE_M_SURF);
}

static bool32 CISailor_Update(s32 t)
{
    s32 end = TI_Beat(5), y, tilt, bob, amp, c;
    u16 bx = sTI->camX, by = sTI->camY;
    s16 top[31];
    amp = 4 + (TI_Ramp(t, 0, TI_Beat(3)) * 20 >> 8);
    tilt = Sin((t * 256 / max(1, TI_Beat(2) - TI_Beat(0))) & 0xFF, amp);   // een schommeling per twee tellen
    bob = Sin((t * 512 / max(1, TI_Beat(2) - TI_Beat(0))) & 0xFF, 3);
    for (y = 0; y < DISPLAY_HEIGHT; y++)
    {
        sTI->back[TIB_WX][y] = bx + ((y - 80) * tilt >> 6);
        sTI->back[TIB_WY][y] = by + bob;
    }
    TI_Tint(TI_World(), TI_Ramp(t, 0, end) * 7 >> 8, RGB(12, 24, 6));
    if (t >= TI_Beat(3))
    {
        s32 lvl = 170 - (TI_Ramp(t, TI_Beat(3), end) * 200 >> 8);
        for (c = 0; c < 31; c++)
            top[c] = lvl + Sin((c * 30 + t * 9) & 0xFF, 7) + ((c * tilt) >> 4);
        TI_DrawColumns(top, sTI->v[0], 15, FALSE);
        if (TI_AT(TI_Beat(3)))
            PlaySE(SE_M_WATERFALL);
    }
    return t >= end;
}

static const struct TIntro sCI_Sailor = {CISailor_Init, CISailor_Update};

// ---------------- Picknicker/Camper: het geruite picknickkleed valt van boven, bessen stuiteren erop
static const u16 sCI_GinghamPal[4] = {0, RGB(29, 6, 6), RGB(31, 31, 31), RGB(31, 20, 20)};
static const u16 sCI_Berries[] = {ITEM_ORAN_BERRY, ITEM_CHERI_BERRY, ITEM_PECHA_BERRY, ITEM_SITRUS_BERRY, ITEM_LEPPA_BERRY};

static void CIPicnic_Init(void)
{
    u32 a, x, y, i;
    TI_SetPal(15, sCI_GinghamPal, 4);
    a = TI_NewTile();
    for (y = 0; y < 8; y++)
        for (x = 0; x < 8; x++)
        {
            u32 rx = (x >> 2) & 1, ry = (y >> 2) & 1;
            TI_TilePixel(a, x, y, rx && ry ? 1 : (rx || ry) ? 3 : 2);
        }
    TI_FillMap(a | (15 << 12));   // hele tilemap: het kleed schuift mee naar beneden
    for (i = 0; i < ARRAY_COUNT(sCI_Berries); i++)
    {
        sTI->v[i] = TI_Item(TI_TAG_ITEM + i, sCI_Berries[i], -30, -30);
        TI_Show(sTI->v[i], FALSE);
    }
    TI_Windows(DISPCNT_WIN0_ON, WININ_WIN0_ALL, TI_NO_BG0 | WINOUT_WIN01_CLR);
    sTI->win0h = WIN_RANGE(0, 240);
    sTI->win0v = WIN_RANGE(0, 1);
    sTI->bg0y = 0;
}

static bool32 CIPicnic_Update(s32 t)
{
    s32 end = TI_Beat(5), b1 = TI_Beat(2), h, i;
    // het kleed valt (met een klein veertje), op tel 2 ligt het
    h = TI_Ramp(t, 0, b1) * 168 >> 8;
    if (t >= b1 && t < b1 + 6)
        h -= Sin(((t - b1) * 40) & 0xFF, 6);
    sTI->win0v = WIN_RANGE(0, max(1, min(160, h)));
    sTI->bg0y = -h;
    if (TI_AT(b1))
        PlaySE(SE_M_TAIL_WHIP);
    for (i = 0; i < (s32)ARRAY_COUNT(sCI_Berries); i++)
    {
        s32 at = TI_Beat2(5 + i);
        if (TI_AT(at))
        {
            struct TIPart *p = TI_Part(sTI->v[i], 40 + i * 40, -16, TI_RandRange(-8, 8), 20, 3, 0);
            if (p)
                p->bounce = TRUE;
            PlaySE(SE_BALL_BOUNCE_1);
        }
    }
    return t >= end;
}

static const struct TIntro sCI_Picnic = {CIPicnic_Init, CIPicnic_Update};

// ---------------- Youngster/School Kid: het beeld stuitert als een trampoline (in- en uitrekken), en knapt
static void CIBounce_Init(void)
{
    TI_Lines(TIF_WY);
    TI_Windows(DISPCNT_WIN0_ON, WININ_WIN0_ALL, 0);
    sTI->win0h = WIN_RANGE(0, 240);
}

static bool32 CIBounce_Update(s32 t)
{
    s32 end = TI_Beat(4) + 4, y, n, sc = 256, top = 0, ph;
    u16 by = sTI->camY;
    // drie boings: per tel inveren (kleiner) en uitrekken
    for (n = 0; n < 3; n++)
    {
        s32 a = TI_Beat(n), b = TI_Beat(n + 1);
        if (t >= a && t < b)
        {
            ph = (t - a) * 128 / max(1, b - a);   // halve sinus
            sc = 256 - Sin(ph & 0xFF, 70 + n * 30) ;
            if (TI_AT(a))
                PlaySE(SE_M_MINIMIZE);
        }
    }
    if (t >= TI_Beat(3))
        sc = 256 + (TI_Ramp(t, TI_Beat(3), end) * 1000 >> 8);
    if (sc < 40)
        sc = 40;
    // beeldlijn y toont kaartlijn ankerY + (y - ankerY) * 256 / sc (anker = onderkant: het beeld veert op de grond)
    for (y = 0; y < DISPLAY_HEIGHT; y++)
    {
        s32 src = 159 + (y - 159) * 256 / sc;
        sTI->back[TIB_WY][y] = by + src - y;
    }
    top = 160 - (160 * sc >> 8);
    if (top < 0)
        top = 0;
    sTI->win0v = WIN_RANGE(top, 160);
    gPlttBufferFaded[0] = RGB(20, 26, 31);
    if (TI_AT(TI_Beat(3)))
        PlaySE(SE_BANG);
    TI_Flash(t, TI_Beat(3), 8, 16, PALETTES_ALL, RGB_WHITE);
    return t >= end;
}

static const struct TIntro sCI_Bounce = {CIBounce_Init, CIBounce_Update};

// ---------------- Pkmn Ranger: de Capture Styler trekt drie lussen om het midden, dan CAPTURED.
static const u16 sCI_StylerPal[4] = {0, RGB(31, 31, 18), RGB(31, 20, 2), RGB(31, 31, 31)};

static void CIRanger_Init(void)
{
    TI_SetPal(15, sCI_StylerPal, 4);
    sTI->v[0] = 0;
    PlaySE(SE_M_THUNDER_WAVE);
}

static bool32 CIRanger_Update(s32 t)
{
    s32 b3 = TI_Beat(3), end = TI_Beat(4) + 8, r, i;
    r = TI_Ramp(t, 0, b3) * 3;   // 0..768 = drie lussen
    for (i = sTI->v[0]; i <= r; i += 2)
    {
        s32 rad = 64 - (i >> 5), x = 120 + Cos(i & 0xFF, rad * 3 / 2), y = 80 + Sin(i & 0xFF, rad);
        TI_Stamp(x, y, 1, 2);
        TI_Plot(x, y, 1);
    }
    sTI->v[0] = r;
    if (TI_AT(TI_Beat(1)) || TI_AT(TI_Beat(2)))
        PlaySE(SE_M_THUNDER_WAVE);
    if (TI_AT(b3))
    {
        TI_TextBg(COMPOUND_STRING("CAPTURED."), 10, 9, 10, 2, -1, 0, 0, 3, 2, FONT_NORMAL, 15);
        PlaySE(SE_RG_BALL_CLICK);
    }
    TI_Tint(TI_World(), TI_Ramp(t, b3, end) * 10 >> 8, RGB(31, 31, 24));
    TI_Flash(t, b3, 8, 14, TI_World(), RGB_WHITE);
    return t >= end;
}

static const struct TIntro sCI_Ranger = {CIRanger_Init, CIRanger_Update};

// ---------------- Beauty & co: bloemblaadjes dwarrelen, roze zweem, een glimlicht schuift schuin over het beeld
#define PT_N 24

static void CIPetal_Init(void)
{
    u32 i;
    for (i = 0; i < PT_N; i++)
    {
        sTI->v[i] = TI_Anim(ANIM_TAG_PINK_PETAL, &gOamData_AffineOff_ObjNormal_8x8, -20, -20, i & 3);
        TI_Show(sTI->v[i], FALSE);
    }
    TI_Lines(TIF_WIN0);
    TI_Windows(DISPCNT_WIN0_ON, WININ_WIN0_ALL, WINOUT_WIN01_BG_ALL | WINOUT_WIN01_OBJ);
    sTI->bldcnt = BLDCNT_TGT1_BG1 | BLDCNT_TGT1_BG2 | BLDCNT_TGT1_BG3 | BLDCNT_TGT1_OBJ | BLDCNT_EFFECT_LIGHTEN;
    sTI->bldy = 9;
    PlaySE(SE_M_PETAL_DANCE);
}

static bool32 CIPetal_Update(s32 t)
{
    s32 end = TI_Beat(4) + 4, i, y, sx;
    for (i = 0; i < PT_N; i++)
    {
        if (TI_AT(i * 3))
        {
            struct TIPart *p = TI_Part(sTI->v[i], TI_RandRange(-40, 200), -8, TI_RandRange(14, 24), TI_RandRange(14, 22), 0, 0);
            (void)p;
        }
        gSprites[sTI->v[i]].x2 = Sin((t * 6 + i * 23) & 0xFF, 8);
    }
    // glimlicht: een schuine band van 24 px breed van links naar rechts
    sx = -80 + (TI_Ramp(t, TI_Beat(2), TI_Beat(3) + 6) * 400 >> 8);
    for (y = 0; y < DISPLAY_HEIGHT; y++)
    {
        s32 x0 = sx + (160 - y) / 2;
        if (t < TI_Beat(2) || x0 + 24 < 0 || x0 > 240)
            sTI->back[TIB_WIN0][y] = 0;
        else
            sTI->back[TIB_WIN0][y] = WIN_RANGE(max(0, x0), min(240, x0 + 24));
    }
    if (TI_AT(TI_Beat(2)))
        PlaySE(SE_SHINY);
    TI_Tint(TI_World(), TI_Ramp(t, 0, end) * 7 >> 8, RGB(31, 20, 26));
    return t >= end;
}

static const struct TIntro sCI_Petal = {CIPetal_Init, CIPetal_Update};

// ---------------- Ninja Boy: rookbom; als de rook optrekt is het beeld leeg (wit). Eén blaadje valt.
#define NJ_N 10

static void CINinja_Init(void)
{
    u32 i;
    for (i = 0; i < NJ_N; i++)
    {
        sTI->v[i] = TI_Anim(ANIM_TAG_GRAY_SMOKE, &gOamData_AffineDouble_ObjNormal_32x32, -40, -40, 0);
        TI_Show(sTI->v[i], FALSE);
    }
    sTI->v[15] = TI_Anim(ANIM_TAG_LEAF, &gOamData_AffineOff_ObjNormal_16x16, -20, -20, 0);
    TI_Show(sTI->v[15], FALSE);
}

static bool32 CINinja_Update(s32 t)
{
    s32 b1 = TI_Beat(1), b3 = TI_Beat(3), end = TI_Beat(5), i;
    if (TI_AT(b1))
    {
        PlaySE(SE_M_EXPLOSION);
        for (i = 0; i < NJ_N; i++)
        {
            s32 a = i * 256 / NJ_N;
            TI_Part(sTI->v[i], 120, 84, Cos(a, 40), Sin(a, 28), 0, 0);
        }
    }
    if (t >= b1)
        for (i = 0; i < NJ_N; i++)
        {
            s32 sc = 256 - min(128, (t - b1) * 6);   // 1x -> 2x (groter knipt de affine-box af)
            struct Sprite *sp = &gSprites[sTI->v[i]];
            TI_Scale(sTI->v[i], sc, sc, 0);
            sp->oam.tileNum = GetSpriteTileStartByTag(ANIM_TAG_GRAY_SMOKE) + min(4, (t - b1) / 6) * 16;
            if (t >= b3)
                sp->invisible = (t - b3) > i * 2;
        }
    TI_Tint(TI_World(), TI_Ramp(t, b1, b1 + 10) * 16 >> 8, RGB(30, 30, 30));
    if (t < b1)
        TI_Tint(TI_World(), 0, 0);
    if (TI_AT(b3))
    {
        TI_HideField();
        TI_Part(sTI->v[15], 100, -10, 6, 8, 0, 0);
        PlaySE(SE_M_GUST);
    }
    if (t > b3)
        gSprites[sTI->v[15]].x2 = Sin((t * 5) & 0xFF, 14);
    return t >= end;
}

static const struct TIntro sCI_Ninja = {CINinja_Init, CINinja_Update};

// ---------------- Breeder/Pokéfan: hartjes stijgen op, een Lucky Egg wiebelt op de tel en komt uit (flits)
#define HT_N 12

static void CIHeart_Init(void)
{
    u32 i;
    for (i = 0; i < HT_N; i++)
    {
        sTI->v[i] = TI_Anim(ANIM_TAG_RED_HEART, i < 2 ? &gOamData_AffineDouble_ObjNormal_16x16 : &gOamData_AffineOff_ObjNormal_16x16, -20, -20, 0);
        TI_Show(sTI->v[i], FALSE);
    }
    sTI->v[20] = TI_Item(TI_TAG_ITEM, ITEM_LUCKY_EGG, 120, 84);
    gSprites[sTI->v[20]].oam.affineMode = ST_OAM_AFFINE_DOUBLE;
    gSprites[sTI->v[20]].oam.matrixNum = AllocOamMatrix();
    CalcCenterToCornerVec(&gSprites[sTI->v[20]], SPRITE_SHAPE(32x32), SPRITE_SIZE(32x32), ST_OAM_AFFINE_DOUBLE);
    TI_Scale(sTI->v[20], 128, 128, 0);
    PlaySE(SE_M_CHARM);
}

static bool32 CIHeart_Update(s32 t)
{
    s32 end = TI_Beat(5), b4 = TI_Beat(4), i, n, rot = 0;
    for (i = 2; i < HT_N; i++)
        if (TI_AT(i * 5))
            TI_Part(sTI->v[i], TI_RandRange(10, 230), 170, 0, -TI_RandRange(20, 34), 0, 0);
    for (i = 2; i < HT_N; i++)
        gSprites[sTI->v[i]].x2 = Sin((t * 7 + i * 30) & 0xFF, 6);
    for (n = 1; n <= 3; n++)
    {
        s32 at = TI_Beat(n);
        if (t >= at && t < at + 12)
            rot = Sin(((t - at) * 42) & 0xFF, 12);
        if (TI_AT(at))
            PlaySE(SE_BALL_BOUNCE_1);
    }
    TI_Scale(sTI->v[20], 128, 128, (rot * 160) & 0xFFFF);
    if (TI_AT(b4))
    {
        PlaySE(SE_EGG_HATCH);
        TI_Show(sTI->v[20], FALSE);
        for (i = 0; i < 2; i++)
            TI_Part(sTI->v[i], 120, 84, i ? 24 : -24, -20, 0, 0);
    }
    if (t > b4)
    {
        s32 sc = max(128, 256 - (t - b4) * 16);
        TI_Scale(sTI->v[0], sc, sc, 0);
        TI_Scale(sTI->v[1], sc, sc, 0);
    }
    TI_Tint(TI_World(), TI_Ramp(t, 0, end) * 6 >> 8, RGB(31, 18, 24));
    TI_Flash(t, b4, 8, 16, PALETTES_ALL, RGB_WHITE);
    return t >= end;
}

static const struct TIntro sCI_Heart = {CIHeart_Init, CIHeart_Update};

// ---------------- Rich Boy/Gentleman: een muntenregen (Pay Day), die blijft liggen; goudzweem; kassa
#define CO_N 20

static void CICoins_Init(void)
{
    u32 i;
    for (i = 0; i < CO_N; i++)
    {
        sTI->v[i] = TI_Anim(ANIM_TAG_COIN, &gOamData_AffineOff_ObjNormal_16x16, -20, -20, 0);
        TI_Show(sTI->v[i], FALSE);
    }
    PlaySE(SE_M_PAY_DAY);
}

static bool32 CICoins_Update(s32 t)
{
    s32 end = TI_Beat(4) + 4, i;
    for (i = 0; i < CO_N; i++)
    {
        s32 at = i * TI_Beat(3) / CO_N;
        if (TI_AT(at))
        {
            struct TIPart *p = TI_Part(sTI->v[i], TI_RandRange(8, 232), -10 - TI_RandRange(0, 20), 0, TI_RandRange(0, 10), 3, 0);
            if (p)
                p->bounce = TRUE;
        }
        gSprites[sTI->v[i]].oam.tileNum = GetSpriteTileStartByTag(ANIM_TAG_COIN) + (((t >> 2) + i) & 3) * 4;
    }
    if (TI_AT(TI_Beat(1)) || TI_AT(TI_Beat(2)))
        PlaySE(SE_M_PAY_DAY);
    if (TI_AT(TI_Beat(3)))
        PlaySE(SE_SHOP);
    TI_Tint(TI_World(), TI_Ramp(t, 0, end) * 7 >> 8, RGB(31, 26, 4));
    TI_Flash(t, TI_Beat(3), 8, 12, PALETTES_ALL, RGB(31, 31, 20));
    return t >= end;
}

static const struct TIntro sCI_Coins = {CICoins_Init, CICoins_Update};

static const struct TIntro *const sClassIntros[CI_COUNT] =
{
    [CI_SWIM] = &sCI_Swim,
    [CI_HIKER] = &sCI_Hiker,
    [CI_BUG] = &sCI_Bug,
    [CI_PSYCHIC] = &sCI_Psychic,
    [CI_FISH] = &sCI_Fish,
    [CI_BIRD] = &sCI_Bird,
    [CI_KINDLER] = &sCI_Kindler,
    [CI_GUITAR] = &sCI_Guitar,
    [CI_RUIN] = &sCI_Ruin,
    [CI_HEX] = &sCI_Hex,
    [CI_CHOP] = &sCI_Chop,
    [CI_COOL] = &sCI_Cool,
    [CI_TRI] = &sCI_Tri,
    [CI_EXPERT] = &sCI_Expert,
    [CI_SAILOR] = &sCI_Sailor,
    [CI_PICNIC] = &sCI_Picnic,
    [CI_BOUNCE] = &sCI_Bounce,
    [CI_RANGER] = &sCI_Ranger,
    [CI_PETAL] = &sCI_Petal,
    [CI_NINJA] = &sCI_Ninja,
    [CI_HEART] = &sCI_Heart,
    [CI_COINS] = &sCI_Coins,
};

static void Task_ClassIntro(u8 taskId)
{
    u32 ci = ClassIntro_ForClass(GetTrainerClassFromId(TRAINER_BATTLE_PARAM.opponentA));
    if (ci == CI_NONE || sClassIntros[ci] == NULL)
        ci = CI_SWIM;
    TI_Run(taskId, sClassIntros[ci]);
}
