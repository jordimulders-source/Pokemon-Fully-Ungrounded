@ Project Grounded: drumkit voor regio_theme2.py (grot). Alleen stock-samples, geen PSG.
@ 36 doffe kick, 37 doffe snare, 38 hyoushigi, 39 ambient tom laag, 40 ambient tom midden, 41 ambient tom hoog, 42 donker bekken, 43 taiko diep.
@ voice_directsound (niet _no_resample): speelt op de rate van de sample, niet op de mixersnelheid.
voice_group regio_cave_drumset, 36
	voice_directsound 58, 64, DirectSoundWaveData_drum_and_percussion_kick, 255, 0, 255, 180
	voice_directsound 52, 64, DirectSoundWaveData_sc88pro_rnd_snare, 255, 0, 255, 170
	voice_directsound 56, 72, DirectSoundWaveData_ethnic_flavours_hyoushigi, 255, 0, 255, 120
	voice_directsound 48, 52, DirectSoundWaveData_sd90_ambient_tom, 255, 0, 255, 180
	voice_directsound 53, 64, DirectSoundWaveData_sd90_ambient_tom, 255, 0, 255, 180
	voice_directsound 58, 76, DirectSoundWaveData_sd90_ambient_tom, 255, 0, 255, 180
	voice_directsound 52, 64, DirectSoundWaveData_sc88pro_orchestra_cymbal_crash, 255, 235, 0, 160
	voice_directsound 46, 64, DirectSoundWaveData_sc88pro_taiko, 255, 0, 255, 180
