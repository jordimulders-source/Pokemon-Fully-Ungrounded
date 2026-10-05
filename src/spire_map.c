// Project Grounded: The Spire - act-kaart (zie SPIRE_DESIGN.md en tools/grounded/spire/mockups.py, versie 4).
// PokéNav-stippen, gele routes met rand, gelopen pad rood, kamers als sprites, baas bovenaan,
// Brendan- of May-hoofdje op je plek, rode hoekhaken als cursor. De kaart scrolt (omhoog/omlaag).
// A = kamer in, START = pauzeren of opgeven.
#include "global.h"
#include "bg.h"
#include "decompress.h"
#include "gpu_regs.h"
#include "item_icon.h"
#include "main.h"
#include "malloc.h"
#include "menu.h"
#include "menu_helpers.h"
#include "palette.h"
#include "pokemon.h"
#include "pokemon_icon.h"
#include "scanline_effect.h"
#include "sound.h"
#include "spire.h"
#include "sprite.h"
#include "string_util.h"
#include "strings.h"
#include "task.h"
#include "text.h"
#include "text_window.h"
#include "window.h"
#include "constants/rgb.h"
#include "constants/songs.h"
#include "constants/species.h"

#define RUN SPIRE_SAVE

#define MAP_W       168
#define MAP_H       256     // hele act (BG van 32 tegels hoog)
#define FLOOR_GAP   30
#define BOSS_X      84
#define BOSS_Y      22
#define FLOOR_Y(f)  (MAP_H - 18 - FLOOR_GAP * (f))
#define SCROLL_MAX  (MAP_H - 160)

enum
{
    WIN_LINES,      // BG1: routes en baasplateau
    WIN_PANEL,      // BG0: act, team, BP, relics
    WIN_INFO,       // BG0: uitleg van de gekozen kamer
    WIN_COUNT,
};

#define PAL_LINES   10
#define PAL_DOTS    11
#define PAL_FRAME   14
#define PAL_TEXT    15
#define FRAME_TILE  0x1F0

#define TAG_NODE    0x5320  // + type
#define TAG_CURSOR  0x5330
#define TAG_HEAD    0x5331
#define TAG_RELIC   0x5332  // + 0/1

enum
{
    MENU_NONE,
    MENU_PAUSE,
    MENU_GIVE_UP,
    MENU_CANCEL,
};

#define EXIT_RELICS 0xFE    // sMap->exiting: naar de relic-lijst (0xFF = kamer in)

struct SpireMapScreen
{
    struct SpireActMap map;
    u8 nodeSpriteIds[SPIRE_FLOORS][SPIRE_MAX_NODES];
    u8 bossSpriteId;
    u8 headSpriteId;
    u8 cursorSpriteId;
    u8 teamSpriteIds[2];
    u8 choices[SPIRE_MAX_NODES];   // bereikbare kamers (index op de volgende verdieping)
    u8 choiceCount;
    u8 choice;
    u8 menu;                        // 0 = geen menu, anders cursor (MENU_*)
    u8 exiting;
    s16 scroll;
    s16 scrollTarget;
    u16 timer;
};

static EWRAM_DATA struct SpireMapScreen *sMap = NULL;

// --- graphics ---------------------------------------------------------------------------------
static const u32 sNodeFightGfx[] = INCBIN_U32("graphics/grounded/spire/node_fight.4bpp");
static const u16 sNodeFightPal[] = INCBIN_U16("graphics/grounded/spire/node_fight.gbapal");
static const u32 sNodeEliteGfx[] = INCBIN_U32("graphics/grounded/spire/node_elite.4bpp");
static const u16 sNodeElitePal[] = INCBIN_U16("graphics/grounded/spire/node_elite.gbapal");
static const u32 sNodeRestGfx[] = INCBIN_U32("graphics/grounded/spire/node_rest.4bpp");
static const u16 sNodeRestPal[] = INCBIN_U16("graphics/grounded/spire/node_rest.gbapal");
static const u32 sNodeShopGfx[] = INCBIN_U32("graphics/grounded/spire/node_shop.4bpp");
static const u16 sNodeShopPal[] = INCBIN_U16("graphics/grounded/spire/node_shop.gbapal");
static const u32 sNodeEventGfx[] = INCBIN_U32("graphics/grounded/spire/node_event.4bpp");
static const u16 sNodeEventPal[] = INCBIN_U16("graphics/grounded/spire/node_event.gbapal");
static const u32 sNodeTreasureGfx[] = INCBIN_U32("graphics/grounded/spire/node_treasure.4bpp");
static const u16 sNodeTreasurePal[] = INCBIN_U16("graphics/grounded/spire/node_treasure.gbapal");
static const u32 sCursorGfx[] = INCBIN_U32("graphics/grounded/spire/cursor.4bpp");
static const u16 sCursorPal[] = INCBIN_U16("graphics/grounded/spire/cursor.gbapal");
static const u32 sBrendanHeadGfx[] = INCBIN_U32("graphics/pokenav/region_map/brendan_icon.4bpp");
static const u16 sBrendanHeadPal[] = INCBIN_U16("graphics/pokenav/region_map/brendan_icon.gbapal");
static const u32 sMayHeadGfx[] = INCBIN_U32("graphics/pokenav/region_map/may_icon.4bpp");
static const u16 sMayHeadPal[] = INCBIN_U16("graphics/pokenav/region_map/may_icon.gbapal");
static const u32 sDotsGfx[] = INCBIN_U32("graphics/pokenav/bg_dots.4bpp");
static const u16 sDotsPal[] = INCBIN_U16("graphics/pokenav/bg_dots.gbapal");

static const u32 *const sNodeGfx[] =
{
    [SPIRE_ROOM_FIGHT] = sNodeFightGfx, [SPIRE_ROOM_ELITE] = sNodeEliteGfx, [SPIRE_ROOM_REST] = sNodeRestGfx,
    [SPIRE_ROOM_SHOP] = sNodeShopGfx, [SPIRE_ROOM_EVENT] = sNodeEventGfx, [SPIRE_ROOM_TREASURE] = sNodeTreasureGfx,
};
static const u16 *const sNodePal[] =
{
    [SPIRE_ROOM_FIGHT] = sNodeFightPal, [SPIRE_ROOM_ELITE] = sNodeElitePal, [SPIRE_ROOM_REST] = sNodeRestPal,
    [SPIRE_ROOM_SHOP] = sNodeShopPal, [SPIRE_ROOM_EVENT] = sNodeEventPal, [SPIRE_ROOM_TREASURE] = sNodeTreasurePal,
};

// routes: 1 geel, 2 bruine rand, 3 rood (gelopen), 4 donkerrode rand, 5 plateau, 6 plateaurand, 7 wit
static const u16 sLinesPal[16] =
{
    RGB(0, 0, 0), RGB(31, 26, 12), RGB(21, 15, 6), RGB(30, 11, 8), RGB(18, 5, 4),
    RGB(25, 8, 7), RGB(15, 4, 4), RGB(31, 31, 31), RGB(21, 5, 5),
};

static const u16 sTextPal[16] =
{
    RGB(31, 31, 31), RGB(31, 31, 31), RGB(8, 8, 9), RGB(26, 26, 27),
    RGB(5, 15, 29), RGB(23, 27, 31), RGB(25, 17, 1), RGB(31, 27, 17),
    RGB(19, 19, 20), RGB(5, 19, 9), RGB(22, 29, 23), RGB(29, 8, 7),
    RGB(31, 24, 23), RGB(10, 10, 11), RGB(15, 9, 22), RGB(26, 22, 30),
};
static const u8 sColor_Dark[]   = {1, 2, 3};
static const u8 sColor_DarkT[]  = {TEXT_COLOR_TRANSPARENT, 2, 3};
static const u8 sColor_Blue[]   = {1, 4, 5};
static const u8 sColor_Gold[]   = {1, 6, 7};
static const u8 sColor_Red[]    = {1, 11, 12};
static const u8 sColor_Purple[] = {1, 14, 15};
static const u8 sColor_Boss[]   = {0, 8, 7};

static const struct BgTemplate sBgTemplates[] =
{
    {.bg = 0, .charBaseIndex = 2, .mapBaseIndex = 31, .priority = 0},
    {.bg = 1, .charBaseIndex = 0, .mapBaseIndex = 30, .priority = 2},
    {.bg = 2, .charBaseIndex = 3, .mapBaseIndex = 29, .priority = 3}, // PokéNav-stippen in de kleuren van het biome
};

static const struct WindowTemplate sWindowTemplates[] =
{
    [WIN_LINES] = {.bg = 1, .tilemapLeft = 0, .tilemapTop = 0, .width = 21, .height = 32, .paletteNum = PAL_LINES, .baseBlock = 0x001},
    [WIN_PANEL] = {.bg = 0, .tilemapLeft = 22, .tilemapTop = 1, .width = 7, .height = 12, .paletteNum = PAL_TEXT, .baseBlock = 0x001},
    [WIN_INFO]  = {.bg = 0, .tilemapLeft = 22, .tilemapTop = 15, .width = 7, .height = 4, .paletteNum = PAL_TEXT, .baseBlock = 0x055},
    DUMMY_WIN_TEMPLATE,
};

static const struct OamData sOam32 = {.shape = SPRITE_SHAPE(32x32), .size = SPRITE_SIZE(32x32), .priority = 1};
static const struct OamData sOam16 = {.shape = SPRITE_SHAPE(16x16), .size = SPRITE_SIZE(16x16), .priority = 1};

static void CB2_SpireMap(void);
static void Task_SpireMap(u8 taskId);

// --- helpers ----------------------------------------------------------------------------------
// Altijd met transparante achtergrond (het venster is al gevuld): anders wist elke regel de onderkant
// van de regel erboven.
static void PrintText(u32 win, u32 font, u32 x, u32 y, const u8 *color, const u8 *str)
{
    u8 c[3] = {TEXT_COLOR_TRANSPARENT, color[1], color[2]};

    AddTextPrinterParameterized3(win, font, x, y, c, TEXT_SKIP_DRAW, str);
}

static u32 PathNode(u32 floor)
{
    return (RUN.path >> (2 * floor)) & 3;
}

static bool32 OnPath(u32 floor, u32 node)
{
    return floor < RUN.floor && PathNode(floor) == node;
}

static void NodePos(u32 floor, u32 node, s16 *x, s16 *y)
{
    if (floor >= SPIRE_FLOORS)
    {
        *x = BOSS_X;
        *y = BOSS_Y;
        return;
    }
    *x = sMap->map.nodes[floor][node].x;
    *y = FLOOR_Y(floor);
}

static void DrawLine(s16 x0, s16 y0, s16 x1, s16 y1, u8 col, u8 edge)
{
    s32 n = max(abs(x1 - x0), abs(y1 - y0));
    s32 s, pass;

    for (pass = 0; pass < 2; pass++)
    {
        for (s = 0; s <= n; s++)
        {
            s32 x = x0 + (x1 - x0) * s / (n ? n : 1);
            s32 y = y0 + (y1 - y0) * s / (n ? n : 1);

            if (pass == 0)
                FillWindowPixelRect(WIN_LINES, PIXEL_FILL(edge), max(0, x - 2), max(0, y - 2), 4, 4);
            else
                FillWindowPixelRect(WIN_LINES, PIXEL_FILL(col), max(0, x - 1), max(0, y - 1), 2, 2);
        }
    }
}

static void DrawRoutes(void)
{
    u32 f, i, j, done;

    FillWindowPixelBuffer(WIN_LINES, PIXEL_FILL(0));
    // eerst gewone routes, dan het gelopen pad eroverheen
    for (done = 0; done < 2; done++)
    {
        for (f = 0; f < SPIRE_FLOORS; f++)
        {
            for (i = 0; i < sMap->map.count[f]; i++)
            {
                s16 x0, y0, x1, y1;

                NodePos(f, i, &x0, &y0);
                if (f + 1 == SPIRE_FLOORS)
                {
                    bool32 taken = OnPath(f, i) && RUN.floor > SPIRE_FLOORS;

                    if (taken == done)
                        DrawLine(x0, y0, BOSS_X, BOSS_Y + 8, taken ? 3 : 1, taken ? 4 : 2);
                    continue;
                }
                for (j = 0; j < sMap->map.count[f + 1]; j++)
                {
                    bool32 taken;

                    if (!(sMap->map.nodes[f][i].links & (1u << j)))
                        continue;
                    taken = OnPath(f, i) && OnPath(f + 1, j);
                    if (taken != done)
                        continue;
                    NodePos(f + 1, j, &x1, &y1);
                    DrawLine(x0, y0, x1, y1, taken ? 3 : 1, taken ? 4 : 2);
                }
            }
        }
    }
    // baasplateau: rode ovaal
    for (j = 0; j < 19; j++)
    {
        s32 dy = (s32)j - 9;
        s32 half = 17 * (81 - dy * dy) / 81;
        u32 w = 0;

        while ((s32)(w * w) < (s32)(17 * 17 - (17 * 17 * dy * dy) / 81))
            w++;
        (void)half;
        FillWindowPixelRect(WIN_LINES, PIXEL_FILL(6), BOSS_X - w - 1, BOSS_Y - 8 + j, 2 * w + 2, 1);
        if (w > 1)
            FillWindowPixelRect(WIN_LINES, PIXEL_FILL(5), BOSS_X - w + 1, BOSS_Y - 8 + j, 2 * w - 2, 1);
    }
    PrintText(WIN_LINES, FONT_SMALL_NARROW, BOSS_X + 20, BOSS_Y - 6, sColor_Boss, COMPOUND_STRING("BOSS"));
    CopyWindowToVram(WIN_LINES, COPYWIN_FULL);
}

static const u8 sText_Battle[] = _("Battle");
static const u8 sText_Elite[] = _("Elite");
static const u8 sText_Rest[] = _("Rest");
static const u8 sText_Mart[] = _("Poké Mart");
static const u8 sText_Event[] = _("Event");
static const u8 sText_Boss[] = _("BOSS");
static const u8 sText_TwoWild[] = _("Two wild ones");
static const u8 sText_WinMove[] = _("Win: a move");
static const u8 sText_StrongFoe[] = _("A strong foe");
static const u8 sText_WinRelic[] = _("Win: relic");
static const u8 sText_HealOr[] = _("Heal, or");
static const u8 sText_Evolve[] = _("upgrade a move");
static const u8 sText_Spend[] = _("Spend your ¥");
static const u8 sText_WhoKnows[] = _("Who knows?");
static const u8 sText_NextAct[] = _("+ next act");
static const u8 sText_Empty[] = _("");
static const u8 sText_Treasure[] = _("Treasure");
static const u8 sText_FreeRelic[] = _("A free relic");

static const u8 *const sRoomText[][3] =
{
    [SPIRE_ROOM_NONE]  = {sText_Battle, sText_TwoWild, sText_WinMove},
    [SPIRE_ROOM_FIGHT] = {sText_Battle, sText_TwoWild, sText_WinMove},
    [SPIRE_ROOM_ELITE] = {sText_Elite, sText_StrongFoe, sText_WinRelic},
    [SPIRE_ROOM_REST]  = {sText_Rest, sText_HealOr, sText_Evolve},
    [SPIRE_ROOM_SHOP]  = {sText_Mart, sText_Spend, sText_Empty},
    [SPIRE_ROOM_EVENT] = {sText_Event, sText_WhoKnows, sText_Empty},
    [SPIRE_ROOM_BOSS]  = {sText_Boss, sText_WinRelic, sText_NextAct},
    [SPIRE_ROOM_TREASURE] = {sText_Treasure, sText_FreeRelic, sText_Empty},
};

static u32 ChoiceType(void)
{
    if (RUN.floor >= SPIRE_FLOORS)
        return SPIRE_ROOM_BOSS;
    return sMap->map.nodes[RUN.floor][sMap->choices[sMap->choice]].type;
}

static void DrawInfo(void)
{
    FillWindowPixelBuffer(WIN_INFO, PIXEL_FILL(1));
    if (sMap->menu != MENU_NONE)
    {
        static const u8 sText_Pause[] = _("Pause run");
        static const u8 sText_GiveUp[] = _("Give up");
        static const u8 sText_Cancel[] = _("Cancel");
        const u8 *const items[] = {sText_Pause, sText_GiveUp, sText_Cancel};
        u32 i;

        for (i = 0; i < 3; i++)
        {
            if (sMap->menu == MENU_PAUSE + i)
                PrintText(WIN_INFO, FONT_NORMAL, 0, i * 10 - 2, sColor_Red, COMPOUND_STRING("▶"));
            PrintText(WIN_INFO, FONT_SMALL_NARROW, 8, i * 10, sColor_Dark, items[i]);
        }
    }
    else
    {
        u32 type = ChoiceType();

        PrintText(WIN_INFO, FONT_NORMAL, 0, 0, type == SPIRE_ROOM_BOSS || type == SPIRE_ROOM_ELITE ? sColor_Red : sColor_Dark, sRoomText[type][0]);
        // transparante achtergrond, anders wist elke regel de onderkant van de regel erboven
        PrintText(WIN_INFO, FONT_SMALL_NARROW, 0, 12, sColor_DarkT, sRoomText[type][1]);
        if (RUN.floor < SPIRE_FLOORS && sMap->choiceCount > 0 && Spire_IsAcroJump(&sMap->map, RUN.floor, sMap->choices[sMap->choice]))
        {
            // Acro Bike (relic): deze kamer ligt niet op je pad, de sprong kost een lading
            ConvertIntToDecimalStringN(gStringVar1, RUN.relicCharges, STR_CONV_MODE_LEFT_ALIGN, 1);
            StringExpandPlaceholders(gStringVar4, COMPOUND_STRING("Acro hop ({STR_VAR_1})"));
            PrintText(WIN_INFO, FONT_SMALL_NARROW, 0, 21, sColor_DarkT, gStringVar4);
        }
        else
        {
            PrintText(WIN_INFO, FONT_SMALL_NARROW, 0, 21, sColor_DarkT, sRoomText[type][2]);
        }
    }
    CopyWindowToVram(WIN_INFO, COPYWIN_FULL);
}

static void DrawPanel(void)
{
    u8 buf[24];
    u32 i, n = 0;

    FillWindowPixelBuffer(WIN_PANEL, PIXEL_FILL(1));
    ConvertIntToDecimalStringN(gStringVar1, RUN.act, STR_CONV_MODE_LEFT_ALIGN, 1);
    StringExpandPlaceholders(buf, COMPOUND_STRING("ACT {STR_VAR_1}"));
    PrintText(WIN_PANEL, FONT_NORMAL, 0, 0, sColor_Purple, buf);
    ConvertIntToDecimalStringN(gStringVar1, min(RUN.floor + 1, SPIRE_FLOORS + 1), STR_CONV_MODE_LEFT_ALIGN, 1);
    ConvertIntToDecimalStringN(gStringVar2, SPIRE_FLOORS + 1, STR_CONV_MODE_LEFT_ALIGN, 1);
    StringExpandPlaceholders(buf, COMPOUND_STRING("{STR_VAR_1}/{STR_VAR_2}"));
    PrintText(WIN_PANEL, FONT_SMALL_NARROW, 38, 2, sColor_Dark, buf);
    for (i = 0; i < 2; i++)
    {
        struct Pokemon *mon = Spire_GetRunMon(i);
        u32 hp = GetMonData(mon, MON_DATA_HP), maxHp = GetMonData(mon, MON_DATA_MAX_HP);
        u32 w = maxHp ? 28 * hp / maxHp : 0;
        u32 col = (hp * 2 > maxHp) ? 9 : (hp * 5 > maxHp) ? 6 : 11;
        u32 y = 16 + i * 22;

        ConvertIntToDecimalStringN(buf, maxHp ? (hp * 100 + maxHp - 1) / maxHp : 0, STR_CONV_MODE_LEFT_ALIGN, 3);
        StringAppend(buf, COMPOUND_STRING("%"));
        PrintText(WIN_PANEL, FONT_SMALL_NARROW, 32, y, sColor_Dark, buf);
        FillWindowPixelRect(WIN_PANEL, PIXEL_FILL(13), 26, y + 12, 30, 4);
        if (w)
            FillWindowPixelRect(WIN_PANEL, PIXEL_FILL(col), 27, y + 13, w, 2);
    }
    ConvertIntToDecimalStringN(gStringVar1, RUN.bp, STR_CONV_MODE_LEFT_ALIGN, 4);
    StringExpandPlaceholders(buf, COMPOUND_STRING("{STR_VAR_1}BP"));
    PrintText(WIN_PANEL, FONT_SMALL_NARROW, 0, 60, sColor_Blue, buf);
    ConvertIntToDecimalStringN(buf, RUN.gold, STR_CONV_MODE_LEFT_ALIGN, 4);
    StringAppend(buf, COMPOUND_STRING("¥"));
    PrintText(WIN_PANEL, FONT_SMALL_NARROW, 28, 60, sColor_Gold, buf);
    n = Spire_CountRelics();
    if (n > 2)
    {
        ConvertIntToDecimalStringN(gStringVar1, n - 2, STR_CONV_MODE_LEFT_ALIGN, 2);
        StringExpandPlaceholders(buf, COMPOUND_STRING("+{STR_VAR_1}"));
        PrintText(WIN_PANEL, FONT_SMALL_NARROW, 44, 72, sColor_Dark, buf);
    }
    else if (n == 0)
    {
        PrintText(WIN_PANEL, FONT_SMALL_NARROW, 0, 76, sColor_Dark, COMPOUND_STRING("No relics"));
    }
    if (n > 0) // R: lijst met uitleg
        PrintText(WIN_PANEL, FONT_SMALL_NARROW, 46, 84, sColor_Blue, COMPOUND_STRING("R"));
    CopyWindowToVram(WIN_PANEL, COPYWIN_FULL);
}

// --- sprites ----------------------------------------------------------------------------------
static u8 CreateGfxSprite(const u32 *gfx, const u16 *pal, u16 tag, const struct OamData *oam, u32 size)
{
    struct SpriteSheet sheet = {gfx, size, tag};
    struct SpritePalette spal = {pal, tag};
    struct SpriteTemplate tmpl = {
        .tileTag = tag, .paletteTag = tag, .oam = oam, .anims = gDummySpriteAnimTable, .images = NULL,
        .affineAnims = gDummySpriteAffineAnimTable, .callback = SpriteCallbackDummy,
    };

    if (GetSpriteTileStartByTag(tag) == 0xFFFF)
        LoadSpriteSheet(&sheet);
    if (IndexOfSpritePaletteTag(tag) == 0xFF)
        LoadSpritePalette(&spal);
    return CreateSprite(&tmpl, 0, 0, 1);
}

static void PlaceSpriteOnMap(u8 spriteId, s16 x, s16 y)
{
    struct Sprite *sprite = &gSprites[spriteId];
    s16 sy = y - sMap->scroll;

    sprite->x = x;
    sprite->y = sy;
    sprite->invisible = (sy < -16 || sy > 176);
}

static void UpdateSpritePositions(void)
{
    u32 f, i;
    s16 x, y;

    for (f = 0; f < SPIRE_FLOORS; f++)
    {
        for (i = 0; i < sMap->map.count[f]; i++)
        {
            NodePos(f, i, &x, &y);
            PlaceSpriteOnMap(sMap->nodeSpriteIds[f][i], x, y);
        }
    }
    PlaceSpriteOnMap(sMap->bossSpriteId, BOSS_X, BOSS_Y - 6);
    if (RUN.floor > 0)
    {
        NodePos(RUN.floor - 1, PathNode(RUN.floor - 1), &x, &y);
        PlaceSpriteOnMap(sMap->headSpriteId, x - 16, y + 2);
    }
    else
    {
        PlaceSpriteOnMap(sMap->headSpriteId, BOSS_X, MAP_H + 8);
        gSprites[sMap->headSpriteId].y = 150;
        gSprites[sMap->headSpriteId].x = 84;
        gSprites[sMap->headSpriteId].invisible = FALSE;
    }
    if (RUN.floor >= SPIRE_FLOORS)
        PlaceSpriteOnMap(sMap->cursorSpriteId, BOSS_X, BOSS_Y);
    else
    {
        NodePos(RUN.floor, sMap->choices[sMap->choice], &x, &y);
        PlaceSpriteOnMap(sMap->cursorSpriteId, x, y);
    }
    if ((sMap->timer & 0x1F) >= 0x18)
        gSprites[sMap->cursorSpriteId].invisible = TRUE;
    SetGpuReg(REG_OFFSET_BG1VOFS, sMap->scroll);
    SetGpuReg(REG_OFFSET_BG2VOFS, sMap->scroll);
}

static void CreateSprites(void)
{
    u32 f, i;

    for (f = 0; f < SPIRE_FLOORS; f++)
    {
        for (i = 0; i < sMap->map.count[f]; i++)
        {
            u32 type = sMap->map.nodes[f][i].type;
            u8 id = CreateGfxSprite(sNodeGfx[type], sNodePal[type], TAG_NODE + type, &sOam32, 0x200);

            // gemiste kamers op verdiepingen die je al voorbij bent: half doorzichtig
            if (f < RUN.floor && !OnPath(f, i))
                gSprites[id].oam.objMode = ST_OAM_OBJ_BLEND;
            sMap->nodeSpriteIds[f][i] = id;
        }
    }
    LoadMonIconPalettes();
    sMap->bossSpriteId = CreateMonIconNoPersonality(Spire_GetBossSpecies(), SpriteCB_MonIcon, 0, 0, 1);
    if (gSaveBlock2Ptr->playerGender == FEMALE)
        sMap->headSpriteId = CreateGfxSprite(sMayHeadGfx, sMayHeadPal, TAG_HEAD, &sOam16, 0x80);
    else
        sMap->headSpriteId = CreateGfxSprite(sBrendanHeadGfx, sBrendanHeadPal, TAG_HEAD, &sOam16, 0x80);
    gSprites[sMap->headSpriteId].oam.priority = 0;
    sMap->cursorSpriteId = CreateGfxSprite(sCursorGfx, sCursorPal, TAG_CURSOR, &sOam32, 0x200);
    gSprites[sMap->cursorSpriteId].oam.priority = 0;

    for (i = 0; i < 2; i++)
    {
        struct Pokemon *mon = Spire_GetRunMon(i);

        sMap->teamSpriteIds[i] = CreateMonIcon(GetMonData(mon, MON_DATA_SPECIES), SpriteCB_MonIcon,
                                               176 + 10, 8 + 16 + i * 22 + 8, 0, GetMonData(mon, MON_DATA_PERSONALITY));
        gSprites[sMap->teamSpriteIds[i]].oam.priority = 0;
    }
    // relics: de eerste twee als item-icoon
    {
        u32 n = 0;

        for (i = 0; i < SPIRE_RELIC_COUNT && n < 2; i++)
        {
            if (Spire_HasRelic(i))
            {
                u8 id = AddItemIconSprite(TAG_RELIC + n, TAG_RELIC + n, gSpireRelics[i].item);

                if (id != MAX_SPRITES)
                {
                    gSprites[id].x = 176 + 12 + n * 22;
                    gSprites[id].y = 8 + 72 + 12;
                    gSprites[id].oam.priority = 0;
                }
                n++;
            }
        }
    }
}

static void FindChoices(void)
{
    u32 i;

    sMap->choiceCount = 0;
    if (RUN.floor >= SPIRE_FLOORS)
    {
        sMap->choices[0] = 0;
        sMap->choiceCount = 1;
        return;
    }
    for (i = 0; i < sMap->map.count[RUN.floor]; i++)
        if (Spire_IsReachable(&sMap->map, RUN.floor, i))
            sMap->choices[sMap->choiceCount++] = i;
    sMap->choice = 0;
}

static void ScrollToChoice(void)
{
    s16 x, y;

    if (RUN.floor >= SPIRE_FLOORS)
        y = BOSS_Y;
    else
        NodePos(RUN.floor, sMap->choices[sMap->choice], &x, &y);
    sMap->scrollTarget = max(0, min(SCROLL_MAX, y - 70));
}

// --- scherm openen en sluiten -----------------------------------------------------------------
static void VBlankCB_SpireMap(void)
{
    LoadOam();
    ProcessSpriteCopyRequests();
    TransferPlttBuffer();
}

static void CB2_SpireMap(void)
{
    RunTasks();
    AnimateSprites();
    BuildOamBuffer();
    RunTextPrinters();
    DoScheduledBgTilemapCopiesToVram();
    UpdatePaletteFade();
}

// Achtergrond: PokéNav-stippen in de kleuren van het biome, met een verloop naar boven toe:
// hoe dichter bij de baas, hoe donkerder en roder (de toren). 8 banden van 4 tegelrijen, paletten 2-9.
#define PAL_BANDS   2
#define NUM_BANDS   8

static const u16 sBiomeColors[SPIRE_BIOME_COUNT] =   // achtergrond onderaan de act; de stip is iets lichter
{
    [SPIRE_BIOME_GROVE] = RGB(5, 11, 6),
    [SPIRE_BIOME_DOCKS] = RGB(4, 8, 14),
    [SPIRE_BIOME_HIVE]  = RGB(13, 10, 4),
    [SPIRE_BIOME_FROST] = RGB(8, 12, 17),
    [SPIRE_BIOME_COURT] = RGB(10, 6, 14),
    [SPIRE_BIOME_ABYSS] = RGB(6, 4, 9),
};
static const u16 sSpireTopColor = RGB(11, 3, 5);

static u16 LerpColor(u16 a, u16 b, u32 t, u32 n)
{
    return RGB(GET_R(a) + ((s32)GET_R(b) - (s32)GET_R(a)) * (s32)t / (s32)n,
               GET_G(a) + ((s32)GET_G(b) - (s32)GET_G(a)) * (s32)t / (s32)n,
               GET_B(a) + ((s32)GET_B(b) - (s32)GET_B(a)) * (s32)t / (s32)n);
}

static void LoadBackground(void)
{
    u16 *tilemap = AllocZeroed(BG_SCREEN_SIZE);
    u32 biome = RUN.biome < SPIRE_BIOME_COUNT ? RUN.biome : 0;
    u32 x, y, b;

    LoadBgTiles(2, sDotsGfx, 0x40, 0);
    for (b = 0; b < NUM_BANDS; b++)
    {
        u16 pal[16];
        u32 t = NUM_BANDS - 1 - b;      // band 0 = bovenaan = de toren in

        CpuCopy16(sDotsPal, pal, sizeof(pal));
        pal[1] = LerpColor(sBiomeColors[biome], sSpireTopColor, t, NUM_BANDS - 1);
        pal[2] = LerpColor(pal[1], RGB_WHITE, 2, 16);   // stip: een tikje lichter (zoals de PokéNav)
        LoadPalette(pal, BG_PLTT_ID(PAL_BANDS + b), PLTT_SIZE_4BPP);
    }
    for (y = 0; y < 32; y++)
        for (x = 0; x < 32; x++)
            tilemap[y * 32 + x] = (x & 1) | ((PAL_BANDS + y * NUM_BANDS / 32) << 12);
    SetBgTilemapBuffer(2, tilemap);
    ScheduleBgCopyTilemapToVram(2);
}

void Spire_OpenMap(void)
{
    sMap = AllocZeroed(sizeof(*sMap));
    Spire_GenerateMap(&sMap->map, RUN.seed);
    FindChoices();
    ScrollToChoice();
    sMap->scroll = sMap->scrollTarget;

    SetVBlankCallback(NULL);
    ScanlineEffect_Stop();
    ResetPaletteFade();
    ResetSpriteData();
    FreeAllSpritePalettes();
    ResetTasks();
    ResetVramOamAndBgCntRegs();
    ResetAllBgsCoordinates();
    ResetBgsAndClearDma3BusyFlags(0);
    InitBgsFromTemplates(0, sBgTemplates, ARRAY_COUNT(sBgTemplates));
    SetBgTilemapBuffer(0, AllocZeroed(BG_SCREEN_SIZE));
    SetBgTilemapBuffer(1, AllocZeroed(BG_SCREEN_SIZE));
    InitWindows(sWindowTemplates);
    DeactivateAllTextPrinters();
    LoadBackground();
    LoadPalette(sLinesPal, BG_PLTT_ID(PAL_LINES), PLTT_SIZE_4BPP);
    LoadPalette(sTextPal, BG_PLTT_ID(PAL_TEXT), PLTT_SIZE_4BPP);
    LoadWindowGfx(WIN_PANEL, 0, FRAME_TILE, BG_PLTT_ID(PAL_FRAME));
    DrawStdFrameWithCustomTileAndPalette(WIN_PANEL, FALSE, FRAME_TILE, PAL_FRAME);
    DrawStdFrameWithCustomTileAndPalette(WIN_INFO, FALSE, FRAME_TILE, PAL_FRAME);
    PutWindowTilemap(WIN_LINES);

    DrawRoutes();
    DrawPanel();
    DrawInfo();
    CreateSprites();
    UpdateSpritePositions();
    ScheduleBgCopyTilemapToVram(0);
    ScheduleBgCopyTilemapToVram(1);

    SetGpuReg(REG_OFFSET_DISPCNT, DISPCNT_OBJ_1D_MAP | DISPCNT_OBJ_ON | DISPCNT_BG0_ON | DISPCNT_BG1_ON | DISPCNT_BG2_ON);
    SetGpuReg(REG_OFFSET_BLDCNT, BLDCNT_TGT2_BG1 | BLDCNT_TGT2_BG2 | BLDCNT_EFFECT_BLEND);
    SetGpuReg(REG_OFFSET_BLDALPHA, BLDALPHA_BLEND(7, 9));
    ShowBg(0);
    ShowBg(1);
    ShowBg(2);
    if (GetCurrentMapMusic() != MUS_B_TOWER)
        PlayNewMapMusic(MUS_B_TOWER);
    BeginNormalPaletteFade(PALETTES_ALL, 0, 16, 0, RGB_BLACK);
    SetVBlankCallback(VBlankCB_SpireMap);
    SetMainCallback2(CB2_SpireMap);
    CreateTask(Task_SpireMap, 0);
}

static void CloseMap(void)
{
    FreeMonIconPalettes();
    FreeAllWindowBuffers();
    Free(GetBgTilemapBuffer(0));
    Free(GetBgTilemapBuffer(1));
    Free(GetBgTilemapBuffer(2));
    SetGpuReg(REG_OFFSET_BLDCNT, 0);
}

// --- invoer -----------------------------------------------------------------------------------
static void Task_SpireMap(u8 taskId)
{
    sMap->timer++;
    if (sMap->scroll != sMap->scrollTarget)
        sMap->scroll += (sMap->scrollTarget > sMap->scroll) ? min(4, sMap->scrollTarget - sMap->scroll)
                                                             : -min(4, sMap->scroll - sMap->scrollTarget);
    UpdateSpritePositions();
    if (gPaletteFade.active)
        return;

    if (sMap->exiting)
    {
        u32 action = sMap->exiting;
        u32 floor = RUN.floor, node = sMap->choices[sMap->choice];

        DestroyTask(taskId);
        CloseMap();
        Free(sMap);
        sMap = NULL;
        if (action == MENU_PAUSE)
            Spire_SuspendRun();
        else if (action == MENU_GIVE_UP)
            Spire_GiveUpRun();
        else if (action == EXIT_RELICS)
            Spire_OpenCards(SPIRE_CARDS_RELIC_LIST, Spire_OpenMap);
        else
            Spire_EnterRoom(floor, node);
        return;
    }

    if (sMap->menu != MENU_NONE)
    {
        if (JOY_NEW(DPAD_UP) && sMap->menu > MENU_PAUSE)
        {
            PlaySE(SE_SELECT);
            sMap->menu--;
            DrawInfo();
        }
        else if (JOY_NEW(DPAD_DOWN) && sMap->menu < MENU_CANCEL)
        {
            PlaySE(SE_SELECT);
            sMap->menu++;
            DrawInfo();
        }
        else if (JOY_NEW(A_BUTTON) && sMap->menu != MENU_CANCEL)
        {
            PlaySE(SE_SELECT);
            sMap->exiting = sMap->menu;
            BeginNormalPaletteFade(PALETTES_ALL, 0, 0, 16, RGB_BLACK);
        }
        else if (JOY_NEW(A_BUTTON | B_BUTTON | START_BUTTON))
        {
            PlaySE(SE_SELECT);
            sMap->menu = MENU_NONE;
            DrawInfo();
        }
        return;
    }

    if (JOY_NEW(DPAD_LEFT) && sMap->choice > 0)
    {
        PlaySE(SE_SELECT);
        sMap->choice--;
        ScrollToChoice();
        DrawInfo();
    }
    else if (JOY_NEW(DPAD_RIGHT) && sMap->choice + 1 < sMap->choiceCount)
    {
        PlaySE(SE_SELECT);
        sMap->choice++;
        ScrollToChoice();
        DrawInfo();
    }
    else if (JOY_HELD(DPAD_UP))
    {
        sMap->scrollTarget = max(0, sMap->scrollTarget - 3);
    }
    else if (JOY_HELD(DPAD_DOWN))
    {
        sMap->scrollTarget = min(SCROLL_MAX, sMap->scrollTarget + 3);
    }
    else if (JOY_NEW(A_BUTTON) && sMap->choiceCount > 0)
    {
        PlaySE(SE_SELECT);
        sMap->exiting = 0xFF;
        BeginNormalPaletteFade(PALETTES_ALL, 0, 0, 16, RGB_BLACK);
    }
    else if (JOY_NEW(START_BUTTON | B_BUTTON))
    {
        PlaySE(SE_SELECT);
        sMap->menu = MENU_PAUSE;
        DrawInfo();
    }
    else if (JOY_NEW(R_BUTTON) && Spire_CountRelics() > 0)
    {
        // R: je relics met uitleg (kaartenscherm), daarna terug naar de kaart
        PlaySE(SE_SELECT);
        sMap->exiting = EXIT_RELICS;
        BeginNormalPaletteFade(PALETTES_ALL, 0, 0, 16, RGB_BLACK);
    }
}
