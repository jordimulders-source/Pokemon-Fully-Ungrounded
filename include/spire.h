#ifndef GUARD_SPIRE_H
#define GUARD_SPIRE_H

// Project Grounded: The Spire (roguelike-faciliteit, zie SPIRE_DESIGN.md)

#define B_ACTION_SPIRE_DEFEND   22

// DEFEND-doel (bitmasker per battler aan eigen kant)
#define SPIRE_DEFEND_BOTH       0xFF

// HP-vermenigvuldigers in procenten (startwaarden uit tools/grounded/spire/balance.py)
#define SPIRE_HP_PLAYER         400
#define SPIRE_HP_NORMAL         100
#define SPIRE_HP_ELITE          250
#define SPIRE_HP_BOSS           450

// Blok = 15% van max HP x verdedigingsfactor x act-factor; verdeeld over beide = 60% elk
#define SPIRE_BLOCK_PERCENT     15
#define SPIRE_BLOCK_SPLIT       60

extern bool8 gSpireBattle;
extern u8 gSpireAct;
extern u16 gSpireBlock[MAX_BATTLERS_COUNT];
extern u16 gSpireBlockAbsorbed[MAX_BATTLERS_COUNT];
extern u8 gSpireDefendTarget[MAX_BATTLERS_COUNT];

void Spire_OnEnemyPartyCreated(void);
void Spire_ClearBlocks(void);
u32 Spire_BlockAmount(u32 battler);
u32 Spire_BlockPercent(u32 amount, u32 target);
void Spire_AbsorbDamage(u32 battlerDef);
void HandleAction_SpireDefend(void);
bool32 Spire_TryPrintBlockAbsorbed(void);
void Spire_StartPrototypeBattle(void);
void Spire_EndBattle(void);
u8 *Spire_GetIntentText(u8 *dst, u32 battler);

#endif // GUARD_SPIRE_H
