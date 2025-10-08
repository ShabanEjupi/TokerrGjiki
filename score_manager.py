"""
Score Manager Module
Persistent score tracking and statistics
"""

import json
import os
from datetime import datetime
from kivy.storage.jsonstore import JsonStore
from kivy.utils import platform


class ScoreManager:
    """Manage game scores and statistics"""
    
    def __init__(self):
        # Determine storage path based on platform
        if platform == 'android':
            from android.storage import app_storage_path
            storage_path = app_storage_path()
        elif platform == 'ios':
            from ios import get_documents_dir
            storage_path = get_documents_dir()
        else:
            storage_path = os.getcwd()
        
        self.store_path = os.path.join(storage_path, 'tokerrgjik_scores.json')
        self.store = JsonStore(self.store_path)
        
        # Initialize default scores
        self.player1_wins = 0
        self.player2_wins = 0
        self.ai_wins = 0
        self.total_games = 0
        self.win_streak = 0
        self.best_streak = 0
        self.total_play_time = 0
        self.achievements = []
    
    def load_scores(self):
        """Load scores from storage"""
        try:
            if self.store.exists('scores'):
                data = self.store.get('scores')
                self.player1_wins = data.get('player1_wins', 0)
                self.player2_wins = data.get('player2_wins', 0)
                self.ai_wins = data.get('ai_wins', 0)
                self.total_games = data.get('total_games', 0)
                self.win_streak = data.get('win_streak', 0)
                self.best_streak = data.get('best_streak', 0)
                self.total_play_time = data.get('total_play_time', 0)
                self.achievements = data.get('achievements', [])
                
                print(f"📊 Scores loaded: P1={self.player1_wins}, P2={self.player2_wins}, AI={self.ai_wins}")
        except Exception as e:
            print(f"⚠️ Error loading scores: {e}")
    
    def save_scores(self):
        """Save scores to storage"""
        try:
            self.store.put('scores',
                          player1_wins=self.player1_wins,
                          player2_wins=self.player2_wins,
                          ai_wins=self.ai_wins,
                          total_games=self.total_games,
                          win_streak=self.win_streak,
                          best_streak=self.best_streak,
                          total_play_time=self.total_play_time,
                          achievements=self.achievements,
                          last_updated=datetime.now().isoformat())
            
            print(f"💾 Scores saved successfully!")
        except Exception as e:
            print(f"⚠️ Error saving scores: {e}")
    
    def record_game(self, winner, vs_ai=True, play_time=0):
        """Record a completed game"""
        self.total_games += 1
        self.total_play_time += play_time
        
        if winner == 1:
            self.player1_wins += 1
            self.win_streak += 1
            
            if self.win_streak > self.best_streak:
                self.best_streak = self.win_streak
        elif winner == 2:
            if vs_ai:
                self.ai_wins += 1
            else:
                self.player2_wins += 1
            
            self.win_streak = 0
        
        # Check for achievements
        self.check_achievements()
        
        # Save to storage
        self.save_scores()
    
    def check_achievements(self):
        """Check and unlock achievements"""
        new_achievements = []
        
        # First win
        if self.player1_wins == 1 and 'first_win' not in self.achievements:
            new_achievements.append('first_win')
            self.achievements.append('first_win')
        
        # Win streak achievements
        if self.win_streak >= 3 and 'streak_3' not in self.achievements:
            new_achievements.append('streak_3')
            self.achievements.append('streak_3')
        
        if self.win_streak >= 5 and 'streak_5' not in self.achievements:
            new_achievements.append('streak_5')
            self.achievements.append('streak_5')
        
        if self.win_streak >= 10 and 'streak_10' not in self.achievements:
            new_achievements.append('streak_10')
            self.achievements.append('streak_10')
        
        # Total wins achievements
        if self.player1_wins >= 10 and 'wins_10' not in self.achievements:
            new_achievements.append('wins_10')
            self.achievements.append('wins_10')
        
        if self.player1_wins >= 50 and 'wins_50' not in self.achievements:
            new_achievements.append('wins_50')
            self.achievements.append('wins_50')
        
        if self.player1_wins >= 100 and 'wins_100' not in self.achievements:
            new_achievements.append('wins_100')
            self.achievements.append('wins_100')
        
        # Playtime achievements (in seconds)
        if self.total_play_time >= 3600 and 'time_1h' not in self.achievements:
            new_achievements.append('time_1h')
            self.achievements.append('time_1h')
        
        if self.total_play_time >= 36000 and 'time_10h' not in self.achievements:
            new_achievements.append('time_10h')
            self.achievements.append('time_10h')
        
        return new_achievements
    
    def get_achievement_name(self, achievement_id):
        """Get readable achievement name"""
        achievement_names = {
            'first_win': '🏆 First Victory',
            'streak_3': '🔥 3-Win Streak',
            'streak_5': '🔥🔥 5-Win Streak',
            'streak_10': '🔥🔥🔥 10-Win Streak',
            'wins_10': '⭐ 10 Victories',
            'wins_50': '⭐⭐ 50 Victories',
            'wins_100': '⭐⭐⭐ 100 Victories',
            'time_1h': '⏰ 1 Hour Played',
            'time_10h': '⏰⏰ 10 Hours Played'
        }
        
        return achievement_names.get(achievement_id, achievement_id)
    
    def get_statistics_summary(self):
        """Get formatted statistics summary"""
        win_rate = (self.player1_wins / self.total_games * 100) if self.total_games > 0 else 0
        
        return {
            'player1_wins': self.player1_wins,
            'player2_wins': self.player2_wins,
            'ai_wins': self.ai_wins,
            'total_games': self.total_games,
            'win_rate': win_rate,
            'win_streak': self.win_streak,
            'best_streak': self.best_streak,
            'total_play_time': self.total_play_time,
            'achievements': len(self.achievements),
            'achievement_list': [self.get_achievement_name(a) for a in self.achievements]
        }
    
    def reset_scores(self):
        """Reset all scores (for testing or user request)"""
        self.player1_wins = 0
        self.player2_wins = 0
        self.ai_wins = 0
        self.total_games = 0
        self.win_streak = 0
        self.best_streak = 0
        self.total_play_time = 0
        self.achievements = []
        
        self.save_scores()
