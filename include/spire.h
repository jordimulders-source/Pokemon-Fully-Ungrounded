#ifndef GUARD_SPIRE_H
#define GUARD_SPIRE_H

// Project Grounded: The Spire (roguelike-faciliteit, zie SPIRE_DESIGN.md)
//   src/spire.c         gevechtsmechaniek (×HP, DEFEND/blok, intenties)
//   src/spire_run.c     run-state (SaveBlock2), kaartgeneratie, kamers, relics, acts
//   src/spire_map.c     act-kaart
//   src/spire_cards.c   kaartenscherm (beloning: moves/relics, vertakte evolutie, berichten)

#define B_ACTION_SPIRE_DEFEND   22

// DEFEND-doel (bitmasker per battler aan eigen kant)
#define SPIRE_DEFEND_BOTH       0xFF

// HP-vermenigvuldiger van de speler in procenten (vijanden: per ontmoeting, zie src/data/spire_encounters.h)
#define SPIRE_HP_PLAYER         400
#define SPIRE_LEVEL             100 // Jordi: alles in de Spire is lv 100, level is geen knop

// Blok = 15% van max HP x verdedigingsfactor x act-factor; verdeeld over beide = 60% elk
#define SPIRE_BLOCK_PERCENT     15
#define SPIRE_BLOCK_SPLIT       60

#define SPIRE_SAVE_MAGIC        0x5A
#define SPIRE_ACTS              3
#define SPIRE_FLOORS            7   // verdiepingen per act; daarboven de baas
#define SPIRE_MAX_NODES         4   // kamers per verdieping
// v0.8.107: getallen uit tools/grounded/spire/runsim.py (vergelijking met Slay the Spire, zie SPIRE_BALANS.md)
#define SPIRE_HEAL_AFTER        8   // procent HP na een gewonnen gevecht (Slay: Burning Blood 6 van 80 HP = 7,5%)
#define SPIRE_REST_HEAL         30  // procent HP op een rustplek (Chansey); Slay 30%. Vanaf dit percentage gaat status weg
#define SPIRE_ACT_HEAL          40  // procent HP bij een nieuwe act (Slay A5+: 75% van het tekort, ±30-40%)
#define SPIRE_START_GOLD        75  // geld aan het begin van een run (Slay: 99 = 40% van het geld van een act)

enum SpireRoom
{
    SPIRE_ROOM_NONE,
    SPIRE_ROOM_FIGHT,
    SPIRE_ROOM_ELITE,
    SPIRE_ROOM_REST,
    SPIRE_ROOM_SHOP,
    SPIRE_ROOM_EVENT,
    SPIRE_ROOM_BOSS,
};

// Relics (50, tools/grounded/spire/relics.py): enum SpireRelic en enum SpireRelicTier
#include "spire_relics.h"

// Waar een relic vandaan komt (bepaalt de zeldzaamheid, zie Spire_RandomRelic)
enum SpireRelicSource
{
    SPIRE_RELIC_FROM_ELITE,     // elite (en events): common 50 / uncommon 33 / rare 17%
    SPIRE_RELIC_FROM_BOSS,      // baas: boss-relics
    SPIRE_RELIC_FROM_SHOP,      // winkel: als elite, nooit 'noShop'
    SPIRE_RELIC_FROM_SHOP_SPECIAL, // tweede winkelplek: shop-relics (op = als SHOP)
};

enum SpireBiomeId
{
    SPIRE_BIOME_GROVE,
    SPIRE_BIOME_DOCKS,
    SPIRE_BIOME_HIVE,
    SPIRE_BIOME_FROST,
    SPIRE_BIOME_COURT,
    SPIRE_BIOME_ABYSS,
    SPIRE_BIOME_COUNT,
};

enum SpireEncounterKind
{
    SPIRE_ENC_WEAK,
    SPIRE_ENC_NORMAL,
    SPIRE_ENC_ELITE,
    SPIRE_ENC_BOSS,
};

enum SpireGimmick
{
    SPIRE_GIMMICK_NONE,
    SPIRE_GIMMICK_SLEEP,    // begint 3 beurten in slaap
    SPIRE_GIMMICK_HIDDEN,   // intentie onleesbaar ("???"): Wobbuffet, steen-papier-schaar
};

struct SpireBiome
{
    u8 act;
    const u8 *name;
    const u8 *desc;
};

// Vijand in een ontmoeting (tools/grounded/spire/encounters.py)
struct SpireFoe
{
    u16 species;
    u16 moves[MAX_MON_MOVES];
    u16 ability;            // ABILITY_NONE = normaal
    u16 item;
    s8 unused;
    u8 hp;                  // HP-vermenigvuldiger in tienden
    u8 gimmick;             // enum SpireGimmick
    s8 boosts[5];           // totem-boosts: Atk, Def, Spe, SpA, SpD
    u8 pattern[8];          // vaste volgorde van moveslots (1-4), 0 = einde; leeg = vrije AI
};

struct SpireEncounter
{
    u8 biome;               // bij bazen: de act
    u8 kind;                // enum SpireEncounterKind
    u8 field;               // STARTING_STATUS_*
    const u8 *name;
    const u8 *hint;
    struct SpireFoe foes[2];
};

// Rentals en evoluties (tools/grounded/spire/spire_pool.py)
struct SpireRental
{
    u16 species;
    u8 tier;                // 0 C - 3 S
    u16 moves[MAX_MON_MOVES];
};

struct SpireEvolution
{
    u16 species;
    u16 targets[3];
};

// Lopende run, in gSaveBlock2Ptr->spireData: een gepauzeerde run overleeft opslaan en uitzetten.
struct SpireSave
{
    u8 magic;           // SPIRE_SAVE_MAGIC = er loopt een run
    u8 act;             // 1-3
    u8 floor;           // aantal afgeronde verdiepingen in deze act (SPIRE_FLOORS = baas aan de beurt)
    u8 node;            // gekozen kamer op die verdieping
    u32 seed;           // seed van de kaart van deze act
    u16 path;           // gekozen kamers per verdieping (2 bits per verdieping)
    u16 bp;             // BP van deze run (gaan naar je totaal als de run eindigt)
    u16 gold;           // geld voor de winkel
    u8 inRoom:1;        // kamer gestart maar nog niet klaar (gevecht gepauzeerd)
    u8 unused:7;
    u8 runsWon;
    u32 relics;         // bitveld met relics
    u8 biome;           // biome van deze act (enum SpireBiomeId)
    u8 relearns;        // aantal keer Move Relearner gebruikt (prijs stijgt)
    u16 usedEncounters; // gevechten die deze act al geweest zijn (index binnen de biome)
    u8 toxicFights;     // events: zoveel gevechten nog Toxic Spikes-risico
    u8 fungalMask;      // events: deze rentals (bit 0/1) zijn het volgende gevecht besmet
    s8 hpBonus[2];      // events: blijvende max-HP-verandering in procentpunten (bijv. -10)
    u32 eventsSeen;     // events die deze run al geweest zijn (0-31)
    struct Pokemon mons[2];
    u32 eventsSeen2;    // events 32-63 (achteraan, zodat een gepauzeerde run blijft werken)
    u32 relics2;        // relics 32-63 (achteraan, idem)
    u8 relicCharges;    // Acro Bike: aantal sprongen naar een kamer buiten je pad
};

#define SPIRE_SAVE (*(struct SpireSave *)gSaveBlock2Ptr->spireData)

struct SpireRelicInfo
{
    u16 item;           // icoon
    const u8 *name;
    const u8 *desc;
    u8 tier;            // enum SpireRelicTier
    bool8 noShop;
    u8 conflicts[2];    // niet aanbieden als je een van deze al hebt (SPIRE_RELIC_COUNT = geen)
};

struct SpireMapNode
{
    u8 type;            // enum SpireRoom
    u8 x;               // pixelpositie op de kaart
    u8 links;           // bitmasker naar kamers op de volgende verdieping
};

struct SpireActMap
{
    u8 count[SPIRE_FLOORS];
    struct SpireMapNode nodes[SPIRE_FLOORS][SPIRE_MAX_NODES];
};

// uitkomst van de laatste kamer, voor de kop van het beloningsscherm
struct SpireResult
{
    u16 bp;
    u16 gold;
    u8 healPercent;
};

extern bool8 gSpireBattle;
extern u8 gSpireAct;
extern u16 gSpireBlock[MAX_BATTLERS_COUNT];
extern u16 gSpireBlockAbsorbed[MAX_BATTLERS_COUNT];
extern u8 gSpireDefendTarget[MAX_BATTLERS_COUNT];
extern u16 gSpireEnemyHp[PARTY_SIZE];
extern struct SpireResult gSpireResult;
extern const struct SpireRelicInfo gSpireRelics[SPIRE_RELIC_COUNT];
extern const struct SpireBiome gSpireBiomes[SPIRE_BIOME_COUNT];
extern u8 gSpirePattern[PARTY_SIZE][8];
extern u8 gSpireStartingStatus;
extern u8 gSpireHiddenIntent;   // bit per vijandelijke partyplek
extern u8 gSpireEnvironment;
extern u8 gSpireEvolveMon;
extern u8 gSpirePatternStep[PARTY_SIZE];
extern u8 gSpireEncounterKind;
extern u8 gSpireRelicSource;    // enum SpireRelicSource van het volgende relic-kaartenscherm  // enum SpireEncounterKind van het lopende gevecht

// spire.c: gevecht
void Spire_OnEnemyPartyCreated(void);
void Spire_ClearBlocks(void);
u32 Spire_BlockAmount(u32 battler);
u32 Spire_BlockPercent(u32 amount, u32 target);
void Spire_AbsorbDamage(u32 battlerDef);
void HandleAction_SpireDefend(void);
bool32 Spire_TryPrintBlockAbsorbed(void);
u8 *Spire_GetIntentText(u8 *dst, u32 battler);
void Spire_ScaleMonHp(struct Pokemon *mon, u32 percent);
void Spire_CreateMon(struct Pokemon *mon, u16 species, u8 level, u8 iv, u32 ev, const u16 *moves);
void Spire_ApplyPattern(u32 battler);
void Spire_EndTurn(void);
bool32 Spire_IsMoveBanned(u16 move);
u32 Spire_BlockSplit(void);
uq4_12_t Spire_RelicDamageModifier(u32 battlerAtk, u32 battlerDef, bool32 isCrit, uq4_12_t typeEffectiveness);
bool32 Spire_TryRelicEndure(u32 battlerDef);
void Spire_OnFirstTurn(void);

// spire_run.c: run
bool32 Spire_RunActive(void);
struct Pokemon *Spire_GetRunMon(u32 i);
bool32 Spire_HasRelic(u32 relic);
void Spire_AddRelic(u32 relic);
void Spire_RemoveRelic(u32 relic);
u32 Spire_CountRelics(void);
u32 Spire_RandomRelic(u32 source, u32 salt, const u8 *exclude, u32 excludeCount);
u32 Spire_RelicHpBonus(void);
void Spire_RefreshMaxHp(void);
u16 Spire_UpgradeRandomMove(u32 *monOut);
void Spire_GenerateMap(struct SpireActMap *map, u32 seed);
bool32 Spire_IsReachable(const struct SpireActMap *map, u32 floor, u32 node);
bool32 Spire_IsAcroJump(const struct SpireActMap *map, u32 floor, u32 node);
void Spire_EnterRoom(u32 floor, u32 node);
void Spire_RoomFinished(void);
void Spire_SuspendRun(void);
void Spire_GiveUpRun(void);
void Spire_HealRun(u32 percent);
void Spire_RestorePP(void);
bool32 Spire_CanEvolve(u32 i);
void Spire_Evolve(u32 i);
void Spire_SetRental(u32 i, u16 species);
u16 Spire_RandomRental(u32 salt);
u16 Spire_RandomMove(u32 rarity, u32 salt);
u16 Spire_RandomMoveOfType(u32 rarity, u32 type, u32 salt);
u16 Spire_RandomHeldItem(u32 rarity, u32 salt);
const u8 *Spire_GetItemDescription(u16 item);
u32 Spire_GetEvolutions(u16 species, u16 *targets);
void Spire_EvolveTo(u32 i, u16 target);
u32 Spire_PlayerHpPercent(u32 i);
const struct SpireRental *Spire_FindRental(u16 species);
u16 Spire_RandomEventRental(u32 salt);
void Spire_SetSpecialDitto(u32 slot);
void Spire_StartEventFight(void);
void Spire_ReturnToField(void);
u16 Spire_GetBossSpecies(void);
void Spire_Enter(void);
void Spire_IsRunActive(void);
void Spire_GiveUpFromField(void);
void Spire_ResetRun(void);
void Spire_DebugOpen(void);

// spire_map.c
void Spire_OpenMap(void);

// spire_shop.c: Poké Mart (scrollende lijst)
void Spire_OpenShop(void (*onDone)(void));

// spire_draft.c: tien rentals, kies er twee
void Spire_OpenDraft(void (*onDone)(void));

// spire_rest.c: Snorlax-kamp en upgrades ("+")
void Spire_OpenRest(void (*onDone)(void));
bool32 Spire_IsSlotUpgraded(struct Pokemon *mon, u32 slot);
void Spire_UpgradeSlot(struct Pokemon *mon, u32 slot);
void Spire_ClearSlotUpgrade(struct Pokemon *mon, u32 slot);
void Spire_CompactMoves(struct Pokemon *mon);
u32 Spire_GetBiomeEnvironment(void);
void Spire_LoadBiomeBackground(u16 tint, u32 amount);
bool32 Spire_IsMoveUpgraded(u32 battler, u32 move);
uq4_12_t Spire_UpgradeDamageModifier(u32 battlerAtk, u32 move);

// spire_event.c: events (data uit tools/grounded/spire/events.py)
enum SpireFx
{
    SPIRE_FX_NONE,
    SPIRE_FX_GOLD,
    SPIRE_FX_GOLD_PCT,
    SPIRE_FX_HEAL,
    SPIRE_FX_HURT_ONE,
    SPIRE_FX_MAXHP,
    SPIRE_FX_BP,
    SPIRE_FX_RELIC,
    SPIRE_FX_LOSE_RELIC,
    SPIRE_FX_ITEM,
    SPIRE_FX_GIVE,
    SPIRE_FX_LOSE_ITEMS,
    SPIRE_FX_TEACH,
    SPIRE_FX_TEACH_TYPE,
    SPIRE_FX_TEACH_MOVE,
    SPIRE_FX_UPGRADE,
    SPIRE_FX_FORGET,
    SPIRE_FX_REMOVE,
    SPIRE_FX_FULLHEAL,
    SPIRE_FX_PP,
    SPIRE_FX_SLEEP,
    SPIRE_FX_TOXIC,
    SPIRE_FX_ELITE,
    SPIRE_FX_RECRUIT,
    SPIRE_FX_RECRUIT_SPECIES,
    SPIRE_FX_DITTO,
    SPIRE_FX_WONDER,
    SPIRE_FX_EVOLVE,
    SPIRE_FX_WHEEL,
    SPIRE_FX_RECRUIT_PSEUDO,
};
extern u8 gSpireForcedEvent;    // debug: 0 = willekeurig, anders event-index + 1
void Spire_OpenEvent(void (*onDone)(void));
void Spire_ChangeMaxHp(s32 delta);
// spire_cards.c
enum SpireCardMode
{
    SPIRE_CARDS_MOVES,      // beloning: kies een move en leer hem aan
    SPIRE_CARDS_RELICS,     // beloning: kies een relic
    SPIRE_CARDS_MESSAGE,    // alleen een bericht (einde run, nieuwe act)
    SPIRE_CARDS_EVOLVE,     // nieuwe act: kies de evolutie van gSpireEvolveMon (vertakking)
    SPIRE_CARDS_RELIC_LIST, // R op de kaart: je relics bekijken (drie per pagina)
};
void Spire_OpenCards(u32 mode, void (*onDone)(void));
void Spire_OpenMessage(const u8 *title, const u8 *text, void (*onDone)(void));

#endif // GUARD_SPIRE_H
