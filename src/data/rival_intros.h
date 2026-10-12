// Project Grounded: de rivaal-intro's (May/Brendan), goedgekeurd door Jordi. Ze escaleren per gevecht:
//   1 Route 103   de starters: op de route zelf valt Birch' tas in beeld, drie Poké Balls springen eruit; vechtspel-VS met
//                 een diagonale streep, de starter van de rivaal groot tegenover die van de speler; de Galarian Zigzagoon
//                 glijdt er vlak voor het gevecht bij (alleen als hij in het team zit)
//   2 Rustboro    Devon Corp. bij zonsondergang (de echte kaart), een Pokédex-pagina: "CAUGHT: jij N, rivaal N+1"
//   3 Route 110   de race: het beeld splitst in een blauwe (speler) en rode (rivaal) helft met snelheidslijnen, Birch'
//                 aantekening "WHO'S FURTHER?"
//   4 Route 119   de storm: regen en bliksem over de route zelf; de twee helften botsen op de tel
//   5 Lilycove    "talk of the town": de krant over de ace van de speler (hoogste level, bij gelijkspel de eerste),
//                 flitslampen en spotlight, naam en level groot; dan de grote mugshot met beide portretten en VS
//   6 Route 136   de finale in de sneeuw: weer de krant (de ace is nog steeds nieuws), dan overspoelt de kleur van de
//                 starter van de rivaal het beeld (gras/vuur/water), beide portretten groot, de ultieme VS
// Geen Pokémon-sprites, behalve de ace van de speler in de krant en de starters (+ Zigzagoon) op Route 103 (Jordi). De kaarten worden uit de ROM getekend (layout +
// tileset), de tas komt uit het starterscherm, de rest is code. Gebruikt de runner van class_intros.h; op de tel van
// MUS_VS_RIVAL (196 BPM, het tempo komt uit de BGM-speler).

// stappen (één regel per trainer in sRivalIntros hieronder; de post-game-ids staan op RIS_PACIFIDLOG en Task_RivalIntro
// kiest Frontier/Paradiso op FLAG_RIVAL_PG_PACIFIDLOG_DONE en de kaart)
enum
{
    RIS_ROUTE_103, RIS_RUSTBORO, RIS_ROUTE_110, RIS_ROUTE_119, RIS_LILYCOVE, RIS_ROUTE_136,
    RIS_PACIFIDLOG,   // gevecht 7 (post-game): de drijvende stad, weer de krant
    RIS_FRONTIER,     // gevecht 8 (post-game): de grootste versie
    RIS_PARADISO,     // dagelijkse rematch in het Paradiso Resort: "gepensioneerde kampioen"-krant in sepia
    RIS_COUNT
};

struct RivalIntroEntry
{
    u16 trainer;
    u8 stage;   // 0-5
    u8 elem;    // starter van de rivaal: 0 gras, 1 vuur, 2 water
};

// _MUDKIP = de speler koos Mudkip, de rivaal heeft Treecko (gras); _TREECKO -> Torchic (vuur); _TORCHIC -> Mudkip (water)
#define RI_ROW(stage, mud, tree, tor) {mud, stage, 0}, {tree, stage, 1}, {tor, stage, 2}
static const struct RivalIntroEntry sRivalIntros[] =
{
    RI_ROW(0, TRAINER_MAY_ROUTE_103_MUDKIP, TRAINER_MAY_ROUTE_103_TREECKO, TRAINER_MAY_ROUTE_103_TORCHIC),
    RI_ROW(0, TRAINER_BRENDAN_ROUTE_103_MUDKIP, TRAINER_BRENDAN_ROUTE_103_TREECKO, TRAINER_BRENDAN_ROUTE_103_TORCHIC),
    RI_ROW(1, TRAINER_MAY_RUSTBORO_MUDKIP, TRAINER_MAY_RUSTBORO_TREECKO, TRAINER_MAY_RUSTBORO_TORCHIC),
    RI_ROW(1, TRAINER_BRENDAN_RUSTBORO_MUDKIP, TRAINER_BRENDAN_RUSTBORO_TREECKO, TRAINER_BRENDAN_RUSTBORO_TORCHIC),
    RI_ROW(2, TRAINER_MAY_ROUTE_110_MUDKIP, TRAINER_MAY_ROUTE_110_TREECKO, TRAINER_MAY_ROUTE_110_TORCHIC),
    RI_ROW(2, TRAINER_BRENDAN_ROUTE_110_MUDKIP, TRAINER_BRENDAN_ROUTE_110_TREECKO, TRAINER_BRENDAN_ROUTE_110_TORCHIC),
    RI_ROW(3, TRAINER_MAY_ROUTE_119_MUDKIP, TRAINER_MAY_ROUTE_119_TREECKO, TRAINER_MAY_ROUTE_119_TORCHIC),
    RI_ROW(3, TRAINER_BRENDAN_ROUTE_119_MUDKIP, TRAINER_BRENDAN_ROUTE_119_TREECKO, TRAINER_BRENDAN_ROUTE_119_TORCHIC),
    RI_ROW(4, TRAINER_MAY_LILYCOVE_MUDKIP, TRAINER_MAY_LILYCOVE_TREECKO, TRAINER_MAY_LILYCOVE_TORCHIC),
    RI_ROW(4, TRAINER_BRENDAN_LILYCOVE_MUDKIP, TRAINER_BRENDAN_LILYCOVE_TREECKO, TRAINER_BRENDAN_LILYCOVE_TORCHIC),
    RI_ROW(5, TRAINER_MAY_ROUTE_136_MUDKIP, TRAINER_MAY_ROUTE_136_TREECKO, TRAINER_MAY_ROUTE_136_TORCHIC),
    RI_ROW(5, TRAINER_BRENDAN_ROUTE_136_MUDKIP, TRAINER_BRENDAN_ROUTE_136_TREECKO, TRAINER_BRENDAN_ROUTE_136_TORCHIC),
    // post-game (één id voor beide geslachten en beide gevechten): Pacifidlog tot FLAG_RIVAL_PG_PACIFIDLOG_DONE, daarna de
    // Frontier (en in het Paradiso Resort de dagelijkse rematch), zie Task_RivalIntro
    RI_ROW(RIS_PACIFIDLOG, TRAINER_RIVAL_POSTGAME_MUDKIP, TRAINER_RIVAL_POSTGAME_TREECKO, TRAINER_RIVAL_POSTGAME_TORCHIC),
};
#undef RI_ROW

static const struct RivalIntroEntry *RivalIntro_Find(u16 trainerId)
{
    u32 i;
    for (i = 0; i < ARRAY_COUNT(sRivalIntros); i++)
        if (sRivalIntros[i].trainer == trainerId)
            return &sRivalIntros[i];
    return NULL;
}

bool32 RivalIntro_IsRival(u16 trainerId)
{
    return RivalIntro_Find(trainerId) != NULL;
}

// ---------------------------------------------------------------------------------------------------------------------
// gedeelde hulpjes

#define RI_TAG_BALL   0x7A11   // +0..2
#define RI_TAG_NAME   0x7A14
#define RI_TAG_VS     0x7A15
#define RI_BAG_TILE   400      // de tas van Birch op BG0 vanaf tile 400 (256 tiles)

static const u16 sRI_ElemCol[3][2] = {{RGB(5, 22, 6), RGB(14, 30, 10)}, {RGB(28, 7, 2), RGB(31, 22, 6)}, {RGB(3, 10, 28), RGB(12, 24, 31)}};
static const u16 sRI_TextPal[4] = {0, RGB(31, 31, 31), RGB(4, 4, 8), 0};
static const u16 sRI_VsPal[4] = {0, RGB(31, 29, 6), RGB(20, 2, 2), 0};

extern const struct MapLayout *const gMapLayouts[];

static bool32 RI_IsPostgame(u16 trainerId)
{
    return trainerId == TRAINER_RIVAL_POSTGAME_MUDKIP || trainerId == TRAINER_RIVAL_POSTGAME_TREECKO
        || trainerId == TRAINER_RIVAL_POSTGAME_TORCHIC;
}

// trainerfoto van de rivaal; de post-game-rivaal deelt één id voor beide geslachten: altijd het andere geslacht dan de speler
static u8 RI_RivalPic(void)
{
    if (RI_IsPostgame(sTI->trainer))
        return gSaveBlock2Ptr->playerGender == MALE ? TRAINER_PIC_MAY : TRAINER_PIC_BRENDAN;
    return GetTrainerPicFromId(sTI->trainer);
}

static bool32 RI_RivalIsMay(void)
{
    return RI_RivalPic() == TRAINER_PIC_MAY || RI_RivalPic() == TRAINER_PIC_RS_MAY;
}

static void RI_Upper(u8 *s)
{
    for (; *s != EOS; s++)
        if (*s >= CHAR_a && *s <= CHAR_z)
            *s -= CHAR_a - CHAR_A;
}

static u16 *RI_BgScreen(u32 bg)
{
    u16 cnt = *(vu16 *)(REG_ADDR_BG0CNT + bg * 2);
    return (u16 *)(BG_VRAM + ((cnt >> 8) & 0x1F) * 0x800);
}

// een stuk van een echte kaart op BG1-3 tekenen (zoals field_camera.c DrawMetatile); tilesets laden als het een
// andere kaart is dan die waar we staan. De kaartsprites gaan weg.
static void RI_DrawScene(const struct MapLayout *layout, s32 mx0, s32 my0)
{
    const struct MapLayout *cur = gMapHeader.mapLayout;
    u16 cnt = REG_BG2CNT;
    u8 *chr = (u8 *)(BG_VRAM + ((cnt >> 2) & 3) * 0x4000);
    u16 *bg1 = RI_BgScreen(1), *bg2 = RI_BgScreen(2), *bg3 = RI_BgScreen(3);
    s32 r, c;

    if (cur == NULL || layout->primaryTileset != cur->primaryTileset)
    {
        const struct Tileset *ts = layout->primaryTileset;
        if (ts->isCompressed)
            DecompressDataWithHeaderVram(ts->tiles, chr);
        else
            CpuCopy16(ts->tiles, chr, NUM_TILES_IN_PRIMARY * 32);
        LoadPalette(ts->palettes, BG_PLTT_ID(0), NUM_PALS_IN_PRIMARY * PLTT_SIZE_4BPP);
    }
    if (cur == NULL || layout->secondaryTileset != cur->secondaryTileset)
    {
        const struct Tileset *ts = layout->secondaryTileset;
        if (ts->isCompressed)
            DecompressDataWithHeaderVram(ts->tiles, chr + NUM_TILES_IN_PRIMARY * 32);
        else
            CpuCopy16(ts->tiles, chr + NUM_TILES_IN_PRIMARY * 32, (NUM_TILES_TOTAL - NUM_TILES_IN_PRIMARY) * 32);
        LoadPalette(ts->palettes[NUM_PALS_IN_PRIMARY], BG_PLTT_ID(NUM_PALS_IN_PRIMARY), (NUM_PALS_TOTAL - NUM_PALS_IN_PRIMARY) * PLTT_SIZE_4BPP);
    }
    for (r = 0; r < 16; r++)
    {
        for (c = 0; c < 16; c++)
        {
            s32 mx = min(max(mx0 + c, 0), layout->width - 1), my = min(max(my0 + r, 0), layout->height - 1);
            u32 id = layout->map[my * layout->width + mx] & MAPGRID_METATILE_ID_MASK, layer, off = r * 64 + c * 2;
            const u16 *mt;
            u16 attr;
            if (id < NUM_METATILES_IN_PRIMARY)
            {
                mt = layout->primaryTileset->metatiles + id * NUM_TILES_PER_METATILE;
                attr = layout->primaryTileset->metatileAttributes[id];
            }
            else
            {
                id -= NUM_METATILES_IN_PRIMARY;
                mt = layout->secondaryTileset->metatiles + id * NUM_TILES_PER_METATILE;
                attr = layout->secondaryTileset->metatileAttributes[id];
            }
            layer = (attr & METATILE_ATTR_LAYER_MASK) >> METATILE_ATTR_LAYER_SHIFT;
            #define RI_PUT(buf, a, b, cc, d) do { buf[off] = (a); buf[off + 1] = (b); buf[off + 32] = (cc); buf[off + 33] = (d); } while (0)
            switch (layer)
            {
            case METATILE_LAYER_TYPE_SPLIT:
                RI_PUT(bg3, mt[0], mt[1], mt[2], mt[3]);
                RI_PUT(bg2, 0, 0, 0, 0);
                RI_PUT(bg1, mt[4], mt[5], mt[6], mt[7]);
                break;
            case METATILE_LAYER_TYPE_COVERED:
                RI_PUT(bg3, mt[0], mt[1], mt[2], mt[3]);
                RI_PUT(bg2, mt[4], mt[5], mt[6], mt[7]);
                RI_PUT(bg1, 0, 0, 0, 0);
                break;
            default:
                RI_PUT(bg3, 0, 0, 0, 0);
                RI_PUT(bg2, mt[0], mt[1], mt[2], mt[3]);
                RI_PUT(bg1, mt[4], mt[5], mt[6], mt[7]);
                break;
            }
            #undef RI_PUT
        }
    }
    TI_HideField();
    sTI->nfield = 0;
    sTI->camX = 0;
    sTI->camY = 0;
}

static u8 RI_PlayerPic(void)
{
    return PlayerGenderToFrontTrainerPicId(gSaveBlock2Ptr->playerGender);
}

// portretten: speler (gespiegeld, kijkt naar rechts) en rivaal; scale 256 = normaal
static void RI_MakePortraits(bool32 affine)
{
    sTI->v[20] = TI_Trainer(RI_PlayerPic(), -80, 100, affine);
    sTI->v[21] = TI_Trainer(RI_RivalPic(), 320, 100, affine);
    if (!affine)
        gSprites[sTI->v[20]].oam.matrixNum |= ST_OAM_HFLIP;
}

static void RI_PortraitScale(s32 sc)
{
    TI_Scale(sTI->v[20], -sc, sc, 0);
    TI_Scale(sTI->v[21], sc, sc, 0);
}

static const u16 *RI_ElemPal(void)
{
    return sRI_ElemCol[sTI->elem];
}

// de ace van de speler: hoogste level, bij gelijkspel de eerste in het team
static struct Pokemon *RI_Ace(void)
{
    u32 i, best = 0, lvl, bestLvl = 0;
    for (i = 0; i < PARTY_SIZE; i++)
    {
        u16 sp = GetMonData(&gPlayerParty[i], MON_DATA_SPECIES);
        if (sp == SPECIES_NONE || GetMonData(&gPlayerParty[i], MON_DATA_IS_EGG))
            continue;
        lvl = GetMonData(&gPlayerParty[i], MON_DATA_LEVEL);
        if (lvl > bestLvl)
        {
            bestLvl = lvl;
            best = i;
        }
    }
    return &gPlayerParty[best];
}

// ---------------------------------------------------------------------------------------------------------------------
// de krant ("talk of the town"): BG0 papier, kop, de foto van de ace (echte frontsprite, shiny-palet als hij shiny is),
// flitslampen, spotlight; naam en level groot als tekst-sprite. Van 'from' (het papier slaat neer) tot 'to' (vliegt weg).
static const u16 sRI_PaperPal[6] = {0, RGB(30, 30, 27), RGB(3, 3, 4), RGB(19, 19, 18), RGB(25, 25, 22), RGB(26, 4, 4)};
#define RI_NEWS_SPR   v[8]
#define RI_NEWS_NAME  v[9]
#define RI_NEWS_FLASH v[10]  // eerste van 3 flitslamp-sprites (v[10..12])

static void RI_NewsInit(const u8 *masthead, const u8 *line1, const u8 *line2, const u8 *small)
{
    struct Pokemon *ace = RI_Ace();
    u16 species = GetMonData(ace, MON_DATA_SPECIES);
    u8 name[POKEMON_NAME_LENGTH + 12], buf[64];
    u32 paper, rule, x, y, i;
    s32 w;
    u16 id;

    TI_SetPal(14, sRI_PaperPal, 6);
    paper = TI_NewTile();
    rule = TI_NewTile();
    TI_SolidTile(paper, 1);
    TI_SolidTile(rule, 1);
    for (x = 0; x < 8; x++)
    {
        TI_TilePixel(rule, x, 3, 2);
        TI_TilePixel(rule, x, 5, 3);
    }
    for (y = 1; y < 19; y++)
        for (x = 1; x < 29; x++)
            TI_Put(x, y, paper | (14 << 12));
    for (x = 2; x < 28; x++)
        TI_Put(x, 4, rule | (14 << 12));
    TI_TextBg(masthead, 2, 2, 26, 2, -1, 0, 1, 2, 3, FONT_NORMAL, 14);
    StringCopy(buf, line1);
    StringAppend(buf, GetSpeciesName(species));
    RI_Upper(buf);
    TI_TextBg(buf, 2, 5, 26, 2, -1, 0, 1, 5, 4, FONT_NORMAL, 14);
    TI_TextBg(line2, 2, 7, 26, 2, -1, 0, 1, 5, 4, FONT_NORMAL, 14);
    TI_TextBg(small, 12, 17, 16, 2, 0, 0, 1, 3, 4, FONT_SMALL, 14);
    sTI->bg0y = -160;   // papier begint onder het scherm

    // de foto (paletteTag = species, zie CLAUDE.md)
    id = CreateMonPicSprite(species, GetMonData(ace, MON_DATA_IS_SHINY), GetMonData(ace, MON_DATA_PERSONALITY), TRUE, 64, 300, 0, species);
    if (id < MAX_SPRITES)
    {
        sTI->monSpr = id;
        TI_Track(id, TIK_MON);
    }
    sTI->RI_NEWS_SPR = id;

    // naam + level als tekst-sprite (64x32, groot geschaald)
    GetMonData(ace, MON_DATA_NICKNAME, name);
    StringGet_Nickname(name);
    RI_Upper(name);
    StringCopy(buf, name);
    StringAppend(buf, COMPOUND_STRING("\nLV. "));
    ConvertIntToDecimalStringN(name, GetMonData(ace, MON_DATA_LEVEL), STR_CONV_MODE_LEFT_ALIGN, 3);
    StringAppend(buf, name);
    sTI->RI_NEWS_NAME = TI_TextSprite(buf, 8, 4, 0, RI_TAG_NAME, sRI_TextPal, &gOamData_AffineDouble_ObjNormal_64x32, 170, 300);
    w = GetStringWidth(FONT_NORMAL, buf, 0);
    sTI->v[13] = max(128, min(256, (w + 4) * 256 / 120));   // schaal: past in 120 px breed, hoogstens 2x
    for (i = 0; i < 3; i++)
    {
        sTI->v[10 + i] = TI_Anim(ANIM_TAG_SPARKLE_2, &gOamData_AffineDouble_ObjNormal_32x32, -40, -40, 0);
        TI_Show(sTI->v[10 + i], FALSE);
    }
}

// TRUE zolang de krant in beeld is
static void RI_NewsUpdate(s32 t, s32 from, s32 to)
{
    s32 y, k;
    u32 i;
    u8 photo = sTI->RI_NEWS_SPR, name = sTI->RI_NEWS_NAME;
    if (t < from)
        return;
    if (t < to)
    {
        // slaat neer in 6 frames, met een klein veertje
        k = TI_Ramp(t, from, from + 6);
        y = -160 + (k * 160 >> 8);
        if (t >= from + 6 && t < from + 10)
            y = -Sin(((t - from - 6) * 64) & 0xFF, 3);
        if (TI_AT(from))
            PlaySE(SE_M_DOUBLE_SLAP);
    }
    else
    {
        k = TI_Ramp(t, to, to + 8);
        y = k * 170 >> 8;   // weg naar boven
    }
    sTI->bg0y = -y;
    TI_Pos(photo, 64, 116 + y);
    TI_Pos(name, 166, 104 + y);
    TI_Scale(name, sTI->v[13], sTI->v[13], 0);
    // flitslampen: drie op de tellen, plus een korte witte flits
    for (i = 0; i < 6; i++)
    {
        s32 at = from + 10 + (s32)i * (TI_Beat(1) - TI_Beat(0)) / 2;
        u8 s = sTI->v[10 + (i % 3)];
        if (TI_AT(at) && at < to)
        {
            TI_Pos(s, TI_RandRange(24, 216), TI_RandRange(20, 140));
            TI_Show(s, TRUE);
            PlaySE(SE_M_DETECT);
        }
        if (TI_AT(at + 6))
            TI_Show(s, FALSE);
        if (t >= at && t < at + 3)
            TI_TintMore(PALETTES_ALL, 10 - (t - at) * 3, RGB_WHITE);
        if (t >= at && t < at + 6)
            TI_Scale(s, 256 - (t - at) * 20, 256 - (t - at) * 20, (t * 2000) & 0xFFFF);
    }
    // spotlight op de foto: daarbuiten wordt het beeld wat donkerder
    for (y = 0; y < DISPLAY_HEIGHT; y++)
    {
        s32 dy = y - (116 - sTI->bg0y), r = 40 + Sin((t * 5) & 0xFF, 2), h;
        if (t >= to || dy * dy >= r * r)
            sTI->back[TIB_WIN0][y] = 0;
        else
        {
            h = Sqrt(r * r - dy * dy);
            sTI->back[TIB_WIN0][y] = WIN_RANGE(max(0, 64 - h), 64 + h);
        }
    }
    sTI->bldy = t >= from + 8 && t < to ? 4 : 0;
}

static void RI_NewsHide(void)
{
    u32 i;
    TI_Show(sTI->RI_NEWS_SPR, FALSE);
    TI_Show(sTI->RI_NEWS_NAME, FALSE);
    for (i = 0; i < 3; i++)
        TI_Show(sTI->v[10 + i], FALSE);
}

// vensters voor de krant: binnen de spotlight alles, erbuiten donkerder (BG0-3, niet de sprites)
static void RI_NewsWindows(void)
{
    TI_Lines(TIF_WIN0);
    TI_Windows(DISPCNT_WIN0_ON, WININ_WIN0_BG_ALL | WININ_WIN0_OBJ, WINOUT_WIN01_ALL);
    sTI->bldcnt = BLDCNT_TGT1_BG0 | BLDCNT_TGT1_BG1 | BLDCNT_TGT1_BG2 | BLDCNT_TGT1_BG3 | BLDCNT_EFFECT_DARKEN;
}

// ---------------------------------------------------------------------------------------------------------------------
// 1 Route 103: de starters. Geen sprong naar Littleroot meer (Jordi: te abrupt), alles gebeurt op de route zelf: Birch'
// tas valt in beeld, drie Poké Balls springen eruit. Eén vliegt naar de kant van de rivaal (rechtsboven), één naar de
// kant van de speler (linksonder), de derde kijkt rond en kruipt terug in de tas. Twee panelen in de kleur van de
// starters schuiven diagonaal over het beeld (vechtspel-VS met een witte streep), de ballen gaan open: de starter van de
// rivaal groot, die van de speler gespiegeld ertegenover. VS. Heeft de speler de Galarian Zigzagoon uit Littleroot bij
// zich, dan glijdt die er vlak voor het gevecht nog bij ("FEAT."), anders niet.
static void RI_VsSprite(void);
static const u16 sRV_StarterSpecies[3] = {SPECIES_TREECKO, SPECIES_TORCHIC, SPECIES_MUDKIP};   // per element
#define RV_SPLIT      25   // eindstand van de streep: tiles met kolom + rij = 25 (45 graden, door het midden van het beeld)
#define RV_BAG_ROW    5    // de tas staat op BG0 vanaf rij 5 (zichtbare rijen 6-14)
#define RV_BAG_COPY   16   // tijdens de panelen staat een kopie van de tas 16 rijen lager (22-30, onzichtbaar)
#define RV_RIVAL_X    184
#define RV_RIVAL_Y    54
#define RV_PLAYER_X   70
#define RV_PLAYER_Y   100
#define RV_ZIG_X      38
#define RV_ZIG_Y      124
#define RV_BAG_X      120
#define RV_BAG_Y      70
// v[]: 0-2 ballen, 3 starter rivaal, 4 starter speler, 5 Zigzagoon, 6 "FEAT.", 7 tas gekopieerd, 19 schudden, 22 VS
#define RV_TAG_FEAT   0x7A16

// een frontsprite (affine, dubbele grootte); wordt aan het eind door TI_Free opgeruimd
static u8 RV_MonPic(u16 species, bool32 shiny, u32 personality, s16 x, s16 y)
{
    u16 id = CreateMonPicSprite(species, shiny, personality, TRUE, x, y, 0, species);
    struct Sprite *s;
    if (id >= MAX_SPRITES)
        return MAX_SPRITES;
    if (sTI->nmons >= ARRAY_COUNT(sTI->mons))
    {
        FreeAndDestroyMonPicSprite(id);
        return MAX_SPRITES;
    }
    sTI->mons[sTI->nmons++] = id;
    s = &gSprites[id];
    s->invisible = TRUE;
    s->oam.matrixNum = AllocOamMatrix();
    if (s->oam.matrixNum == 0xFF)
    {
        s->oam.matrixNum = 0;
    }
    else
    {
        s->oam.affineMode = ST_OAM_AFFINE_DOUBLE;
        s->affineAnimPaused = TRUE;
        CalcCenterToCornerVec(s, SPRITE_SHAPE(64x64), SPRITE_SIZE(64x64), ST_OAM_AFFINE_DOUBLE);
        SetOamMatrixRotationScaling(s->oam.matrixNum, 256, 256, 0);
    }
    return TI_Track(id, TIK_MON);
}

// de eerste Pokémon van die soort in het team (shiny/persoonlijkheid), of NULL
static struct Pokemon *RV_FindInParty(u16 species)
{
    u32 i;
    for (i = 0; i < PARTY_SIZE; i++)
        if (GetMonData(&gPlayerParty[i], MON_DATA_SPECIES) == species && !GetMonData(&gPlayerParty[i], MON_DATA_IS_EGG))
            return &gPlayerParty[i];
    return NULL;
}

static u8 RV_PartyMonPic(u16 species, s16 x, s16 y)
{
    struct Pokemon *mon = RV_FindInParty(species);
    if (mon == NULL)
        return RV_MonPic(species, FALSE, 0, x, y);
    return RV_MonPic(species, GetMonData(mon, MON_DATA_IS_SHINY), GetMonData(mon, MON_DATA_PERSONALITY), x, y);
}

// de panelen (45 graden): links de speler tot c + r = sL, rechts de rivaal vanaf c + r = sR + 1, met een witte streep
// ertussen. Tiles: 0 speler, 1 rivaal, 2 wit, 3 speler|wit, 4 wit|rivaal, 5 wit|leeg (rand speler), 6 leeg|wit (rand
// rivaal). De strepen in de kleurvlakken lopen (fase ph). Elke tile krijgt meteen zijn eindwaarde (geen wissen eerst).
enum { RVT_P, RVT_R, RVT_W, RVT_PW, RVT_WR, RVT_W0, RVT_0W, RVT_COUNT };
static const u8 sRV_EdgeLo[RVT_COUNT] = {8, 0, 0, 4, 0, 0, 0};    // x + y < lo: linkerdeel
static const u8 sRV_EdgeHi[RVT_COUNT] = {16, 0, 16, 16, 8, 8, 4}; // x + y < hi: middendeel, daarna rechterdeel
static const u8 sRV_EdgeKind[RVT_COUNT][3] = {{1, 1, 1}, {2, 2, 2}, {3, 3, 3}, {1, 3, 3}, {3, 3, 2}, {3, 3, 0}, {0, 0, 3}};

static void RV_PanelTiles(u32 ph)
{
    u32 n, x, y;
    for (n = 0; n < RVT_COUNT; n++)
    {
        u32 tile = sTI->v[16] + n;
        for (y = 0; y < 8; y++)
            for (x = 0; x < 8; x++)
            {
                u32 sum = x + y, kind = sRV_EdgeKind[n][sum < sRV_EdgeLo[n] ? 0 : (sum < sRV_EdgeHi[n] ? 1 : 2)], c = 0;
                if (kind == 1)
                    c = ((x + y + ph) & 7) < 2 ? 2 : 1;
                else if (kind == 2)
                    c = ((x + 8 - y + ph) & 7) < 2 ? 4 : 3;
                else if (kind == 3)
                    c = 5;
                TI_TilePixel(tile, x, y, c);
            }
    }
}

static void RV_PanelMap(s32 sL, s32 sR)
{
    s32 r, c, a = sTI->v[16];
    for (r = 0; r < 21; r++)
    {
        u16 *row = &sTI->bg0map[r * 32];
        bool32 bag = r >= RV_BAG_ROW + 1 && r <= RV_BAG_ROW + 9;
        for (c = 0; c < 31; c++)
        {
            s32 d = c + r, pl = -1, rv = -1, k;
            if (d < sL)
                pl = RVT_P;
            else if (d == sL)
                pl = RVT_PW;
            else if (d == sL + 1)
                pl = RVT_W0;
            if (d > sR + 1)
                rv = RVT_R;
            else if (d == sR + 1)
                rv = RVT_WR;
            else if (d == sR)
                rv = RVT_0W;
            if (pl >= 0 && rv >= 0)
                k = pl == RVT_W0 && rv == RVT_0W ? RVT_W : (pl == RVT_PW ? RVT_PW : rv);
            else
                k = pl >= 0 ? pl : rv;
            if (k >= 0)
                row[c] = (a + k) | (15 << 12);
            else
                row[c] = bag ? sTI->bg0map[(r + RV_BAG_COPY) * 32 + c] : 0;
        }
    }
}

static void RI1_Init(void)
{
    u8 *buf;
    u16 *map;
    u32 i, r, c;
    u32 rivalElem = sTI->elem, playerElem = sTI->elem == 0 ? 2 : sTI->elem - 1;
    u16 cols[6];
    struct Pokemon *zig = RV_FindInParty(SPECIES_ZIGZAGOON_GALAR);

    // de tas (starterscherm): tiles naar BG0 vanaf RI_BAG_TILE, palet 13/14; hij begint boven het scherm (bg0y)
    buf = Alloc(0x2000);
    map = Alloc(0x800);
    if (buf != NULL && map != NULL)
    {
        DecompressDataWithHeaderWram(gBirchBagGrass_Gfx, buf);
        CpuCopy16(buf, &sTI->bg0tiles[RI_BAG_TILE * 16], 256 * 32);
        DecompressDataWithHeaderWram(gBirchBagTilemap, map);
        for (r = 1; r < 10; r++)
            for (c = 0; c < 30; c++)
            {
                u16 e = map[r * 32 + c];
                if ((e & 0x3FF) == 0)
                    continue;
                TI_Put(c, r + RV_BAG_ROW, ((e & 0x3FF) + RI_BAG_TILE) | (e & 0x0C00) | (((e >> 12) + 13) << 12));
            }
        LoadPalette(gBirchBagGrass_Pal, BG_PLTT_ID(13), 2 * PLTT_SIZE_4BPP);
    }
    TRY_FREE_AND_SET_NULL(buf);
    TRY_FREE_AND_SET_NULL(map);
    sTI->bg0y = 120;
    REG_BG0VOFS = 120;   // meteen: BG0 staat al aan (tekstvakken) en de tilemap is al geschreven; anders staat de tas
                         // één beeld lang op zijn eindplek
    SetGpuReg(REG_OFFSET_BG0VOFS, 120);

    // panelen: 1/2 kleur van de speler, 3/4 van de rivaal, 5 wit
    cols[0] = 0;
    cols[1] = sRI_ElemCol[playerElem][0];
    cols[2] = sRI_ElemCol[playerElem][1];
    cols[3] = sRI_ElemCol[rivalElem][0];
    cols[4] = sRI_ElemCol[rivalElem][1];
    cols[5] = RGB_WHITE;
    TI_SetPal(15, cols, 6);
    sTI->v[16] = sTI->nextTile;
    for (i = 0; i < RVT_COUNT; i++)
        TI_NewTile();
    RV_PanelTiles(0);

    for (i = 0; i < 3; i++)
    {
        sTI->v[i] = TI_Item(RI_TAG_BALL + i, ITEM_POKE_BALL, RV_BAG_X, RV_BAG_Y);
        TI_Show(sTI->v[i], FALSE);
    }
    sTI->v[3] = RV_MonPic(sRV_StarterSpecies[rivalElem], FALSE, 0, RV_RIVAL_X, RV_RIVAL_Y);
    sTI->v[4] = RV_PartyMonPic(sRV_StarterSpecies[playerElem], RV_PLAYER_X, RV_PLAYER_Y);
    if (sTI->v[4] < MAX_SPRITES)
        gSprites[sTI->v[4]].subpriority = 2;
    sTI->v[5] = MAX_SPRITES;
    sTI->v[6] = MAX_SPRITES;
    if (zig != NULL)
    {
        u8 name[POKEMON_NAME_LENGTH + 12], nick[POKEMON_NAME_LENGTH + 1];
        sTI->v[5] = RV_MonPic(SPECIES_ZIGZAGOON_GALAR, GetMonData(zig, MON_DATA_IS_SHINY), GetMonData(zig, MON_DATA_PERSONALITY), -60, RV_ZIG_Y);
        if (sTI->v[5] < MAX_SPRITES)
            gSprites[sTI->v[5]].subpriority = 0;   // vóór de starter
        GetMonData(zig, MON_DATA_NICKNAME, nick);
        StringGet_Nickname(nick);
        RI_Upper(nick);
        StringCopy(name, COMPOUND_STRING("FEAT.\n"));
        StringAppend(name, nick);
        sTI->v[6] = TI_TextSprite(name, 8, 4, 0, RV_TAG_FEAT, sRI_TextPal, &gOamData_AffineDouble_ObjNormal_64x32, 104, 144);
        TI_Show(sTI->v[6], FALSE);
    }
    RI_VsSprite();
}

// pop uit de bal: van niets naar 2x (met een klein doorschot), eerst wit
static void RV_Emerge(s32 t, s32 at, u8 id, bool32 flip)
{
    s32 k, size;
    if (id >= MAX_SPRITES || t < at)
        return;
    if (TI_AT(at))
    {
        TI_Show(id, TRUE);
        PlaySE(SE_BALL_OPEN);
    }
    k = t - at;
    if (k < 6)
        size = 16 + k * 98;           // 1/16 -> 2,3x
    else if (k < 10)
        size = 604 - (k - 6) * 23;    // terug naar 2x
    else
        size = 512;
    TI_Scale(id, flip ? -(65536 / size) : 65536 / size, 65536 / size, 0);
    if (k < 8)
        TI_TintMore(TI_PalBit(id), 16 - k * 2, RGB_WHITE);
    gSprites[id].y2 = k >= 10 ? Sin(((t - at) * 6) & 0xFF, 2) : 0;
}

static bool32 RI1_Update(s32 t)
{
    s32 b = TI_Beat(1) - TI_Beat(0), land = TI_Beat(1), pop = TI_Beat2(3), panels = TI_Beat(2), meet = TI_Beat(3);
    s32 vs = TI_Beat(4), zig = TI_Beat(5), flash, end, i, k;
    bool32 hasZig = sTI->v[5] < MAX_SPRITES;
    static const s16 sBallTo[3][3] = {{RV_RIVAL_X, RV_RIVAL_Y + 8, 40}, {RV_PLAYER_X, RV_PLAYER_Y + 8, 28}, {RV_BAG_X, RV_BAG_Y, 22}};

    flash = hasZig ? TI_Beat(7) : TI_Beat(6);
    end = flash + 8;

    // de route wordt donkerder (de kaart blijft staan: geen sprong naar Littleroot)
    TI_Tint(TI_World(), TI_Ramp(t, 0, land) * 7 >> 8, RGB(2, 3, 9));

    // de tas valt (BG0) en landt op tel 1
    if (t < land)
    {
        k = TI_Ramp(t, 0, land);
        sTI->bg0y = 120 - ((k * k >> 8) * 120 >> 8);
    }
    else
    {
        if (TI_AT(land))
        {
            PlaySE(SE_M_STRENGTH);
            sTI->v[19] = 4;
        }
        if (sTI->v[19] > 0)
            sTI->v[19]--;
        TI_Shake(sTI->v[19]);
    }

    // drie ballen springen eruit: twee naar de zijkanten, de derde terug de tas in
    for (i = 0; i < 3; i++)
    {
        s32 at = pop + i * 2, dur = i == 2 ? b : 12;
        u8 s = sTI->v[i];
        if (t < at)
            continue;
        if (TI_AT(at))
        {
            TI_Show(s, TRUE);
            PlaySE(SE_BALL_BOUNCE_1);
        }
        k = TI_Ramp(t, at, at + dur);
        TI_Pos(s, RV_BAG_X + ((sBallTo[i][0] - RV_BAG_X) * k >> 8), RV_BAG_Y + ((sBallTo[i][1] - RV_BAG_Y) * k >> 8) - (sBallTo[i][2] * k * (256 - k) >> 14));
        if (i == 2)
        {
            // de overgebleven bal kijkt even rond (wiebelt) en kruipt terug
            gSprites[s].x2 = k > 64 && k < 200 ? ((t >> 2) & 1 ? 2 : -2) : 0;
            if (k >= 256)
                TI_Show(s, FALSE);
        }
    }

    // panelen schuiven van de hoeken naar de diagonaal en raken elkaar op tel 3
    if (t >= panels)
    {
        if (sTI->v[7] == 0)
        {
            sTI->v[7] = 1;
            for (i = RV_BAG_ROW + 1; i <= RV_BAG_ROW + 9; i++)   // CpuCopy16: VRAM niet per byte
                CpuCopy16(&sTI->bg0map[i * 32], &sTI->bg0map[(i + RV_BAG_COPY) * 32], 32 * 2);
            PlaySE(SE_M_DOUBLE_TEAM);
        }
        k = TI_Ramp(t, panels, meet);
        k = 256 - ((256 - k) * (256 - k) >> 8);   // ease-out
        RV_PanelMap(-2 + ((RV_SPLIT + 2) * k >> 8), 50 - ((50 - RV_SPLIT) * k >> 8));
        RV_PanelTiles(t >> 1);   // de strepen lopen
        if (TI_AT(meet))
        {
            PlaySE(SE_M_MEGA_KICK);
            sTI->v[19] = 5;
        }
    }

    // de ballen gaan open: eerst de starter van de rivaal, een halve tel later die van de speler (gespiegeld)
    if (TI_AT(meet))
        TI_Show(sTI->v[0], FALSE);
    if (TI_AT(meet + b / 2))
        TI_Show(sTI->v[1], FALSE);
    RV_Emerge(t, meet, sTI->v[3], FALSE);
    RV_Emerge(t, meet + b / 2, sTI->v[4], TRUE);

    // VS slaat in op de streep
    if (t >= vs)
    {
        s32 sc = 256 * 256 / max(256, 1600 - (t - vs) * 260);
        if (sc > 64)
            sc = 64;
        TI_Show(sTI->v[22], TRUE);
        TI_Pos(sTI->v[22], 124, 80);
        TI_Scale(sTI->v[22], sc, sc, t < vs + 6 ? (u16)((vs + 6 - t) * 3000) : 0);
        if (TI_AT(vs))
        {
            PlaySE(SE_M_MEGA_KICK);
            sTI->v[19] = 8;
        }
    }

    // vlak voor het gevecht: de Galarian Zigzagoon glijdt erbij
    if (hasZig && t >= zig)
    {
        u8 z = sTI->v[5];
        k = TI_Ramp(t, zig, zig + 8);
        k = 256 - ((256 - k) * (256 - k) >> 8);
        if (TI_AT(zig))
        {
            TI_Show(z, TRUE);
            PlaySE(SE_M_TAIL_WHIP);
        }
        TI_Scale(z, -176, 176, 0);   // 1,5x, kijkt naar rechts
        TI_Pos(z, -60 + ((RV_ZIG_X + 60) * k >> 8), RV_ZIG_Y);
        gSprites[z].x2 = t >= zig + 8 && t < zig + 12 ? (zig + 12 - t) : 0;   // remt af
        if (sTI->v[4] < MAX_SPRITES && t >= zig + 6 && t < zig + 12)
            gSprites[sTI->v[4]].y2 = -5;   // de starter schrikt
        if (t >= zig + 10 && sTI->v[6] < MAX_SPRITES)
        {
            s32 sc = min(256, 128 + (t - zig - 10) * 32);   // van 2x naar 1x
            TI_Show(sTI->v[6], TRUE);
            TI_Scale(sTI->v[6], sc, sc, 0);
            if (TI_AT(zig + 10))
                PlaySE(SE_PIN);
        }
    }

    TI_Flash(t, flash, 8, 14, PALETTES_ALL, RGB_WHITE);
    return t >= end;
}

static const struct TIntro sRI_103 = {RI1_Init, RI1_Update};

// ---------------------------------------------------------------------------------------------------------------------
// 2 Rustboro: Devon Corp. bij zonsondergang, een Pokédex-pagina (rivaal altijd eentje voor)
static const u16 sRI_DexPal[6] = {0, RGB(26, 4, 4), RGB(30, 29, 25), RGB(3, 3, 5), RGB(18, 17, 15), RGB(16, 2, 2)};

static void RI_DexPanel(const u8 *title, u32 count, u32 rivalCount, const u8 *footnote)
{
    u32 red, cream, x, y;
    u8 buf[48], num[8];
    TI_SetPal(15, sRI_DexPal, 6);
    red = TI_NewTile();
    cream = TI_NewTile();
    TI_SolidTile(red, 1);
    TI_SolidTile(cream, 2);
    for (y = 3; y < 17; y++)
        for (x = 4; x < 26; x++)
            TI_Put(x, y, ((y == 3 || y == 16 || x == 4 || x == 25) ? red : cream) | (15 << 12));
    TI_TextBg(title, 5, 4, 20, 2, -1, 0, 1, 2, 5, FONT_NORMAL, 15);
    StringCopy(buf, gSaveBlock2Ptr->playerName);
    StringAppend(buf, COMPOUND_STRING(": "));
    ConvertIntToDecimalStringN(num, count, STR_CONV_MODE_LEFT_ALIGN, 4);
    StringAppend(buf, num);
    TI_TextBg(buf, 5, 7, 20, 2, 8, 0, 2, 3, 4, FONT_NORMAL, 15);
    StringCopy(buf, GetTrainerNameFromId(sTI->trainer));
    StringAppend(buf, COMPOUND_STRING(": "));
    ConvertIntToDecimalStringN(num, rivalCount, STR_CONV_MODE_LEFT_ALIGN, 4);
    StringAppend(buf, num);
    TI_TextBg(buf, 5, 10, 20, 2, 8, 0, 2, 3, 4, FONT_NORMAL, 15);
    TI_TextBg(footnote, 5, 13, 20, 2, -1, 0, 2, 4, 3, FONT_SMALL, 15);
}

static void RI2_Init(void)
{
    u32 n = GetNationalPokedexCount(FLAG_GET_CAUGHT);
    RI_DrawScene(gMapLayouts[LAYOUT_RUSTBORO_CITY - 1], 4, 3);
    sTI->camX = 0;
    sTI->camY = 56;
    RI_DexPanel(COMPOUND_STRING("POKéDEX  CAUGHT"), n, n + 1, COMPOUND_STRING("(One of them is a Wurmple. Twice.)"));
    sTI->bg0y = -168;
    TI_Windows(DISPCNT_WIN0_ON, WININ_WIN0_ALL, TI_NO_BG0 | WINOUT_WIN01_CLR);   // BG0 alleen vanaf de bovenrand van de pagina
    sTI->win0h = WIN_RANGE(0, DISPLAY_WIDTH);
    sTI->win0v = WIN_RANGE(159, DISPLAY_HEIGHT);
    RI_MakePortraits(FALSE);
}

static bool32 RI2_Update(s32 t)
{
    s32 end = TI_Beat(10), k, b = TI_Beat(1) - TI_Beat(0);
    // de skyline: de camera kantelt omhoog langs de toren, zonsondergang
    k = TI_Ramp(t, 0, TI_Beat(3));
    sTI->camY = 56 - (k * 56 >> 8);
    TI_Tint(0x1FFF, 3 + (k * 4 >> 8), RGB(31, 13, 6));
    // de Pokédex-pagina schuift omhoog op tel 3
    if (t >= TI_Beat(3))
    {
        k = TI_Ramp(t, TI_Beat(3), TI_Beat(3) + 8);
        sTI->bg0y = -168 + (k * 168 >> 8);
        sTI->win0v = WIN_RANGE(min(159, max(0, 24 - sTI->bg0y)), DISPLAY_HEIGHT);
        if (TI_AT(TI_Beat(3)))
            PlaySE(SE_M_SWIFT);
    }
    if (TI_AT(TI_Beat(5)))
        PlaySE(SE_PIN);
    if (t >= TI_Beat(5) && t < TI_Beat(5) + 8)
        sTI->bg0x = Sin(((t - TI_Beat(5)) * 64) & 0xFF, 3);   // de pagina schudt even ("+1")
    else
        sTI->bg0x = 0;
    if (t >= TI_Beat(7))
    {
        k = TI_Ramp(t, TI_Beat(7), TI_Beat(7) + b);
        TI_Pos(sTI->v[20], -40 + (k * 84 >> 8), 120);
        TI_Pos(sTI->v[21], 280 - (k * 84 >> 8), 120);
        if (TI_AT(TI_Beat(7)))
            PlaySE(SE_M_SWAGGER);
    }
    TI_Flash(t, TI_Beat(9), 8, 14, PALETTES_ALL, RGB_WHITE);
    return t >= end;
}

static const struct TIntro sRI_Rustboro = {RI2_Init, RI2_Update};

// ---------------------------------------------------------------------------------------------------------------------
// 3 Route 110: de race. Twee helften (speler blauw, rivaal rood) met snelheidslijnen, Birch' notitie "WHO'S FURTHER?"
// palet 15: 1 blauw, 2 lichtblauw (lijnen), 3 rood, 4 lichtrood, 5 wit (scheiding)
static const u16 sRI_RacePal[6] = {0, RGB(3, 8, 24), RGB(16, 24, 31), RGB(24, 3, 4), RGB(31, 18, 16), RGB(31, 31, 31)};
#define RI_STREAKS 4

// snelheidslijnen: 4 tiles per kleur, horizontaal periodiek; elke frame een paar pixels verder
static void RI_StreakTiles(u32 base, u32 shift)
{
    u32 k, x, y, half;
    for (half = 0; half < 2; half++)
        for (k = 0; k < RI_STREAKS; k++)
        {
            u32 n = base + half * RI_STREAKS + k;
            for (y = 0; y < 8; y++)
                for (x = 0; x < 8; x++)
                {
                    u32 seed = (k * 8 + y) * 2654435761u, on = ((seed >> 13) & 3) == 0 && (((x + shift + (seed >> 7)) & 7) < 5);
                    TI_TilePixel(n, x, y, on ? 2 + half * 2 : 1 + half * 2);
                }
        }
}

static void RI_SplitHalves(u32 base, s32 leftCols, s32 rightCol)
{
    s32 r, c;
    for (r = 0; r < 21; r++)
        for (c = 0; c < 31; c++)
        {
            u16 e = 0;
            if (c < leftCols)
                e = base + ((r * 3 + c) & 3);
            else if (c >= rightCol)
                e = base + RI_STREAKS + ((r * 5 + c) & 3);
            if (c == leftCols - 1 || c == rightCol)
                e = base + 2 * RI_STREAKS;   // rand
            if (sTI->v[17] == 1 && r >= 1 && r <= 4 && c >= 3 && c < 27)
                continue;   // Birch' notitie ligt erover
            sTI->bg0map[r * 32 + c] = e ? (e | (15 << 12)) : 0;
        }
}

static void RI_RaceTiles(void)
{
    u32 base = sTI->nextTile, k, y;
    for (k = 0; k < RI_STREAKS * 2 + 1; k++)
        TI_NewTile();
    TI_SolidTile(base + 2 * RI_STREAKS, 5);
    for (y = 0; y < 8; y++)
    {
        TI_TilePixel(base + 2 * RI_STREAKS, 0, y, 0);
        TI_TilePixel(base + 2 * RI_STREAKS, 7, y, 0);
    }
    sTI->v[16] = base;
    RI_StreakTiles(base, 0);
    TI_SetPal(15, sRI_RacePal, 6);
}

static void RI3_Init(void)
{
    u32 n = GetNationalPokedexCount(FLAG_GET_SEEN);
    u8 buf[40], num[8];
    RI_RaceTiles();
    RI_SplitHalves(sTI->v[16], 0, 31);
    // Birch' notitie (rijen 22-25 van de tilemap, wordt op tel 5 naar boven gekopieerd)
    TI_TextBg(COMPOUND_STRING("PROF. BIRCH: WHO'S FURTHER?"), 0, 22, 24, 2, -1, 0, 5, 3, 4, FONT_NORMAL, 15);
    StringCopy(buf, gSaveBlock2Ptr->playerName);
    StringAppend(buf, COMPOUND_STRING(" SEEN "));
    ConvertIntToDecimalStringN(num, n, STR_CONV_MODE_LEFT_ALIGN, 4);
    StringAppend(buf, num);
    StringAppend(buf, COMPOUND_STRING(" / "));
    StringAppend(buf, GetTrainerNameFromId(sTI->trainer));
    StringAppend(buf, COMPOUND_STRING(" SEEN "));
    ConvertIntToDecimalStringN(num, n + 1, STR_CONV_MODE_LEFT_ALIGN, 4);
    StringAppend(buf, num);
    TI_TextBg(buf, 0, 24, 24, 2, -1, 0, 5, 1, 2, FONT_SMALL, 15);
    RI_MakePortraits(FALSE);
    TI_Blend(BLDCNT_TGT1_BG0 | BLDCNT_EFFECT_BLEND | BLDCNT_TGT2_BG1 | BLDCNT_TGT2_BG2 | BLDCNT_TGT2_BG3, 10, 8);
    TI_Windows(DISPCNT_WIN0_ON, WININ_WIN0_BG_ALL | WININ_WIN0_OBJ, WINOUT_WIN01_ALL);
    sTI->win0h = 0;
    sTI->win0v = 0;
    PlaySE(SE_M_SWIFT);
}

static bool32 RI3_Update(s32 t)
{
    s32 end = TI_Beat(10), k, cols, r, b = TI_Beat(1) - TI_Beat(0);
    // de helften schuiven van links/rechts naar het midden (in tiles), dan rennen
    k = TI_Ramp(t, 0, TI_Beat(1));
    cols = k * 15 >> 8;
    RI_SplitHalves(sTI->v[16], cols, 30 - cols);
    RI_StreakTiles(sTI->v[16], t * 3);
    // de wereld raast voorbij
    sTI->wx = t * t / 24;
    TI_Pos(sTI->v[20], -40 + (k * 100 >> 8), 112);
    TI_Pos(sTI->v[21], 280 - (k * 100 >> 8), 112);
    gSprites[sTI->v[20]].y2 = -abs(Sin((t * 16) & 0xFF, 4));
    gSprites[sTI->v[21]].y2 = -abs(Sin((t * 16 + 64) & 0xFF, 4));
    // wie loopt voor? Op de tellen springt telkens de ander een stukje naar voren
    gSprites[sTI->v[20]].x2 = (t / b) & 1 ? 8 : 0;
    gSprites[sTI->v[21]].x2 = (t / b) & 1 ? 0 : -8;
    // Birch' notitie valt op tel 5 van boven in beeld (ondoorzichtig: venster 0 zonder blend)
    if (t >= TI_Beat(5))
    {
        s32 h = TI_Ramp(t, TI_Beat(5), TI_Beat(5) + 6) * 32 >> 8;
        if (TI_AT(TI_Beat(5)))
            PlaySE(SE_PIN);
        if (sTI->v[17] != 1)
        {
            sTI->v[17] = 1;
            for (r = 0; r < 4; r++)   // CpuCopy16: een gewone lus wordt memcpy, en bytes schrijven in VRAM gaat mis
                CpuCopy16(&sTI->bg0map[(22 + r) * 32], &sTI->bg0map[(1 + r) * 32 + 3], 24 * 2);
        }
        sTI->win0h = WIN_RANGE(24, 216);
        sTI->win0v = WIN_RANGE(8, 8 + h);
    }
    TI_Flash(t, TI_Beat(9), 8, 14, PALETTES_ALL, RGB_WHITE);
    return t >= end;
}

static const struct TIntro sRI_110 = {RI3_Init, RI3_Update};

// ---------------------------------------------------------------------------------------------------------------------
// 4 Route 119: de storm. Regen en bliksem op de route zelf, de helften komen van de zijkanten en botsen op de tel
#define R4_RAIN 14

static void RI4_Init(void)
{
    u32 i;
    RI_RaceTiles();
    RI_SplitHalves(sTI->v[16], 0, 31);
    for (i = 0; i < R4_RAIN; i++)
        sTI->v[i] = TI_Anim(ANIM_TAG_RAIN_DROPS, &gOamData_AffineOff_ObjNormal_16x32, (i * 53) % 240, (i * 37) % 160, 0);
    sTI->v[14] = TI_Anim(ANIM_TAG_LIGHTNING, &gOamData_AffineOff_ObjNormal_32x32, -40, -40, 0);
    sTI->v[15] = TI_Anim(ANIM_TAG_LIGHTNING, &gOamData_AffineOff_ObjNormal_32x32, -40, -40, 16);
    sTI->v[18] = TI_Anim(ANIM_TAG_IMPACT, &gOamData_AffineDouble_ObjNormal_32x32, 120, 84, 0);
    TI_Show(sTI->v[18], FALSE);
    RI_MakePortraits(FALSE);
    TI_Blend(BLDCNT_TGT1_BG0 | BLDCNT_EFFECT_BLEND | BLDCNT_TGT2_BG1 | BLDCNT_TGT2_BG2 | BLDCNT_TGT2_BG3 | BLDCNT_TGT2_OBJ, 11, 7);
    PlaySE(SE_M_RAIN_DANCE);
}

static bool32 RI4_Update(s32 t)
{
    s32 end = TI_Beat(10), hit = TI_Beat(6), i, k, cols;
    // regen
    for (i = 0; i < R4_RAIN; i++)
    {
        struct Sprite *sp = &gSprites[sTI->v[i]];
        sp->x -= 3;
        sp->y += 9;
        if (sp->y > 176)
        {
            sp->y -= 192;
            sp->x = TI_RandRange(0, 280);
        }
    }
    TI_Tint(TI_World(), 8, RGB(3, 5, 10));
    // bliksem op tel 1 en 3
    for (i = 0; i < 2; i++)
    {
        s32 at = TI_Beat(1 + i * 2);
        if (TI_AT(at))
        {
            PlaySE(SE_THUNDER);
            TI_Pos(sTI->v[14], i ? 180 : 60, 20);
            TI_Pos(sTI->v[15], i ? 180 : 60, 52);
        }
        if (t >= at && t < at + 8)
            TI_TintMore(TI_World() | (0xE000), 14 - (t - at) * 2, RGB(30, 30, 31));
        if (t == at + 8)
        {
            TI_Pos(sTI->v[14], -40, -40);
            TI_Pos(sTI->v[15], -40, -40);
        }
    }
    // de helften schuiven naar elkaar toe en botsen op tel 6
    k = TI_Ramp(t, TI_Beat(4), hit);
    k = k * k >> 8;
    cols = t >= hit ? 15 : (k * 15 >> 8);
    RI_SplitHalves(sTI->v[16], cols, 30 - cols);
    RI_StreakTiles(sTI->v[16], t * 2);
    TI_Pos(sTI->v[20], -40 + (cols * 8 * 100 / 120), 112);
    TI_Pos(sTI->v[21], 280 - (cols * 8 * 100 / 120), 112);
    if (TI_AT(hit))
    {
        PlaySE(SE_M_MEGA_KICK);
        TI_Show(sTI->v[18], TRUE);
        sTI->v[19] = 10;
    }
    if (t >= hit)
    {
        s32 sc = max(128, 256 - (t - hit) * 40);
        TI_Scale(sTI->v[18], sc, sc, 0);
        TI_Show(sTI->v[18], t < hit + 10);
    }
    if (sTI->v[19] > 0)
        sTI->v[19]--;
    TI_Shake(sTI->v[19]);
    TI_Flash(t, hit, 10, 16, PALETTES_ALL, RGB_WHITE);
    return t >= end;
}

static const struct TIntro sRI_119 = {RI4_Init, RI4_Update};

// ---------------------------------------------------------------------------------------------------------------------
// 5/6: de grote mugshot (beide portretten groot) en VS
// BG0: diagonaal gesplitst, linksonder de kleur van de speler (blauw), rechtsboven die van de rivaal (stage 5: roze/blauw
// van de mugshot, stage 6: de kleur van zijn starter, met een golvende rand die het hele beeld overspoelt)
static const u16 sRI_MugPal[6] = {0, RGB(3, 7, 20), RGB(10, 16, 30), RGB(30, 12, 20), RGB(31, 22, 27), RGB(31, 31, 31)};

static void RI_VsTiles(void)
{
    u32 a = TI_NewTile(), b = TI_NewTile(), w = TI_NewTile(), x, y;
    for (y = 0; y < 8; y++)
        for (x = 0; x < 8; x++)
        {
            TI_TilePixel(a, x, y, ((x + y) & 7) < 2 ? 2 : 1);
            TI_TilePixel(b, x, y, ((x - y) & 7) < 2 ? 4 : 3);
        }
    TI_SolidTile(w, 5);
    sTI->v[16] = a;
}

// diagonaal: kolom c van rij r hoort bij de rivaal als c > split - r/2 (split in tiles, 0..45)
static void RI_VsMap(s32 split)
{
    s32 r, c, a = sTI->v[16];
    for (r = 0; r < 21; r++)
        for (c = 0; c < 31; c++)
        {
            s32 d = c - (split - r * 2 / 3);
            u16 e = d > 0 ? a + 1 : (d == 0 ? a + 2 : a);
            sTI->bg0map[r * 32 + c] = e | (15 << 12);
        }
}

static void RI_VsSprite(void)
{
    sTI->v[22] = TI_TextSprite(COMPOUND_STRING("VS"), 8, 4, 8, RI_TAG_VS, sRI_VsPal, &gOamData_AffineDouble_ObjNormal_64x32, 120, 80);
    TI_Show(sTI->v[22], FALSE);
}

// portretten groot binnenschuiven (vanaf 'at'), VS slaat in op 'vs'
static void RI_BigVersus(s32 t, s32 at, s32 vs, s32 big)
{
    s32 k = TI_Ramp(t, at, at + 8), sc;
    if (t < at)
        return;
    RI_PortraitScale(big);
    TI_Pos(sTI->v[20], -60 + (k * 130 >> 8), 104 + Sin((t * 4) & 0xFF, 2));
    TI_Pos(sTI->v[21], 300 - (k * 130 >> 8), 64 - Sin((t * 4) & 0xFF, 2));
    if (TI_AT(at))
        PlaySE(SE_M_SWAGGER);
    if (t >= vs)
    {
        sc = 256 * 256 / max(256, 1600 - (t - vs) * 260);   // groot -> 4x
        if (sc > 64)
            sc = 64;
        TI_Show(sTI->v[22], TRUE);
        TI_Scale(sTI->v[22], sc, sc, t < vs + 6 ? (u16)((vs + 6 - t) * 3000) : 0);
        if (TI_AT(vs))
        {
            PlaySE(SE_M_MEGA_KICK);
            sTI->v[19] = 8;
        }
    }
}

// ---------------- 5 Lilycove
static void RI5_Init(void)
{
    u8 head[32];
    StringCopy(head, COMPOUND_STRING("LOCAL "));
    TI_SetPal(15, sRI_MugPal, 6);
    if (!RI_RivalIsMay())
    {
        TI_SetCol(15, 3, RGB(2, 14, 30));
        TI_SetCol(15, 4, RGB(14, 24, 31));
        TI_SetCol(15, 1, RGB(22, 6, 4));
        TI_SetCol(15, 2, RGB(30, 16, 10));
    }
    RI_NewsInit(COMPOUND_STRING("THE LILYCOVE LOWDOWN"), head, COMPOUND_STRING("TAKES HOENN BY STORM"),
                COMPOUND_STRING("Experts: “It is fine.”"));
    RI_NewsWindows();
    RI_MakePortraits(TRUE);
    RI_VsSprite();
    sTI->v[23] = sTI->nextTile;  // daarna: VS-tiles
}

static bool32 RI5_Update(s32 t)
{
    s32 swap = TI_Beat(6), end = TI_Beat(13);
    RI_NewsUpdate(t, TI_Beat(0), swap);
    if (t >= swap + 8 && sTI->v[7] == 0)
    {
        // de krant is weg: BG0 wordt de mugshot
        RI_NewsHide();
        sTI->v[7] = 1;
        sTI->nextTile = sTI->reserved = sTI->v[23];
        RI_VsTiles();
        sTI->bg0y = 0;
        sTI->bldy = 0;
        TI_Windows(0, 0, 0);
        sTI->regs = FALSE;
        SetGpuReg(REG_OFFSET_BLDCNT, 0);
        sTI->lineFlags = 0;
    }
    if (sTI->v[7])
    {
        s32 split = 15 + Sin((t * 3) & 0xFF, 2) + 4;
        RI_VsMap(split);
        sTI->bg0x = (-(t * 3)) & 7;
    }
    RI_BigVersus(t, TI_Beat(7), TI_Beat(9), 170);
    if (sTI->v[19] > 0)
        sTI->v[19]--;
    if (t >= swap + 8)
        TI_Shake(sTI->v[19]);
    TI_Flash(t, TI_Beat(9), 10, 16, PALETTES_ALL, RGB_WHITE);
    TI_Flash(t, TI_Beat(11), 6, 8, TI_World(), RGB_WHITE);
    return t >= end;
}

static const struct TIntro sRI_Lilycove = {RI5_Init, RI5_Update};

// ---------------- 6+ de finales: Route 136 (sneeuw), Pacifidlog (zee) en de Frontier (de grootste; ook de dagelijkse
// rematch in het Paradiso Resort, met een "gepensioneerde kampioen"-krant). Eén functie met een parameterblok.
enum { RG_WEATHER_NONE, RG_WEATHER_SNOW, RG_WEATHER_SEA, RG_WEATHER_SPOT };
enum { RG_FLOOD_SIDE, RG_FLOOD_RISE };

struct RivalGrand
{
    const u8 *masthead, *line1, *line2, *small;
    u8 weather;
    u8 flood;
    u8 hits;       // klappen na de VS (op de tellen)
    u8 sepia;      // de krant in sepia (Paradiso)
    u16 tint;      // kleurzweem van de wereld tijdens de krant
    u8 vsBeat;     // tel waarop VS inslaat (de portretten komen 2 tellen eerder)
};

static const struct RivalGrand sRG_136 =
{
    COMPOUND_STRING("ASHFROST WEEKLY"), COMPOUND_STRING("STILL "), COMPOUND_STRING("SNOW: STILL COLD."),
    COMPOUND_STRING("Rival “not worried.”"), RG_WEATHER_SNOW, RG_FLOOD_SIDE, 3, FALSE, RGB(28, 30, 31), 12,
};

static const struct RivalGrand sRG_Pacifidlog =
{
    COMPOUND_STRING("THE PACIFIDLOG DRIFTER"), COMPOUND_STRING("LOCAL "), COMPOUND_STRING("STILL AFLOAT, SOMEHOW"),
    COMPOUND_STRING("Town: also still afloat."), RG_WEATHER_SEA, RG_FLOOD_RISE, 3, FALSE, RGB(8, 20, 31), 12,
};

static const struct RivalGrand sRG_Frontier =
{
    COMPOUND_STRING("FRONTIER: FINAL EDITION"), COMPOUND_STRING("HALL OF FAME "), COMPOUND_STRING("WANTS IT BACK. NO."),
    COMPOUND_STRING("Printed in actual gold."), RG_WEATHER_SPOT, RG_FLOOD_SIDE, 5, FALSE, RGB(31, 26, 8), 12,
};

static const struct RivalGrand sRG_Paradiso =
{
    COMPOUND_STRING("PARADISO RESORT GAZETTE"), COMPOUND_STRING("RETIRED CHAMP'S "), COMPOUND_STRING("WILL NOT RETIRE"),
    COMPOUND_STRING("Rival: here. Again. Daily."), RG_WEATHER_SPOT, RG_FLOOD_RISE, 4, TRUE, RGB(31, 24, 14), 12,
};

static EWRAM_DATA const struct RivalGrand *sRG = NULL;
#define RG_WEATHER_N 14

static void RG_Init(void)
{
    u32 i;
    u8 head[24];
    StringCopy(head, sRG->line1);
    RI_NewsInit(sRG->masthead, head, sRG->line2, sRG->small);
    if (sRG->sepia)
    {
        TI_SetCol(14, 1, RGB(29, 26, 19));
        TI_SetCol(14, 3, RGB(18, 14, 9));
        TI_SetCol(14, 4, RGB(24, 20, 14));
        TI_SetCol(14, 5, RGB(17, 9, 4));
    }
    RI_NewsWindows();
    RI_MakePortraits(TRUE);
    RI_VsSprite();
    for (i = 0; i < RG_WEATHER_N && sRG->weather != RG_WEATHER_NONE; i++)
    {
        if (sRG->weather == RG_WEATHER_SNOW)
            sTI->extra[i] = TI_Anim(ANIM_TAG_SNOWFLAKES, &gOamData_AffineOff_ObjNormal_16x32, (i * 71) % 256, (i * 29) % 160, 0);
        else if (sRG->weather == RG_WEATHER_SEA)
            sTI->extra[i] = TI_Anim(ANIM_TAG_SMALL_BUBBLES, &gOamData_AffineOff_ObjNormal_16x16, (i * 71) % 256, 160 + (i * 29) % 60, (i & 1) * 4);
        else
            sTI->extra[i] = TI_Anim(ANIM_TAG_SPARKLE_2, &gOamData_AffineOff_ObjNormal_32x32, (i * 71) % 256, (i * 29) % 160, (i % 4) * 16);
    }
    sTI->v[23] = sTI->nextTile;
    PlaySE(sRG->weather == RG_WEATHER_SEA ? SE_M_SURF : (sRG->weather == RG_WEATHER_SNOW ? SE_M_ICY_WIND : SE_M_HEAL_BELL));
}

static void RG_Weather(s32 t)
{
    s32 i;
    for (i = 0; i < RG_WEATHER_N && sRG->weather != RG_WEATHER_NONE; i++)
    {
        struct Sprite *sp = &gSprites[sTI->extra[i]];
        switch (sRG->weather)
        {
        case RG_WEATHER_SNOW:
            sp->x -= 4 + (i & 1);
            sp->y += 2 + (i % 3);
            sp->y2 = Sin((t * 6 + i * 20) & 0xFF, 3);
            break;
        case RG_WEATHER_SEA:
            sp->y -= 1 + (i % 3);
            sp->x2 = Sin((t * 5 + i * 30) & 0xFF, 4);
            break;
        default: // gouden glinsteringen die oplichten en weer weg gaan
            sp->invisible = ((t + i * 5) % 24) > 12;
            if (((t + i * 5) % 24) == 0)
            {
                sp->x = TI_RandRange(8, 232);
                sp->y = TI_RandRange(8, 152);
            }
            break;
        }
        if (sp->x < -16)
            sp->x += 272;
        if (sp->y > 176)
            sp->y -= 192;
        if (sp->y < -16)
            sp->y += 200;
    }
    if (sRG->weather == RG_WEATHER_SEA)
        TI_WorldMove(Sin((t * 3) & 0xFF, 2), Sin((t * 4) & 0xFF, 3));   // drijvende stad: de wereld deint
}

static bool32 RG_Update(s32 t)
{
    s32 swap = TI_Beat(6), flood = TI_Beat(7), full = TI_Beat(10), vs = TI_Beat(sRG->vsBeat), end, i, y;
    end = TI_Beat(sRG->vsBeat + 2 + sRG->hits);
    RG_Weather(t);
    if (t < swap + 8)
        TI_Tint(TI_World(), 6, sRG->tint);
    RI_NewsUpdate(t, TI_Beat(0), swap);
    if (t >= swap + 8 && sTI->v[7] == 0)
    {
        u32 n, x;
        const u16 *ec = RI_ElemPal();
        RI_NewsHide();
        sTI->v[7] = 1;
        sTI->nextTile = sTI->reserved = sTI->v[23];
        // de vloedgolf in de kleur van de starter van de rivaal (lichte strepen), per beeldlijn een venster
        TI_SetCol(15, 1, ec[0]);
        TI_SetCol(15, 2, ec[1]);
        TI_SetCol(15, 3, RGB(31, 31, 31));
        n = TI_NewTile();
        for (y = 0; y < 8; y++)
            for (x = 0; x < 8; x++)
                TI_TilePixel(n, x, y, ((x * 2 + y) & 7) == 0 ? 2 : 1);
        TI_FillMap(n | (15 << 12));
        sTI->bg0y = 0;
        sTI->bldy = 0;
        sTI->bldcnt = 0;
        sTI->winin = WININ_WIN0_ALL;
        sTI->winout = TI_NO_BG0;
        sTI->win0v = WIN_RANGE(0, DISPLAY_HEIGHT);
        for (y = 0; y < DISPLAY_HEIGHT; y++)
            sTI->back[TIB_WIN0][y] = 0;
        if (sRG->flood == RG_FLOOD_RISE)
        {
            sTI->lineFlags &= ~TIF_WIN0;
            sTI->win0h = WIN_RANGE(0, DISPLAY_WIDTH);
            sTI->win0v = WIN_RANGE(159, DISPLAY_HEIGHT);
        }
    }
    if (sTI->v[7])
    {
        s32 k = TI_Ramp(t, flood, full);
        if (sRG->flood == RG_FLOOD_SIDE)
        {
            s32 edge = 240 - (k * 290 >> 8);
            for (y = 0; y < DISPLAY_HEIGHT; y++)
            {
                s32 e = edge + Sin((y * 6 + t * 7) & 0xFF, 10) + ((y - 80) * (y - 80) >> 7);
                e = max(0, min(240, e));
                sTI->back[TIB_WIN0][y] = e >= 240 ? 0 : WIN_RANGE(e, 240);
            }
        }
        else
        {
            s32 top = 160 - (k * 170 >> 8);
            sTI->win0v = WIN_RANGE(max(0, min(159, top)), DISPLAY_HEIGHT);
        }
        sTI->bg0x = (t * 2) & 0x1FF;
        if (TI_AT(flood))
            PlaySE(sTI->elem == 0 ? SE_M_PETAL_DANCE : (sTI->elem == 1 ? SE_M_SACRED_FIRE : SE_M_WATERFALL));
        TI_Tint(TI_World(), k * 10 >> 8, RI_ElemPal()[0]);
    }
    RI_BigVersus(t, vs - (TI_Beat(2) - TI_Beat(0)), vs, sRG->hits >= 5 ? 220 : 200);
    // de ultieme VS: daarna nog een paar klappen op de tellen
    for (i = 0; i < sRG->hits; i++)
    {
        s32 at = TI_Beat(sRG->vsBeat + 1 + i);
        if (TI_AT(at))
        {
            PlaySE(i == sRG->hits - 1 ? SE_M_EXPLOSION : SE_M_COMET_PUNCH);
            sTI->v[19] = 6 + i * 2;
        }
        TI_Flash(t, at, 6, 6 + i * 2, PALETTES_ALL, RGB_WHITE);
    }
    if (sTI->v[19] > 0)
        sTI->v[19]--;
    if (t >= swap + 8)
        TI_Shake(sTI->v[19]);
    TI_Flash(t, vs, 10, 16, PALETTES_ALL, RGB_WHITE);
    return t >= end;
}

static void RG_Init136(void) { sRG = &sRG_136; RG_Init(); }
static void RG_InitPacifidlog(void) { sRG = &sRG_Pacifidlog; RG_Init(); }
static void RG_InitFrontier(void) { sRG = &sRG_Frontier; RG_Init(); }
static void RG_InitParadiso(void) { sRG = &sRG_Paradiso; RG_Init(); }

static const struct TIntro sRI_136 = {RG_Init136, RG_Update};
static const struct TIntro sRI_Pacifidlog = {RG_InitPacifidlog, RG_Update};
static const struct TIntro sRI_Frontier = {RG_InitFrontier, RG_Update};
static const struct TIntro sRI_Paradiso = {RG_InitParadiso, RG_Update};

static const struct TIntro *const sRivalIntroTable[RIS_COUNT] =
{
    [RIS_ROUTE_103] = &sRI_103,
    [RIS_RUSTBORO] = &sRI_Rustboro,
    [RIS_ROUTE_110] = &sRI_110,
    [RIS_ROUTE_119] = &sRI_119,
    [RIS_LILYCOVE] = &sRI_Lilycove,
    [RIS_ROUTE_136] = &sRI_136,
    [RIS_PACIFIDLOG] = &sRI_Pacifidlog,
    [RIS_FRONTIER] = &sRI_Frontier,
    [RIS_PARADISO] = &sRI_Paradiso,
};

static void Task_RivalIntro(u8 taskId)
{
    const struct RivalIntroEntry *e = RivalIntro_Find(TRAINER_BATTLE_PARAM.opponentA);
    u32 stage = e != NULL ? e->stage : RIS_ROUTE_103;
    // post-game: na Pacifidlog (gevecht 7) is het de Frontier (gevecht 8)
    if (stage == RIS_PACIFIDLOG && FlagGet(FLAG_RIVAL_PG_PACIFIDLOG_DONE))
        stage = RIS_FRONTIER;
    // de dagelijkse rematch in het Paradiso Resort gebruikt de ids van het Frontier-gevecht
    if (stage == RIS_FRONTIER && gMapHeader.regionMapSectionId == MAPSEC_PARADISO_RESORT)
        stage = RIS_PARADISO;
    if (gTasks[taskId].data[0] == 0)
        sTI_PendingElem = e != NULL ? e->elem : 0;
    TI_Run(taskId, sRivalIntroTable[stage]);
}
