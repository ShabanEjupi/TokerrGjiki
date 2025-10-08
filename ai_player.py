"""
AI Player Module
Intelligent opponent with Minimax and Alpha-Beta pruning algorithms
"""

import random
from typing import List, Tuple, Optional
from game_engine import GameEngine
import copy


class AIPlayer:
    """AI opponent with advanced strategic decision making using Minimax algorithm"""
    
    DIFFICULTY_LEVELS = {
        'easy': {'depth': 1, 'use_minimax': False, 'error_rate': 0.4},
        'medium': {'depth': 2, 'use_minimax': True, 'error_rate': 0.15},
        'hard': {'depth': 3, 'use_minimax': True, 'error_rate': 0.05},
        'expert': {'depth': 4, 'use_minimax': True, 'error_rate': 0.01}
    }
    
    def __init__(self, difficulty='hard'):
        self.difficulty = difficulty.lower()
        self.config = self.DIFFICULTY_LEVELS.get(self.difficulty, 
                                                 self.DIFFICULTY_LEVELS['hard'])
        self.nodes_evaluated = 0
    
    def make_move(self, game: GameEngine) -> bool:
        """Make an AI move"""
        if game.is_game_over:
            return False
        
        # Check if we need to remove a piece
        if game.awaiting_removal:
            return self.remove_piece(game)
        
        # Make a move based on phase
        if game.phase == 'placement':
            return self.place_piece(game)
        else:
            return self.move_piece(game)
    
    def place_piece(self, game: GameEngine) -> bool:
        """Place a piece using Minimax strategy"""
        # Random error injection for easier difficulties
        if random.random() < self.config['error_rate']:
            return self.make_random_placement(game)
        
        if not self.config['use_minimax']:
            return self.place_piece_heuristic(game)
        
        ai_player = game.current_player
        best_score = float('-inf')
        best_move = None
        
        # Try all possible placements
        for pos in range(game.BOARD_SIZE):
            if game.board[pos] == 0:
                # Simulate move
                game_copy = self.copy_game_state(game)
                if game_copy.place_piece(pos):
                    # Handle mill formation in simulation
                    if game_copy.awaiting_removal:
                        # Simulate removing best opponent piece
                        removable = game_copy.get_removable_pieces()
                        if removable:
                            best_remove = self.choose_best_removal(game_copy, removable)
                            game_copy.remove_piece(best_remove)
                    
                    # Evaluate position with minimax
                    score = self.minimax(game_copy, self.config['depth'] - 1, 
                                       float('-inf'), float('inf'), False, ai_player)
                    
                    if score > best_score:
                        best_score = score
                        best_move = pos
        
        if best_move is not None:
            return game.place_piece(best_move)
        
        return self.make_random_placement(game)
    
    def place_piece_heuristic(self, game: GameEngine) -> bool:
        """Place piece using heuristic rules (for easy difficulty)"""
        ai_player = game.current_player
        opponent = 3 - ai_player
        
        # Priority 1: Complete our mill
        for pos in range(game.BOARD_SIZE):
            if game.board[pos] == 0:
                game.board[pos] = ai_player
                if game.is_mill_formed(pos):
                    game.board[pos] = 0
                    return game.place_piece(pos)
                game.board[pos] = 0
        
        # Priority 2: Block opponent's mill
        for pos in range(game.BOARD_SIZE):
            if game.board[pos] == 0:
                game.board[pos] = opponent
                if game.is_mill_formed(pos):
                    game.board[pos] = 0
                    return game.place_piece(pos)
                game.board[pos] = 0
        
        # Priority 3: Strategic positions
        strategic_positions = [1, 4, 7, 10, 13, 16, 19, 22]
        random.shuffle(strategic_positions)
        
        for pos in strategic_positions:
            if game.board[pos] == 0:
                return game.place_piece(pos)
        
        return self.make_random_placement(game)
    
    def move_piece(self, game: GameEngine) -> bool:
        """Move a piece using Minimax strategy"""
        # Random error injection
        if random.random() < self.config['error_rate']:
            return self.make_random_move(game)
        
        if not self.config['use_minimax']:
            return self.move_piece_heuristic(game)
        
        ai_player = game.current_player
        valid_moves = game.get_valid_moves(ai_player)
        
        if not valid_moves:
            return False
        
        best_score = float('-inf')
        best_move = None
        
        # Evaluate all possible moves
        for from_pos, to_pos in valid_moves:
            game_copy = self.copy_game_state(game)
            
            if game_copy.move_piece(from_pos, to_pos):
                # Handle mill formation
                if game_copy.awaiting_removal:
                    removable = game_copy.get_removable_pieces()
                    if removable:
                        best_remove = self.choose_best_removal(game_copy, removable)
                        game_copy.remove_piece(best_remove)
                
                # Evaluate with minimax
                score = self.minimax(game_copy, self.config['depth'] - 1,
                                   float('-inf'), float('inf'), False, ai_player)
                
                if score > best_score:
                    best_score = score
                    best_move = (from_pos, to_pos)
        
        if best_move:
            return game.move_piece(best_move[0], best_move[1])
        
        return self.make_random_move(game)
    
    def move_piece_heuristic(self, game: GameEngine) -> bool:
        """Move piece using heuristic rules"""
        ai_player = game.current_player
        opponent = 3 - ai_player
        valid_moves = game.get_valid_moves(ai_player)
        
        if not valid_moves:
            return False
        
        # Priority 1: Form a mill
        for from_pos, to_pos in valid_moves:
            game.board[from_pos] = 0
            game.board[to_pos] = ai_player
            
            if game.is_mill_formed(to_pos):
                game.board[from_pos] = ai_player
                game.board[to_pos] = 0
                return game.move_piece(from_pos, to_pos)
            
            game.board[from_pos] = ai_player
            game.board[to_pos] = 0
        
        # Priority 2: Block opponent mill
        for from_pos, to_pos in valid_moves:
            # Simulate opponent forming mill at to_pos
            game.board[to_pos] = opponent
            blocks_mill = game.is_mill_formed(to_pos)
            game.board[to_pos] = 0
            
            if blocks_mill:
                return game.move_piece(from_pos, to_pos)
        
        # Priority 3: Random valid move
        return self.make_random_move(game)
    
    def minimax(self, game: GameEngine, depth: int, alpha: float, beta: float, 
                maximizing: bool, ai_player: int) -> float:
        """
        Minimax algorithm with alpha-beta pruning
        
        Args:
            game: Current game state
            depth: Remaining search depth
            alpha: Alpha value for pruning
            beta: Beta value for pruning
            maximizing: True if maximizing player's turn
            ai_player: AI player number (1 or 2)
        
        Returns:
            Evaluation score
        """
        self.nodes_evaluated += 1
        
        # Terminal conditions
        if depth == 0 or game.is_game_over:
            return self.evaluate_position(game, ai_player)
        
        if maximizing:
            max_eval = float('-inf')
            
            # Get all valid moves
            if game.phase == 'placement':
                moves = [(None, i) for i in range(game.BOARD_SIZE) if game.board[i] == 0]
            else:
                moves = game.get_valid_moves(game.current_player)
            
            for move in moves:
                game_copy = self.copy_game_state(game)
                
                # Make move
                if move[0] is None:  # Placement
                    if not game_copy.place_piece(move[1]):
                        continue
                else:  # Movement
                    if not game_copy.move_piece(move[0], move[1]):
                        continue
                
                # Handle mill removal
                if game_copy.awaiting_removal:
                    removable = game_copy.get_removable_pieces()
                    if removable:
                        best_remove = self.choose_best_removal(game_copy, removable)
                        game_copy.remove_piece(best_remove)
                
                eval_score = self.minimax(game_copy, depth - 1, alpha, beta, False, ai_player)
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                
                if beta <= alpha:
                    break  # Beta cutoff
            
            return max_eval
        
        else:
            min_eval = float('inf')
            
            # Get all valid moves for opponent
            if game.phase == 'placement':
                moves = [(None, i) for i in range(game.BOARD_SIZE) if game.board[i] == 0]
            else:
                moves = game.get_valid_moves(game.current_player)
            
            for move in moves:
                game_copy = self.copy_game_state(game)
                
                # Make move
                if move[0] is None:
                    if not game_copy.place_piece(move[1]):
                        continue
                else:
                    if not game_copy.move_piece(move[0], move[1]):
                        continue
                
                # Handle mill removal
                if game_copy.awaiting_removal:
                    removable = game_copy.get_removable_pieces()
                    if removable:
                        # Opponent removes our best piece
                        worst_remove = max(removable, 
                                         key=lambda p: self.evaluate_piece_value(game_copy, p, ai_player))
                        game_copy.remove_piece(worst_remove)
                
                eval_score = self.minimax(game_copy, depth - 1, alpha, beta, True, ai_player)
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                
                if beta <= alpha:
                    break  # Alpha cutoff
            
            return min_eval
    
    def remove_piece(self, game: GameEngine) -> bool:
        """Remove opponent's piece strategically"""
        removable = game.get_removable_pieces()
        
        if not removable:
            return False
        
        # Random error
        if random.random() < self.config['error_rate']:
            return game.remove_piece(random.choice(removable))
        
        # Choose best piece to remove
        best_piece = self.choose_best_removal(game, removable)
        return game.remove_piece(best_piece)
    
    def choose_best_removal(self, game: GameEngine, removable: List[int]) -> int:
        """Choose the best opponent piece to remove"""
        opponent = 3 - game.current_player
        best_score = float('-inf')
        best_piece = removable[0]
        
        for pos in removable:
            score = self.evaluate_piece_value(game, pos, opponent)
            if score > best_score:
                best_score = score
                best_piece = pos
        
        return best_piece
    
    def evaluate_piece_value(self, game: GameEngine, position: int, player: int) -> int:
        """Evaluate the value of removing a specific piece"""
        score = 0
        
        # Strategic positions are more valuable
        strategic_positions = [1, 4, 7, 10, 13, 16, 19, 22]
        if position in strategic_positions:
            score += 10
        
        # Count potential mills this piece is part of
        mills_count = 0
        for mill in game.MILLS:
            if position in mill:
                # Check if removing this piece breaks a potential mill
                other_pieces = [p for p in mill if p != position]
                if sum(1 for p in other_pieces if game.board[p] == player) >= 1:
                    mills_count += 1
        
        score += mills_count * 15
        
        # Count adjacent empty positions (mobility)
        if position in game.ADJACENCY:
            empty_adjacent = sum(1 for adj in game.ADJACENCY[position] 
                               if game.board[adj] == 0)
            score += empty_adjacent * 3
        
        return score
    
    def evaluate_position(self, game: GameEngine, player: int) -> int:
        """
        Comprehensive position evaluation function
        
        Factors considered:
        - Piece advantage
        - Mill formations
        - Two-piece configurations (potential mills)
        - Mobility (number of valid moves)
        - Strategic positions
        - Blocking opponent mills
        """
        if game.is_game_over:
            if game.winner == player:
                return 10000
            else:
                return -10000
        
        score = 0
        opponent = 3 - player
        
        # 1. Piece count advantage (most important)
        player_pieces = game.player1_on_board if player == 1 else game.player2_on_board
        opponent_pieces = game.player1_on_board if opponent == 1 else game.player2_on_board
        score += (player_pieces - opponent_pieces) * 100
        
        # 2. Formed mills
        player_mills = sum(1 for mill in game.MILLS 
                          if all(game.board[p] == player for p in mill))
        opponent_mills = sum(1 for mill in game.MILLS 
                            if all(game.board[p] == opponent for p in mill))
        score += (player_mills - opponent_mills) * 50
        
        # 3. Two-piece configurations (potential mills)
        player_two_pieces = 0
        opponent_two_pieces = 0
        
        for mill in game.MILLS:
            player_count = sum(1 for p in mill if game.board[p] == player)
            opponent_count = sum(1 for p in mill if game.board[p] == opponent)
            empty_count = sum(1 for p in mill if game.board[p] == 0)
            
            if player_count == 2 and empty_count == 1:
                player_two_pieces += 1
            if opponent_count == 2 and empty_count == 1:
                opponent_two_pieces += 1
        
        score += (player_two_pieces - opponent_two_pieces) * 30
        
        # 4. Mobility (number of valid moves)
        player_moves = len(game.get_valid_moves(player))
        opponent_moves = len(game.get_valid_moves(opponent))
        score += (player_moves - opponent_moves) * 10
        
        # 5. Strategic position control
        strategic_positions = [1, 4, 7, 10, 13, 16, 19, 22]
        player_strategic = sum(1 for pos in strategic_positions 
                              if game.board[pos] == player)
        opponent_strategic = sum(1 for pos in strategic_positions 
                                if game.board[pos] == opponent)
        score += (player_strategic - opponent_strategic) * 20
        
        # 6. Blocked opponent pieces (pieces with no valid moves)
        if game.phase in ['movement', 'flying'] and opponent_pieces > 3:
            opponent_blocked = 0
            for i in range(game.BOARD_SIZE):
                if game.board[i] == opponent:
                    can_move = False
                    if i in game.ADJACENCY:
                        for adj in game.ADJACENCY[i]:
                            if game.board[adj] == 0:
                                can_move = True
                                break
                    if not can_move:
                        opponent_blocked += 1
            score += opponent_blocked * 15
        
        return score
    
    def copy_game_state(self, game: GameEngine) -> GameEngine:
        """Create a deep copy of game state for simulation"""
        new_game = GameEngine()
        new_game.board = game.board.copy()
        new_game.current_player = game.current_player
        new_game.phase = game.phase
        new_game.player1_pieces = game.player1_pieces
        new_game.player2_pieces = game.player2_pieces
        new_game.player1_placed = game.player1_placed
        new_game.player2_placed = game.player2_placed
        new_game.player1_on_board = game.player1_on_board
        new_game.player2_on_board = game.player2_on_board
        new_game.is_game_over = game.is_game_over
        new_game.winner = game.winner
        new_game.awaiting_removal = game.awaiting_removal
        new_game.selected_position = game.selected_position
        return new_game  # MUST return the copied game!
    
    def make_random_placement(self, game: GameEngine) -> bool:
        """Make a random placement"""
        empty_positions = [i for i in range(game.BOARD_SIZE) if game.board[i] == 0]
        
        if empty_positions:
            return game.place_piece(random.choice(empty_positions))
        
        return False
    
    def make_random_move(self, game: GameEngine) -> bool:
        """Make a random move"""
        valid_moves = game.get_valid_moves(game.current_player)
        
        if valid_moves:
            from_pos, to_pos = random.choice(valid_moves)
            return game.move_piece(from_pos, to_pos)
        
        return False
