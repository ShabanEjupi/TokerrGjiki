"""
Game Engine Module
Core game logic for Tokerrgjik (Nine Men's Morris)
"""

from typing import List, Tuple, Optional, Callable
import copy


class GameEngine:
    """Core game engine for Tokerrgjik"""
    
    # Board positions (0-23)
    BOARD_SIZE = 24
    
    # Mill combinations (3 positions that form a mill)
    MILLS = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],           # Outer square
        [9, 10, 11], [12, 13, 14], [15, 16, 17],   # Middle square
        [18, 19, 20], [21, 22, 23],                # Inner square
        [0, 9, 21], [3, 10, 18], [6, 11, 15],      # Left verticals
        [1, 4, 7], [16, 19, 22],                   # Center verticals
        [8, 12, 17], [5, 13, 20], [2, 14, 23]      # Right verticals
    ]
    
    # Adjacent positions for movement
    ADJACENCY = {
        0: [1, 9], 1: [0, 2, 4], 2: [1, 14],
        3: [4, 10], 4: [1, 3, 5, 7], 5: [4, 13],
        6: [7, 11], 7: [4, 6, 8], 8: [7, 12],
        9: [0, 10, 21], 10: [3, 9, 11, 18], 11: [6, 10, 15],
        12: [8, 13, 17], 13: [5, 12, 14, 20], 14: [2, 13, 23],
        15: [11, 16], 16: [15, 17, 19], 17: [12, 16],
        18: [10, 19], 19: [16, 18, 20, 22], 20: [13, 19],
        21: [9, 22], 22: [19, 21, 23], 23: [14, 22]
    }
    
    def __init__(self):
        # Game state
        self.board = [0] * self.BOARD_SIZE  # 0=empty, 1=player1, 2=player2
        self.current_player = 1
        self.phase = 'placement'  # placement, movement, flying
        
        # Piece counts
        self.player1_pieces = 9
        self.player2_pieces = 9
        self.player1_placed = 0
        self.player2_placed = 0
        self.player1_on_board = 0
        self.player2_on_board = 0
        
        # Game state
        self.is_game_over = False
        self.winner = None
        self.awaiting_removal = False
        self.selected_position = None
        
        # Undo/Redo system
        self.history = []
        self.redo_stack = []
        
        # Callbacks
        self.on_player_switch = None
        self.on_mill_formed = None
        self.on_piece_removed = None
        self.on_game_over = None
    
    def get_state_copy(self):
        """Get a copy of current game state for undo/redo"""
        return {
            'board': self.board.copy(),
            'current_player': self.current_player,
            'phase': self.phase,
            'player1_pieces': self.player1_pieces,
            'player2_pieces': self.player2_pieces,
            'player1_placed': self.player1_placed,
            'player2_placed': self.player2_placed,
            'player1_on_board': self.player1_on_board,
            'player2_on_board': self.player2_on_board,
            'awaiting_removal': self.awaiting_removal,
            'selected_position': self.selected_position
        }
    
    def restore_state(self, state):
        """Restore game state from a saved state"""
        self.board = state['board'].copy()
        self.current_player = state['current_player']
        self.phase = state['phase']
        self.player1_pieces = state['player1_pieces']
        self.player2_pieces = state['player2_pieces']
        self.player1_placed = state['player1_placed']
        self.player2_placed = state['player2_placed']
        self.player1_on_board = state['player1_on_board']
        self.player2_on_board = state['player2_on_board']
        self.awaiting_removal = state['awaiting_removal']
        self.selected_position = state['selected_position']
    
    def save_state_to_history(self):
        """Save current state to history"""
        self.history.append(self.get_state_copy())
        self.redo_stack.clear()
    
    def undo(self):
        """Undo last move"""
        if len(self.history) > 0:
            current_state = self.get_state_copy()
            self.redo_stack.append(current_state)
            previous_state = self.history.pop()
            self.restore_state(previous_state)
            return True
        return False
    
    def redo(self):
        """Redo move"""
        if len(self.redo_stack) > 0:
            current_state = self.get_state_copy()
            self.history.append(current_state)
            next_state = self.redo_stack.pop()
            self.restore_state(next_state)
            return True
        return False
    
    def new_game(self):
        """Reset game to initial state"""
        self.__init__()
    
    def place_piece(self, position: int) -> bool:
        """Place a piece during placement phase"""
        if self.phase != 'placement' or self.awaiting_removal:
            return False
        
        if position < 0 or position >= self.BOARD_SIZE:
            return False
        
        if self.board[position] != 0:
            return False
        
        # Save state before move
        self.save_state_to_history()
        
        # Place piece
        self.board[position] = self.current_player
        
        if self.current_player == 1:
            self.player1_placed += 1
            self.player1_on_board += 1
        else:
            self.player2_placed += 1
            self.player2_on_board += 1
        
        # Check for mill
        if self.is_mill_formed(position):
            self.awaiting_removal = True
            if self.on_mill_formed:
                self.on_mill_formed(self.current_player)
        else:
            self.switch_player()
        
        # Check if placement phase is complete
        if self.player1_placed == 9 and self.player2_placed == 9:
            self.phase = 'movement'
        
        return True
    
    def move_piece(self, from_pos: int, to_pos: int) -> bool:
        """Move a piece during movement or flying phase"""
        if self.phase == 'placement' or self.awaiting_removal:
            return False
        
        if from_pos < 0 or from_pos >= self.BOARD_SIZE:
            return False
        
        if to_pos < 0 or to_pos >= self.BOARD_SIZE:
            return False
        
        if self.board[from_pos] != self.current_player:
            return False
        
        if self.board[to_pos] != 0:
            return False
        
        # Check adjacency for movement phase
        if self.phase == 'movement':
            pieces_on_board = (self.player1_on_board if self.current_player == 1 
                             else self.player2_on_board)
            
            if pieces_on_board > 3:  # Normal movement
                if to_pos not in self.ADJACENCY[from_pos]:
                    return False
            else:  # Flying phase
                self.phase = 'flying'
        
        # Save state before move
        self.save_state_to_history()
        
        # Move piece
        self.board[from_pos] = 0
        self.board[to_pos] = self.current_player
        
        # Check for mill
        if self.is_mill_formed(to_pos):
            self.awaiting_removal = True
            if self.on_mill_formed:
                self.on_mill_formed(self.current_player)
        else:
            self.switch_player()
        
        return True
    
    def remove_piece(self, position: int) -> bool:
        """Remove opponent's piece after forming a mill"""
        if not self.awaiting_removal:
            return False
        
        if position < 0 or position >= self.BOARD_SIZE:
            return False
        
        opponent = 3 - self.current_player
        
        if self.board[position] != opponent:
            return False
        
        # Check if piece is in a mill (can only remove if no other option)
        if self.is_mill_formed(position):
            # Check if all opponent pieces are in mills
            can_remove_non_mill = False
            for i in range(self.BOARD_SIZE):
                if self.board[i] == opponent and not self.is_mill_formed(i):
                    can_remove_non_mill = True
                    break
            
            if can_remove_non_mill:
                return False  # Must remove non-mill piece first
        
        # Remove piece
        self.board[position] = 0
        
        if opponent == 1:
            self.player1_on_board -= 1
        else:
            self.player2_on_board -= 1
        
        if self.on_piece_removed:
            self.on_piece_removed(position, opponent)
        
        self.awaiting_removal = False
        self.switch_player()
        
        # Check win condition
        self.check_game_over()
        
        return True
    
    def is_mill_formed(self, position: int) -> bool:
        """Check if position is part of a mill"""
        player = self.board[position]
        if player == 0:
            return False
        
        for mill in self.MILLS:
            if position in mill:
                if all(self.board[p] == player for p in mill):
                    return True
        
        return False
    
    def switch_player(self):
        """Switch to other player"""
        self.current_player = 3 - self.current_player
        
        if self.on_player_switch:
            self.on_player_switch(self.current_player)
    
    def check_game_over(self):
        """Check if game is over"""
        # Win by reducing opponent to 2 pieces
        if self.player1_on_board < 3 and self.phase != 'placement':
            self.is_game_over = True
            self.winner = 2
            if self.on_game_over:
                self.on_game_over(2)
            return True
        
        if self.player2_on_board < 3 and self.phase != 'placement':
            self.is_game_over = True
            self.winner = 1
            if self.on_game_over:
                self.on_game_over(1)
            return True
        
        # Win by blocking all moves (only check in movement phase)
        if self.phase in ['movement', 'flying']:
            if not self.has_valid_moves(self.current_player):
                self.is_game_over = True
                self.winner = 3 - self.current_player
                if self.on_game_over:
                    self.on_game_over(self.winner)
                return True
        
        return False
    
    def has_valid_moves(self, player: int) -> bool:
        """Check if player has any valid moves"""
        pieces_on_board = (self.player1_on_board if player == 1 
                          else self.player2_on_board)
        
        # Flying phase - can move anywhere
        if pieces_on_board <= 3:
            for i in range(self.BOARD_SIZE):
                if self.board[i] == player:
                    for j in range(self.BOARD_SIZE):
                        if self.board[j] == 0:
                            return True
            return False
        
        # Normal movement - check adjacent positions
        for i in range(self.BOARD_SIZE):
            if self.board[i] == player:
                for adj in self.ADJACENCY[i]:
                    if self.board[adj] == 0:
                        return True
        
        return False
    
    def get_valid_moves(self, player: int = None) -> List[Tuple[int, int]]:
        """Get all valid moves for player"""
        if player is None:
            player = self.current_player
        
        valid_moves = []
        
        if self.phase == 'placement':
            # All empty positions
            for i in range(self.BOARD_SIZE):
                if self.board[i] == 0:
                    valid_moves.append((None, i))
        else:
            pieces_on_board = (self.player1_on_board if player == 1 
                             else self.player2_on_board)
            
            for i in range(self.BOARD_SIZE):
                if self.board[i] == player:
                    if pieces_on_board <= 3:  # Flying
                        for j in range(self.BOARD_SIZE):
                            if self.board[j] == 0:
                                valid_moves.append((i, j))
                    else:  # Normal movement
                        for adj in self.ADJACENCY[i]:
                            if self.board[adj] == 0:
                                valid_moves.append((i, adj))
        
        return valid_moves
    
    def get_removable_pieces(self) -> List[int]:
        """Get list of opponent pieces that can be removed"""
        opponent = 3 - self.current_player
        removable = []
        
        # First, try to find pieces not in mills
        for i in range(self.BOARD_SIZE):
            if self.board[i] == opponent and not self.is_mill_formed(i):
                removable.append(i)
        
        # If all pieces are in mills, can remove any
        if not removable:
            for i in range(self.BOARD_SIZE):
                if self.board[i] == opponent:
                    removable.append(i)
        
        return removable
    
    def get_phase_name(self) -> str:
        """Get readable phase name"""
        if self.phase == 'placement':
            return 'Vendosja • Placement'
        elif self.phase == 'movement':
            return 'Lëvizja • Movement'
        else:
            return 'Fluturimi • Flying'
    
    def get_status_message(self) -> str:
        """Get current game status message"""
        if self.is_game_over:
            player_name = 'Lojtari 1 • Player 1' if self.winner == 1 else 'Lojtari 2 • Player 2'
            return f'🏆 {player_name} Fitoi! • Won!'
        
        if self.awaiting_removal:
            return '💥 Hiq një copë • Remove a piece'
        
        player_name = 'Lojtari 1 • Player 1' if self.current_player == 1 else 'Lojtari 2 • Player 2'
        return f'🎯 Radhja e {player_name} • {player_name}\'s turn'
