@ Project Grounded: drumkit voor regio_theme.py (onderwater). Alleen stock-samples, geen PSG.
@ 36 kick, 37 doffe snare, 38 belletjes, 39 taiko diep, 40 bekkenzwel, 41 triangel dof.
@ voice_directsound (niet _no_resample): speelt op de rate van de sample, niet op de mixersnelheid.
voice_group regio_underwater_drumset, 36
	voice_directsound 58, 64, DirectSoundWaveData_drum_and_percussion_kick, 255, 0, 255, 180
	voice_directsound 50, 64, DirectSoundWaveData_sc88pro_rnd_snare, 255, 0, 255, 170
	voice_directsound 60, 64, DirectSoundWaveData_sc88pro_bubbles, 255, 0, 255, 170
	voice_directsound 46, 64, DirectSoundWaveData_sc88pro_taiko, 255, 0, 255, 180
	voice_directsound 48, 64, DirectSoundWaveData_sc88pro_orchestra_cymbal_crash, 40, 0, 255, 140
	voice_directsound 62, 70, DirectSoundWaveData_sd90_open_triangle, 255, 0, 255, 150
