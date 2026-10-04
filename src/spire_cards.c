// Project Grounded: The Spire - kaartenscherm (zie SPIRE_DESIGN.md en tools/grounded/spire/mockups.py).
// Eén scherm voor alles met "kies een van drie": moves na een gevecht, relics, de draft van rentals,
// de rustplek, de winkel en events. Plus een simpel berichtscherm (einde run, nieuwe act).
// Stijl: torenstenen op de achtergrond, kaarten in kaders, rode rand om de gekozen kaart, de PC-hand.
#include "global.h"
#include "battle.h"
#include "battle_main.h"
#include "bg.h"
#include "decompress.h"
#include "gpu_regs.h"
#include "graphics.h"
#include "item.h"
#include "item_icon.h"
#include "main.h"
#include "malloc.h"
#include "menu.h"
#include "menu_helpers.h"
#include "move.h"
#include "palette.h"
#include "pokemon.h"
#include "pokemon_icon.h"
#include "pokemon_summary_screen.h"
#include "random.h"
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
#include "constants/items.h"
#include "constants/moves.h"
#include "constants/rgb.h"
#include "constants/songs.h"
#include "constants/species.h"

#define RUN SPIRE_SAVE

enum
{
    WIN_HEADER,
    WIN_CARD_0,
    WIN_CARD_1,
    WIN_CARD_2,
    WIN_BOTTOM,
    WIN_COUNT,
};

enum
{
    CARD_NONE,
    CARD_MOVE,
    CARD_MON,
    CARD_RELIC,
    CARD_OPTION,
    CARD_ITEM,      // vasthouditem (winkel, events)
};

// opties (rust, winkel, events)
enum
{
    OPT_REST,
    OPT_EVOLVE_0,
    OPT_EVOLVE_1,
    OPT_POTION,
    OPT_EV_SAMPLE,
    OPT_EV_STEAL,
    OPT_EV_LEAVE,
    OPT_EV_READ,
    OPT_EV_GRAMMAR,
    OPT_EV_ACCEPT,
    OPT_EV_RUDE,
    OPT_RELEARN,
    OPT_EV_DITTO_TAKE,
    OPT_EV_SHROOM_FEW,
    OPT_EV_SHROOM_MANY,
    OPT_EV_SPIKES_WALK,
    OPT_EV_SPIKES_AROUND,
    OPT_EV_DELETER_LET,
    OPT_EV_DELETER_TIP,
    OPT_EV_TUTOR_CHEAP,
    OPT_EV_TUTOR_DEAR,
    OPT_EV_LUNCH_BERRY,
    OPT_EV_LUNCH_CANDY,
    OPT_EV_LUNCH_BOX,
    OPT_EV_CHEST_TAKE,
    OPT_EV_JOY_HEAL,
    OPT_EV_JOY_UPGRADE,
    OPT_EV_WHEEL_SPIN,
    OPT_EV_ACE_SEARCH,
    OPT_EV_GLITCH_ENTER,
    OPT_EV_CANDLE_OFFER,
    OPT_EV_RECRUIT,
};

enum
{
    STATE_CARDS,
    STATE_CHOOSE_MON,
    STATE_CHOOSE_SLOT,
    STATE_MESSAGE,
    STATE_RELEARN,      // Move Relearner: kies een move uit de leerset
    STATE_EXIT,
};

#define MAX_CARDS       6   // winkel: twee schappen van drie
#define CARDS_PER_PAGE  3
#define MAX_RELEARN     40

#define FRAME_TILE    0x200
#define BRICK_TILE    0x000
#define PAL_BRICKS    12
#define PAL_FRAME_SEL 13
#define PAL_FRAME     14
#define PAL_TEXT      15
#define TAG_HAND      0x5301
#define TAG_ITEM      0x5310

struct SpireCard
{
    u8 kind;
    u8 rarity;      // 0 common, 1 uncommon, 2 rare
    u8 sold:1;
    u16 value;      // move, soort, relic of optie
    u16 price;      // winkel; 0 = gratis
};

struct SpireCards
{
    void (*onDone)(void);
    const u8 *title;
    const u8 *text;
    struct SpireCard cards[MAX_CARDS];
    u8 count;
    u8 page;
    u8 relearnCount;
    u8 relearnCursor;
    u8 relearnPaid;     // 1 = deze teach is een Move Relearner (betalen bij het leren)
    u16 giveItem;       // vasthouditem dat een Pokémon krijgt (STATE_CHOOSE_MON)
    u16 replaceSpecies; // events: deze Pokémon vervangt een rental (STATE_CHOOSE_MON); SPECIES_DITTO = de speciale Ditto
    u16 recruitSpecies; // event 'A STRONG STRANGER'
    u16 relearnMoves[MAX_RELEARN];
    u8 mode;
    u8 state;
    u8 card;
    u8 mon;
    u8 slot;
    u8 afterMessage;        // 0 = klaar, 1 = terug naar de kaarten
    u8 event;
    u16 teachMove;
    u8 handSpriteId;
    u8 iconSpriteIds[2];
    u8 cardSpriteIds[CARDS_PER_PAGE][3];
    u8 bob;
    u8 message[160];
};

static EWRAM_DATA struct SpireCards *sCards = NULL;

// --- graphics ---------------------------------------------------------------------------------
static const u16 sHandCursor_Pal[] = INCBIN_U16("graphics/pokemon_storage/hand_cursor.gbapal");
static const u8 sHandCursor_Gfx[] = INCBIN_U8("graphics/pokemon_storage/hand_cursor.4bpp");

// stenen: twee tegels, 16x8 per steen, verspringend per rij (index 1 = steen, 2 = voeg)
static const u32 sBrickTiles[2][8] =
{
    {0x11111112, 0x11111112, 0x11111112, 0x11111112, 0x11111112, 0x11111112, 0x11111112, 0x22222222},
    {0x11111111, 0x11111111, 0x11111111, 0x11111111, 0x11111111, 0x11111111, 0x11111111, 0x22222222},
};
static const u16 sBrickPal[16] = {RGB(5, 4, 9), RGB(5, 4, 9), RGB(8, 7, 14)};

// tekstpalet: 1 wit, 2 donker, 3 schaduw, 4/5 blauw, 6/7 goud, 8 grijs, 9/10 groen, 11/12 rood, 13 balk
static const u16 sTextPal[16] =
{
    RGB(31, 31, 31), RGB(31, 31, 31), RGB(8, 8, 9), RGB(26, 26, 27),
    RGB(5, 15, 29), RGB(23, 27, 31), RGB(25, 17, 1), RGB(31, 27, 17),
    RGB(19, 19, 20), RGB(5, 19, 9), RGB(22, 29, 23), RGB(29, 8, 7),
    RGB(31, 24, 23), RGB(10, 10, 11), RGB(15, 9, 22), RGB(26, 22, 30),
};

static const u8 sColor_Dark[]   = {1, 2, 3};
static const u8 sColor_Blue[]   = {1, 4, 5};
static const u8 sColor_Gold[]   = {1, 6, 7};
static const u8 sColor_Gray[]   = {1, 8, 3};
static const u8 sColor_Green[]  = {1, 9, 10};
static const u8 sColor_Red[]    = {1, 11, 12};
static const u8 sColor_Purple[] = {1, 14, 15};
static const u8 sColor_DarkT[]  = {TEXT_COLOR_TRANSPARENT, 2, 3};
static const u8 sColor_RedT[]   = {TEXT_COLOR_TRANSPARENT, 11, 12};
static const u8 sColor_GrayT[]  = {TEXT_COLOR_TRANSPARENT, 8, 3};

static const u8 sRarityBarColor[] = {8, 4, 6};
static const u8 *const sRarityTextColor[] = {sColor_Gray, sColor_Blue, sColor_Gold};
static const u8 sText_Common[] = _("COMMON");
static const u8 sText_Uncommon[] = _("UNCOMMON");
static const u8 sText_Rare[] = _("RARE");
static const u8 *const sRarityName[] = {sText_Common, sText_Uncommon, sText_Rare};
static const u8 sText_Phys[] = _("Phys.");
static const u8 sText_Spec[] = _("Spec.");
static const u8 sText_Status[] = _("Stat.");

static const struct BgTemplate sBgTemplates[] =
{
    {.bg = 0, .charBaseIndex = 0, .mapBaseIndex = 31, .priority = 1},
    {.bg = 1, .charBaseIndex = 2, .mapBaseIndex = 30, .priority = 3},
};

static const struct WindowTemplate sWindowTemplates[] =
{
    [WIN_HEADER] = {.bg = 0, .tilemapLeft = 1, .tilemapTop = 1, .width = 28, .height = 2, .paletteNum = PAL_TEXT, .baseBlock = 0x001},
    [WIN_CARD_0] = {.bg = 0, .tilemapLeft = 1, .tilemapTop = 5, .width = 8, .height = 6, .paletteNum = PAL_TEXT, .baseBlock = 0x039},
    [WIN_CARD_1] = {.bg = 0, .tilemapLeft = 11, .tilemapTop = 5, .width = 8, .height = 6, .paletteNum = PAL_TEXT, .baseBlock = 0x069},
    [WIN_CARD_2] = {.bg = 0, .tilemapLeft = 21, .tilemapTop = 5, .width = 8, .height = 6, .paletteNum = PAL_TEXT, .baseBlock = 0x099},
    [WIN_BOTTOM] = {.bg = 0, .tilemapLeft = 1, .tilemapTop = 13, .width = 28, .height = 6, .paletteNum = PAL_TEXT, .baseBlock = 0x0C9},
    DUMMY_WIN_TEMPLATE,
};

static const struct OamData sOam_Hand = {.shape = SPRITE_SHAPE(32x32), .size = SPRITE_SIZE(32x32), .priority = 0};
static const struct SpriteSheet sSpriteSheet_Hand = {sHandCursor_Gfx, 0x200, TAG_HAND};
static const struct SpritePalette sSpritePal_Hand = {sHandCursor_Pal, TAG_HAND};
static void SpriteCB_Hand(struct Sprite *sprite);
static const struct SpriteTemplate sSpriteTemplate_Hand =
{
    .tileTag = TAG_HAND, .paletteTag = TAG_HAND, .oam = &sOam_Hand, .anims = gDummySpriteAnimTable,
    .images = NULL, .affineAnims = gDummySpriteAffineAnimTable, .callback = SpriteCB_Hand,
};

static void CB2_SpireCards(void);
static void Task_SpireCards(u8 taskId);
static void Redraw(void);

// --- events (placeholders; Jordi herschrijft) --------------------------------------------------
struct SpireEvent
{
    const u8 *title;
    const u8 *story;
    u8 options[3];
};

// Events: Jordi's ideeën (speciale Ditto, paddenstoelenpad, Toxic Spikes, smerige Move Deleter, move tutor),
// Slay the Spire 1/2 in Pokémon-vorm (Big Fish, Golden Idol, Cleric, Wheel of Change, Dead Adventurer, Shining Light,
// Bonfire Spirits) en eigen ideeën. Sommige zijn bewust gemeen. Elk event één keer per run.
static const struct SpireEvent sEvents[] =
{
    {COMPOUND_STRING("A VERY SPECIAL DITTO"), COMPOUND_STRING("A shiny Ditto. Perfect genes, a Choice Scarf and\nImposter. It wants in. It knows it is worth it."),
     {OPT_EV_DITTO_TAKE, OPT_EV_LEAVE, OPT_EV_LEAVE}},
    {COMPOUND_STRING("MUSHROOM PATH"), COMPOUND_STRING("Berries grow between the mushrooms. The further\nyou reach, the more spores you breathe."),
     {OPT_EV_SHROOM_FEW, OPT_EV_SHROOM_MANY, OPT_EV_LEAVE}},
    {COMPOUND_STRING("A FLOOR OF SPIKES"), COMPOUND_STRING("Toxic Spikes, wall to wall. Someone dropped a\nwallet in the middle. Of course they did."),
     {OPT_EV_SPIKES_WALK, OPT_EV_SPIKES_AROUND, OPT_EV_LEAVE}},
    {COMPOUND_STRING("THE MOVE DELETER"), COMPOUND_STRING("A man in a trench coat offers to clean up your\nmoves. He does not say which. He smells of glue."),
     {OPT_EV_DELETER_LET, OPT_EV_DELETER_TIP, OPT_EV_LEAVE}},
    {COMPOUND_STRING("MOVE TUTOR"), COMPOUND_STRING("A tutor sits behind a desk in the stairwell.\nPayment upfront. Refunds never."),
     {OPT_EV_TUTOR_CHEAP, OPT_EV_TUTOR_DEAR, OPT_EV_LEAVE}},
    {COMPOUND_STRING("SNORLAX'S LUNCH"), COMPOUND_STRING("A sleeping Snorlax guards its lunch. You can\ntake one thing before it wakes up."),
     {OPT_EV_LUNCH_BERRY, OPT_EV_LUNCH_CANDY, OPT_EV_LUNCH_BOX}},
    {COMPOUND_STRING("GIMMIGHOUL'S CHEST"), COMPOUND_STRING("A chest full of coins. One of the coins is\nlooking at you."),
     {OPT_EV_CHEST_TAKE, OPT_EV_LEAVE, OPT_EV_LEAVE}},
    {COMPOUND_STRING("NURSE ON A BREAK"), COMPOUND_STRING("Nurse Joy's cousin is on her lunch break.\nShe will help, for a fee. A big fee."),
     {OPT_EV_JOY_HEAL, OPT_EV_JOY_UPGRADE, OPT_EV_LEAVE}},
    {COMPOUND_STRING("SPINDA'S WHEEL"), COMPOUND_STRING("A Spinda spins a prize wheel. It is very dizzy.\nSo is the wheel."),
     {OPT_EV_WHEEL_SPIN, OPT_EV_LEAVE, OPT_EV_LEAVE}},
    {COMPOUND_STRING("A FAINTED ACE"), COMPOUND_STRING("An Ace Trainer lies fainted on the stairs. Her\nbag is open. Her partner is only sleeping."),
     {OPT_EV_ACE_SEARCH, OPT_EV_LEAVE, OPT_EV_LEAVE}},
    {COMPOUND_STRING("A GLITCH IN THE WALL"), COMPOUND_STRING("A Porygon-Z hums inside a crack of light.\nStep in and your moves get rewritten. Painfully."),
     {OPT_EV_GLITCH_ENTER, OPT_EV_LEAVE, OPT_EV_LEAVE}},
    {COMPOUND_STRING("LITWICK'S CANDLE"), COMPOUND_STRING("A Litwick offers warmth. It only asks for a\nmemory. A move, to be exact."),
     {OPT_EV_CANDLE_OFFER, OPT_EV_LEAVE, OPT_EV_LEAVE}},
    {COMPOUND_STRING("A STRONG STRANGER"), COMPOUND_STRING("A wild Pokémon blocks the stairs. It is strong.\nIt wants a fight, or a team."),
     {OPT_EV_RECRUIT, OPT_EV_LEAVE, OPT_EV_LEAVE}},
    {COMPOUND_STRING("FREE SAMPLES"), COMPOUND_STRING("A Meowth runs a free sample stand.\nIt is suspiciously free."),
     {OPT_EV_SAMPLE, OPT_EV_STEAL, OPT_EV_LEAVE}},
    {COMPOUND_STRING("WRITING ON THE WALL"), COMPOUND_STRING("An Unown spells out a word on the wall.\nIt is an insult. About you."),
     {OPT_EV_READ, OPT_EV_GRAMMAR, OPT_EV_LEAVE}},
    {COMPOUND_STRING("A HELPFUL HIKER"), COMPOUND_STRING("A Hiker offers to carry your team\nup a floor. He insists. Loudly."),
     {OPT_EV_ACCEPT, OPT_EV_RUDE, OPT_EV_LEAVE}},
};

struct SpireOption
{
    const u8 *name;
    const u8 *line1;
    const u8 *line2;
    const u8 *desc;
    u16 iconSpecies;
};

static const struct SpireOption sOptions[] =
{
    [OPT_REST]       = {COMPOUND_STRING("Rest"), COMPOUND_STRING("Heal HP"), COMPOUND_STRING("and all PP"), COMPOUND_STRING("Chansey patches your team up.\nNo questions. No insurance."), SPECIES_CHANSEY},
    [OPT_EVOLVE_0]   = {COMPOUND_STRING("Evolve"), COMPOUND_STRING("your first"), COMPOUND_STRING("Pokémon"), COMPOUND_STRING("Evolve now. Stronger, bigger,\nslightly more opinionated."), SPECIES_NONE},
    [OPT_EVOLVE_1]   = {COMPOUND_STRING("Evolve"), COMPOUND_STRING("your second"), COMPOUND_STRING("Pokémon"), COMPOUND_STRING("Evolve now. Stronger, bigger,\nslightly more opinionated."), SPECIES_NONE},
    [OPT_POTION]     = {COMPOUND_STRING("Potion"), COMPOUND_STRING("Heal both"), COMPOUND_STRING("for 30%"), COMPOUND_STRING("A Potion for the whole team.\nShaken, not stirred."), SPECIES_NONE},
    [OPT_EV_SAMPLE]  = {COMPOUND_STRING("Taste it"), COMPOUND_STRING("Heal 30%"), COMPOUND_STRING("...or not"), COMPOUND_STRING("Probably food. Probably."), SPECIES_NONE},
    [OPT_EV_STEAL]   = {COMPOUND_STRING("Steal it"), COMPOUND_STRING("+40 ¥"), COMPOUND_STRING("-15% HP"), COMPOUND_STRING("Meowth counts its coins.\nAll of them. Twice."), SPECIES_NONE},
    [OPT_EV_LEAVE]   = {COMPOUND_STRING("Leave"), COMPOUND_STRING("Nothing"), COMPOUND_STRING("happens"), COMPOUND_STRING("The safest choice.\nThe tower judges you for it."), SPECIES_NONE},
    [OPT_EV_READ]    = {COMPOUND_STRING("Read it"), COMPOUND_STRING("Learn a"), COMPOUND_STRING("rare move"), COMPOUND_STRING("Say the word out loud.\nSomething answers."), SPECIES_NONE},
    [OPT_EV_GRAMMAR] = {COMPOUND_STRING("Correct it"), COMPOUND_STRING("+30 ¥"), COMPOUND_STRING(""), COMPOUND_STRING("Fix the spelling. The Unown\npays you to go away."), SPECIES_NONE},
    [OPT_EV_DITTO_TAKE]    = {COMPOUND_STRING("Take it"), COMPOUND_STRING("Replaces"), COMPOUND_STRING("a Pokémon"), COMPOUND_STRING("It transforms into a foe at the start\nof every battle. Your choice who leaves."), SPECIES_DITTO},
    [OPT_EV_SHROOM_FEW]    = {COMPOUND_STRING("Reach a bit"), COMPOUND_STRING("1 berry"), COMPOUND_STRING("25% spores"), COMPOUND_STRING("One berry for one Pokémon. Spores put\nit to sleep at the start of the next battle."), SPECIES_NONE},
    [OPT_EV_SHROOM_MANY]   = {COMPOUND_STRING("Reach deep"), COMPOUND_STRING("2 berries"), COMPOUND_STRING("70% spores"), COMPOUND_STRING("A berry for both. Very likely a nap\nin the next battle. For one of them. Or both."), SPECIES_NONE},
    [OPT_EV_SPIKES_WALK]   = {COMPOUND_STRING("Walk on"), COMPOUND_STRING("+90 ¥"), COMPOUND_STRING("spikes x3"), COMPOUND_STRING("Next 3 battles: 40% to start poisoned.\nPoison, Steel and Heavy-Duty Boots: safe."), SPECIES_NONE},
    [OPT_EV_SPIKES_AROUND] = {COMPOUND_STRING("Climb around"), COMPOUND_STRING("-12% HP"), COMPOUND_STRING(""), COMPOUND_STRING("Along the outside wall. Slow, windy,\nand nobody is poisoned. Probably."), SPECIES_NONE},
    [OPT_EV_DELETER_LET]   = {COMPOUND_STRING("Let him"), COMPOUND_STRING("+110 ¥"), COMPOUND_STRING("lose a move"), COMPOUND_STRING("He erases a random move of a random\nPokémon and pays you for the privilege."), SPECIES_NONE},
    [OPT_EV_DELETER_TIP]   = {COMPOUND_STRING("Tip him"), COMPOUND_STRING("-40 ¥"), COMPOUND_STRING("a move +"), COMPOUND_STRING("For a tip he polishes a random move\ninstead. 1 in 4 he deletes it anyway."), SPECIES_NONE},
    [OPT_EV_TUTOR_CHEAP]   = {COMPOUND_STRING("Lesson"), COMPOUND_STRING("-45 ¥"), COMPOUND_STRING("uncommon"), COMPOUND_STRING("An uncommon move of one of your types.\nHe picks which. You pick who learns it."), SPECIES_NONE},
    [OPT_EV_TUTOR_DEAR]    = {COMPOUND_STRING("Masterclass"), COMPOUND_STRING("-100 ¥"), COMPOUND_STRING("rare move"), COMPOUND_STRING("A rare move. He insists it is worth it.\nHe is usually right."), SPECIES_NONE},
    [OPT_EV_LUNCH_BERRY]   = {COMPOUND_STRING("Oran Berry"), COMPOUND_STRING("Heal 30%"), COMPOUND_STRING(""), COMPOUND_STRING("A big Oran Berry. Snorlax will not\nmiss it. It will miss it a lot."), SPECIES_NONE},
    [OPT_EV_LUNCH_CANDY]   = {COMPOUND_STRING("Rare Candy"), COMPOUND_STRING("+5% max HP"), COMPOUND_STRING("both"), COMPOUND_STRING("They are already level 100. It still\nhelps. Do not think about it too hard."), SPECIES_NONE},
    [OPT_EV_LUNCH_BOX]     = {COMPOUND_STRING("Lunch box"), COMPOUND_STRING("A relic"), COMPOUND_STRING("-8% max HP"), COMPOUND_STRING("Something good inside. Snorlax wakes\nup and sits on someone. Permanently."), SPECIES_NONE},
    [OPT_EV_CHEST_TAKE]    = {COMPOUND_STRING("Grab coins"), COMPOUND_STRING("+130 ¥"), COMPOUND_STRING("50% -20% HP"), COMPOUND_STRING("Coins are coins. Unless they are\nGimmighoul. Then they bite."), SPECIES_NONE},
    [OPT_EV_JOY_HEAL]      = {COMPOUND_STRING("Heal"), COMPOUND_STRING("-40 ¥"), COMPOUND_STRING("Heal 40%"), COMPOUND_STRING("A quick patch-up between bites of\nher sandwich."), SPECIES_CHANSEY},
    [OPT_EV_JOY_UPGRADE]   = {COMPOUND_STRING("Special"), COMPOUND_STRING("-75 ¥"), COMPOUND_STRING("a move +"), COMPOUND_STRING("She knows a Porygon2. It upgrades a\nrandom move. No questions asked."), SPECIES_PORYGON2},
    [OPT_EV_WHEEL_SPIN]    = {COMPOUND_STRING("Spin it"), COMPOUND_STRING("Anything"), COMPOUND_STRING("can happen"), COMPOUND_STRING("Gold, a relic, a full heal, a fresh move,\nor a slap. Spinda does not know either."), SPECIES_SPINDA},
    [OPT_EV_ACE_SEARCH]    = {COMPOUND_STRING("Search bag"), COMPOUND_STRING("Loot"), COMPOUND_STRING("or a fight"), COMPOUND_STRING("Half the time: money and an item. The\nother half: her partner wakes up. Elite."), SPECIES_NONE},
    [OPT_EV_GLITCH_ENTER]  = {COMPOUND_STRING("Step in"), COMPOUND_STRING("2 moves +"), COMPOUND_STRING("-20% HP"), COMPOUND_STRING("Two random moves get upgraded. Your\nteam gets rewritten too, a bit."), SPECIES_PORYGON_Z},
    [OPT_EV_CANDLE_OFFER]  = {COMPOUND_STRING("Offer"), COMPOUND_STRING("lose a move"), COMPOUND_STRING("full heal"), COMPOUND_STRING("A random move burns away. Your team\nis fully healed in the warmth."), SPECIES_LITWICK},
    [OPT_EV_RECRUIT]       = {COMPOUND_STRING("Recruit"), COMPOUND_STRING("-25% HP"), COMPOUND_STRING("join team"), COMPOUND_STRING("Earn its respect the hard way. It\nreplaces one of your Pokémon."), SPECIES_NONE},
    [OPT_EV_ACCEPT]  = {COMPOUND_STRING("Accept"), COMPOUND_STRING("Heal 25%"), COMPOUND_STRING(""), COMPOUND_STRING("Being carried is undignified.\nAlso very relaxing."), SPECIES_NONE},
    [OPT_RELEARN]    = {COMPOUND_STRING("Relearner"), COMPOUND_STRING("Relearn"), COMPOUND_STRING("any move"), COMPOUND_STRING("The Move Relearner takes a fee and\nteaches a move from the Pokémon's own list."), SPECIES_NONE},
    [OPT_EV_RUDE]    = {COMPOUND_STRING("Refuse"), COMPOUND_STRING("+2 BP"), COMPOUND_STRING(""), COMPOUND_STRING("He respects your rudeness.\nHikers are like that."), SPECIES_NONE},
};

// --- helpers ----------------------------------------------------------------------------------
// Altijd met transparante achtergrond (het venster is al gevuld): anders wist elke regel de onderkant
// van de regel erboven.
static void PrintText(u32 win, u32 font, u32 x, u32 y, const u8 *color, const u8 *str)
{
    u8 c[3] = {TEXT_COLOR_TRANSPARENT, color[1], color[2]};

    AddTextPrinterParameterized3(win, font, x, y, c, TEXT_SKIP_DRAW, str);
}

static void PrintCentered(u32 win, u32 font, u32 y, u32 width, const u8 *color, const u8 *str)
{
    s32 x;

    if (font == FONT_SMALL_NARROW && GetStringWidth(font, str, 0) > (s32)width - 2)
        font = FONT_SMALL_NARROWER; // lange namen (Heavy-Duty Boots)
    x = (width - GetStringWidth(font, str, 0)) / 2;
    PrintText(win, font, x < 0 ? 0 : x, y, color, str);
}

// Itembeschrijvingen uit de game zijn drie smalle regels; hier passen er twee brede (max 220 px).
static const u8 *Reflow(const u8 *src)
{
    u8 *dst = gStringVar4, *lineStart = gStringVar4, *lastSpace = NULL;
    u32 lines = 0;

    while (*src != EOS && dst < gStringVar4 + 200)
    {
        u8 ch = (*src == CHAR_NEWLINE) ? CHAR_SPACE : *src;

        src++;
        *dst = ch;
        dst[1] = EOS;
        if (ch == CHAR_SPACE)
            lastSpace = dst;
        if (GetStringWidth(FONT_SMALL_NARROW, lineStart, 0) > 220 && lastSpace != NULL && lines == 0)
        {
            *lastSpace = CHAR_NEWLINE;
            lineStart = lastSpace + 1;
            lastSpace = NULL;
            lines++;
        }
        dst++;
    }
    *dst = EOS;
    return gStringVar4;
}

static bool32 MonKnowsMove(struct Pokemon *mon, u32 move)
{
    u32 i;

    for (i = 0; i < MAX_MON_MOVES; i++)
        if (GetMonData(mon, MON_DATA_MOVE1 + i) == move)
            return TRUE;
    return FALSE;
}

static bool32 IsStab(struct Pokemon *mon, u32 move)
{
    u32 species = GetMonData(mon, MON_DATA_SPECIES);
    enum Type type = GetMoveType(move);

    return !IsBattleMoveStatus(move) && (GetSpeciesType(species, 0) == type || GetSpeciesType(species, 1) == type);
}

static bool32 IsSecondDraft(void)
{
    return GetMonData(&RUN.mons[0], MON_DATA_SPECIES) != SPECIES_NONE;
}

static bool32 CardTaken(u32 n, u32 kind, u32 value)
{
    u32 j;

    for (j = 0; j < n; j++)
        if (sCards->cards[j].kind == kind && sCards->cards[j].value == value)
            return TRUE;
    return FALSE;
}

// prijzen (zie SPIRE_BALANS.md): ±7 gevechten + 1,5 elite + baas = ±280¥ per act
static const u16 sMovePrice[] = {45, 70, 120};
static const u16 sItemPrice[] = {50, 85, 140};

static void AddMoveCard(u32 i, s32 forceRarity)
{
    struct SpireCard *c = &sCards->cards[i];
    u32 tries = 0;

    c->kind = CARD_MOVE;
    do
    {
        u32 roll = Random() % 100;

        u32 type = TYPE_NONE;

        if (forceRarity >= 0)
            c->rarity = forceRarity;
        else
            c->rarity = roll < 10 ? 2 : roll < 40 ? 1 : 0;
        if (i < 2 && sCards->mode == SPIRE_CARDS_MOVES)
        {
            u16 species = GetMonData(&RUN.mons[i], MON_DATA_SPECIES);
            type = GetSpeciesType(species, (Random() & 1) ? 1 : 0);
        }
        c->value = Spire_RandomMoveOfType(c->rarity, type, i + tries);
    } while (CardTaken(i, CARD_MOVE, c->value) && ++tries < 20);
}

static void BuildCards(void)
{
    u32 i;

    memset(sCards->cards, 0, sizeof(sCards->cards));
    sCards->count = 3;
    switch (sCards->mode)
    {
    case SPIRE_CARDS_MOVES:
        // kaart 1 past bij je eerste Pokémon, kaart 2 bij je tweede, kaart 3 is willekeurig (zoals klassekaarten in Slay)
        for (i = 0; i < 3; i++)
            AddMoveCard(i, -1);
        break;
    case SPIRE_CARDS_RELICS:
        sCards->count = 0;
        for (i = 0; i < 3; i++)
        {
            u32 relic, tries = 0;

            do
                relic = Spire_RandomNewRelic(i * 3 + tries);
            while (relic < SPIRE_RELIC_COUNT && CardTaken(sCards->count, CARD_RELIC, relic) && ++tries < 20);
            if (relic >= SPIRE_RELIC_COUNT || CardTaken(sCards->count, CARD_RELIC, relic))
                break;
            sCards->cards[sCards->count].kind = CARD_RELIC;
            sCards->cards[sCards->count].value = relic;
            sCards->cards[sCards->count].rarity = 2;
            sCards->count++;
        }
        break;
    case SPIRE_CARDS_DRAFT:
        for (i = 0; i < 3; i++)
        {
            u32 tries = 0;
            u16 species;

            do
                species = Spire_RandomRental(i + tries * 3);
            while ((CardTaken(i, CARD_MON, species) || (IsSecondDraft() && GetMonData(&RUN.mons[0], MON_DATA_SPECIES) == species))
                && ++tries < 30);
            sCards->cards[i].kind = CARD_MON;
            sCards->cards[i].value = species;
        }
        break;
    case SPIRE_CARDS_REST:
        sCards->count = 1;
        sCards->cards[0].kind = CARD_OPTION;
        sCards->cards[0].value = OPT_REST;
        for (i = 0; i < 2; i++)
        {
            if (Spire_CanEvolve(i))
            {
                sCards->cards[sCards->count].kind = CARD_OPTION;
                sCards->cards[sCards->count].value = OPT_EVOLVE_0 + i;
                sCards->count++;
            }
        }
        break;
    case SPIRE_CARDS_SHOP:
        // schap 1: twee moves en een relic; schap 2: twee vasthouditems en de Move Relearner (altijd)
        sCards->count = MAX_CARDS;
        AddMoveCard(0, 1);
        AddMoveCard(1, 1 + (Random() % 3 == 0));
        for (i = 0; i < 2; i++)
            sCards->cards[i].price = sMovePrice[sCards->cards[i].rarity];
        sCards->cards[2].kind = CARD_RELIC;
        sCards->cards[2].value = Spire_RandomNewRelic(0);
        sCards->cards[2].rarity = 2;
        sCards->cards[2].price = 120;
        if (sCards->cards[2].value >= SPIRE_RELIC_COUNT)
        {
            AddMoveCard(2, 2);
            sCards->cards[2].price = sMovePrice[2];
        }
        for (i = 3; i < 5; i++)
        {
            u32 roll = Random() % 100, tries = 0;

            sCards->cards[i].kind = CARD_ITEM;
            sCards->cards[i].rarity = roll < 10 ? 2 : roll < 45 ? 1 : 0;
            do
                sCards->cards[i].value = Spire_RandomHeldItem(sCards->cards[i].rarity, i + tries * 5);
            while (i == 4 && sCards->cards[4].value == sCards->cards[3].value && ++tries < 10);
            sCards->cards[i].price = sItemPrice[sCards->cards[i].rarity];
        }
        sCards->cards[5].kind = CARD_OPTION;
        sCards->cards[5].value = OPT_RELEARN;
        sCards->cards[5].price = 50 + 25 * RUN.relearns;
        break;
    case SPIRE_CARDS_EVOLVE:
    {
        u16 targets[3];

        sCards->count = Spire_GetEvolutions(GetMonData(&RUN.mons[gSpireEvolveMon], MON_DATA_SPECIES), targets);
        for (i = 0; i < sCards->count; i++)
        {
            sCards->cards[i].kind = CARD_MON;
            sCards->cards[i].value = targets[i];
        }
        break;
    }
    case SPIRE_CARDS_EVENT:
    {
        u32 n = 0, pick;

        for (i = 0; i < ARRAY_COUNT(sEvents); i++)
            if (!(RUN.eventsSeen & (1u << i)))
                n++;
        if (n == 0)
        {
            RUN.eventsSeen = 0;
            n = ARRAY_COUNT(sEvents);
        }
        pick = Random() % n;
        for (i = 0; i < ARRAY_COUNT(sEvents); i++)
            if (!(RUN.eventsSeen & (1u << i)) && pick-- == 0)
                break;
        sCards->event = i;
        RUN.eventsSeen |= 1u << i;
        sCards->recruitSpecies = Spire_RandomEventRental(Random());
        // dubbele 'Leave' achteraan telt niet mee
        sCards->count = (sEvents[sCards->event].options[2] == sEvents[sCards->event].options[1]) ? 2 : 3;
        for (i = 0; i < sCards->count; i++)
        {
            sCards->cards[i].kind = CARD_OPTION;
            sCards->cards[i].value = sEvents[sCards->event].options[i];
        }
        break;
    }
    default:
        sCards->count = 0;
        break;
    }
}

// --- tekenen ----------------------------------------------------------------------------------
static void DrawHeader(void)
{
    u8 buf[32];
    u32 x;

    FillWindowPixelBuffer(WIN_HEADER, PIXEL_FILL(1));
    switch (sCards->mode)
    {
    case SPIRE_CARDS_MOVES:
    case SPIRE_CARDS_RELICS:
        PrintText(WIN_HEADER, FONT_NORMAL, 4, 1, sColor_Dark, sCards->mode == SPIRE_CARDS_MOVES ? COMPOUND_STRING("VICTORY!") : COMPOUND_STRING("TREASURE!"));
        x = 96;
        buf[0] = CHAR_PLUS;
        ConvertIntToDecimalStringN(buf + 1, gSpireResult.bp, STR_CONV_MODE_LEFT_ALIGN, 3);
        StringAppend(buf, COMPOUND_STRING(" BP"));
        PrintText(WIN_HEADER, FONT_NORMAL, x, 1, sColor_Blue, buf);
        x += GetStringWidth(FONT_NORMAL, buf, 0) + 8;
        buf[0] = CHAR_PLUS;
        ConvertIntToDecimalStringN(buf + 1, gSpireResult.gold, STR_CONV_MODE_LEFT_ALIGN, 3);
        StringAppend(buf, COMPOUND_STRING("¥"));
        PrintText(WIN_HEADER, FONT_NORMAL, x, 1, sColor_Gold, buf);
        x += GetStringWidth(FONT_NORMAL, buf, 0) + 8;
        buf[0] = CHAR_PLUS;
        ConvertIntToDecimalStringN(buf + 1, gSpireResult.healPercent, STR_CONV_MODE_LEFT_ALIGN, 3);
        StringAppend(buf, COMPOUND_STRING("% HP"));
        PrintText(WIN_HEADER, FONT_NORMAL, x, 1, sColor_Green, buf);
        break;
    case SPIRE_CARDS_DRAFT:
        PrintText(WIN_HEADER, FONT_NORMAL, 4, 1, sColor_Purple, COMPOUND_STRING("THE SPIRE"));
        PrintText(WIN_HEADER, FONT_NORMAL, 84, 1, sColor_Dark,
                  IsSecondDraft() ? COMPOUND_STRING("Pick your 2nd Pokémon") : COMPOUND_STRING("Pick your 1st Pokémon"));
        break;
    case SPIRE_CARDS_REST:
        PrintText(WIN_HEADER, FONT_NORMAL, 4, 1, sColor_Red, COMPOUND_STRING("POKéMON CENTER"));
        PrintText(WIN_HEADER, FONT_NORMAL, 130, 1, sColor_Dark, COMPOUND_STRING("Take a breather."));
        break;
    case SPIRE_CARDS_SHOP:
        PrintText(WIN_HEADER, FONT_NORMAL, 4, 1, sColor_Blue, COMPOUND_STRING("POKé MART"));
        PrintText(WIN_HEADER, FONT_SMALL_NARROW, 72, 3, sColor_Gray,
                  sCards->page == 0 ? COMPOUND_STRING("Shelf 1/2: moves, relic {DOWN_ARROW}") : COMPOUND_STRING("Shelf 2/2: items, tutor {UP_ARROW}"));
        ConvertIntToDecimalStringN(buf, RUN.gold, STR_CONV_MODE_LEFT_ALIGN, 4);
        StringAppend(buf, COMPOUND_STRING("¥"));
        PrintText(WIN_HEADER, FONT_NORMAL, 214 - GetStringWidth(FONT_NORMAL, buf, 0), 1, sColor_Gold, buf);
        break;
    case SPIRE_CARDS_EVENT:
        PrintText(WIN_HEADER, FONT_NORMAL, 4, 1, sColor_Purple, sEvents[sCards->event].title);
        break;
    case SPIRE_CARDS_MESSAGE:
        PrintText(WIN_HEADER, FONT_NORMAL, 4, 1, sColor_Purple, sCards->title);
        break;
    case SPIRE_CARDS_EVOLVE:
        GetMonData(&RUN.mons[gSpireEvolveMon], MON_DATA_NICKNAME, gStringVar1);
        StringExpandPlaceholders(gStringVar4, COMPOUND_STRING("{STR_VAR_1} is evolving!"));
        PrintText(WIN_HEADER, FONT_NORMAL, 4, 1, sColor_Purple, gStringVar4);
        PrintText(WIN_HEADER, FONT_NORMAL, 150, 1, sColor_Dark, COMPOUND_STRING("Into what?"));
        break;
    }
    CopyWindowToVram(WIN_HEADER, COPYWIN_FULL);
}

// Alleen de rand (tilemap), zonder de inhoud van het venster te wissen.
static void DrawFrameOnly(u32 win, u32 pal)
{
    u32 l = GetWindowAttribute(win, WINDOW_TILEMAP_LEFT), t = GetWindowAttribute(win, WINDOW_TILEMAP_TOP);
    u32 w = GetWindowAttribute(win, WINDOW_WIDTH), h = GetWindowAttribute(win, WINDOW_HEIGHT);

    FillBgTilemapBufferRect(0, FRAME_TILE + 0, l - 1, t - 1, 1, 1, pal);
    FillBgTilemapBufferRect(0, FRAME_TILE + 1, l, t - 1, w, 1, pal);
    FillBgTilemapBufferRect(0, FRAME_TILE + 2, l + w, t - 1, 1, 1, pal);
    FillBgTilemapBufferRect(0, FRAME_TILE + 3, l - 1, t, 1, h, pal);
    FillBgTilemapBufferRect(0, FRAME_TILE + 5, l + w, t, 1, h, pal);
    FillBgTilemapBufferRect(0, FRAME_TILE + 6, l - 1, t + h, 1, 1, pal);
    FillBgTilemapBufferRect(0, FRAME_TILE + 7, l, t + h, w, 1, pal);
    FillBgTilemapBufferRect(0, FRAME_TILE + 8, l + w, t + h, 1, 1, pal);
}

// slot = plek op het scherm (0-2); de kaart is sCards->page * 3 + slot
static void DrawCardFrame(u32 slot)
{
    u32 i = sCards->page * CARDS_PER_PAGE + slot;

    DrawFrameOnly(WIN_CARD_0 + slot, (i == sCards->card && sCards->state == STATE_CARDS) ? PAL_FRAME_SEL : PAL_FRAME);
}

static void DrawFooter(u32 win, struct SpireCard *c, const u8 *fallback, const u8 *color)
{
    u8 buf[12];

    if (c->sold)
    {
        PrintCentered(win, FONT_SMALL_NARROW, 37, 64, sColor_Red, COMPOUND_STRING("SOLD"));
    }
    else if (c->price)
    {
        ConvertIntToDecimalStringN(buf, c->price, STR_CONV_MODE_LEFT_ALIGN, 4);
        StringAppend(buf, COMPOUND_STRING("¥"));
        PrintCentered(win, FONT_SMALL_NARROW, 37, 64, RUN.gold >= c->price ? sColor_Gold : sColor_Red, buf);
    }
    else if (fallback != NULL)
    {
        PrintCentered(win, FONT_SMALL_NARROW, 37, 64, color, fallback);
    }
}

static void DrawCard(u32 i)
{
    u32 win = WIN_CARD_0 + i % CARDS_PER_PAGE;
    struct SpireCard *c = &sCards->cards[i];
    u8 buf[16];

    DrawCardFrame(i % CARDS_PER_PAGE);
    PutWindowTilemap(win);
    FillWindowPixelBuffer(win, PIXEL_FILL(1));
    switch (c->kind)
    {
    case CARD_MOVE:
    {
        const u8 *cat;

        FillWindowPixelRect(win, PIXEL_FILL(sRarityBarColor[c->rarity]), 0, 0, 64, 3);
        PrintCentered(win, FONT_SMALL_NARROW, 3, 64, sColor_Dark, GetMoveName(c->value));
        switch (GetMoveCategory(c->value))
        {
        case DAMAGE_CATEGORY_PHYSICAL: cat = sText_Phys; break;
        case DAMAGE_CATEGORY_SPECIAL:  cat = sText_Spec; break;
        default:                       cat = sText_Status; break;
        }
        PrintText(win, FONT_SMALL_NARROW, 40, 15, sColor_Dark, cat);
        if (GetMovePower(c->value) > 1)
        {
            StringCopy(buf, COMPOUND_STRING("PWR "));
            ConvertIntToDecimalStringN(buf + 4, GetMovePower(c->value), STR_CONV_MODE_LEFT_ALIGN, 3);
        }
        else
        {
            StringCopy(buf, COMPOUND_STRING("PWR -"));
        }
        PrintText(win, FONT_SMALL_NARROW, 2, 26, sColor_Dark, buf);
        StringCopy(buf, COMPOUND_STRING("PP "));
        ConvertIntToDecimalStringN(buf + 3, GetMovePP(c->value), STR_CONV_MODE_LEFT_ALIGN, 2);
        PrintText(win, FONT_SMALL_NARROW, 40, 26, sColor_Dark, buf);
        DrawFooter(win, c, sRarityName[c->rarity], sRarityTextColor[c->rarity]);
        break;
    }
    case CARD_MON:
        FillWindowPixelRect(win, PIXEL_FILL(14), 0, 0, 64, 3);
        PrintCentered(win, FONT_SMALL_NARROW, 3, 64, sColor_Dark, GetSpeciesName(c->value));
        break;
    case CARD_RELIC:
        FillWindowPixelRect(win, PIXEL_FILL(6), 0, 0, 64, 3);
        PrintCentered(win, FONT_SMALL_NARROW, 3, 64, sColor_Dark, gSpireRelics[c->value].name);
        DrawFooter(win, c, COMPOUND_STRING("RELIC"), sColor_Gold);
        break;
    case CARD_ITEM:
        FillWindowPixelRect(win, PIXEL_FILL(sRarityBarColor[c->rarity]), 0, 0, 64, 3);
        PrintCentered(win, FONT_SMALL_NARROW, 3, 64, sColor_Dark, GetItemName(c->value));
        DrawFooter(win, c, COMPOUND_STRING("HELD ITEM"), sRarityTextColor[c->rarity]);
        break;
    case CARD_OPTION:
    {
        const struct SpireOption *o = &sOptions[c->value];

        FillWindowPixelRect(win, PIXEL_FILL(11), 0, 0, 64, 3);
        PrintCentered(win, FONT_SMALL_NARROW, 3, 64, sColor_Dark, o->name);
        if (c->value == OPT_EVOLVE_0 || c->value == OPT_EVOLVE_1)
        {
            PrintCentered(win, FONT_SMALL_NARROW, 37, 64, sColor_Purple,
                          GetSpeciesName(GetMonData(&RUN.mons[c->value - OPT_EVOLVE_0], MON_DATA_SPECIES)));
        }
        else if (o->iconSpecies == SPECIES_NONE && c->value != OPT_RELEARN && c->value != OPT_EV_RECRUIT)
        {
            PrintCentered(win, FONT_SMALL_NARROW, 16, 64, sColor_Dark, o->line1);
            PrintCentered(win, FONT_SMALL_NARROW, 26, 64, sColor_Dark, o->line2);
        }
        DrawFooter(win, c, NULL, sColor_Dark);
        break;
    }
    }
    CopyWindowToVram(win, COPYWIN_FULL);
}

static void DrawHpBar(u32 win, u32 x, u32 y, struct Pokemon *mon)
{
    u32 hp = GetMonData(mon, MON_DATA_HP), maxHp = GetMonData(mon, MON_DATA_MAX_HP);
    u32 w = maxHp ? 40 * hp / maxHp : 0;
    u32 col = (hp * 2 > maxHp) ? 9 : (hp * 5 > maxHp) ? 6 : 11;

    FillWindowPixelRect(win, PIXEL_FILL(13), x, y, 42, 4);
    if (w)
        FillWindowPixelRect(win, PIXEL_FILL(col), x + 1, y + 1, w, 2);
}

static bool32 ShowTeam(void)
{
    return sCards->mode != SPIRE_CARDS_DRAFT && sCards->mode != SPIRE_CARDS_MESSAGE && sCards->mode != SPIRE_CARDS_EVOLVE
        && sCards->state != STATE_CHOOSE_SLOT && sCards->state != STATE_MESSAGE && sCards->state != STATE_RELEARN;
}

static void DrawTeamRow(u32 y, u32 move)
{
    u32 i;

    for (i = 0; i < 2; i++)
    {
        struct Pokemon *mon = Spire_GetRunMon(i);
        u8 nick[POKEMON_NAME_LENGTH + 1];
        u8 buf[8];
        u32 x = 40 + i * 104;
        u32 hp = GetMonData(mon, MON_DATA_HP), maxHp = GetMonData(mon, MON_DATA_MAX_HP);

        GetMonData(mon, MON_DATA_NICKNAME, nick);
        if (sCards->state == STATE_CHOOSE_MON && sCards->mon == i)
            PrintText(WIN_BOTTOM, FONT_NORMAL, x - 38, y + 4, sColor_Red, COMPOUND_STRING("▶"));
        PrintText(WIN_BOTTOM, FONT_SMALL_NARROW, x, y, sColor_Dark, nick);
        if (move != MOVE_NONE && IsStab(mon, move))
            PrintText(WIN_BOTTOM, FONT_SMALL_NARROW, x + 46, y, sColor_Red, COMPOUND_STRING("STAB"));
        DrawHpBar(WIN_BOTTOM, x, y + 13, mon);
        ConvertIntToDecimalStringN(buf, maxHp ? (hp * 100 + maxHp - 1) / maxHp : 0, STR_CONV_MODE_LEFT_ALIGN, 3);
        StringAppend(buf, COMPOUND_STRING("%"));
        PrintText(WIN_BOTTOM, FONT_SMALL_NARROW, x + 44, y + 9, sColor_Dark, buf);
    }
}

static const u8 *const sTierName[] = {COMPOUND_STRING("COMMON"), COMPOUND_STRING("COMMON"), COMPOUND_STRING("UNCOMMON"), COMPOUND_STRING("RARE")};

// Startmoves en evoluties van een rental in de draft.
static void DrawDraftLine(u16 species)
{
    const struct SpireRental *rental = Spire_FindRental(species);
    u16 targets[3];
    u8 *p = gStringVar4;
    u32 i;

    if (rental)
    {
        for (i = 0; i < MAX_MON_MOVES; i++)
        {
            if (rental->moves[i] == MOVE_NONE)
                continue;
            if (p != gStringVar4)
                p = StringCopy(p, COMPOUND_STRING(", "));
            p = StringCopy(p, GetMoveName(rental->moves[i]));
        }
        PrintText(WIN_BOTTOM, FONT_SMALL_NARROW, 2, 24, sColor_Dark, gStringVar4);
        PrintText(WIN_BOTTOM, FONT_SMALL_NARROW, 170, 0, rental->tier >= 3 ? sColor_Gold : rental->tier == 2 ? sColor_Blue : sColor_Gray,
                  sTierName[rental->tier]);
    }
    p = gStringVar4;
    if (Spire_GetEvolutions(species, targets))
    {
        u16 mid = targets[0];

        p = StringCopy(p, COMPOUND_STRING("Act 2: "));
        p = StringCopy(p, GetSpeciesName(mid));
        if (Spire_GetEvolutions(species, targets) > 1)
            p = StringCopy(p, COMPOUND_STRING(" (or more)"));
        if (Spire_GetEvolutions(mid, targets))
        {
            p = StringCopy(p, COMPOUND_STRING("  Act 3: "));
            p = StringCopy(p, GetSpeciesName(targets[0]));
        }
    }
    else
    {
        p = StringCopy(p, COMPOUND_STRING("Does not evolve. Strong now, never stronger."));
    }
    PrintText(WIN_BOTTOM, FONT_SMALL_NARROW, 2, 36, sColor_Purple, gStringVar4);
}

static void DrawSpeciesStats(u16 species)
{
    u8 buf[64];
    u8 *p = buf;

    p = StringCopy(p, COMPOUND_STRING("HP "));
    p = ConvertIntToDecimalStringN(p, gSpeciesInfo[species].baseHP, STR_CONV_MODE_LEFT_ALIGN, 3);
    p = StringCopy(p, COMPOUND_STRING("  Atk "));
    p = ConvertIntToDecimalStringN(p, gSpeciesInfo[species].baseAttack, STR_CONV_MODE_LEFT_ALIGN, 3);
    p = StringCopy(p, COMPOUND_STRING("  Def "));
    p = ConvertIntToDecimalStringN(p, gSpeciesInfo[species].baseDefense, STR_CONV_MODE_LEFT_ALIGN, 3);
    p = StringCopy(p, COMPOUND_STRING("  SpA "));
    p = ConvertIntToDecimalStringN(p, gSpeciesInfo[species].baseSpAttack, STR_CONV_MODE_LEFT_ALIGN, 3);
    p = StringCopy(p, COMPOUND_STRING("  SpD "));
    p = ConvertIntToDecimalStringN(p, gSpeciesInfo[species].baseSpDefense, STR_CONV_MODE_LEFT_ALIGN, 3);
    p = StringCopy(p, COMPOUND_STRING("  Spe "));
    p = ConvertIntToDecimalStringN(p, gSpeciesInfo[species].baseSpeed, STR_CONV_MODE_LEFT_ALIGN, 3);
    PrintText(WIN_BOTTOM, FONT_SMALL_NARROW, 2, 0, sColor_Dark, GetSpeciesName(species));
    PrintText(WIN_BOTTOM, FONT_SMALL_NARROW, 2, 12, sColor_Gray, buf);
    DrawDraftLine(species);
}

static void SetSpritesVisible(void)
{
    u32 i;
    bool32 team = ShowTeam();

    for (i = 0; i < 2; i++)
        if (sCards->iconSpriteIds[i] != SPRITE_NONE)
            gSprites[sCards->iconSpriteIds[i]].invisible = !team;
}

static void DrawBottom(void)
{
    struct SpireCard *c = &sCards->cards[sCards->card];
    u32 move = (c->kind == CARD_MOVE) ? c->value : MOVE_NONE;

    FillWindowPixelBuffer(WIN_BOTTOM, PIXEL_FILL(1));
    switch (sCards->state)
    {
    case STATE_CARDS:
        if (sCards->count == 0)
        {
            PrintText(WIN_BOTTOM, FONT_SMALL_NARROW, 2, 0, sColor_Dark, COMPOUND_STRING("Nothing left to take. Press A."));
            break;
        }
        if (sCards->mode == SPIRE_CARDS_EVENT)
            PrintText(WIN_BOTTOM, FONT_SMALL_NARROW, 2, 0, sColor_Dark, sEvents[sCards->event].story);
        else if (c->kind == CARD_MOVE)
            PrintText(WIN_BOTTOM, FONT_SMALL_NARROW, 2, 0, sColor_Dark, GetMoveDescription(c->value));
        else if (c->kind == CARD_RELIC)
            PrintText(WIN_BOTTOM, FONT_SMALL_NARROW, 2, 0, sColor_Dark, gSpireRelics[c->value].desc);
        else if (c->kind == CARD_ITEM)
            PrintText(WIN_BOTTOM, FONT_SMALL_NARROW, 2, 0, sColor_Dark, Reflow(Spire_GetItemDescription(c->value)));
        else if (c->kind == CARD_OPTION)
            PrintText(WIN_BOTTOM, FONT_SMALL_NARROW, 2, 0, sColor_Dark, sOptions[c->value].desc);
        if (sCards->mode == SPIRE_CARDS_DRAFT || sCards->mode == SPIRE_CARDS_EVOLVE)
            DrawSpeciesStats(c->value);
        else
            DrawTeamRow(22, move);
        break;
    case STATE_CHOOSE_MON:
        if (sCards->giveItem != ITEM_NONE)
        {
            StringCopy(gStringVar1, GetItemName(sCards->giveItem));
            StringExpandPlaceholders(gStringVar4, COMPOUND_STRING("Who holds the {STR_VAR_1}? (B: refund)"));
        }
        else if (sCards->replaceSpecies != SPECIES_NONE)
        {
            StringCopy(gStringVar1, GetSpeciesName(sCards->replaceSpecies));
            StringExpandPlaceholders(gStringVar4, COMPOUND_STRING("Who makes room for {STR_VAR_1}?"));
        }
        else if (sCards->relearnPaid && sCards->teachMove == MOVE_NONE)
        {
            StringCopy(gStringVar4, COMPOUND_STRING("Who remembers a move? You pay only if it works."));
        }
        else
        {
            StringCopy(gStringVar1, GetMoveName(sCards->teachMove));
            StringExpandPlaceholders(gStringVar4, COMPOUND_STRING("Teach {STR_VAR_1} to whom?"));
        }
        PrintText(WIN_BOTTOM, FONT_SMALL_NARROW, 2, 0, sColor_Dark, gStringVar4);
        DrawTeamRow(22, sCards->teachMove);
        break;
    case STATE_CHOOSE_SLOT:
    {
        struct Pokemon *mon = Spire_GetRunMon(sCards->mon);
        u32 i;

        StringCopy(gStringVar1, GetMoveName(sCards->teachMove));
        StringExpandPlaceholders(gStringVar4, COMPOUND_STRING("Forget which move for {STR_VAR_1}?"));
        PrintText(WIN_BOTTOM, FONT_SMALL_NARROW, 2, 0, sColor_Dark, gStringVar4);
        for (i = 0; i < MAX_MON_MOVES; i++)
        {
            u32 m = GetMonData(mon, MON_DATA_MOVE1 + i);

            if (sCards->slot == i)
                PrintText(WIN_BOTTOM, FONT_NORMAL, 26 + (i % 2) * 100, 14 + (i / 2) * 14, sColor_Red, COMPOUND_STRING("▶"));
            PrintText(WIN_BOTTOM, FONT_SMALL_NARROW, 36 + (i % 2) * 100, 16 + (i / 2) * 14, sColor_Dark,
                      m ? GetMoveName(m) : COMPOUND_STRING("-"));
        }
        break;
    }
    case STATE_MESSAGE:
        PrintText(WIN_BOTTOM, FONT_SMALL_NARROW, 2, 0, sColor_Dark, sCards->message);
        break;
    case STATE_RELEARN:
    {
        u32 first = (sCards->relearnCursor / 6) * 6, k;

        GetMonData(Spire_GetRunMon(sCards->mon), MON_DATA_NICKNAME, gStringVar1);
        StringExpandPlaceholders(gStringVar4, COMPOUND_STRING("Which move does {STR_VAR_1} remember?"));
        PrintText(WIN_BOTTOM, FONT_SMALL_NARROW, 2, 0, sColor_Blue, gStringVar4);
        for (k = first; k < first + 6 && k < sCards->relearnCount; k++)
        {
            u32 x = 12 + ((k - first) % 2) * 108, y = 12 + ((k - first) / 2) * 11;

            if (k == sCards->relearnCursor)
                PrintText(WIN_BOTTOM, FONT_SMALL_NARROW, x - 9, y, sColor_RedT, COMPOUND_STRING("▶"));
            PrintText(WIN_BOTTOM, FONT_SMALL_NARROW, x, y, sColor_DarkT, GetMoveName(sCards->relearnMoves[k]));
        }
        if (first + 6 < sCards->relearnCount)
            PrintText(WIN_BOTTOM, FONT_SMALL_NARROW, 210, 34, sColor_GrayT, COMPOUND_STRING("{DOWN_ARROW}"));
        break;
    }
    }
    CopyWindowToVram(WIN_BOTTOM, COPYWIN_FULL);
    SetSpritesVisible();
}

static void PlaceHand(void)
{
    struct Sprite *hand = &gSprites[sCards->handSpriteId];

    if (sCards->state == STATE_CARDS && sCards->count > 0)
    {
        hand->x = 8 + (sCards->card % CARDS_PER_PAGE) * 80 + 52;
        hand->y = 34;
        hand->invisible = FALSE;
    }
    else
    {
        hand->invisible = TRUE;
    }
}

static void SpriteCB_Hand(struct Sprite *sprite)
{
    sCards->bob++;
    sprite->y2 = (sCards->bob & 0x10) ? 2 : 0;
}

static void Redraw(void)
{
    u32 i;

    for (i = 0; i < CARDS_PER_PAGE; i++)
        if (sCards->page * CARDS_PER_PAGE + i < sCards->count)
            DrawCardFrame(i);
    ScheduleBgCopyTilemapToVram(0);
    DrawBottom();
    PlaceHand();
}

// --- sprites op de kaarten --------------------------------------------------------------------
static u8 CreateTypeSprite(enum Type type, s16 x, s16 y)
{
    u8 id = CreateSprite(&gSpriteTemplate_MoveTypes, x, y, 0);

    StartSpriteAnim(&gSprites[id], type);
    gSprites[id].oam.paletteNum = gTypesInfo[type].palette;
    gSprites[id].oam.priority = 0;
    return id;
}

static void CreateCardSprites(u32 card)
{
    struct SpireCard *c = &sCards->cards[card];
    u32 i = card % CARDS_PER_PAGE;
    s16 left = 8 + i * 80;
    u8 id;

    sCards->cardSpriteIds[i][0] = sCards->cardSpriteIds[i][1] = sCards->cardSpriteIds[i][2] = SPRITE_NONE;
    switch (c->kind)
    {
    case CARD_MOVE:
        sCards->cardSpriteIds[i][0] = CreateTypeSprite(GetMoveType(c->value), left + 18, 40 + 16 + 4);
        break;
    case CARD_MON:
        id = CreateMonIconNoPersonality(c->value, SpriteCB_MonIcon, left + 18, 40 + 30, 0);
        gSprites[id].oam.priority = 0;
        sCards->cardSpriteIds[i][0] = id;
        sCards->cardSpriteIds[i][1] = CreateTypeSprite(GetSpeciesType(c->value, 0), left + 50, 40 + 22);
        if (GetSpeciesType(c->value, 1) != GetSpeciesType(c->value, 0))
            sCards->cardSpriteIds[i][2] = CreateTypeSprite(GetSpeciesType(c->value, 1), left + 50, 40 + 38);
        break;
    case CARD_RELIC:
    case CARD_ITEM:
        id = AddItemIconSprite(TAG_ITEM + i, TAG_ITEM + i, c->kind == CARD_ITEM ? c->value : gSpireRelics[c->value].item);
        if (id != MAX_SPRITES)
        {
            gSprites[id].x = left + 32;
            gSprites[id].y = 40 + 26;
            gSprites[id].oam.priority = 0;
            sCards->cardSpriteIds[i][0] = id;
        }
        break;
    case CARD_OPTION:
    {
        u16 species = sOptions[c->value].iconSpecies;

        if (c->value == OPT_RELEARN)
        {
            id = AddItemIconSprite(TAG_ITEM + i, TAG_ITEM + i, ITEM_HEART_SCALE);
            if (id != MAX_SPRITES)
            {
                gSprites[id].x = left + 32;
                gSprites[id].y = 40 + 22;
                gSprites[id].oam.priority = 0;
                sCards->cardSpriteIds[i][0] = id;
            }
            break;
        }
        if (c->value == OPT_EV_RECRUIT)
            species = sCards->recruitSpecies;
        if (species != SPECIES_NONE)
        {
            id = CreateMonIconNoPersonality(species, SpriteCB_MonIcon, left + 32, 40 + 26, 0);
            gSprites[id].oam.priority = 0;
            sCards->cardSpriteIds[i][0] = id;
        }
        break;
    }
    }
}

static void DestroyCardSprites(u32 slot)
{
    u32 j;

    for (j = 0; j < 3; j++)
    {
        u8 id = sCards->cardSpriteIds[slot][j];

        if (id == SPRITE_NONE || id >= MAX_SPRITES)
            continue;
        DestroySprite(&gSprites[id]);
        sCards->cardSpriteIds[slot][j] = SPRITE_NONE;
    }
    // item-iconen hebben een eigen tag per plek: altijd vrijgeven, anders erft de volgende kaart het oude icoon
    FreeSpriteTilesByTag(TAG_ITEM + slot);
    FreeSpritePaletteByTag(TAG_ITEM + slot);
}

// Kaarten van de huidige pagina tekenen (winkel: twee schappen).
static void ShowPage(void)
{
    u32 slot;

    for (slot = 0; slot < CARDS_PER_PAGE; slot++)
    {
        u32 i = sCards->page * CARDS_PER_PAGE + slot;

        DestroyCardSprites(slot);
        if (i < sCards->count)
        {
            CreateCardSprites(i);
            DrawCard(i);
        }
        else
        {
            FillWindowPixelBuffer(WIN_CARD_0 + slot, PIXEL_FILL(1));
            CopyWindowToVram(WIN_CARD_0 + slot, COPYWIN_FULL);
        }
    }
}

// --- scherm openen en sluiten -----------------------------------------------------------------
static void VBlankCB_SpireCards(void)
{
    LoadOam();
    ProcessSpriteCopyRequests();
    TransferPlttBuffer();
}

static void CB2_SpireCards(void)
{
    RunTasks();
    AnimateSprites();
    BuildOamBuffer();
    RunTextPrinters();
    DoScheduledBgTilemapCopiesToVram();
    UpdatePaletteFade();
}

static void LoadBricks(void)
{
    u16 *tilemap = AllocZeroed(BG_SCREEN_SIZE);
    u32 x, y;

    LoadBgTiles(1, sBrickTiles, sizeof(sBrickTiles), BRICK_TILE);
    LoadPalette(sBrickPal, BG_PLTT_ID(PAL_BRICKS), PLTT_SIZE_4BPP);
    for (y = 0; y < 32; y++)
        for (x = 0; x < 32; x++)
            tilemap[y * 32 + x] = (((x + (y & 1)) & 1) + BRICK_TILE) | (PAL_BRICKS << 12);
    SetBgTilemapBuffer(1, tilemap);
    ScheduleBgCopyTilemapToVram(1);
}

static void SetupScreen(void)
{
    u32 i;

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
    InitWindows(sWindowTemplates);
    DeactivateAllTextPrinters();

    LoadBricks();
    LoadPalette(sTextPal, BG_PLTT_ID(PAL_TEXT), PLTT_SIZE_4BPP);
    LoadWindowGfx(WIN_HEADER, 0, FRAME_TILE, BG_PLTT_ID(PAL_FRAME));
    // rode variant van het kader voor de gekozen kaart (randkleuren 2-6)
    CpuCopy16(&gPlttBufferUnfaded[BG_PLTT_ID(PAL_FRAME)], &gPlttBufferUnfaded[BG_PLTT_ID(PAL_FRAME_SEL)], PLTT_SIZE_4BPP);
    gPlttBufferUnfaded[BG_PLTT_ID(PAL_FRAME_SEL) + 2] = RGB(18, 3, 3);
    gPlttBufferUnfaded[BG_PLTT_ID(PAL_FRAME_SEL) + 3] = RGB(29, 8, 6);
    gPlttBufferUnfaded[BG_PLTT_ID(PAL_FRAME_SEL) + 4] = RGB(24, 5, 5);
    gPlttBufferUnfaded[BG_PLTT_ID(PAL_FRAME_SEL) + 5] = RGB(31, 13, 10);
    gPlttBufferUnfaded[BG_PLTT_ID(PAL_FRAME_SEL) + 6] = RGB(31, 19, 16);
    gPlttBufferUnfaded[0] = RGB(5, 4, 9);

    DrawFrameOnly(WIN_HEADER, PAL_FRAME);
    DrawFrameOnly(WIN_BOTTOM, PAL_FRAME);
    PutWindowTilemap(WIN_HEADER);
    PutWindowTilemap(WIN_BOTTOM);

    LoadMonIconPalettes();
    LoadSpriteSheet(&sSpriteSheet_Hand);
    LoadSpritePalette(&sSpritePal_Hand);
    LoadCompressedSpriteSheet(&gSpriteSheet_MoveTypes);
    LoadPalette(gMoveTypes_Pal, OBJ_PLTT_ID(13), 3 * PLTT_SIZE_4BPP);

    for (i = 0; i < CARDS_PER_PAGE; i++)
        sCards->cardSpriteIds[i][0] = sCards->cardSpriteIds[i][1] = sCards->cardSpriteIds[i][2] = SPRITE_NONE;
    ShowPage();
    for (i = 0; i < 2; i++)
    {
        struct Pokemon *mon = Spire_GetRunMon(i);

        sCards->iconSpriteIds[i] = SPRITE_NONE;
        if (sCards->mode != SPIRE_CARDS_DRAFT && sCards->mode != SPIRE_CARDS_MESSAGE && sCards->mode != SPIRE_CARDS_EVOLVE && GetMonData(mon, MON_DATA_SPECIES) != SPECIES_NONE)
        {
            sCards->iconSpriteIds[i] = CreateMonIcon(GetMonData(mon, MON_DATA_SPECIES), SpriteCB_MonIcon,
                                                     8 + 24 + i * 104, 104 + 22 + 10, 0, GetMonData(mon, MON_DATA_PERSONALITY));
            gSprites[sCards->iconSpriteIds[i]].oam.priority = 0;
        }
    }
    sCards->handSpriteId = CreateSprite(&sSpriteTemplate_Hand, 0, 0, 0);

    DrawHeader();
    if (sCards->mode == SPIRE_CARDS_MESSAGE)
    {
        sCards->state = STATE_MESSAGE;
        StringCopy(sCards->message, sCards->text);
        sCards->afterMessage = 0;
    }
    Redraw();
    ScheduleBgCopyTilemapToVram(0);

    SetGpuReg(REG_OFFSET_DISPCNT, DISPCNT_OBJ_1D_MAP | DISPCNT_OBJ_ON | DISPCNT_BG0_ON | DISPCNT_BG1_ON);
    SetGpuReg(REG_OFFSET_BLDCNT, 0);
    ShowBg(0);
    ShowBg(1);
    BeginNormalPaletteFade(PALETTES_ALL, 0, 16, 0, RGB_BLACK);
    SetVBlankCallback(VBlankCB_SpireCards);
    SetMainCallback2(CB2_SpireCards);
    CreateTask(Task_SpireCards, 0);
}

static void OpenCards(u32 mode, const u8 *title, const u8 *text, void (*onDone)(void))
{
    sCards = AllocZeroed(sizeof(*sCards));
    sCards->mode = mode;
    sCards->onDone = onDone;
    sCards->title = title;
    sCards->text = text;
    BuildCards();
    SetupScreen();
}

void Spire_OpenCards(u32 mode, void (*onDone)(void))
{
    OpenCards(mode, NULL, NULL, onDone);
}

void Spire_OpenMessage(const u8 *title, const u8 *text, void (*onDone)(void))
{
    OpenCards(SPIRE_CARDS_MESSAGE, title, text, onDone);
}

static void CloseScreen(void)
{
    void (*onDone)(void) = sCards->onDone;

    FreeMonIconPalettes();
    FreeAllWindowBuffers();
    Free(GetBgTilemapBuffer(0));
    Free(GetBgTilemapBuffer(1));
    Free(sCards);
    sCards = NULL;
    onDone();
}

static void Exit(void)
{
    sCards->state = STATE_EXIT;
    BeginNormalPaletteFade(PALETTES_ALL, 0, 0, 16, RGB_BLACK);
}

static void ShowMessage(const u8 *text, bool32 backToCards)
{
    StringCopy(sCards->message, text);
    sCards->state = STATE_MESSAGE;
    sCards->afterMessage = backToCards;
    Redraw();
}

static void StartTeach(u16 move)
{
    sCards->teachMove = move;
    sCards->mon = 0;
    sCards->state = STATE_CHOOSE_MON;
    Redraw();
}

static void LoseHp(u32 percent)
{
    u32 i;

    for (i = 0; i < 2; i++)
    {
        struct Pokemon *mon = &RUN.mons[i];
        u32 hp = GetMonData(mon, MON_DATA_HP), loss = GetMonData(mon, MON_DATA_MAX_HP) * percent / 100;

        hp = (hp > loss) ? hp - loss : 1;
        SetMonData(mon, MON_DATA_HP, &hp);
    }
}

static void AddGold(u32 gold)
{
    RUN.gold = min(9999, RUN.gold + gold);
}

// --- keuzes uitvoeren -------------------------------------------------------------------------
// Blijvende max-HP-verandering (events): in procentpunten van de gewone max HP, voor beide rentals.
static void ChangeMaxHp(s32 delta)
{
    u32 i;

    for (i = 0; i < 2; i++)
    {
        struct Pokemon *mon = &RUN.mons[i];
        u32 hp = GetMonData(mon, MON_DATA_HP), maxHp = GetMonData(mon, MON_DATA_MAX_HP), newMax;

        RUN.hpBonus[i] = max(-60, min(60, RUN.hpBonus[i] + delta));
        CalculateMonStats(mon);
        Spire_ScaleMonHp(mon, Spire_PlayerHpPercent(i));
        newMax = GetMonData(mon, MON_DATA_MAX_HP);
        hp = (delta > 0) ? hp + (newMax - min(newMax, maxHp)) : min(hp, newMax);
        if (hp == 0 && GetMonData(mon, MON_DATA_HP) == 0)
            hp = 0;
        SetMonData(mon, MON_DATA_HP, &hp);
    }
}

// Een willekeurige move van een willekeurige Pokémon vergeten (laat er altijd één over).
static void ForgetRandomMove(u8 *dst, const u8 *suffix)
{
    u32 i = Random() & 1, slot, n = 0, tries;
    struct Pokemon *mon = &RUN.mons[i];

    for (slot = 0; slot < MAX_MON_MOVES; slot++)
        if (GetMonData(mon, MON_DATA_MOVE1 + slot) != MOVE_NONE)
            n++;
    if (n <= 1)
    {
        mon = &RUN.mons[i ^ 1];
        i ^= 1;
    }
    for (tries = 0; tries < 20; tries++)
    {
        slot = Random() % MAX_MON_MOVES;
        if (GetMonData(mon, MON_DATA_MOVE1 + slot) != MOVE_NONE)
            break;
    }
    GetMonData(mon, MON_DATA_NICKNAME, gStringVar1);
    StringCopy(gStringVar2, GetMoveName(GetMonData(mon, MON_DATA_MOVE1 + slot)));
    SetMonMoveSlot(mon, MOVE_NONE, slot);
    Spire_ClearSlotUpgrade(mon, slot);
    StringExpandPlaceholders(gStringVar4, COMPOUND_STRING("{STR_VAR_1} forgot {STR_VAR_2}.\n"));
    StringAppend(gStringVar4, suffix);
    StringCopy(dst, gStringVar4);
    sCards->state = STATE_MESSAGE;
    sCards->afterMessage = 0;
    Redraw();
}

static void UpgradeRandomMoves(u32 count, const u8 *suffix)
{
    u8 *p = sCards->message;
    u32 k, tries;

    for (k = 0; k < count; k++)
    {
        for (tries = 0; tries < 30; tries++)
        {
            u32 i = Random() & 1, slot = Random() % MAX_MON_MOVES;
            struct Pokemon *mon = &RUN.mons[i];

            if (GetMonData(mon, MON_DATA_MOVE1 + slot) == MOVE_NONE || Spire_IsSlotUpgraded(mon, slot))
                continue;
            Spire_UpgradeSlot(mon, slot);
            StringCopy(gStringVar1, GetMoveName(GetMonData(mon, MON_DATA_MOVE1 + slot)));
            StringExpandPlaceholders(gStringVar4, COMPOUND_STRING("{STR_VAR_1}+! "));
            p = StringCopy(p, gStringVar4);
            break;
        }
    }
    *p++ = CHAR_NEWLINE;
    StringCopy(p, suffix);
    sCards->state = STATE_MESSAGE;
    sCards->afterMessage = 0;
    Redraw();
}

static void SpinWheel(void)
{
    switch (Random() % 6)
    {
    case 0:
        AddGold(100);
        ShowMessage(COMPOUND_STRING("Jackpot! +100¥. Spinda falls over."), FALSE);
        break;
    case 1:
    {
        u32 relic = Spire_RandomNewRelic(1);

        if (relic < SPIRE_RELIC_COUNT)
        {
            Spire_AddRelic(relic);
            StringCopy(gStringVar1, gSpireRelics[relic].name);
            StringExpandPlaceholders(gStringVar4, COMPOUND_STRING("A relic: the {STR_VAR_1}! Spinda is jealous."));
            ShowMessage(gStringVar4, FALSE);
            break;
        }
        // geen relics meer: dan geld
        AddGold(100);
        ShowMessage(COMPOUND_STRING("+100¥. Spinda claps, slightly off-beat."), FALSE);
        break;
    }
    case 2:
        Spire_HealRun(100);
        Spire_RestorePP();
        ShowMessage(COMPOUND_STRING("Full heal! Spinda is very proud of you."), FALSE);
        break;
    case 3:
        LoseHp(15);
        ShowMessage(COMPOUND_STRING("Spinda slaps everyone. -15% HP.\nIt was an accident. Probably."), FALSE);
        break;
    case 4:
        UpgradeRandomMoves(1, COMPOUND_STRING("The wheel stops on 'upgrade'. Huh."));
        break;
    default:
        ForgetRandomMove(sCards->message, COMPOUND_STRING("The wheel stops on 'forget'. Sorry."));
        break;
    }
}

static void PickOption(u32 opt)
{
    switch (opt)
    {
    case OPT_REST:
        Spire_HealRun(Spire_HasRelic(SPIRE_RELIC_SOOTHE_BELL) ? 80 : SPIRE_REST_HEAL);
        Spire_RestorePP();
        ShowMessage(COMPOUND_STRING("Your team rests. HP and PP restored."), FALSE);
        break;
    case OPT_EVOLVE_0:
    case OPT_EVOLVE_1:
    {
        u32 i = opt - OPT_EVOLVE_0;

        GetMonData(&RUN.mons[i], MON_DATA_NICKNAME, gStringVar1);
        Spire_Evolve(i);
        StringCopy(gStringVar2, GetSpeciesName(GetMonData(&RUN.mons[i], MON_DATA_SPECIES)));
        StringExpandPlaceholders(gStringVar4, COMPOUND_STRING("{STR_VAR_1} evolved into {STR_VAR_2}!"));
        ShowMessage(gStringVar4, FALSE);
        break;
    }
    case OPT_POTION:
        Spire_HealRun(30);
        ShowMessage(COMPOUND_STRING("Both Pokémon feel better."), TRUE);
        break;
    case OPT_EV_SAMPLE:
        if (Random() % 2)
        {
            Spire_HealRun(30);
            ShowMessage(COMPOUND_STRING("Delicious! Your team heals 30%."), FALSE);
        }
        else
        {
            LoseHp(10);
            ShowMessage(COMPOUND_STRING("It was a sock. Your team loses 10% HP."), FALSE);
        }
        break;
    case OPT_EV_STEAL:
        AddGold(40);
        LoseHp(15);
        ShowMessage(COMPOUND_STRING("You grab 40¥. Meowth grabs you back."), FALSE);
        break;
    case OPT_EV_READ:
        StartTeach(Spire_RandomMove(2, Random()));
        break;
    case OPT_EV_GRAMMAR:
        AddGold(30);
        ShowMessage(COMPOUND_STRING("The Unown pays you 30¥ to leave."), FALSE);
        break;
    case OPT_EV_DITTO_TAKE:
    case OPT_EV_RECRUIT:
        if (opt == OPT_EV_RECRUIT)
            LoseHp(25);
        sCards->replaceSpecies = (opt == OPT_EV_DITTO_TAKE) ? SPECIES_DITTO : sCards->recruitSpecies;
        sCards->mon = 0;
        sCards->state = STATE_CHOOSE_MON;
        Redraw();
        break;
    case OPT_EV_SHROOM_FEW:
    case OPT_EV_SHROOM_MANY:
    {
        bool32 many = (opt == OPT_EV_SHROOM_MANY);
        u32 i, chance = many ? 70 : 25;
        static const u16 sBerries[] = {ITEM_SITRUS_BERRY, ITEM_LUM_BERRY, ITEM_LIECHI_BERRY, ITEM_PETAYA_BERRY,
                                       ITEM_SALAC_BERRY, ITEM_GANLON_BERRY, ITEM_APICOT_BERRY};
        u8 *p = sCards->message;

        for (i = 0; i < 2; i++)
        {
            u16 berry;

            if (!many && i != (Random() & 1))
                continue;
            berry = sBerries[Random() % ARRAY_COUNT(sBerries)];
            SetMonData(&RUN.mons[i], MON_DATA_HELD_ITEM, &berry);
            GetMonData(&RUN.mons[i], MON_DATA_NICKNAME, gStringVar1);
            StringCopy(gStringVar2, GetItemName(berry));
            StringExpandPlaceholders(gStringVar4, COMPOUND_STRING("{STR_VAR_1} holds a {STR_VAR_2}. "));
            p = StringCopy(p, gStringVar4);
            if (Random() % 100 < chance)
            {
                RUN.fungalMask |= 1 << i;
                p = StringCopy(p, COMPOUND_STRING("Spores!\n"));
            }
            else
            {
                p = StringCopy(p, COMPOUND_STRING("\n"));
            }
        }
        sCards->state = STATE_MESSAGE;
        sCards->afterMessage = 0;
        Redraw();
        break;
    }
    case OPT_EV_SPIKES_WALK:
        AddGold(90);
        RUN.toxicFights = 3;
        ShowMessage(COMPOUND_STRING("+90¥ from the wallet. Your feet tingle.\nThe next 3 battles might start with poison."), FALSE);
        break;
    case OPT_EV_SPIKES_AROUND:
        LoseHp(12);
        ShowMessage(COMPOUND_STRING("A long climb in the wind. Your team loses\n12% HP and gains a fear of heights."), FALSE);
        break;
    case OPT_EV_DELETER_LET:
        AddGold(110);
        ForgetRandomMove(sCards->message, COMPOUND_STRING("Done. 110¥ for you."));
        break;
    case OPT_EV_DELETER_TIP:
        if (RUN.gold < 40)
        {
            PlaySE(SE_FAILURE);
            ShowMessage(COMPOUND_STRING("He looks at your wallet. He looks at you.\nHe leaves."), FALSE);
            break;
        }
        RUN.gold -= 40;
        if (Random() % 4 == 0)
            ForgetRandomMove(sCards->message, COMPOUND_STRING("Oops. He deleted it anyway. No refunds."));
        else
            UpgradeRandomMoves(1, COMPOUND_STRING("He polishes it until it shines."));
        break;
    case OPT_EV_TUTOR_CHEAP:
    case OPT_EV_TUTOR_DEAR:
    {
        u32 price = (opt == OPT_EV_TUTOR_CHEAP) ? 45 : 100;

        if (RUN.gold < price)
        {
            PlaySE(SE_FAILURE);
            ShowMessage(COMPOUND_STRING("Upfront, he said. You do not have it."), TRUE);
            break;
        }
        RUN.gold -= price;
        DrawHeader();
        StartTeach(Spire_RandomMoveOfType(opt == OPT_EV_TUTOR_CHEAP ? 1 : 2,
                                          GetSpeciesType(GetMonData(&RUN.mons[Random() & 1], MON_DATA_SPECIES), Random() & 1), Random()));
        break;
    }
    case OPT_EV_LUNCH_BERRY:
        Spire_HealRun(30);
        ShowMessage(COMPOUND_STRING("Your team shares the Oran Berry. 30% HP.\nSnorlax snores, betrayed."), FALSE);
        break;
    case OPT_EV_LUNCH_CANDY:
        ChangeMaxHp(5);
        ShowMessage(COMPOUND_STRING("Rare Candy! Both Pokémon gain 5% max HP.\nThey were already level 100. Whatever."), FALSE);
        break;
    case OPT_EV_LUNCH_BOX:
    {
        u32 relic = Spire_RandomNewRelic(0);

        ChangeMaxHp(-8);
        if (relic < SPIRE_RELIC_COUNT)
        {
            Spire_AddRelic(relic);
            StringCopy(gStringVar1, gSpireRelics[relic].name);
            StringExpandPlaceholders(gStringVar4, COMPOUND_STRING("You got the {STR_VAR_1}! Snorlax wakes up and\nsits on you. -8% max HP, for good."));
        }
        else
        {
            StringCopy(gStringVar4, COMPOUND_STRING("The box is empty. Snorlax sits on you anyway.\n-8% max HP, for good."));
        }
        ShowMessage(gStringVar4, FALSE);
        break;
    }
    case OPT_EV_CHEST_TAKE:
        AddGold(130);
        if (Random() & 1)
        {
            LoseHp(20);
            ShowMessage(COMPOUND_STRING("+130¥! One coin was a Gimmighoul.\nIt bites everyone. -20% HP."), FALSE);
        }
        else
        {
            ShowMessage(COMPOUND_STRING("+130¥! The coin with eyes stays quiet.\nFor now."), FALSE);
        }
        break;
    case OPT_EV_JOY_HEAL:
    case OPT_EV_JOY_UPGRADE:
    {
        u32 price = (opt == OPT_EV_JOY_HEAL) ? 40 : 75;

        if (RUN.gold < price)
        {
            PlaySE(SE_FAILURE);
            ShowMessage(COMPOUND_STRING("She points at the price list. Then at\nthe door."), TRUE);
            break;
        }
        RUN.gold -= price;
        if (opt == OPT_EV_JOY_HEAL)
        {
            Spire_HealRun(40);
            ShowMessage(COMPOUND_STRING("She heals your team 40% without putting\ndown her sandwich. Professional."), FALSE);
        }
        else
        {
            UpgradeRandomMoves(1, COMPOUND_STRING("Her Porygon2 sends its regards."));
        }
        break;
    }
    case OPT_EV_WHEEL_SPIN:
        SpinWheel();
        break;
    case OPT_EV_ACE_SEARCH:
        if (Random() & 1)
        {
            u16 item = Spire_RandomHeldItem(1, Random());

            AddGold(60);
            sCards->giveItem = item;
            sCards->mon = 0;
            StringCopy(gStringVar1, GetItemName(item));
            StringExpandPlaceholders(sCards->message, COMPOUND_STRING("60¥ and a {STR_VAR_1}! Who holds it?"));
            sCards->state = STATE_CHOOSE_MON;
            Redraw();
        }
        else
        {
            sCards->onDone = Spire_StartEventFight;
            ShowMessage(COMPOUND_STRING("Her partner wakes up. It is very loyal.\nAnd very, very strong."), FALSE);
        }
        break;
    case OPT_EV_GLITCH_ENTER:
        LoseHp(20);
        UpgradeRandomMoves(2, COMPOUND_STRING("The glitch hurts. -20% HP."));
        break;
    case OPT_EV_CANDLE_OFFER:
        Spire_HealRun(100);
        ForgetRandomMove(sCards->message, COMPOUND_STRING("Litwick burns it. Your team is fully healed."));
        break;
    case OPT_EV_ACCEPT:
        Spire_HealRun(25);
        ShowMessage(COMPOUND_STRING("You are carried. It is humiliating.\nYour team heals 25%."), FALSE);
        break;
    case OPT_EV_RUDE:
        RUN.bp += 2;
        ShowMessage(COMPOUND_STRING("The Hiker nods with respect. +2 BP."), FALSE);
        break;
    default:
        ShowMessage(COMPOUND_STRING("You walk on. Nothing happens.\nThe tower sighs."), FALSE);
        break;
    }
}

// Vasthouditem geven: het oude item gaat weg (één item per Pokémon).
static void GiveHeldItem(void)
{
    struct Pokemon *mon = Spire_GetRunMon(sCards->mon);
    u16 old = GetMonData(mon, MON_DATA_HELD_ITEM);

    PlaySE(SE_SELECT);
    SetMonData(mon, MON_DATA_HELD_ITEM, &sCards->giveItem);
    GetMonData(mon, MON_DATA_NICKNAME, gStringVar1);
    StringCopy(gStringVar2, GetItemName(sCards->giveItem));
    if (old != ITEM_NONE)
    {
        StringCopy(gStringVar3, GetItemName(old));
        StringExpandPlaceholders(gStringVar4, COMPOUND_STRING("{STR_VAR_1} now holds the {STR_VAR_2}.\nThe {STR_VAR_3} was left behind."));
    }
    else
    {
        StringExpandPlaceholders(gStringVar4, COMPOUND_STRING("{STR_VAR_1} now holds the {STR_VAR_2}."));
    }
    sCards->giveItem = ITEM_NONE;
    ShowMessage(gStringVar4, sCards->mode == SPIRE_CARDS_SHOP);
}

// Move Relearner: alle level-up-moves van de huidige soort (ongeacht level; een Remoraid kent dus niet
// alles van Octillery), zonder moves die hij al kent of die verboden zijn.
static void BuildRelearnList(void)
{
    struct Pokemon *mon = Spire_GetRunMon(sCards->mon);
    const struct LevelUpMove *learnset = GetSpeciesLevelUpLearnset(GetMonData(mon, MON_DATA_SPECIES));
    u32 i, j;

    sCards->relearnCount = 0;
    for (i = 0; learnset[i].move != LEVEL_UP_MOVE_END && sCards->relearnCount < MAX_RELEARN; i++)
    {
        u16 move = learnset[i].move;
        bool32 dup = MonKnowsMove(mon, move) || Spire_IsMoveBanned(move);

        for (j = 0; j < sCards->relearnCount && !dup; j++)
            if (sCards->relearnMoves[j] == move)
                dup = TRUE;
        if (!dup)
            sCards->relearnMoves[sCards->relearnCount++] = move;
    }
}

static void StartTeachTo(u16 move, u32 monIndex)
{
    struct Pokemon *mon = Spire_GetRunMon(monIndex);
    u32 i;

    sCards->teachMove = move;
    sCards->mon = monIndex;
    for (i = 0; i < MAX_MON_MOVES; i++)
        if (GetMonData(mon, MON_DATA_MOVE1 + i) == MOVE_NONE)
            break;
    sCards->slot = (i < MAX_MON_MOVES) ? i : 0;
    sCards->state = STATE_CHOOSE_SLOT;
    Redraw();
}

static void PickCard(void)
{
    struct SpireCard *c = &sCards->cards[sCards->card];

    if (c->sold)
    {
        PlaySE(SE_FAILURE);
        return;
    }
    if (c->price)
    {
        if (RUN.gold < c->price)
        {
            PlaySE(SE_FAILURE);
            ShowMessage(COMPOUND_STRING("Not enough money. The Mart is not\na charity, unlike the Pokémon Center."), TRUE);
            return;
        }
        if (c->kind == CARD_OPTION && c->value == OPT_RELEARN)
        {
            // de Move Relearner rekent pas af als er echt iets geleerd is
            PlaySE(SE_SELECT);
            sCards->relearnPaid = TRUE;
            sCards->giveItem = ITEM_NONE;
            sCards->teachMove = MOVE_NONE;
            sCards->mon = 0;
            sCards->state = STATE_CHOOSE_MON;
            Redraw();
            return;
        }
        RUN.gold -= c->price;
        c->sold = TRUE;
        DrawHeader();
        DrawCard(sCards->card);
    }
    PlaySE(SE_SELECT);
    switch (c->kind)
    {
    case CARD_MOVE:
        StartTeach(c->value);
        break;
    case CARD_ITEM:
        sCards->giveItem = c->value;
        sCards->teachMove = MOVE_NONE;
        sCards->mon = 0;
        sCards->state = STATE_CHOOSE_MON;
        Redraw();
        break;
    case CARD_RELIC:
        Spire_AddRelic(c->value);
        StringCopy(gStringVar1, gSpireRelics[c->value].name);
        StringExpandPlaceholders(gStringVar4, COMPOUND_STRING("You got the {STR_VAR_1}!"));
        ShowMessage(gStringVar4, sCards->mode == SPIRE_CARDS_SHOP);
        break;
    case CARD_MON:
    {
        u32 slot = IsSecondDraft() ? 1 : 0;

        if (sCards->mode == SPIRE_CARDS_EVOLVE)
        {
            GetMonData(&RUN.mons[gSpireEvolveMon], MON_DATA_NICKNAME, gStringVar1);
            Spire_EvolveTo(gSpireEvolveMon, c->value);
            StringCopy(gStringVar2, GetSpeciesName(c->value));
            StringExpandPlaceholders(gStringVar4, COMPOUND_STRING("{STR_VAR_1} evolved into {STR_VAR_2}!"));
            ShowMessage(gStringVar4, FALSE);
            break;
        }

        Spire_SetRental(slot, c->value);
        StringCopy(gStringVar1, GetSpeciesName(c->value));
        StringExpandPlaceholders(gStringVar4, COMPOUND_STRING("{STR_VAR_1} joins you!"));
        ShowMessage(gStringVar4, FALSE);
        break;
    }
    case CARD_OPTION:
        PickOption(c->value);
        break;
    }
}

// --- invoer -----------------------------------------------------------------------------------
static void HandleCards(void)
{
    if (sCards->count == 0)
    {
        if (JOY_NEW(A_BUTTON | B_BUTTON))
            Exit();
        return;
    }
    if (JOY_NEW(DPAD_LEFT) && sCards->card % CARDS_PER_PAGE > 0)
    {
        PlaySE(SE_SELECT);
        sCards->card--;
        Redraw();
    }
    else if (JOY_NEW(DPAD_RIGHT) && sCards->card % CARDS_PER_PAGE + 1 < CARDS_PER_PAGE && sCards->card + 1 < sCards->count)
    {
        PlaySE(SE_SELECT);
        sCards->card++;
        Redraw();
    }
    else if (JOY_NEW(DPAD_UP | DPAD_DOWN) && sCards->count > CARDS_PER_PAGE)
    {
        // ander schap
        PlaySE(SE_SELECT);
        sCards->page ^= 1;
        sCards->card = min(sCards->page * CARDS_PER_PAGE + sCards->card % CARDS_PER_PAGE, sCards->count - 1);
        ShowPage();
        DrawHeader();
        Redraw();
    }
    else if (JOY_NEW(A_BUTTON))
    {
        PickCard();
    }
    else if (JOY_NEW(B_BUTTON) && (sCards->mode == SPIRE_CARDS_MOVES || sCards->mode == SPIRE_CARDS_RELICS || sCards->mode == SPIRE_CARDS_SHOP))
    {
        PlaySE(SE_SELECT);
        Exit();
    }
}

static void HandleChooseMon(void)
{
    if (JOY_NEW(DPAD_LEFT | DPAD_RIGHT))
    {
        PlaySE(SE_SELECT);
        sCards->mon ^= 1;
        Redraw();
    }
    else if (JOY_NEW(A_BUTTON) && sCards->giveItem != ITEM_NONE)
    {
        GiveHeldItem();
    }
    else if (JOY_NEW(A_BUTTON) && sCards->replaceSpecies != SPECIES_NONE)
    {
        PlaySE(SE_SELECT);
        GetMonData(Spire_GetRunMon(sCards->mon), MON_DATA_NICKNAME, gStringVar1);
        if (sCards->replaceSpecies == SPECIES_DITTO)
            Spire_SetSpecialDitto(sCards->mon);
        else
            Spire_SetRental(sCards->mon, sCards->replaceSpecies);
        StringCopy(gStringVar2, GetSpeciesName(sCards->replaceSpecies));
        sCards->replaceSpecies = SPECIES_NONE;
        StringExpandPlaceholders(gStringVar4, COMPOUND_STRING("{STR_VAR_1} goes home. {STR_VAR_2} joins your team!"));
        ShowMessage(gStringVar4, FALSE);
    }
    else if (JOY_NEW(A_BUTTON) && sCards->relearnPaid && sCards->teachMove == MOVE_NONE)
    {
        PlaySE(SE_SELECT);
        BuildRelearnList();
        if (sCards->relearnCount == 0)
        {
            sCards->relearnPaid = FALSE;
            ShowMessage(COMPOUND_STRING("The Relearner shrugs. There is nothing\nto remember. No fee."), TRUE);
        }
        else
        {
            sCards->relearnCursor = 0;
            sCards->state = STATE_RELEARN;
            Redraw();
        }
    }
    else if (JOY_NEW(A_BUTTON))
    {
        struct Pokemon *mon = Spire_GetRunMon(sCards->mon);

        PlaySE(SE_SELECT);
        if (MonKnowsMove(mon, sCards->teachMove))
        {
            GetMonData(mon, MON_DATA_NICKNAME, gStringVar1);
            StringExpandPlaceholders(gStringVar4, COMPOUND_STRING("{STR_VAR_1} already knows it!"));
            ShowMessage(gStringVar4, TRUE);
        }
        else
        {
            u32 i;

            // lege plek? dan meteen leren
            for (i = 0; i < MAX_MON_MOVES; i++)
            {
                if (GetMonData(mon, MON_DATA_MOVE1 + i) == MOVE_NONE)
                    break;
            }
            sCards->slot = (i < MAX_MON_MOVES) ? i : 0;
            sCards->state = STATE_CHOOSE_SLOT;
            Redraw();
        }
    }
    else if (JOY_NEW(B_BUTTON) && sCards->mode != SPIRE_CARDS_EVENT)
    {
        struct SpireCard *c = &sCards->cards[sCards->card];

        PlaySE(SE_SELECT);
        if (sCards->giveItem != ITEM_NONE && c->kind == CARD_ITEM && c->sold)
        {
            // toch niet: geld terug
            RUN.gold += c->price;
            c->sold = FALSE;
            DrawHeader();
            DrawCard(sCards->card);
        }
        sCards->giveItem = ITEM_NONE;
        sCards->relearnPaid = FALSE;
        sCards->state = STATE_CARDS;
        Redraw();
    }
}

static void HandleRelearn(void)
{
    u32 n = sCards->relearnCount, cur = sCards->relearnCursor;

    if (JOY_NEW(DPAD_LEFT) && cur % 2 == 1)
        cur--;
    else if (JOY_NEW(DPAD_RIGHT) && cur % 2 == 0 && cur + 1 < n)
        cur++;
    else if (JOY_NEW(DPAD_UP) && cur >= 2)
        cur -= 2;
    else if (JOY_NEW(DPAD_DOWN) && cur + 2 < n)
        cur += 2;
    else if (JOY_NEW(A_BUTTON))
    {
        PlaySE(SE_SELECT);
        StartTeachTo(sCards->relearnMoves[cur], sCards->mon);
        return;
    }
    else if (JOY_NEW(B_BUTTON))
    {
        PlaySE(SE_SELECT);
        sCards->state = STATE_CHOOSE_MON;
        Redraw();
        return;
    }
    if (cur != sCards->relearnCursor)
    {
        PlaySE(SE_SELECT);
        sCards->relearnCursor = cur;
        Redraw();
    }
}

static void HandleChooseSlot(void)
{
    if (JOY_NEW(DPAD_LEFT | DPAD_RIGHT))
    {
        PlaySE(SE_SELECT);
        sCards->slot ^= 1;
        Redraw();
    }
    else if (JOY_NEW(DPAD_UP | DPAD_DOWN))
    {
        PlaySE(SE_SELECT);
        sCards->slot ^= 2;
        Redraw();
    }
    else if (JOY_NEW(A_BUTTON))
    {
        struct Pokemon *mon = Spire_GetRunMon(sCards->mon);

        PlaySE(SE_RG_BALL_CLICK);
        SetMonMoveSlot(mon, sCards->teachMove, sCards->slot);
        Spire_ClearSlotUpgrade(mon, sCards->slot);
        if (sCards->relearnPaid)
        {
            struct SpireCard *c = &sCards->cards[sCards->card];

            RUN.gold -= min(RUN.gold, c->price);
            RUN.relearns++;
            c->price = 50 + 25 * RUN.relearns;
            sCards->relearnPaid = FALSE;
            DrawHeader();
            DrawCard(sCards->card);
        }
        GetMonData(mon, MON_DATA_NICKNAME, gStringVar1);
        StringCopy(gStringVar2, GetMoveName(sCards->teachMove));
        StringExpandPlaceholders(gStringVar4, COMPOUND_STRING("{STR_VAR_1} learned {STR_VAR_2}!"));
        ShowMessage(gStringVar4, sCards->mode == SPIRE_CARDS_SHOP);
    }
    else if (JOY_NEW(B_BUTTON))
    {
        PlaySE(SE_SELECT);
        sCards->state = STATE_CHOOSE_MON;
        Redraw();
    }
}

static void Task_SpireCards(u8 taskId)
{
    if (gPaletteFade.active)
        return;

    switch (sCards->state)
    {
    case STATE_CARDS:
        HandleCards();
        break;
    case STATE_CHOOSE_MON:
        HandleChooseMon();
        break;
    case STATE_CHOOSE_SLOT:
        HandleChooseSlot();
        break;
    case STATE_RELEARN:
        HandleRelearn();
        break;
    case STATE_MESSAGE:
        if (JOY_NEW(A_BUTTON | B_BUTTON))
        {
            PlaySE(SE_SELECT);
            if (sCards->afterMessage)
            {
                sCards->state = STATE_CARDS;
                Redraw();
            }
            else
            {
                Exit();
            }
        }
        break;
    case STATE_EXIT:
        DestroyTask(taskId);
        CloseScreen();
        break;
    }
}
