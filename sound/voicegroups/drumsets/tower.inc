@ Project Grounded: drumkit voor tower_theme.py (Battle! Pokémon Tower). Alleen stock-samples, geen PSG.
@ 36 kick, 37 snare, 38 crash, 39 tom laag, 40 tom midden, 41 tom hoog, 42 taiko, 43 kotsuzumi, 44 atarigane, 45 hyoushigi.
@ voice_directsound (niet _no_resample): speelt op de rate van de sample, niet op de mixersnelheid.
voice_group tower_drumset, 36
	voice_directsound 67, 64, DirectSoundWaveData_drum_and_percussion_kick, 255, 0, 255, 180
	voice_directsound 60, 64, DirectSoundWaveData_sc88pro_rnd_snare, 255, 0, 255, 180
	voice_directsound 60, 64, DirectSoundWaveData_trinity_cymbal_crash, 255, 235, 0, 165
	voice_directsound 45, 52, DirectSoundWaveData_unused_sc55_tom, 255, 210, 77, 180
	voice_directsound 51, 64, DirectSoundWaveData_unused_sc55_tom, 255, 210, 77, 180
	voice_directsound 57, 76, DirectSoundWaveData_unused_sc55_tom, 255, 210, 77, 180
	voice_directsound 63, 64, DirectSoundWaveData_sc88pro_taiko, 255, 0, 255, 180
	voice_directsound 64, 84, DirectSoundWaveData_ethnic_flavours_kotsuzumi, 255, 0, 255, 160
	voice_directsound 60, 40, DirectSoundWaveData_ethnic_flavours_atarigane, 255, 0, 255, 180
	voice_directsound 60, 88, DirectSoundWaveData_ethnic_flavours_hyoushigi, 255, 0, 255, 150
