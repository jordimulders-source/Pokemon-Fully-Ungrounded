// Project Grounded: The Spire - de run (zie SPIRE_DESIGN.md).
// De run staat in gSaveBlock2Ptr->spire, dus een gepauzeerde run blijft bewaard na opslaan en uitzetten.
// Verloop: Spire_Enter (special) → draft van twee rentals → act-kaart → kamer → beloning → kaart ...
// Na de baas van act 1 en 2 een nieuwe act (rentals evolueren); na de baas van act 3 is de run gewonnen.
#include "global.h"
#include "battle.h"
#include "battle_main.h"
#include "battle_setup.h"
#include "event_data.h"
#include "item.h"
#include "main.h"
#include "move.h"
#include "overworld.h"
#include "palette.h"
#include "pokemon.h"
#include "random.h"
#include "script.h"
#include "sound.h"
#include "spire.h"
#include "string_util.h"
#include "task.h"
#include "constants/battle.h"
#include "constants/items.h"
#include "constants/moves.h"
#include "constants/songs.h"
#include "constants/species.h"

#define RUN SPIRE_SAVE

STATIC_ASSERT(sizeof(struct SpireSave) <= SPIRE_SAVE_SIZE, SpireSaveFitsInSaveBlock2);

EWRAM_DATA struct SpireResult gSpireResult = {0};
EWRAM_DATA static struct Pokemon sSavedParty[PARTY_SIZE] = {0};
EWRAM_DATA static u8 sSavedPartyCount = 0;
EWRAM_DATA static u8 sRoomType = 0;
EWRAM_DATA static u8 sDraftStep = 0;
EWRAM_DATA static u8 sEndMessage[160] = {0};

static void StartRoomBattle(u32 type);
static void CB2_EndSpireBattle(void);
static void NextAct(void);
static void PickBiome(void);

// ---------------------------------------------------------------------------------------------
// Relics

const struct SpireRelicInfo gSpireRelics[SPIRE_RELIC_COUNT] =
{
    [SPIRE_RELIC_BERRY_POUCH] = {ITEM_BERRY_POUCH, COMPOUND_STRING("Berry Pouch"), COMPOUND_STRING("Heal 10% more HP\nafter every battle.")},
    [SPIRE_RELIC_AMULET_COIN] = {ITEM_AMULET_COIN, COMPOUND_STRING("Amulet Coin"), COMPOUND_STRING("Earn 50% more money\nin every battle.")},
    [SPIRE_RELIC_GUARD_SPEC]  = {ITEM_GUARD_SPEC,  COMPOUND_STRING("Guard Spec."), COMPOUND_STRING("DEFEND gives 30%\nmore Block.")},
    [SPIRE_RELIC_DIRE_HIT]    = {ITEM_DIRE_HIT,    COMPOUND_STRING("Dire Hit"),    COMPOUND_STRING("Your Pokémon land\ncritical hits more often.")},
    [SPIRE_RELIC_MUSCLE_BAND] = {ITEM_MUSCLE_BAND, COMPOUND_STRING("Muscle Band"), COMPOUND_STRING("Your Pokémon deal\n10% more damage.")},
    [SPIRE_RELIC_WIDE_LENS]   = {ITEM_WIDE_LENS,   COMPOUND_STRING("Wide Lens"),   COMPOUND_STRING("Your moves that hit\nboth foes lose no power.")},
    [SPIRE_RELIC_SOOTHE_BELL] = {ITEM_SOOTHE_BELL, COMPOUND_STRING("Soothe Bell"), COMPOUND_STRING("Resting at camp heals\n30% more HP.")},
    [SPIRE_RELIC_SACRED_ASH]  = {ITEM_SACRED_ASH,  COMPOUND_STRING("Sacred Ash"),  COMPOUND_STRING("Fainted Pokémon come back\nwith 30% HP, not 1 HP.")},
};

bool32 Spire_RunActive(void)
{
    return RUN.magic == SPIRE_SAVE_MAGIC;
}

bool32 Spire_HasRelic(u32 relic)
{
    return Spire_RunActive() && (RUN.relics & (1u << relic));
}

void Spire_AddRelic(u32 relic)
{
    RUN.relics |= 1u << relic;
}

// Een relic die je nog niet hebt; SPIRE_RELIC_COUNT als je alles al hebt.
u32 Spire_RandomNewRelic(u32 salt)
{
    u32 i, n = 0, pick;

    for (i = 0; i < SPIRE_RELIC_COUNT; i++)
        if (!(RUN.relics & (1u << i)))
            n++;
    if (n == 0)
        return SPIRE_RELIC_COUNT;
    pick = (Random() + salt) % n;
    for (i = 0; i < SPIRE_RELIC_COUNT; i++)
    {
        if (!(RUN.relics & (1u << i)) && pick-- == 0)
            return i;
    }
    return SPIRE_RELIC_COUNT;
}

struct Pokemon *Spire_GetRunMon(u32 i)
{
    return &RUN.mons[i];
}

// ---------------------------------------------------------------------------------------------
// Pools: berekend door tools/grounded/spire/spire_pool.py en encounters.py (zie SPIRE_BALANS.md)

#include "data/spire_pool.h"
#include "data/spire_encounters.h"

// Vasthouditems (winkel, events). Eén per Pokémon; een gebruikt item (Focus Sash, bes) is weg voor de rest van de run.
// Niet in de pool, want nutteloos in de Spire: Red Card, Eject Button/Pack, Shed Shell, Smoke Ball, Exp. Share,
// Lucky Egg, Everstone, evolutie-items (Up-Grade, ...), Destiny Knot, Float Stone, Iron Ball, Lagging Tail, Sticky Barb,
// Ring Target, Full Incense, Macho Brace, Power-items, Cleanse Tag, Amulet Coin/Soothe Bell (die zijn relics).
static const u16 sCommonItems[] =
{
    ITEM_SITRUS_BERRY, ITEM_LUM_BERRY, ITEM_QUICK_CLAW, ITEM_KINGS_ROCK, ITEM_SHELL_BELL, ITEM_BIG_ROOT,
    ITEM_ZOOM_LENS, ITEM_SCOPE_LENS, ITEM_WISE_GLASSES, ITEM_PUNCHING_GLOVE, ITEM_WHITE_HERB, ITEM_MENTAL_HERB,
    ITEM_POWER_HERB, ITEM_AIR_BALLOON, ITEM_PROTECTIVE_PADS, ITEM_METRONOME, ITEM_LIGHT_CLAY, ITEM_BLACK_SLUDGE,
    ITEM_NONE, // = typeversterker die past bij je team (Charcoal, Mystic Water, ...)
};
static const u16 sUncommonItems[] =
{
    ITEM_LIFE_ORB, ITEM_CHOICE_BAND, ITEM_CHOICE_SPECS, ITEM_CHOICE_SCARF, ITEM_ASSAULT_VEST, ITEM_EVIOLITE,
    ITEM_EXPERT_BELT, ITEM_WEAKNESS_POLICY, ITEM_ROCKY_HELMET, ITEM_HEAVY_DUTY_BOOTS, ITEM_COVERT_CLOAK,
    ITEM_CLEAR_AMULET, ITEM_LOADED_DICE, ITEM_THROAT_SPRAY, ITEM_FOCUS_SASH, ITEM_BLUNDER_POLICY,
};
static const u16 sRareItems[] = {ITEM_LEFTOVERS, ITEM_FOCUS_SASH, ITEM_LIFE_ORB, ITEM_ASSAULT_VEST};

static const u16 sTypeBoosters[NUMBER_OF_MON_TYPES] =
{
    [TYPE_NORMAL] = ITEM_SILK_SCARF, [TYPE_FIGHTING] = ITEM_BLACK_BELT, [TYPE_FLYING] = ITEM_SHARP_BEAK,
    [TYPE_POISON] = ITEM_POISON_BARB, [TYPE_GROUND] = ITEM_SOFT_SAND, [TYPE_ROCK] = ITEM_HARD_STONE,
    [TYPE_BUG] = ITEM_SILVER_POWDER, [TYPE_GHOST] = ITEM_SPELL_TAG, [TYPE_STEEL] = ITEM_METAL_COAT,
    [TYPE_FIRE] = ITEM_CHARCOAL, [TYPE_WATER] = ITEM_MYSTIC_WATER, [TYPE_GRASS] = ITEM_MIRACLE_SEED,
    [TYPE_ELECTRIC] = ITEM_MAGNET, [TYPE_PSYCHIC] = ITEM_TWISTED_SPOON, [TYPE_ICE] = ITEM_NEVER_MELT_ICE,
    [TYPE_DRAGON] = ITEM_DRAGON_FANG, [TYPE_DARK] = ITEM_BLACK_GLASSES, [TYPE_FAIRY] = ITEM_FAIRY_FEATHER,
};

u16 Spire_RandomHeldItem(u32 rarity, u32 salt)
{
    u32 r = Random() + salt * 11;
    u16 item;

    switch (rarity)
    {
    case 2:  item = sRareItems[r % ARRAY_COUNT(sRareItems)]; break;
    case 1:  item = sUncommonItems[r % ARRAY_COUNT(sUncommonItems)]; break;
    default: item = sCommonItems[r % ARRAY_COUNT(sCommonItems)]; break;
    }
    if (item == ITEM_NONE)
    {
        u16 species = GetMonData(&RUN.mons[(r >> 4) & 1], MON_DATA_SPECIES);
        u32 type = GetSpeciesType(species, (r >> 5) & 1);

        item = type < NUMBER_OF_MON_TYPES && sTypeBoosters[type] ? sTypeBoosters[type] : ITEM_CHARCOAL;
    }
    return item;
}

// Beschrijving van een vasthouditem in de Spire (waar de Spire het item anders laat werken).
static const u8 sDesc_LifeOrb[] = _("Moves hit 30% harder. Each\nattack costs 2% of max HP.");
static const u8 sDesc_FocusSash[] = _("Survive one knockout hit with\n1 HP, at any HP. Then it is gone.");
static const u8 sDesc_Leftovers[] = _("Heals 1/32 of max HP every\nturn. Very strong. Very rare.");

const u8 *Spire_GetItemDescription(u16 item)
{
    switch (item)
    {
    case ITEM_LIFE_ORB:   return sDesc_LifeOrb;
    case ITEM_FOCUS_SASH: return sDesc_FocusSash;
    case ITEM_LEFTOVERS:  return sDesc_Leftovers;
    default:              return GetItemDescription(item);
    }
}

bool32 Spire_IsMoveBanned(u16 move)
{
    u32 i;

    for (i = 0; i < ARRAY_COUNT(sSpireBannedMoves); i++)
        if (sSpireBannedMoves[i] == move)
            return TRUE;
    return FALSE;
}

static const u16 *const sMovePools[] = {sSpireCommonMoves, sSpireUncommonMoves, sSpireRareMoves};
static const u16 sMovePoolSizes[] = {ARRAY_COUNT(sSpireCommonMoves), ARRAY_COUNT(sSpireUncommonMoves), ARRAY_COUNT(sSpireRareMoves)};

u16 Spire_RandomMove(u32 rarity, u32 salt)
{
    rarity = min(rarity, 2);
    return sMovePools[rarity][(Random() + salt * 7) % sMovePoolSizes[rarity]];
}

// Een move van dit type (TYPE_NONE = alles); geen move van dit type in de pool, dan een willekeurige.
u16 Spire_RandomMoveOfType(u32 rarity, u32 type, u32 salt)
{
    const u16 *pool;
    u32 i, n = 0, pick;

    rarity = min(rarity, 2);
    pool = sMovePools[rarity];
    if (type != TYPE_NONE)
    {
        for (i = 0; i < sMovePoolSizes[rarity]; i++)
            if (GetMoveType(pool[i]) == type)
                n++;
    }
    if (n == 0)
        return Spire_RandomMove(rarity, salt);
    pick = (Random() + salt * 7) % n;
    for (i = 0; i < sMovePoolSizes[rarity]; i++)
        if (GetMoveType(pool[i]) == type && pick-- == 0)
            return pool[i];
    return Spire_RandomMove(rarity, salt);
}

// Draft: kans per tier (C, B, A, S), zoals de zeldzaamheid van kaarten.
static const u8 sTierChance[] = {35, 35, 22, 8};

u16 Spire_RandomRental(u32 salt)
{
    u32 roll = (Random() + salt * 31) % 100, tier = 0, i, n = 0, pick;

    while (tier < 3 && roll >= sTierChance[tier])
        roll -= sTierChance[tier++];
    for (i = 0; i < ARRAY_COUNT(sSpireRentals); i++)
        if (sSpireRentals[i].tier == tier)
            n++;
    pick = (Random() + salt * 13) % (n ? n : 1);
    for (i = 0; i < ARRAY_COUNT(sSpireRentals); i++)
        if (sSpireRentals[i].tier == tier && pick-- == 0)
            return sSpireRentals[i].species;
    return sSpireRentals[0].species;
}

u16 Spire_RandomEventRental(u32 salt)
{
    return sSpireEventRentals[(Random() + salt) % ARRAY_COUNT(sSpireEventRentals)].species;
}

const struct SpireRental *Spire_FindRental(u16 species)
{
    u32 i;

    for (i = 0; i < ARRAY_COUNT(sSpireRentals); i++)
        if (sSpireRentals[i].species == species)
            return &sSpireRentals[i];
    for (i = 0; i < ARRAY_COUNT(sSpireEventRentals); i++)
        if (sSpireEventRentals[i].species == species)
            return &sSpireEventRentals[i];
    return NULL;
}

// Max-HP-percentage van een rental: x4 plus blijvende event-effecten (bijv. -10).
u32 Spire_PlayerHpPercent(u32 i)
{
    s32 pct = SPIRE_HP_PLAYER + 4 * RUN.hpBonus[i];

    return pct < 100 ? 100 : pct;
}

// Rental: lv 100 met de startkit uit de rekensheet (STAB 40-50, [STAB], statusmove, grounded move).
void Spire_SetRental(u32 slot, u16 species)
{
    struct Pokemon *mon = &RUN.mons[slot];
    const struct SpireRental *rental = Spire_FindRental(species);
    static const u16 sFallback[MAX_MON_MOVES] = {MOVE_TACKLE, MOVE_GROWL, MOVE_NONE, MOVE_NONE};

    Spire_CreateMon(mon, species, SPIRE_LEVEL, 31, 84, rental ? rental->moves : sFallback);
    RUN.hpBonus[slot] = 0;
    Spire_ScaleMonHp(mon, Spire_PlayerHpPercent(slot));
}

// Event 'A VERY SPECIAL DITTO' (Jordi): shiny, 31 IV, Imposter, Choice Scarf.
void Spire_SetSpecialDitto(u32 slot)
{
    struct Pokemon *mon = &RUN.mons[slot];
    static const u16 sMoves[MAX_MON_MOVES] = {MOVE_TRANSFORM};
    u32 abilityNum = 2, shiny = TRUE;
    u16 item = ITEM_CHOICE_SCARF;

    Spire_CreateMon(mon, SPECIES_DITTO, SPIRE_LEVEL, 31, 84, sMoves);
    if (GetSpeciesAbility(SPECIES_DITTO, 2) != ABILITY_IMPOSTER)
        abilityNum = (GetSpeciesAbility(SPECIES_DITTO, 1) == ABILITY_IMPOSTER) ? 1 : 0;
    SetMonData(mon, MON_DATA_ABILITY_NUM, &abilityNum);
    SetMonData(mon, MON_DATA_IS_SHINY, &shiny);
    SetMonData(mon, MON_DATA_HELD_ITEM, &item);
    RUN.hpBonus[slot] = 0;
    Spire_ScaleMonHp(mon, Spire_PlayerHpPercent(slot));
}

// ---------------------------------------------------------------------------------------------
// Kaart van een act: SPIRE_FLOORS verdiepingen met 2-4 kamers, daarboven de baas.

static u32 Lcg(u32 *state)
{
    *state = *state * 1103515245 + 12345;
    return (*state >> 16) & 0x7FFF;
}

void Spire_GenerateMap(struct SpireActMap *map, u32 seed)
{
    u32 f, i, j, st = seed;

    for (f = 0; f < SPIRE_FLOORS; f++)
    {
        u32 n = (f == 0) ? 3 : (f == SPIRE_FLOORS - 1) ? 2 : 2 + Lcg(&st) % 3;

        map->count[f] = n;
        for (i = 0; i < n; i++)
        {
            struct SpireMapNode *node = &map->nodes[f][i];
            u32 r = Lcg(&st) % 100;

            node->x = 18 + (132 * (2 * i + 1)) / (2 * n) + (Lcg(&st) % 9) - 4;
            node->links = 0;
            if (f == 0)
                node->type = SPIRE_ROOM_FIGHT;
            else if (f == SPIRE_FLOORS - 1)
                node->type = SPIRE_ROOM_REST;
            else if (r < 45)
                node->type = SPIRE_ROOM_FIGHT;
            else if (r < 65)
                node->type = SPIRE_ROOM_EVENT;
            else if (r < 80 && f >= 2)
                node->type = SPIRE_ROOM_ELITE;
            else if (r < 90)
                node->type = SPIRE_ROOM_SHOP;
            else if (f >= 3)
                node->type = SPIRE_ROOM_REST;
            else
                node->type = SPIRE_ROOM_FIGHT;
        }
    }
    // verbindingen zonder kruisingen: kamer i gaat naar j0(i) (oplopend met i) en soms ook naar j0(i)+1,
    // maar alleen als de volgende kamer daar niet onder begint. Losse kamers krijgen een buur van links.
    for (f = 0; f + 1 < SPIRE_FLOORS; f++)
    {
        u32 n0 = map->count[f], n1 = map->count[f + 1];
        u8 j0s[SPIRE_MAX_NODES];
        u8 incoming = 0;

        for (i = 0; i < n0; i++)
            j0s[i] = (n0 == 1) ? 0 : (i * (n1 - 1) + (n0 - 1) / 2) / (n0 - 1);
        for (i = 0; i < n0; i++)
        {
            map->nodes[f][i].links |= 1u << j0s[i];
            if (j0s[i] + 1 < n1 && (i + 1 >= n0 || j0s[i + 1] > j0s[i]) && Lcg(&st) % 2)
                map->nodes[f][i].links |= 1u << (j0s[i] + 1);
            incoming |= map->nodes[f][i].links;
        }
        for (j = 0; j < n1; j++)
        {
            if (!(incoming & (1u << j)))
            {
                // de laatste kamer links van j (j0 < j) neemt hem erbij; anders de eerste
                u32 from = 0;

                for (i = 0; i < n0; i++)
                    if (j0s[i] < j)
                        from = i;
                map->nodes[f][from].links |= 1u << j;
            }
        }
    }
}

static u32 PathNode(u32 floor)
{
    return (RUN.path >> (2 * floor)) & 3;
}

// Kun je deze kamer nu kiezen? RUN.floor = aantal afgeronde verdiepingen in deze act.
bool32 Spire_IsReachable(const struct SpireActMap *map, u32 floor, u32 node)
{
    if (floor != RUN.floor || node >= map->count[floor])
        return FALSE;
    if (floor == 0)
        return TRUE;
    return (map->nodes[floor - 1][PathNode(floor - 1)].links & (1u << node)) != 0;
}

// ---------------------------------------------------------------------------------------------
// Run starten, pauzeren, beëindigen

static void SaveParty(void)
{
    u32 i;

    for (i = 0; i < PARTY_SIZE; i++)
        sSavedParty[i] = gPlayerParty[i];
    sSavedPartyCount = gPlayerPartyCount;
}

static void RestoreParty(void)
{
    u32 i;

    for (i = 0; i < PARTY_SIZE; i++)
        gPlayerParty[i] = sSavedParty[i];
    gPlayerPartyCount = sSavedPartyCount;
}

void Spire_ReturnToField(void)
{
    SetMainCallback2(CB2_ReturnToFieldContinueScriptPlayMapMusic);
}

static void AwardBP(void)
{
    u32 bp = gSaveBlock2Ptr->frontier.battlePoints + RUN.bp;

    gSaveBlock2Ptr->frontier.battlePoints = bp > 9999 ? 9999 : bp;
}

static void EndRun(bool32 won)
{
    u32 bp = RUN.bp;

    AwardBP();
    if (won)
        RUN.runsWon++;
    RUN.magic = 0;
    ConvertIntToDecimalStringN(gStringVar1, bp, STR_CONV_MODE_LEFT_ALIGN, 4);
    ConvertIntToDecimalStringN(gStringVar2, RUN.act, STR_CONV_MODE_LEFT_ALIGN, 1);
    if (won)
        StringExpandPlaceholders(sEndMessage, COMPOUND_STRING("You conquered the Spire!\nYou earned {STR_VAR_1} BP."));
    else
        StringExpandPlaceholders(sEndMessage, COMPOUND_STRING("Your run ended in act {STR_VAR_2}.\nYou earned {STR_VAR_1} BP. The tower keeps the rest."));
    Spire_OpenMessage(won ? COMPOUND_STRING("THE SPIRE IS YOURS!") : COMPOUND_STRING("RUN OVER"), sEndMessage, Spire_ReturnToField);
}

static void NewRun(void)
{
    u8 runsWon = RUN.runsWon;

    memset(&RUN, 0, sizeof(RUN));
    RUN.runsWon = runsWon;
    ZeroMonData(&RUN.mons[0]);
    ZeroMonData(&RUN.mons[1]);
    RUN.magic = SPIRE_SAVE_MAGIC;
    RUN.act = 1;
    RUN.floor = 0;
    RUN.seed = Random32();
    PickBiome();
    sDraftStep = 0;
}

static void DraftDone(void)
{
    Spire_OpenMap();
}

// special: vanuit een script (lockall; special Spire_Enter; waitstate; releaseall)
void Spire_Enter(void)
{
    CleanupOverworldWindowsAndTilemaps();
    if (!Spire_RunActive())
    {
        NewRun();
        Spire_OpenDraft(DraftDone); // tien rentals, kies er twee
    }
    else if (RUN.inRoom)
    {
        Spire_EnterRoom(RUN.floor, RUN.node);
    }
    else
    {
        Spire_OpenMap();
    }
}

// Debug (testscripts): VAR_0x8004 = 0 rustplek, 1 winkel, 2 event, 3 kaart, 4 elite, 5 baas. Zonder run: snelle run met twee rentals.
void Spire_DebugOpen(void)
{
    CleanupOverworldWindowsAndTilemaps();
    if (!Spire_RunActive())
    {
        NewRun();
        Spire_SetRental(0, Spire_RandomRental(1));
        Spire_SetRental(1, Spire_RandomRental(2));
    }
    switch (gSpecialVar_0x8004)
    {
    case 0:  Spire_OpenRest(Spire_ReturnToField); break;
    case 1:  Spire_OpenShop(Spire_ReturnToField); break;
    case 2:  gSpireForcedEvent = gSpecialVar_0x8005; Spire_OpenEvent(Spire_ReturnToField); break;
    case 4:  RUN.floor = 3; RUN.inRoom = TRUE; sRoomType = SPIRE_ROOM_ELITE; StartRoomBattle(SPIRE_ROOM_ELITE); break;
    case 5:  RUN.floor = SPIRE_FLOORS; RUN.inRoom = TRUE; sRoomType = SPIRE_ROOM_BOSS; StartRoomBattle(SPIRE_ROOM_BOSS); break;
    default: Spire_OpenMap(); break;
    }
}

void Spire_ResetRun(void)
{
    RUN.magic = 0;
}

void Spire_SuspendRun(void)
{
    Spire_OpenMessage(COMPOUND_STRING("RUN PAUSED"),
                      COMPOUND_STRING("Your run is waiting for you.\nSave the game to keep it."), Spire_ReturnToField);
}

void Spire_GiveUpRun(void)
{
    EndRun(FALSE);
}

// specials voor de receptioniste: VAR_RESULT = TRUE als er een run loopt; opgeven vanuit de lobby
void Spire_IsRunActive(void)
{
    gSpecialVar_Result = Spire_RunActive();
}

void Spire_GiveUpFromField(void)
{
    CleanupOverworldWindowsAndTilemaps();
    EndRun(FALSE);
}

// ---------------------------------------------------------------------------------------------
// Rentals: heal, PP, evolutie

void Spire_HealRun(u32 percent)
{
    u32 i;

    for (i = 0; i < 2; i++)
    {
        struct Pokemon *mon = &RUN.mons[i];
        u32 hp = GetMonData(mon, MON_DATA_HP), maxHp = GetMonData(mon, MON_DATA_MAX_HP);

        if (hp == 0)
            hp = Spire_HasRelic(SPIRE_RELIC_SACRED_ASH) ? maxHp * 30 / 100 : 1;
        else
            hp = min(maxHp, hp + maxHp * percent / 100);
        SetMonData(mon, MON_DATA_HP, &hp);
        if (percent >= SPIRE_REST_HEAL)
        {
            u32 status = 0;
            SetMonData(mon, MON_DATA_STATUS, &status);
        }
    }
}

void Spire_RestorePP(void)
{
    u32 i, j;

    for (i = 0; i < 2; i++)
    {
        for (j = 0; j < MAX_MON_MOVES; j++)
        {
            u32 move = GetMonData(&RUN.mons[i], MON_DATA_MOVE1 + j);
            u32 pp = CalculatePPWithBonus(move, GetMonData(&RUN.mons[i], MON_DATA_PP_BONUSES), j);
            SetMonData(&RUN.mons[i], MON_DATA_PP1 + j, &pp);
        }
    }
}

// Evoluties in de Spire (uit de rekensheet): max 3 keuzes; bij meer dan één kiest de speler.
u32 Spire_GetEvolutions(u16 species, u16 *targets)
{
    u32 i, j, n = 0;

    for (i = 0; i < ARRAY_COUNT(sSpireEvolutions); i++)
    {
        if (sSpireEvolutions[i].species != species)
            continue;
        for (j = 0; j < 3; j++)
            if (sSpireEvolutions[i].targets[j] != SPECIES_NONE)
                targets[n++] = sSpireEvolutions[i].targets[j];
        break;
    }
    return n;
}

bool32 Spire_CanEvolve(u32 i)
{
    u16 targets[3];

    return Spire_GetEvolutions(GetMonData(&RUN.mons[i], MON_DATA_SPECIES), targets) != 0;
}

// Evolueren met behoud van HP-verhouding (x4 HP en event-effecten blijven).
void Spire_EvolveTo(u32 i, u16 target)
{
    struct Pokemon *mon = &RUN.mons[i];
    u32 hp = GetMonData(mon, MON_DATA_HP), maxHp = GetMonData(mon, MON_DATA_MAX_HP), newHp;
    u8 nick[POKEMON_NAME_LENGTH + 1];

    if (target == SPECIES_NONE)
        return;
    // rentals hebben geen bijnaam: de naam evolueert mee (anders heet een Charmeleon nog Charmander)
    GetMonData(mon, MON_DATA_NICKNAME, nick);
    if (StringCompare(nick, GetSpeciesName(GetMonData(mon, MON_DATA_SPECIES))) == 0)
        SetMonData(mon, MON_DATA_NICKNAME, GetSpeciesName(target));
    SetMonData(mon, MON_DATA_SPECIES, &target);
    CalculateMonStats(mon);
    Spire_ScaleMonHp(mon, Spire_PlayerHpPercent(i));
    newHp = GetMonData(mon, MON_DATA_MAX_HP) * hp / (maxHp ? maxHp : 1);
    if (newHp == 0 && hp != 0)
        newHp = 1;
    SetMonData(mon, MON_DATA_HP, &newHp);
}

void Spire_Evolve(u32 i)
{
    u16 targets[3];

    if (Spire_GetEvolutions(GetMonData(&RUN.mons[i], MON_DATA_SPECIES), targets))
        Spire_EvolveTo(i, targets[0]);
}

// ---------------------------------------------------------------------------------------------
// Kamers

void Spire_EnterRoom(u32 floor, u32 node)
{
    struct SpireActMap map;
    u32 type;

    Spire_GenerateMap(&map, RUN.seed);
    if (floor >= SPIRE_FLOORS)
        type = SPIRE_ROOM_BOSS;
    else
        type = map.nodes[floor][node].type;
    RUN.floor = floor;
    RUN.node = node;
    RUN.inRoom = TRUE;
    sRoomType = type;

    switch (type)
    {
    case SPIRE_ROOM_FIGHT:
    case SPIRE_ROOM_ELITE:
    case SPIRE_ROOM_BOSS:
        StartRoomBattle(type);
        break;
    case SPIRE_ROOM_REST:
        Spire_OpenRest(Spire_RoomFinished);
        break;
    case SPIRE_ROOM_SHOP:
        Spire_OpenShop(Spire_RoomFinished);
        break;
    default:
        Spire_OpenEvent(Spire_RoomFinished);
        break;
    }
}

void Spire_RoomFinished(void)
{
    RUN.inRoom = FALSE;
    if (RUN.floor < SPIRE_FLOORS)
        RUN.path = (RUN.path & ~(3u << (2 * RUN.floor))) | (RUN.node << (2 * RUN.floor));
    RUN.floor++;
    if (RUN.floor > SPIRE_FLOORS)
        NextAct();
    else
        Spire_OpenMap();
}

// Na de baas van act 1 en 2 evolueert elke rental die dat kan (Jordi: Gible -> Gabite -> Garchomp).
// Bij een vertakking (Eevee, Kirlia, Gloom, ...) kiest de speler op het kaartenscherm.
EWRAM_DATA u8 gSpireEvolveMon = 0;
EWRAM_DATA static u8 sEvolveStep = 0;

static void ContinueActEvolutions(void);

static void AppendEvolved(u32 i, const u8 *oldName)
{
    StringAppend(sEndMessage, COMPOUND_STRING("\n"));
    StringAppend(sEndMessage, oldName);
    StringAppend(sEndMessage, COMPOUND_STRING(" became "));
    StringAppend(sEndMessage, GetSpeciesName(GetMonData(&RUN.mons[i], MON_DATA_SPECIES)));
    StringAppend(sEndMessage, COMPOUND_STRING("!"));
}

// aangeroepen door het kaartenscherm na de keuze (de evolutie is dan al gedaan)
void Spire_EvolveChoiceDone(void)
{
    sEvolveStep++;
    ContinueActEvolutions();
}

static void ContinueActEvolutions(void)
{
    while (sEvolveStep < 2)
    {
        u32 i = sEvolveStep;
        u16 targets[3];
        u32 n = Spire_GetEvolutions(GetMonData(&RUN.mons[i], MON_DATA_SPECIES), targets);

        if (n > 1)
        {
            gSpireEvolveMon = i;
            Spire_OpenCards(SPIRE_CARDS_EVOLVE, Spire_EvolveChoiceDone);
            return;
        }
        if (n == 1)
        {
            u8 nick[POKEMON_NAME_LENGTH + 1];

            GetMonData(&RUN.mons[i], MON_DATA_NICKNAME, nick);
            Spire_EvolveTo(i, targets[0]);
            AppendEvolved(i, nick);
        }
        sEvolveStep++;
    }
    ConvertIntToDecimalStringN(gStringVar1, RUN.act, STR_CONV_MODE_LEFT_ALIGN, 1);
    StringCopy(gStringVar2, gSpireBiomes[RUN.biome].name);
    StringExpandPlaceholders(gStringVar4, COMPOUND_STRING("ACT {STR_VAR_1}: {STR_VAR_2}"));
    Spire_OpenMessage(gStringVar4, sEndMessage, Spire_OpenMap);
}

// Biome van een act: één van de biomes van die act, op de seed.
static void PickBiome(void)
{
    u32 i, n = 0, pick;

    for (i = 0; i < SPIRE_BIOME_COUNT; i++)
        if (gSpireBiomes[i].act == RUN.act)
            n++;
    pick = (RUN.seed >> 4) % (n ? n : 1);
    for (i = 0; i < SPIRE_BIOME_COUNT; i++)
        if (gSpireBiomes[i].act == RUN.act && pick-- == 0)
            RUN.biome = i;
    RUN.usedEncounters = 0;
}

static void NextAct(void)
{
    if (RUN.act >= SPIRE_ACTS)
    {
        EndRun(TRUE);
        return;
    }
    RUN.act++;
    RUN.floor = 0;
    RUN.path = 0;
    RUN.seed = Random32();
    PickBiome();
    StringCopy(sEndMessage, gSpireBiomes[RUN.biome].desc);
    Spire_HealRun(SPIRE_REST_HEAL);
    Spire_RestorePP();
    sEvolveStep = 0;
    ContinueActEvolutions();
}

// ---------------------------------------------------------------------------------------------
// Gevechten

// Baas van deze act: één uit de bazen van de act, op de seed.
static const struct SpireEncounter *GetBoss(void)
{
    u32 i, n = 0, pick;

    for (i = 0; i < ARRAY_COUNT(sSpireBosses); i++)
        if (sSpireBosses[i].biome == RUN.act)
            n++;
    pick = (RUN.seed >> 8) % (n ? n : 1);
    for (i = 0; i < ARRAY_COUNT(sSpireBosses); i++)
        if (sSpireBosses[i].biome == RUN.act && pick-- == 0)
            return &sSpireBosses[i];
    return &sSpireBosses[0];
}

u16 Spire_GetBossSpecies(void)
{
    return GetBoss()->foes[0].species;
}

// Ontmoeting voor deze kamer: vast op de seed (pauzeren en terugkomen = dezelfde vijanden),
// verdieping 1-2 uit de zwakke pool, daarna gewoon; elites apart. Niet twee keer dezelfde in een act.
static u32 PickEncounter(u32 type)
{
    u32 kind = (type == SPIRE_ROOM_ELITE) ? SPIRE_ENC_ELITE : (RUN.floor < 2) ? SPIRE_ENC_WEAK : SPIRE_ENC_NORMAL;
    u32 i, n = 0, local = 0, pick, fresh = 0;
    u32 st = RUN.seed ^ (RUN.floor * 0x9E3779B1) ^ (RUN.node * 0x85EBCA6B);

    for (i = 0; i < ARRAY_COUNT(sSpireEncounters); i++)
    {
        if (sSpireEncounters[i].biome != RUN.biome)
            continue;
        if (sSpireEncounters[i].kind == kind)
        {
            n++;
            if (!(RUN.usedEncounters & (1u << local)))
                fresh++;
        }
        local++;
    }
    pick = (st >> 7) % (fresh ? fresh : (n ? n : 1));
    local = 0;
    for (i = 0; i < ARRAY_COUNT(sSpireEncounters); i++)
    {
        if (sSpireEncounters[i].biome != RUN.biome)
            continue;
        if (sSpireEncounters[i].kind == kind && (!fresh || !(RUN.usedEncounters & (1u << local))) && pick-- == 0)
            return i;
        local++;
    }
    return 0;
}

static void MarkEncounterUsed(u32 index)
{
    u32 i, local = 0;

    for (i = 0; i < index; i++)
        if (sSpireEncounters[i].biome == sSpireEncounters[index].biome)
            local++;
    if (local < 16)
        RUN.usedEncounters |= 1u << local;
}

EWRAM_DATA static s16 sEncounterIndex = 0;
EWRAM_DATA u8 gSpireStartingStatus = 0;
EWRAM_DATA u8 gSpireEnvironment = 0;

static u32 AbilitySlot(u16 species, u16 ability)
{
    u32 i;

    for (i = 0; i < NUM_ABILITY_SLOTS; i++)
        if (GetSpeciesAbility(species, i) == ability)
            return i;
    return 0;
}

static void CreateFoe(u32 partyIndex, const struct SpireFoe *foe)
{
    struct Pokemon *mon = &gEnemyParty[partyIndex];
    u32 battler = partyIndex == 0 ? B_POSITION_OPPONENT_LEFT : B_POSITION_OPPONENT_RIGHT;
    u32 i;

    Spire_CreateMon(mon, foe->species, SPIRE_LEVEL, 20, 0, foe->moves[0] != MOVE_NONE ? foe->moves : NULL);
    // vrije moves (zonder lijst): verboden moves eruit
    for (i = 0; i < MAX_MON_MOVES; i++)
        if (Spire_IsMoveBanned(GetMonData(mon, MON_DATA_MOVE1 + i)))
            SetMonMoveSlot(mon, MOVE_NONE, i);
    if (foe->ability != ABILITY_NONE)
    {
        u32 slot = AbilitySlot(foe->species, foe->ability);
        SetMonData(mon, MON_DATA_ABILITY_NUM, &slot);
    }
    if (foe->item != ITEM_NONE)
        SetMonData(mon, MON_DATA_HELD_ITEM, &foe->item);
    if (foe->gimmick == SPIRE_GIMMICK_HIDDEN)
        gSpireHiddenIntent |= 1u << partyIndex;
    if (foe->gimmick == SPIRE_GIMMICK_SLEEP)
    {
        u32 status = STATUS1_SLEEP_TURN(3);
        SetMonData(mon, MON_DATA_STATUS, &status);
    }
    gSpireEnemyHp[partyIndex] = foe->hp * 10;
    for (i = 0; i < 8; i++)
        gSpirePattern[partyIndex][i] = foe->pattern[i];
    gSpirePatternStep[partyIndex] = 0;
    // totem-aura (STAT_ATK ... STAT_SPDEF)
    memset(&gQueuedStatBoosts[battler], 0, sizeof(gQueuedStatBoosts[battler]));
    for (i = 0; i < 5; i++)
    {
        if (foe->boosts[i] != 0)
        {
            gQueuedStatBoosts[battler].stats |= (1 << i) | 0x80;
            gQueuedStatBoosts[battler].statChanges[i] = foe->boosts[i];
        }
    }
}

// Events: sporen (de Pokémon begint dit gevecht in slaap) en Toxic Spikes (3 gevechten lang 40% kans op gif;
// Poison- en Steel-types en Heavy-Duty Boots zijn veilig).
static void ApplyEventEffects(void)
{
    u32 i;

    for (i = 0; i < 2; i++)
    {
        struct Pokemon *mon = &gPlayerParty[i];
        u16 species = GetMonData(mon, MON_DATA_SPECIES);
        u32 status = GetMonData(mon, MON_DATA_STATUS);

        if (GetMonData(mon, MON_DATA_HP) == 0 || status != 0)
            continue;
        if (RUN.fungalMask & (1 << i))
        {
            status = STATUS1_SLEEP_TURN(2);
        }
        else if (RUN.toxicFights && GetMonData(mon, MON_DATA_HELD_ITEM) != ITEM_HEAVY_DUTY_BOOTS
              && GetSpeciesType(species, 0) != TYPE_POISON && GetSpeciesType(species, 1) != TYPE_POISON
              && GetSpeciesType(species, 0) != TYPE_STEEL && GetSpeciesType(species, 1) != TYPE_STEEL
              && Random() % 100 < 40)
        {
            status = STATUS1_POISON;
        }
        SetMonData(mon, MON_DATA_STATUS, &status);
    }
    RUN.fungalMask = 0;
    if (RUN.toxicFights)
        RUN.toxicFights--;
}

static void StartEncounter(const struct SpireEncounter *enc, u32 song)
{
    u32 i;

    ZeroEnemyPartyMons();
    memset(gQueuedStatBoosts, 0, sizeof(gQueuedStatBoosts));
    gSpireHiddenIntent = 0;
    for (i = 0; i < PARTY_SIZE; i++)
    {
        gSpireEnemyHp[i] = 100;
        gSpirePattern[i][0] = 0;
    }
    for (i = 0; i < 2; i++)
        if (enc->foes[i].species != SPECIES_NONE)
            CreateFoe(i, &enc->foes[i]);
    gSpireStartingStatus = enc->field;

    SaveParty();
    ZeroPlayerPartyMons();
    gPlayerParty[0] = RUN.mons[0];
    gPlayerParty[1] = RUN.mons[1];
    CalculatePlayerPartyCount();
    ApplyEventEffects();

    gSpireBattle = TRUE;
    gSpireAct = RUN.act;
    Spire_ClearBlocks();
    gBattleTypeFlags = BATTLE_TYPE_DOUBLE;
    // achtergrond van het biome; bazen in een eigen arena
    if (enc->kind == SPIRE_ENC_BOSS)
        gSpireEnvironment = (RUN.act == 1) ? BATTLE_ENVIRONMENT_LEADER : (RUN.act == 2) ? BATTLE_ENVIRONMENT_CHAMPION : BATTLE_ENVIRONMENT_RAYQUAZA;
    else
        gSpireEnvironment = Spire_GetBiomeEnvironment();
    gMain.savedCallback = CB2_EndSpireBattle;
    PlayMapChosenOrBattleBGM(song);
    SetMainCallback2(CB2_InitBattle);
}

static void StartRoomBattle(u32 type)
{
    if (type == SPIRE_ROOM_BOSS)
    {
        sEncounterIndex = -1;
        StartEncounter(GetBoss(), MUS_VS_FRONTIER_BRAIN);
    }
    else
    {
        sEncounterIndex = PickEncounter(type);
        StartEncounter(&sSpireEncounters[sEncounterIndex], type == SPIRE_ROOM_ELITE ? MUS_VS_ELITE_FOUR : MUS_VS_WILD);
    }
}

// Event 'A FAINTED ACE': het gevecht na het zoeken (telt als elite: relic + moves)
void Spire_StartEventFight(void)
{
    sRoomType = SPIRE_ROOM_ELITE;
    StartRoomBattle(SPIRE_ROOM_ELITE);
}

static void RewardMoves(void)
{
    Spire_OpenCards(SPIRE_CARDS_MOVES, Spire_RoomFinished);
}

static void CB2_EndSpireBattle(void)
{
    u32 i, gold, heal;

    for (i = 0; i < 2; i++)
        RUN.mons[i] = gPlayerParty[i];
    gSpireBattle = FALSE;
    Spire_ClearBlocks();
    RestoreParty();
    PlayNewMapMusic(MUS_B_TOWER);

    if (gBattleOutcome == B_OUTCOME_RAN || gBattleOutcome == B_OUTCOME_PLAYER_TELEPORTED)
    {
        // RUN in een gevecht = pauzeren; de kamer begint opnieuw als je terugkomt
        Spire_SuspendRun();
        return;
    }
    if (gBattleOutcome != B_OUTCOME_WON)
    {
        EndRun(FALSE);
        return;
    }

    if (sEncounterIndex >= 0)
        MarkEncounterUsed(sEncounterIndex);
    heal = SPIRE_HEAL_AFTER + (Spire_HasRelic(SPIRE_RELIC_BERRY_POUCH) ? 10 : 0);
    Spire_HealRun(heal);
    switch (sRoomType)
    {
    case SPIRE_ROOM_BOSS:  gold = 80; gSpireResult.bp = 10; break;
    case SPIRE_ROOM_ELITE: gold = 35 + Random() % 11; gSpireResult.bp = 3; break;
    default:               gold = 15 + Random() % 11; gSpireResult.bp = 1; break;
    }
    if (Spire_HasRelic(SPIRE_RELIC_AMULET_COIN))
        gold = gold * 3 / 2;
    gSpireResult.bp *= RUN.act;
    gSpireResult.gold = gold;
    gSpireResult.healPercent = heal;
    RUN.gold = min(9999, RUN.gold + gold);
    RUN.bp += gSpireResult.bp;

    if (sRoomType == SPIRE_ROOM_ELITE || sRoomType == SPIRE_ROOM_BOSS)
        Spire_OpenCards(SPIRE_CARDS_RELICS, RewardMoves);
    else
        RewardMoves();
}
