"""
Sound Manager Module
Audio effects and background music
"""

from kivy.core.audio import SoundLoader
from kivy.utils import platform
import os


class SoundManager:
    """Manage game sounds and music"""
    
    def __init__(self):
        self.sounds = {}
        self.music = None
        self.sound_enabled = True
        self.music_enabled = True
        self.volume = 0.7
        
        # Load sounds (will create placeholder for now)
        self.load_sounds()
    
    def load_sounds(self):
        """Load sound effects"""
        sound_files = {
            'place': 'sounds/place.wav',
            'move': 'sounds/move.wav',
            'remove': 'sounds/remove.wav',
            'mill': 'sounds/mill.wav',
            'win': 'sounds/win.wav',
            'lose': 'sounds/lose.wav',
            'click': 'sounds/click.wav',
            'error': 'sounds/error.wav'
        }
        
        # Create sounds directory if it doesn't exist
        if not os.path.exists('sounds'):
            os.makedirs('sounds')
            print("📁 Created sounds directory. Please add sound files.")
        
        # Try to load each sound
        for sound_name, sound_path in sound_files.items():
            try:
                if os.path.exists(sound_path):
                    sound = SoundLoader.load(sound_path)
                    if sound:
                        sound.volume = self.volume
                        self.sounds[sound_name] = sound
                        print(f"🔊 Loaded sound: {sound_name}")
                else:
                    print(f"⚠️ Sound file not found: {sound_path}")
            except Exception as e:
                print(f"⚠️ Error loading sound {sound_name}: {e}")
    
    def play_sound(self, sound_name):
        """Play a sound effect"""
        if not self.sound_enabled:
            return
        
        if sound_name in self.sounds:
            try:
                self.sounds[sound_name].play()
            except Exception as e:
                print(f"⚠️ Error playing sound {sound_name}: {e}")
    
    def play_place_sound(self):
        """Play piece placement sound"""
        self.play_sound('place')
    
    def play_move_sound(self):
        """Play piece movement sound"""
        self.play_sound('move')
    
    def play_remove_sound(self):
        """Play piece removal sound"""
        self.play_sound('remove')
    
    def play_mill_sound(self):
        """Play mill formation sound"""
        self.play_sound('mill')
    
    def play_win_sound(self):
        """Play victory sound"""
        self.play_sound('win')
    
    def play_lose_sound(self):
        """Play defeat sound"""
        self.play_sound('lose')
    
    def play_click_sound(self):
        """Play UI click sound"""
        self.play_sound('click')
    
    def play_error_sound(self):
        """Play error sound"""
        self.play_sound('error')
    
    def toggle_sound(self):
        """Toggle sound effects on/off"""
        self.sound_enabled = not self.sound_enabled
        return self.sound_enabled
    
    def toggle_music(self):
        """Toggle background music on/off"""
        self.music_enabled = not self.music_enabled
        
        if self.music_enabled and self.music:
            self.music.play()
        elif self.music:
            self.music.stop()
        
        return self.music_enabled
    
    def set_volume(self, volume):
        """Set volume level (0.0 to 1.0)"""
        self.volume = max(0.0, min(1.0, volume))
        
        # Update all loaded sounds
        for sound in self.sounds.values():
            sound.volume = self.volume
        
        if self.music:
            self.music.volume = self.volume * 0.5  # Music quieter than effects
