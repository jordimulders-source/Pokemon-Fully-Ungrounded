// Project Grounded: Battle Stadium - schermen (zie STADIUM_DESIGN.md).
// - Wedstrijdkaart (rondes vóór de kwartfinale): jij en je tegenstander groot tegenover elkaar.
// - Bracket op papier (vanaf de kwartfinale): acht trainers, lijnen naar het midden, de weg van de
//   winnaars in rood, wie eruit ligt verbleekt.
// - Compagnonkeuze (doubles): collectie met groot plaatje, de drie Pokémon en hoe je ze vrijspeelt.
// - Melding "NEW PARTNER!" na een gevecht.
#include "global.h"
#include "battle_main.h"
#include "bg.h"
#include "data.h"
#include "decompress.h"
#include "event_data.h"
#include "gpu_regs.h"
#include "main.h"
#include "malloc.h"
#include "menu.h"
#include "menu_helpers.h"
#include "overworld.h"
#include "palette.h"
#include "pokemon.h"
#include "pokemon_icon.h"
#include "scanline_effect.h"
#include "script.h"
#include "sound.h"
#include "sprite.h"
#include "stadium.h"
#include "string_util.h"
#include "task.h"
#include "text.h"
#include "text_window.h"
#include "trainer_pokemon_sprites.h"
#include "window.h"
#include "constants/battle_partner.h"
#include "constants/rgb.h"
#include "constants/songs.h"
#include "constants/trainers.h"

enum
{
    SCREEN_BRACKET,
    SCREEN_COMPANIONS,
    SCREEN_UNLOCK,
};

#define PAL_TABLE   12
#define PAL_FRAME   14
#define PAL_TEXT    15
#define FRAME_TILE  0x200
#define MAX_PICS    8
#define LIST_ROWS   9
#define UNKNOWN     0xFE

struct StadiumScreen
{
    void (*onDone)(void);
    u8 screen;
    u8 exiting;
    u8 cursor;
    u8 scroll;
    u8 unlock;
    u8 pics[MAX_PICS];
    u8 picCount;
    u8 portraitMask;    // welke pics[] een portret zijn (eigen tegels, geen trainerpic-sprite)
    u8 icons[PARTY_SIZE];
    u8 iconCount;
    u8 shownPicFor;
    u8 list[STADIUM_MAX_COMPANIONS];   // zichtbare compagnons (cursor/scroll wijzen hierin)
    u8 listCount;
};

static EWRAM_DATA struct StadiumScreen *sScr = NULL;

// tafel (houtnerf) en papier
static const u32 sTableTiles[2][8] =
{
    {0x11111111, 0x11211111, 0x11111111, 0x11111112, 0x11111111, 0x12111111, 0x11111111, 0x11111211},
    {0x11111111, 0x11111111, 0x11112111, 0x11111111, 0x21111111, 0x11111111, 0x11111121, 0x11111111},
};
static const u16 sTablePal[16] = {RGB(10, 6, 3), RGB(10, 6, 3), RGB(8, 5, 2)};

// tekstpalet: 1 = papier, 2/3 donker, 4/5 rood, 6/7 grijs, 8/9 blauw, 10 lijn, 11/12 goud
static const u16 sTextPal[16] =
{
    RGB(31, 30, 26), RGB(31, 30, 26), RGB(6, 5, 4), RGB(24, 23, 19),
    RGB(28, 4, 4), RGB(31, 22, 20), RGB(17, 16, 14), RGB(26, 25, 21),
    RGB(4, 10, 24), RGB(21, 24, 30), RGB(14, 11, 8), RGB(24, 17, 2), RGB(31, 27, 15),
};
#define PAPER   1
#define INK     10
#define RED_INK 4
static const u8 sColor_Dark[] = {0, 2, 3};
static const u8 sColor_Red[]  = {0, 4, 5};
static const u8 sColor_Gray[] = {0, 6, 7};
static const u8 sColor_Blue[] = {0, 8, 9};
static const u8 sColor_Gold[] = {0, 11, 12};

static const struct BgTemplate sBgTemplates[] =
{
    {.bg = 0, .charBaseIndex = 0, .mapBaseIndex = 31, .priority = 1},
    {.bg = 1, .charBaseIndex = 2, .mapBaseIndex = 30, .priority = 3},
};

// één groot papiervel (28×18 tegels = 504 + 1 lege tegel 0, past in charblock 0)
static const struct WindowTemplate sWindowTemplates[] =
{
    {.bg = 0, .tilemapLeft = 1, .tilemapTop = 1, .width = 28, .height = 18, .paletteNum = PAL_TEXT, .baseBlock = 0x001},
    DUMMY_WIN_TEMPLATE,
};
#define WIN 0
#define WX(x) ((x) - 8)     // schermcoördinaat -> venster
#define WY(y) ((y) - 8)

static void Task_StadiumScreen(u8 taskId);

// --- hulpjes ----------------------------------------------------------------------------------
static void PrintText(u32 font, u32 x, u32 y, const u8 *color, const u8 *str)
{
    AddTextPrinterParameterized3(WIN, font, x, y, color, TEXT_SKIP_DRAW, str);
}

static void PrintCentered(u32 font, u32 cx, u32 y, const u8 *color, const u8 *str)
{
    s32 w = GetStringWidth(font, str, 0);

    PrintText(font, max(0, (s32)cx - w / 2), y, color, str);
}

static void Line(s32 x0, s32 y0, s32 x1, s32 y1, u8 color)
{
    // alleen horizontaal of verticaal, 2 px dik, in schermcoördinaten
    if (y0 == y1)
        FillWindowPixelRect(WIN, PIXEL_FILL(color), WX(min(x0, x1)), WY(y0), abs(x1 - x0) + 2, 2);
    else
        FillWindowPixelRect(WIN, PIXEL_FILL(color), WX(x0), WY(min(y0, y1)), 2, abs(y1 - y0) + 2);
}

// Trainerplaatje (64×64); klein = halve grootte via affine matrix 0
#define TAG_PORTRAIT 0x5400

static const struct OamData sOam_Portrait = {.shape = SPRITE_SHAPE(32x32), .size = SPRITE_SIZE(32x32), .priority = 0};

static u8 Pixel(const u8 *pic, u32 x, u32 y)
{
    u8 b = pic[((y / 8) * 8 + x / 8) * 32 + (y % 8) * 4 + (x % 8) / 2];

    return (x & 1) ? b >> 4 : b & 0xF;
}

// Portret voor de bracket: 32x32 rond het hoofd uit de 64x64-trainerfoto, op ware pixelgrootte
// (verkleinen gooit elke tweede pixel weg en ziet er rommelig uit)
static u8 AddPortrait(u16 picId, s16 x, s16 y, u8 slot)
{
    u8 *pic = Alloc(64 * 64 / 2), *out = AllocZeroed(32 * 32 / 2);
    s32 top = 0, minX = 63, maxX = 0, x0, y0, px, py, row;
    struct SpriteSheet sheet = {out, 32 * 32 / 2, TAG_PORTRAIT + slot};
    struct SpriteTemplate tmpl = {TAG_PORTRAIT + slot, TAG_NONE, &sOam_Portrait, gDummySpriteAnimTable, NULL, gDummySpriteAffineAnimTable, SpriteCallbackDummy};
    u8 id;

    DecompressPicFromTable(&gTrainerSprites[picId].frontPic, pic);
    // bovenkant van de figuur, en het midden van het hoofd (de eerste 16 rijen)
    for (top = 0; top < 64; top++)
    {
        for (px = 0; px < 64 && !Pixel(pic, px, top); px++)
            ;
        if (px < 64)
            break;
    }
    for (row = top; row < top + 16 && row < 64; row++)
    {
        for (px = 0; px < 64; px++)
        {
            if (Pixel(pic, px, row))
            {
                minX = min(minX, px);
                maxX = max(maxX, px);
            }
        }
    }
    x0 = max(0, min(32, (minX + maxX) / 2 - 16));
    y0 = max(0, min(32, top - 2));
    for (py = 0; py < 32; py++)
    {
        for (px = 0; px < 32; px++)
        {
            u8 v = Pixel(pic, x0 + px, y0 + py);
            u8 *b = &out[((py / 8) * 4 + px / 8) * 32 + (py % 8) * 4 + (px % 8) / 2];

            *b |= (px & 1) ? v << 4 : v;
        }
    }
    LoadSpriteSheet(&sheet);
    LoadPalette(gTrainerSprites[picId].palette.data, OBJ_PLTT_ID(slot), PLTT_SIZE_4BPP);
    Free(pic);
    Free(out);
    id = CreateSprite(&tmpl, x, y, 0);
    if (id != MAX_SPRITES)
        gSprites[id].oam.paletteNum = slot;
    return id;
}

// Trainerplaatje (64x64), of als portret (32x32) in de bracket
static u8 AddPic(u16 picId, s16 x, s16 y, bool32 small)
{
    u8 slot = sScr->picCount;
    u16 id;

    if (slot >= MAX_PICS)
        return MAX_SPRITES;
    if (small)
    {
        id = AddPortrait(picId, x, y, slot);
        if (id == MAX_SPRITES)
            return MAX_SPRITES;
        sScr->portraitMask |= 1 << slot;
    }
    else
    {
        id = CreateTrainerPicSprite(picId, TRUE, x, y, slot, TAG_NONE);
        if (id == 0xFFFF)
            return MAX_SPRITES;
    }
    gSprites[id].oam.priority = 0;
    sScr->pics[sScr->picCount++] = id;
    return id;
}

static void FreePics(void)
{
    u32 i;

    for (i = 0; i < sScr->picCount; i++)
    {
        if (sScr->portraitMask & (1 << i))
        {
            DestroySprite(&gSprites[sScr->pics[i]]);
            FreeSpriteTilesByTag(TAG_PORTRAIT + i);
        }
        else
        {
            FreeAndDestroyTrainerPicSprite(sScr->pics[i]);
        }
    }
    sScr->picCount = 0;
    sScr->portraitMask = 0;
    for (i = 0; i < sScr->iconCount; i++)
        FreeAndDestroyMonIconSprite(&gSprites[sScr->icons[i]]);
    sScr->iconCount = 0;
}

// palet van een plaatje naar papierkleur trekken (uitgeschakeld) of zwart (nog niet vrijgespeeld)
static void FadePic(u8 slot, u8 coeff, u16 color)
{
    u32 i;

    for (i = 1; i < 16; i++)
    {
        u16 c = gPlttBufferUnfaded[OBJ_PLTT_ID(slot) + i];
        s32 r = GET_R(c), g = GET_G(c), b = GET_B(c);

        r += ((GET_R(color) - r) * coeff) >> 4;
        g += ((GET_G(color) - g) * coeff) >> 4;
        b += ((GET_B(color) - b) * coeff) >> 4;
        gPlttBufferUnfaded[OBJ_PLTT_ID(slot) + i] = gPlttBufferFaded[OBJ_PLTT_ID(slot) + i] = RGB(r, g, b);
    }
}

// --- bracket ------------------------------------------------------------------------------------
// posities (schermcentrum) van de acht kwartfinalisten
static const s16 sQfY[] = {38, 70, 102, 134};
#define QF_LX   30
#define QF_RX   210

static bool32 Decided(u8 v)
{
    return v != UNKNOWN;
}

static void DrawMatchCard(void)
{
    u32 round = Stadium_GetRound(), pos = 0, n = (1 << Stadium_GetRoundCount()) >> round;
    u8 opp, name[64];
    const u8 *const sRoundNames[] = {
        COMPOUND_STRING("ROUND OF 32"), COMPOUND_STRING("ROUND OF 16"), COMPOUND_STRING("QUARTERFINAL"),
        COMPOUND_STRING("SEMIFINAL"), COMPOUND_STRING("FINAL") };
    u32 roundName = round + (5 - Stadium_GetRoundCount());

    for (pos = 0; pos < n; pos++)
        if (Stadium_GetBracketSlot(round, pos) == 0)
            break;
    opp = Stadium_GetBracketSlot(round, pos ^ 1);
    PrintCentered(FONT_NORMAL, 112, 4, sColor_Dark, sRoundNames[min(roundName, 4)]);
    ConvertIntToDecimalStringN(name, round + 1, STR_CONV_MODE_LEFT_ALIGN, 1);
    StringAppend(name, COMPOUND_STRING(" of "));
    ConvertIntToDecimalStringN(name + StringLength(name), Stadium_GetRoundCount(), STR_CONV_MODE_LEFT_ALIGN, 1);
    PrintCentered(FONT_SMALL, 112, 20, sColor_Gray, name);
    PrintCentered(FONT_NORMAL, 112, 64, sColor_Red, COMPOUND_STRING("VS"));
    Stadium_GetEntrantName(0, name);
    PrintCentered(FONT_SMALL_NARROW, 56, 116, sColor_Blue, name);
    Stadium_GetEntrantName(opp, name);
    PrintCentered(FONT_SMALL_NARROW, 168, 116, sColor_Dark, name);
    AddPic(Stadium_EntrantPic(0), 64, 80, FALSE);
    AddPic(Stadium_EntrantPic(opp), 176, 80, FALSE);
    PrintCentered(FONT_SMALL, 112, 128, sColor_Gray, COMPOUND_STRING("Everyone fights at level 50."));
}

static void DrawPaperBracket(void)
{
    u32 q = Stadium_GetRoundCount() - 3, p, side;
    u8 name[64];
    const u8 *const sTitles[] = {
        COMPOUND_STRING("QUARTERFINALS"), COMPOUND_STRING("SEMIFINALS"), COMPOUND_STRING("THE FINAL"), COMPOUND_STRING("CHAMPION!") };
    u32 stage = Stadium_GetRound() - q;
    u8 champ = Stadium_GetBracketSlot(q + 3, 0);

    PrintCentered(FONT_NORMAL, 112, 2, stage >= 3 ? sColor_Gold : sColor_Dark, sTitles[min(stage, 3)]);
    for (side = 0; side < 2; side++)
    {
        s32 dir = side ? -1 : 1;
        s32 x0 = (side ? QF_RX : QF_LX) + dir * 18;         // rand van het plaatje
        s32 xSf = x0 + dir * 14, xF = x0 + dir * 38, xC = 120;

        for (p = 0; p < 4; p++)
        {
            u32 qp = side * 4 + p;
            u8 e = Stadium_GetBracketSlot(q, qp), sf = Stadium_GetBracketSlot(q + 1, qp / 2);
            bool32 won = Decided(sf) && sf == e;

            Line(x0, sQfY[p], xSf, sQfY[p], won ? RED_INK : INK);
        }
        for (p = 0; p < 2; p++)
        {
            u32 sp = side * 2 + p;
            s32 yA = sQfY[p * 2], yB = sQfY[p * 2 + 1], yM = (yA + yB) / 2;
            u8 sf = Stadium_GetBracketSlot(q + 1, sp), f = Stadium_GetBracketSlot(q + 2, sp / 2);
            bool32 topWon = Decided(sf) && sf == Stadium_GetBracketSlot(q, sp * 2);
            bool32 won = Decided(f) && f == sf;

            Line(xSf, yA, xSf, yM, topWon ? RED_INK : INK);
            Line(xSf, yM, xSf, yB, (Decided(sf) && !topWon) ? RED_INK : INK);
            Line(xSf, yM, xF, yM, won ? RED_INK : INK);
        }
        {
            s32 yA = (sQfY[0] + sQfY[1]) / 2, yB = (sQfY[2] + sQfY[3]) / 2, yM = (yA + yB) / 2;
            u8 f = Stadium_GetBracketSlot(q + 2, side);
            bool32 topWon = Decided(f) && f == Stadium_GetBracketSlot(q + 1, side * 2);

            Line(xF, yA, xF, yM, topWon ? RED_INK : INK);
            Line(xF, yM, xF, yB, (Decided(f) && !topWon) ? RED_INK : INK);
            Line(xF, yM, xC, yM, (Decided(champ) && champ == f) ? RED_INK : INK);
        }
    }
    // de acht plaatjes; uitgeschakeld = verbleekt
    for (p = 0; p < 8; p++)
    {
        u8 e = Stadium_GetBracketSlot(q, p);
        s32 cx = p < 4 ? QF_LX : QF_RX, cy = sQfY[p % 4];
        u8 id = AddPic(Stadium_EntrantPic(e), cx, cy, TRUE);

        // fotokadertje om het portret
        FillWindowPixelRect(WIN, PIXEL_FILL(INK), WX(cx - 17), WY(cy - 17), 34, 1);
        FillWindowPixelRect(WIN, PIXEL_FILL(INK), WX(cx - 17), WY(cy + 16), 34, 1);
        FillWindowPixelRect(WIN, PIXEL_FILL(INK), WX(cx - 17), WY(cy - 17), 1, 34);
        FillWindowPixelRect(WIN, PIXEL_FILL(INK), WX(cx + 16), WY(cy - 17), 1, 34);
        u32 r;
        bool32 out = FALSE;

        for (r = q + 1; r <= q + 3; r++)
        {
            u8 v = Stadium_GetBracketSlot(r, p >> (r - q));
            if (!Decided(v))
                break;
            if (v != e)
            {
                out = TRUE;
                break;
            }
        }
        if (id != MAX_SPRITES && out)
            FadePic(gSprites[id].oam.paletteNum, 11, RGB(31, 30, 26));
    }
    // onderaan: jouw volgende wedstrijd of de kampioen
    if (Decided(champ))
    {
        Stadium_GetEntrantName(champ, name);
        PrintCentered(FONT_NORMAL, 112, 128, champ == 0 ? sColor_Red : sColor_Dark, name);
    }
    else
    {
        u32 round = Stadium_GetRound(), n = (1 << Stadium_GetRoundCount()) >> round, pos;
        u8 *s;

        for (pos = 0; pos < n; pos++)
            if (Stadium_GetBracketSlot(round, pos) == 0)
                break;
        s = StringCopy(name, COMPOUND_STRING("Next: you vs "));
        Stadium_GetEntrantName(Stadium_GetBracketSlot(round, pos ^ 1), s);
        PrintCentered(FONT_SMALL_NARROW, 112, 130, sColor_Blue, name);
    }
}

static void DrawBracket(void)
{
    if (Stadium_GetRound() + 3 < Stadium_GetRoundCount())
        DrawMatchCard();
    else
        DrawPaperBracket();
}

// --- compagnons ---------------------------------------------------------------------------------
static const struct Trainer *PartnerData(u32 companion)
{
    u16 id = TRAINER_PARTNER(Stadium_GetCompanion(companion)->partnerId);

    return &gBattlePartners[GetBattlePartnerDifficultyLevel(id)][id - TRAINER_PARTNER(PARTNER_NONE)];
}

static void BuildCompanionList(void)
{
    u32 i;

    sScr->listCount = 0;
    for (i = 0; i < Stadium_CompanionCount(); i++)
        if (Stadium_IsCompanionVisible(i))
            sScr->list[sScr->listCount++] = i;
}

static void DrawCompanionDetail(void)
{
    u32 c = sScr->list[sScr->cursor], i;
    const struct Trainer *t = PartnerData(c);
    bool32 unlocked = Stadium_IsCompanionUnlocked(c);
    const struct StadiumCompanion *sc = Stadium_GetCompanion(c);
    u8 id;

    FreePics();
    id = AddPic(t->trainerPic, 176, 64, FALSE);
    if (id != MAX_SPRITES && !unlocked)
        FadePic(gSprites[id].oam.paletteNum, 16, RGB_BLACK);
    FillWindowPixelRect(WIN, PIXEL_FILL(PAPER), 120, 0, 104, 144);
    if (unlocked)
    {
        PrintCentered(FONT_NORMAL, 176, 104, sColor_Dark, t->trainerName);
        for (i = 0; i < t->partySize && i < 3; i++)
        {
            sScr->icons[sScr->iconCount] = CreateMonIcon(t->party[i].species, SpriteCB_MonIcon, 144 + i * 32, 140, 0, 0);
            gSprites[sScr->icons[sScr->iconCount]].oam.priority = 0;
            sScr->iconCount++;
        }
    }
    else
    {
        PrintCentered(FONT_NORMAL, 176, 104, sColor_Gray, COMPOUND_STRING("???"));
        if (sc->unlockType == STADIUM_UNLOCK_BEAT)
        {
            StringCopy(gStringVar1, GetTrainerNameFromId(sc->unlockValue));
            StringExpandPlaceholders(gStringVar4, COMPOUND_STRING("Beat {STR_VAR_1}\nin the Stadium."));
        }
        else
        {
            StringCopy(gStringVar4, COMPOUND_STRING("Keep battling in\nthe Stadium."));
        }
        PrintCentered(FONT_SMALL_NARROW, 176, 120, sColor_Gray, gStringVar4);
    }
}

static void DrawCompanionList(void)
{
    u32 r, n = sScr->listCount, unlocked = 0;
    u8 buf[24];

    FillWindowPixelRect(WIN, PIXEL_FILL(PAPER), 0, 0, 120, 144);
    for (r = 0; r < n; r++)
        unlocked += Stadium_IsCompanionUnlocked(sScr->list[r]);
    PrintText(FONT_NORMAL, 4, 0, sColor_Dark, COMPOUND_STRING("PARTNERS"));
    ConvertIntToDecimalStringN(buf, unlocked, STR_CONV_MODE_LEFT_ALIGN, 3);
    StringAppend(buf, COMPOUND_STRING("/"));
    ConvertIntToDecimalStringN(buf + StringLength(buf), n, STR_CONV_MODE_LEFT_ALIGN, 3);
    PrintText(FONT_SMALL, 76, 3, sColor_Gray, buf);
    for (r = 0; r < LIST_ROWS && sScr->scroll + r < n; r++)
    {
        u32 i = sScr->list[sScr->scroll + r];
        bool32 open = Stadium_IsCompanionUnlocked(i);

        if (sScr->scroll + r == sScr->cursor)
            PrintText(FONT_SMALL_NARROW, 2, 18 + r * 14, sColor_Red, COMPOUND_STRING("▶"));
        PrintText(FONT_SMALL_NARROW, 10, 18 + r * 14, open ? sColor_Dark : sColor_Gray,
                  open ? PartnerData(i)->trainerName : COMPOUND_STRING("??????"));
    }
}

// --- melding ------------------------------------------------------------------------------------
static void DrawUnlock(void)
{
    const struct Trainer *t = PartnerData(sScr->unlock);

    PrintCentered(FONT_NORMAL, 112, 8, sColor_Gold, COMPOUND_STRING("NEW PARTNER!"));
    AddPic(t->trainerPic, 120, 76, FALSE);
    PrintCentered(FONT_NORMAL, 112, 108, sColor_Dark, t->trainerName);
    PrintCentered(FONT_SMALL_NARROW, 112, 124, sColor_Gray, COMPOUND_STRING("can now team up with you in Doubles."));
}

// --- scherm -------------------------------------------------------------------------------------
static void Redraw(void)
{
    FreePics();
    FillWindowPixelBuffer(WIN, PIXEL_FILL(PAPER));
    switch (sScr->screen)
    {
    case SCREEN_BRACKET:
        DrawBracket();
        break;
    case SCREEN_COMPANIONS:
        DrawCompanionList();
        DrawCompanionDetail();
        break;
    case SCREEN_UNLOCK:
        DrawUnlock();
        break;
    }
    CopyWindowToVram(WIN, COPYWIN_FULL);
}

static void VBlankCB_Stadium(void)
{
    LoadOam();
    ProcessSpriteCopyRequests();
    TransferPlttBuffer();
}

static void CB2_Stadium(void)
{
    RunTasks();
    AnimateSprites();
    BuildOamBuffer();
    RunTextPrinters();
    DoScheduledBgTilemapCopiesToVram();
    UpdatePaletteFade();
}

static void OpenScreen(u32 screen, void (*onDone)(void))
{
    u16 *tilemap;
    u32 x, y;

    sScr = AllocZeroed(sizeof(*sScr));
    sScr->onDone = onDone;
    sScr->screen = screen;

    SetVBlankCallback(NULL);
    ScanlineEffect_Stop();
    ResetPaletteFade();
    ResetSpriteData();
    FreeAllSpritePalettes();
    ResetAllPicSprites();
    ResetTasks();
    ResetVramOamAndBgCntRegs();
    ResetAllBgsCoordinates();
    ResetBgsAndClearDma3BusyFlags(0);
    InitBgsFromTemplates(0, sBgTemplates, ARRAY_COUNT(sBgTemplates));
    SetBgTilemapBuffer(0, AllocZeroed(BG_SCREEN_SIZE));
    InitWindows(sWindowTemplates);
    DeactivateAllTextPrinters();

    tilemap = AllocZeroed(BG_SCREEN_SIZE);
    LoadBgTiles(1, sTableTiles, sizeof(sTableTiles), 0);
    LoadPalette(sTablePal, BG_PLTT_ID(PAL_TABLE), PLTT_SIZE_4BPP);
    for (y = 0; y < 32; y++)
        for (x = 0; x < 32; x++)
            tilemap[y * 32 + x] = ((x * 7 + y * 3) % 5 == 0) | (PAL_TABLE << 12);
    SetBgTilemapBuffer(1, tilemap);
    ScheduleBgCopyTilemapToVram(1);
    LoadPalette(sTextPal, BG_PLTT_ID(PAL_TEXT), PLTT_SIZE_4BPP);
    PutWindowTilemap(WIN);

    LoadMonIconPalettes();
    Redraw();
    ScheduleBgCopyTilemapToVram(0);

    SetGpuReg(REG_OFFSET_DISPCNT, DISPCNT_OBJ_1D_MAP | DISPCNT_OBJ_ON | DISPCNT_BG0_ON | DISPCNT_BG1_ON);
    SetGpuReg(REG_OFFSET_BLDCNT, 0);
    ShowBg(0);
    ShowBg(1);
    BeginNormalPaletteFade(PALETTES_ALL, 0, 16, 0, RGB_BLACK);
    SetVBlankCallback(VBlankCB_Stadium);
    SetMainCallback2(CB2_Stadium);
    CreateTask(Task_StadiumScreen, 0);
}

static void CloseScreen(void)
{
    void (*onDone)(void) = sScr->onDone;

    FreePics();
    FreeMonIconPalettes();
    FreeAllWindowBuffers();
    Free(GetBgTilemapBuffer(0));
    Free(GetBgTilemapBuffer(1));
    Free(sScr);
    sScr = NULL;
    onDone();
}

static void Exit(void)
{
    sScr->exiting = TRUE;
    BeginNormalPaletteFade(PALETTES_ALL, 0, 0, 16, RGB_BLACK);
}

static void Task_StadiumScreen(u8 taskId)
{
    if (gPaletteFade.active)
        return;
    if (sScr->exiting)
    {
        DestroyTask(taskId);
        CloseScreen();
        return;
    }
    switch (sScr->screen)
    {
    case SCREEN_BRACKET:
    case SCREEN_UNLOCK:
        if (JOY_NEW(A_BUTTON | B_BUTTON))
        {
            PlaySE(SE_SELECT);
            Exit();
        }
        break;
    case SCREEN_COMPANIONS:
    {
        u32 n = sScr->listCount, cur = sScr->cursor;

        if (JOY_REPEAT(DPAD_UP) && cur > 0)
            cur--;
        else if (JOY_REPEAT(DPAD_DOWN) && cur + 1 < n)
            cur++;
        else if (JOY_NEW(A_BUTTON))
        {
            if (!Stadium_IsCompanionUnlocked(sScr->list[cur]))
            {
                PlaySE(SE_FAILURE);
                break;
            }
            PlaySE(SE_SELECT);
            Stadium_SetCompanionIndex(sScr->list[cur]);
            gSpecialVar_Result = TRUE;
            Exit();
            break;
        }
        else if (JOY_NEW(B_BUTTON))
        {
            PlaySE(SE_SELECT);
            gSpecialVar_Result = FALSE;
            Exit();
            break;
        }
        if (cur != sScr->cursor)
        {
            PlaySE(SE_SELECT);
            sScr->cursor = cur;
            if (cur < sScr->scroll)
                sScr->scroll = cur;
            else if (cur >= sScr->scroll + LIST_ROWS)
                sScr->scroll = cur - LIST_ROWS + 1;
            Redraw();
        }
        break;
    }
    }
}

// --- specials -----------------------------------------------------------------------------------
static void ReturnToField(void)
{
    SetMainCallback2(CB2_ReturnToFieldContinueScriptPlayMapMusic);
}

void Stadium_ShowNextMatch(void)
{
    CleanupOverworldWindowsAndTilemaps();
    OpenScreen(SCREEN_BRACKET, ReturnToField);
}

void Stadium_ChooseCompanion(void)
{
    u32 i;

    CleanupOverworldWindowsAndTilemaps();
    OpenScreen(SCREEN_COMPANIONS, ReturnToField);
    BuildCompanionList();
    // begin bij de laatst gekozen (of de eerste die vrij is)
    sScr->cursor = 0;
    for (i = 0; i < sScr->listCount; i++)
    {
        if (sScr->list[i] == STADIUM_SAVE.lastCompanion && Stadium_IsCompanionUnlocked(sScr->list[i]))
        {
            sScr->cursor = i;
            break;
        }
    }
    if (i == sScr->listCount)
        for (i = 0; i < sScr->listCount && !Stadium_IsCompanionUnlocked(sScr->list[i]); i++)
            sScr->cursor = i + 1;
    if (sScr->cursor >= sScr->listCount)
        sScr->cursor = 0;
    sScr->scroll = sScr->cursor >= LIST_ROWS ? sScr->cursor - LIST_ROWS + 1 : 0;
    Redraw();
}

static void NextUnlock(void)
{
    u8 c = Stadium_TakeNewUnlock();

    if (c == 0xFF)
    {
        ReturnToField();
        return;
    }
    OpenScreen(SCREEN_UNLOCK, NextUnlock);
    sScr->unlock = c;
    PlayFanfare(MUS_LEVEL_UP);
    Redraw();
}

// Alle nieuwe compagnons één voor één tonen (het script vraagt eerst Stadium_HasNewUnlocks)
void Stadium_ShowUnlocks(void)
{
    u8 c = Stadium_TakeNewUnlock();

    CleanupOverworldWindowsAndTilemaps();
    OpenScreen(SCREEN_UNLOCK, NextUnlock);
    sScr->unlock = c;
    PlayFanfare(MUS_LEVEL_UP);
    Redraw();
}
