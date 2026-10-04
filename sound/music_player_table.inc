	.equiv TRACK_SIZE, 0x50
	.equiv NUM_TRACKS_BGM, 16 @ Project Grounded: was 10 (eigen nummers hebben tot 16 sporen; daarboven speelde niets)
	.equiv NUM_TRACKS_SE1, 3
	.equiv NUM_TRACKS_SE2, 9
	.equiv NUM_TRACKS_SE3, 1

    @ Project Grounded: de BGM-sporen (16 x 0x50 = 1280 bytes) staan in EWRAM (.sbss) i.p.v. IWRAM,
    @ zodat de stack in IWRAM genoeg marge houdt.
    .section .sbss
    .align 2

gMPlayTrack_BGM::
    .space TRACK_SIZE * NUM_TRACKS_BGM
    .size gMPlayTrack_BGM, .-gMPlayTrack_BGM

    .bss
    .align 2

gMPlayTrack_SE1::
    .space TRACK_SIZE * NUM_TRACKS_SE1
    .size gMPlayTrack_SE1, .-gMPlayTrack_SE1

gMPlayTrack_SE2::
    .space TRACK_SIZE * NUM_TRACKS_SE2
    .size gMPlayTrack_SE2, .-gMPlayTrack_SE2

gMPlayTrack_SE3::
    .space TRACK_SIZE * NUM_TRACKS_SE3
    .size gMPlayTrack_SE3, .-gMPlayTrack_SE3

	.section .rodata

	.align 2
gMPlayTable::
	music_player gMPlayInfo_BGM, gMPlayTrack_BGM, NUM_TRACKS_BGM, 0
	music_player gMPlayInfo_SE1, gMPlayTrack_SE1, NUM_TRACKS_SE1, 1
	music_player gMPlayInfo_SE2, gMPlayTrack_SE2, NUM_TRACKS_SE2, 1
	music_player gMPlayInfo_SE3, gMPlayTrack_SE3, NUM_TRACKS_SE3, 0
