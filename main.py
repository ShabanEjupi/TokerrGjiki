"""
🎮 TOKERRGJIK - Ultimate Cross-Platform Edition
Traditional Albanian Board Game (Nine Men's Morris)

Developed by: Shaban Ejupi
IT Expert & Computer Science Master
Republic of Kosovo Customs - University of Prishtina

Version: 11.0 - Python Cross-Platform Edition
Platforms: Android, iOS, Windows, Linux, macOS, Web
"""

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle, Ellipse, Line
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.properties import NumericProperty, BooleanProperty, StringProperty
from kivy.core.audio import SoundLoader
from kivy.storage.jsonstore import JsonStore
from kivy.utils import platform
import os
import json
from datetime import datetime

# Import game modules
from game_engine import GameEngine
from ai_player import AIPlayer
from ui_components import ModernButton, GameBoard, ScorePanel, MenuBar
from score_manager import ScoreManager
from sound_manager import SoundManager


class MainMenuScreen(Screen):
    """Main menu with game mode selection"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()
        
        # Background gradient
        with layout.canvas.before:
            Color(0.1, 0.24, 0.31, 1)  # Dark slate background
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
        
        self.bind(size=self._update_bg, pos=self._update_bg)
        
        # Title
        title = Label(
            text='[b]⚡ TOKERRGJIK ⚡[/b]\n🇦🇱 Loja Tradicionale Shqiptare',
            markup=True,
            font_size='32sp',
            size_hint=(1, 0.3),
            pos_hint={'center_x': 0.5, 'top': 0.95},
            color=(0.1, 0.74, 0.61, 1)
        )
        
        # Menu buttons
        button_layout = BoxLayout(
            orientation='vertical',
            spacing=20,
            size_hint=(0.7, 0.5),
            pos_hint={'center_x': 0.5, 'center_y': 0.4}
        )
        
        btn_vs_ai = ModernButton(
            text='🤖 Luaj kundër AI\nPlay vs AI',
            on_press=self.start_vs_ai
        )
        
        btn_vs_human = ModernButton(
            text='👥 Dy Lojtarë\nTwo Players',
            on_press=self.start_vs_human
        )
        
        btn_stats = ModernButton(
            text='📊 Statistikat\nStatistics',
            on_press=self.show_statistics
        )
        
        btn_settings = ModernButton(
            text='⚙️ Cilësimet\nSettings',
            on_press=self.show_settings
        )
        
        btn_help = ModernButton(
            text='❓ Ndihmë\nHelp',
            on_press=self.show_help
        )
        
        button_layout.add_widget(btn_vs_ai)
        button_layout.add_widget(btn_vs_human)
        button_layout.add_widget(btn_stats)
        button_layout.add_widget(btn_settings)
        button_layout.add_widget(btn_help)
        
        # Developer credits
        credits = Label(
            text='Developed by Shaban Ejupi\nv11.0 - Cross-Platform Edition',
            font_size='12sp',
            size_hint=(1, 0.1),
            pos_hint={'center_x': 0.5, 'y': 0.02},
            color=(0.8, 0.8, 0.8, 0.7)
        )
        
        layout.add_widget(title)
        layout.add_widget(button_layout)
        layout.add_widget(credits)
        
        self.add_widget(layout)
    
    def _update_bg(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
    
    def start_vs_ai(self, *args):
        self.manager.get_screen('game').setup_game(vs_ai=True)
        self.manager.current = 'game'
    
    def start_vs_human(self, *args):
        self.manager.get_screen('game').setup_game(vs_ai=False)
        self.manager.current = 'game'
    
    def show_statistics(self, *args):
        self.manager.current = 'statistics'
    
    def show_settings(self, *args):
        self.manager.current = 'settings'
    
    def show_help(self, *args):
        self.manager.current = 'help'


class GameScreen(Screen):
    """Main game screen with board and controls"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.game_engine = None
        self.ai_player = None
        self.vs_ai = True
        self.game_board = None
        
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Top menu bar
        self.menu_bar = MenuBar(game_screen=self)
        self.layout.add_widget(self.menu_bar)
        
        # Score panel
        self.score_panel = ScorePanel()
        self.layout.add_widget(self.score_panel)
        
        # Game board (will be initialized in setup_game)
        # Give MUCH more space to board, minimize buttons
        self.board_container = FloatLayout(size_hint=(1, 0.78))  # Increased from 0.7
        self.layout.add_widget(self.board_container)
        
        # Control buttons - much smaller so they don't cover board
        control_layout = BoxLayout(
            orientation='horizontal',
            size_hint=(1, 0.06),  # Reduced from 0.08
            spacing=5,
            padding=[5, 2]
        )
        
        self.btn_undo = ModernButton(text='↩️ Undo', on_press=self.undo_move)
        self.btn_redo = ModernButton(text='↪️ Redo', on_press=self.redo_move)
        self.btn_new_game = ModernButton(text='🆕 New Game', on_press=self.new_game)
        self.btn_menu = ModernButton(text='🏠 Menu', on_press=self.go_to_menu)
        
        control_layout.add_widget(self.btn_undo)
        control_layout.add_widget(self.btn_redo)
        control_layout.add_widget(self.btn_new_game)
        control_layout.add_widget(self.btn_menu)
        
        self.layout.add_widget(control_layout)
        
        self.add_widget(self.layout)
    
    def setup_game(self, vs_ai=True):
        """Initialize a new game"""
        self.vs_ai = vs_ai
        self.game_engine = GameEngine()
        
        if vs_ai:
            self.ai_player = AIPlayer(difficulty='hard')
        
        # Create game board
        if self.game_board:
            self.board_container.remove_widget(self.game_board)
        
        self.game_board = GameBoard(
            game_engine=self.game_engine,
            game_screen=self
        )
        self.board_container.add_widget(self.game_board)
        
        # Update UI
        self.update_ui()
    
    def update_ui(self):
        """Update all UI elements"""
        if self.game_engine:
            self.score_panel.update_score(
                self.game_engine.player1_pieces,
                self.game_engine.player2_pieces,
                self.game_engine.current_player,
                self.game_engine.get_phase_name()
            )
            
            self.menu_bar.update_status(
                self.game_engine.get_status_message(),
                self.game_engine.is_game_over
            )
    
    def undo_move(self, *args):
        """Undo last move"""
        if self.game_engine and self.game_engine.undo():
            self.game_board.redraw()
            self.update_ui()
    
    def redo_move(self, *args):
        """Redo move"""
        if self.game_engine and self.game_engine.redo():
            self.game_board.redraw()
            self.update_ui()
    
    def new_game(self, *args):
        """Start a new game"""
        self.setup_game(vs_ai=self.vs_ai)
    
    def go_to_menu(self, *args):
        """Return to main menu"""
        self.manager.current = 'main_menu'
    
    def on_ai_turn(self):
        """Handle AI turn"""
        if self.vs_ai and self.ai_player and not self.game_engine.is_game_over:
            # Delay AI move for better UX
            Clock.schedule_once(lambda dt: self.make_ai_move(), 0.8)
    
    def make_ai_move(self):
        """Make AI move"""
        if self.ai_player:
            self.ai_player.make_move(self.game_engine)
            self.game_board.redraw()
            self.update_ui()


class StatisticsScreen(Screen):
    """Statistics and achievements screen"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Will be implemented with detailed statistics


class SettingsScreen(Screen):
    """Settings and preferences screen"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Will be implemented with sound, difficulty, language settings


class HelpScreen(Screen):
    """Help and tutorial screen"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Will be implemented with game rules and tutorial


class TokerrgjikApp(App):
    """Main application class"""
    
    def build(self):
        # Set window background color
        Window.clearcolor = (0.1, 0.24, 0.31, 1)
        
        # Initialize managers
        self.score_manager = ScoreManager()
        self.sound_manager = SoundManager()
        
        # Create screen manager
        sm = ScreenManager()
        
        # Add screens
        sm.add_widget(MainMenuScreen(name='main_menu'))
        sm.add_widget(GameScreen(name='game'))
        sm.add_widget(StatisticsScreen(name='statistics'))
        sm.add_widget(SettingsScreen(name='settings'))
        sm.add_widget(HelpScreen(name='help'))
        
        return sm
    
    def on_start(self):
        """Called when app starts"""
        print("🚀 TOKERRGJIK - Cross-Platform Edition Started!")
        print(f"Platform: {platform}")
        
        # Load saved data
        self.score_manager.load_scores()
    
    def on_pause(self):
        """Called when app is paused (mobile)"""
        self.score_manager.save_scores()
        return True
    
    def on_resume(self):
        """Called when app resumes (mobile)"""
        pass
    
    def on_stop(self):
        """Called when app stops"""
        self.score_manager.save_scores()


if __name__ == '__main__':
    TokerrgjikApp().run()
