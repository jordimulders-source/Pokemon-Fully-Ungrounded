@ Project Grounded: drumkit voor Battle! Neo Team Plasma v7 (neo_plasma_theme.py): standaard GBA-samples.
@ 36 kick (+7 halve tonen), 37 off-beat-clap (909), 38 snare, 39 open hihat, 40 crash, 41 splash,
@ 42 dichte hihat, 43 scherpe snare (2 en 4, ghosts). Alles DirectSound.
voice_group neo_plasma_drumset, 36
	voice_directsound 67, 0, DirectSoundWaveData_drum_and_percussion_kick, 255, 0, 255, 0
	voice_directsound_no_resample 60, 0, DirectSoundWaveData_sc88pro_tr909_hand_clap, 255, 0, 255, 180
	voice_directsound_no_resample 60, 0, DirectSoundWaveData_sc88pro_rnd_snare, 255, 0, 255, 220
	voice_directsound_no_resample 60, 0, DirectSoundWaveData_unknown_open_hihat, 255, 242, 141, 0
	voice_directsound_no_resample 60, 0, DirectSoundWaveData_trinity_cymbal_crash, 255, 235, 0, 165
	voice_directsound 67, 0, DirectSoundWaveData_trinity_cymbal_crash, 255, 200, 0, 140
	voice_directsound_no_resample 60, 0, DirectSoundWaveData_unknown_close_hihat, 255, 0, 255, 0
	voice_directsound_no_resample 60, 0, DirectSoundWaveData_unknown_synth_snare, 255, 0, 255, 200
