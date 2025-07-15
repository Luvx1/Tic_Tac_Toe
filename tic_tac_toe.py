"""
Tic-Tac-Toe Game with GUI
A simple 3x3 Tic-Tac-Toe game with two modes: Player vs Player and Player vs Computer.
Features intelligent AI using Minimax algorithm with Alpha-Beta Pruning.
Includes score tracking and statistics.
Beautiful modern UI with gradient backgrounds and smooth animations.
"""

import tkinter as tk
import random
import json
import os
from typing import List, Optional, Tuple, Dict
from tkinter import messagebox, ttk
from tkinter.font import Font


class ModernButton(tk.Button):
    """Custom modern button with hover effects."""
    
    def __init__(self, master, **kwargs):
        # Default modern styling
        kwargs.setdefault('font', ('Segoe UI', 12, 'bold'))
        kwargs.setdefault('bg', '#4CAF50')
        kwargs.setdefault('fg', 'white')
        kwargs.setdefault('activebackground', '#45a049')
        kwargs.setdefault('activeforeground', 'white')
        kwargs.setdefault('relief', 'flat')
        kwargs.setdefault('borderwidth', 0)
        kwargs.setdefault('padx', 20)
        kwargs.setdefault('pady', 10)
        kwargs.setdefault('cursor', 'hand2')
        
        super().__init__(master, **kwargs)
        
        # Bind hover events
        self.bind('<Enter>', self.on_enter)
        self.bind('<Leave>', self.on_leave)
    
    def on_enter(self, event):
        """Handle mouse enter event."""
        self.config(bg='#45a049')
    
    def on_leave(self, event):
        """Handle mouse leave event."""
        self.config(bg='#4CAF50')


class TicTacToe:
    """Tic-Tac-Toe game class with modern GUI interface and intelligent AI."""
    
    def __init__(self, root: tk.Tk) -> None:
        """Initialize the Tic-Tac-Toe game.
        
        Args:
            root: The main Tkinter window
        """
        self.root = root
        self.root.title("🎮 Tic-Tac-Toe 3x3 - Modern Edition")
        # Full screen mode
        self.root.state('zoomed')  # For Windows
        # self.root.attributes('-fullscreen', True)  # Alternative for other OS
        self.root.resizable(True, True)
        
        # Set modern theme colors
        self.colors = {
            'primary': '#2196F3',      # Blue
            'secondary': '#FF9800',    # Orange
            'success': '#4CAF50',      # Green
            'danger': '#F44336',       # Red
            'warning': '#FFC107',      # Yellow
            'info': '#00BCD4',         # Cyan
            'light': '#F5F5F5',        # Light gray
            'dark': '#212121',         # Dark gray
            'white': '#FFFFFF',        # White
            'black': '#000000'         # Black
        }
        
        # Configure root window
        self.root.configure(bg=self.colors['light'])
        
        self.mode: Optional[str] = None  # 'pvp' or 'pve'
        self.ai_difficulty: str = 'hard'  # 'easy', 'medium', 'hard'
        self.current_player: Optional[str] = None
        self.board: Optional[List[List[Optional[str]]]] = None
        self.buttons: Optional[List[List[Optional[tk.Button]]]] = None
        self.status_label: Optional[tk.Label] = None
        self.timer_label: Optional[tk.Label] = None
        self.turn_time: int = 30
        self.timer_id: Optional[str] = None
        self.reset_btn: Optional[ModernButton] = None
        self.back_btn: Optional[ModernButton] = None
        self.stats_btn: Optional[ModernButton] = None
        self.draw_request_btn: Optional[ModernButton] = None
        self.draw_request_active: bool = False
        self.draw_request_player: Optional[str] = None
        self.game_count: int = 0  # Đếm số trận đã chơi
        self.score_file = "tic_tac_toe_scores.json"
        self.load_scores()
        self.create_mode_selection()

    def load_scores(self) -> None:
        """Load scores from JSON file."""
        try:
            if os.path.exists(self.score_file):
                with open(self.score_file, 'r', encoding='utf-8') as f:
                    self.scores = json.load(f)
            else:
                self.scores = {
                    'pvp': {'wins': 0, 'losses': 0, 'draws': 0},
                    'pve_easy': {'wins': 0, 'losses': 0, 'draws': 0},
                    'pve_medium': {'wins': 0, 'losses': 0, 'draws': 0},
                    'pve_hard': {'wins': 0, 'losses': 0, 'draws': 0}
                }
        except Exception:
            self.scores = {
                'pvp': {'wins': 0, 'losses': 0, 'draws': 0},
                'pve_easy': {'wins': 0, 'losses': 0, 'draws': 0},
                'pve_medium': {'wins': 0, 'losses': 0, 'draws': 0},
                'pve_hard': {'wins': 0, 'losses': 0, 'draws': 0}
            }

    def save_scores(self) -> None:
        """Save scores to JSON file."""
        try:
            with open(self.score_file, 'w', encoding='utf-8') as f:
                json.dump(self.scores, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving scores: {e}")

    def update_score(self, result: str) -> None:
        """Update score based on game result.
        
        Args:
            result: Game result ('win', 'loss', 'draw')
        """
        if self.mode == 'pvp':
            key = 'pvp'
        else:
            key = f'pve_{self.ai_difficulty}'
        
        if result == 'win':
            self.scores[key]['wins'] += 1
        elif result == 'loss':
            self.scores[key]['losses'] += 1
        else:  # draw
            self.scores[key]['draws'] += 1
        
        self.save_scores()

    def create_title_frame(self, title: str) -> tk.Frame:
        """Create a beautiful title frame.
        
        Args:
            title: Title text
            
        Returns:
            Title frame widget
        """
        title_frame = tk.Frame(self.root, bg=self.colors['primary'], height=80)
        title_frame.pack(fill='x', pady=(0, 20))
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame,
            text=title,
            font=('Segoe UI', 24, 'bold'),
            fg=self.colors['white'],
            bg=self.colors['primary']
        )
        title_label.pack(expand=True)
        
        return title_frame

    def create_mode_selection(self) -> None:
        """Create the mode selection screen."""
        self.clear_window()
        
        # Create title
        self.create_title_frame("🎮 Chọn Chế Độ Chơi")
        
        # Main content frame
        content_frame = tk.Frame(self.root, bg=self.colors['light'])
        content_frame.pack(expand=True, fill='both', padx=100, pady=50)
        
        # Mode buttons
        btn_pvp = ModernButton(
            content_frame, 
            text="👥 Người vs Người", 
            font=('Segoe UI', 16, 'bold'),
            bg=self.colors['primary'],
            activebackground='#1976D2',
            width=25,
            height=2,
            command=lambda: self.start_game('pvp')
        )
        btn_pvp.pack(pady=15)
        
        btn_pve = ModernButton(
            content_frame, 
            text="🤖 Người vs Máy", 
            font=('Segoe UI', 16, 'bold'),
            bg=self.colors['secondary'],
            activebackground='#E68900',
            width=25,
            height=2,
            command=self.create_ai_difficulty_selection
        )
        btn_pve.pack(pady=15)
        
        self.stats_btn = ModernButton(
            content_frame, 
            text="📊 Xem Thống Kê", 
            font=('Segoe UI', 14, 'bold'),
            bg=self.colors['info'],
            activebackground='#00ACC1',
            width=25,
            height=2,
            command=self.show_statistics
        )
        self.stats_btn.pack(pady=15)

    def show_statistics(self) -> None:
        """Show game statistics."""
        self.clear_window()
        
        # Create title
        self.create_title_frame("📊 Thống Kê Trò Chơi")
        
        # Main content frame
        main_frame = tk.Frame(self.root, bg=self.colors['light'])
        main_frame.pack(expand=True, fill='both', padx=20, pady=10)
        
        # Create scrollable frame for statistics
        canvas = tk.Canvas(main_frame, bg=self.colors['light'], highlightthickness=0)
        scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['light'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Display statistics for each mode
        modes = [
            ('👥 Người vs Người', 'pvp', self.colors['primary']),
            ('🤖 Người vs Máy (Dễ)', 'pve_easy', self.colors['success']),
            ('🤖 Người vs Máy (Trung bình)', 'pve_medium', self.colors['warning']),
            ('🤖 Người vs Máy (Khó)', 'pve_hard', self.colors['danger'])
        ]
        
        for mode_name, mode_key, color in modes:
            stats = self.scores[mode_key]
            total_games = stats['wins'] + stats['losses'] + stats['draws']
            
            if total_games == 0:
                win_rate = 0
                loss_rate = 0
                draw_rate = 0
            else:
                win_rate = (stats['wins'] / total_games) * 100
                loss_rate = (stats['losses'] / total_games) * 100
                draw_rate = (stats['draws'] / total_games) * 100
            
            # Mode card frame
            card_frame = tk.Frame(
                scrollable_frame, 
                bg=self.colors['white'], 
                relief='raised', 
                borderwidth=2
            )
            card_frame.pack(fill='x', padx=10, pady=10)
            
            # Mode header
            header_frame = tk.Frame(card_frame, bg=color, height=50)
            header_frame.pack(fill='x')
            header_frame.pack_propagate(False)
            
            mode_label = tk.Label(
                header_frame, 
                text=mode_name, 
                font=('Segoe UI', 14, 'bold'),
                fg=self.colors['white'],
                bg=color
            )
            mode_label.pack(expand=True)
            
            # Statistics content
            content_frame = tk.Frame(card_frame, bg=self.colors['white'], padx=20, pady=15)
            content_frame.pack(fill='x')
            
            stats_text = f"""
📈 Tổng số ván: {total_games}
✅ Thắng: {stats['wins']} ({win_rate:.1f}%)
❌ Thua: {stats['losses']} ({loss_rate:.1f}%)
🤝 Hòa: {stats['draws']} ({draw_rate:.1f}%)
            """
            
            stats_label = tk.Label(
                content_frame, 
                text=stats_text, 
                font=('Segoe UI', 12),
                justify="left",
                bg=self.colors['white']
            )
            stats_label.pack()
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Back button
        back_btn = ModernButton(
            main_frame, 
            text="🔙 Quay lại", 
            font=('Segoe UI', 12, 'bold'),
            bg=self.colors['dark'],
            activebackground='#424242',
            command=self.create_mode_selection
        )
        back_btn.pack(pady=10)

    def create_ai_difficulty_selection(self) -> None:
        """Create the AI difficulty selection screen."""
        self.clear_window()
        
        # Create title
        self.create_title_frame("🤖 Chọn Độ Khó AI")
        
        # Main content frame
        content_frame = tk.Frame(self.root, bg=self.colors['light'])
        content_frame.pack(expand=True, fill='both', padx=40, pady=20)
        
        # Difficulty buttons
        btn_easy = ModernButton(
            content_frame, 
            text="😊 Dễ (Đánh ngẫu nhiên)", 
            font=('Segoe UI', 14, 'bold'),
            bg=self.colors['success'],
            activebackground='#388E3C',
            width=30,
            height=2,
            command=lambda: self.start_game_with_ai('easy')
        )
        btn_easy.pack(pady=12)
        
        btn_medium = ModernButton(
            content_frame, 
            text="😐 Trung bình (Đôi khi thông minh)", 
            font=('Segoe UI', 14, 'bold'),
            bg=self.colors['warning'],
            activebackground='#F57C00',
            width=30,
            height=2,
            command=lambda: self.start_game_with_ai('medium')
        )
        btn_medium.pack(pady=12)
        
        btn_hard = ModernButton(
            content_frame, 
            text="😈 Khó (Luôn thông minh)", 
            font=('Segoe UI', 14, 'bold'),
            bg=self.colors['danger'],
            activebackground='#D32F2F',
            width=30,
            height=2,
            command=lambda: self.start_game_with_ai('hard')
        )
        btn_hard.pack(pady=12)
        
        back_btn = ModernButton(
            content_frame, 
            text="🔙 Quay lại", 
            font=('Segoe UI', 12, 'bold'),
            bg=self.colors['dark'],
            activebackground='#424242',
            command=self.create_mode_selection
        )
        back_btn.pack(pady=20)

    def start_game_with_ai(self, difficulty: str) -> None:
        """Start a new game with AI at specified difficulty.
        
        Args:
            difficulty: AI difficulty level ('easy', 'medium', 'hard')
        """
        self.ai_difficulty = difficulty
        self.start_game('pve')

    def start_game(self, mode: str) -> None:
        """Start a new game with the specified mode.
        
        Args:
            mode: Game mode ('pvp' for player vs player, 'pve' for player vs computer)
        """
        self.mode = mode
        self.board = [[None for _ in range(3)] for _ in range(3)]
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        
        # Xác định người chơi đầu tiên dựa trên số trận đã chơi
        if mode == 'pvp':
            # Trận lẻ: X là người chơi 1, trận chẵn: X là người chơi 2
            if self.game_count % 2 == 0:
                self.current_player = 'X'  # X đi trước (người chơi 1)
            else:
                self.current_player = 'O'  # O đi trước (X là người chơi 2)
        else:
            self.current_player = 'X'  # Trong PvE, X luôn đi trước
        
        self.clear_window()
        
        # Create title
        title_text = "🎮 Tic-Tac-Toe"
        if mode == 'pve':
            difficulty_map = {'easy': 'Dễ', 'medium': 'Trung bình', 'hard': 'Khó'}
            title_text += f" vs AI ({difficulty_map[self.ai_difficulty]})"
        self.create_title_frame(title_text)
        
        # Main game container
        main_container = tk.Frame(self.root, bg=self.colors['light'])
        main_container.pack(expand=True, fill='both', padx=15, pady=5)
        
        # Left panel - Game info and controls
        left_panel = tk.Frame(main_container, bg=self.colors['white'], relief='raised', borderwidth=2)
        left_panel.pack(side='left', fill='y', padx=(0, 8))
        
        # Game info section
        info_frame = tk.Frame(left_panel, bg=self.colors['white'], padx=15, pady=15)
        info_frame.pack(fill='x')
        
        # Current player info
        difficulty_text = ""
        player_info = ""
        if mode == 'pve':
            difficulty_map = {'easy': 'Dễ', 'medium': 'Trung bình', 'hard': 'Khó'}
            difficulty_text = f" (AI: {difficulty_map[self.ai_difficulty]})"
        else:  # pvp mode
            # Xác định người chơi dựa trên lượt hiện tại và số trận đã chơi
            if self.game_count % 2 == 0:
                # Trận lẻ: X là người chơi 1, O là người chơi 2
                player_info = f" (Người chơi {1 if self.current_player == 'X' else 2})"
            else:
                # Trận chẵn: O là người chơi 1, X là người chơi 2
                player_info = f" (Người chơi {1 if self.current_player == 'O' else 2})"
        
        self.status_label = tk.Label(
            info_frame, 
            text=f"🎯 Lượt của: {self.current_player}{player_info}{difficulty_text}", 
            font=('Segoe UI', 16, 'bold'),
            fg=self.colors['primary'],
            bg=self.colors['white']
        )
        self.status_label.pack(pady=(0, 10))
        
        # Timer
        self.timer_label = tk.Label(
            info_frame,
            text=f"⏰ Thời gian còn lại: {self.turn_time}s",
            font=('Segoe UI', 14, 'bold'),
            fg=self.colors['danger'],
            bg=self.colors['white']
        )
        self.timer_label.pack(pady=(0, 20))
        
        # Control buttons
        controls_frame = tk.Frame(left_panel, bg=self.colors['white'], padx=15, pady=15)
        controls_frame.pack(fill='x')
        
        self.reset_btn = ModernButton(
            controls_frame, 
            text="🔄 Chơi lại", 
            font=('Segoe UI', 12, 'bold'),
            bg=self.colors['success'],
            activebackground='#388E3C',
            width=20,
            command=self.reset_game
        )
        self.reset_btn.pack(pady=5)
        
        self.stats_btn = ModernButton(
            controls_frame, 
            text="📊 Thống kê", 
            font=('Segoe UI', 12, 'bold'),
            bg=self.colors['info'],
            activebackground='#00ACC1',
            width=20,
            command=self.show_statistics
        )
        self.stats_btn.pack(pady=5)
        
        # Draw request button (only for PvP mode)
        if mode == 'pvp':
            self.draw_request_btn = ModernButton(
                controls_frame, 
                text="🤝 Cầu hòa", 
                font=('Segoe UI', 12, 'bold'),
                bg=self.colors['warning'],
                activebackground='#FFA000',
                width=20,
                command=self.request_draw
            )
            self.draw_request_btn.pack(pady=5)
        
        self.back_btn = ModernButton(
            controls_frame, 
            text="🔙 Quay lại chọn chế độ", 
            font=('Segoe UI', 12, 'bold'),
            bg=self.colors['dark'],
            activebackground='#424242',
            width=20,
            command=self.create_mode_selection
        )
        self.back_btn.pack(pady=5)
        
        # Game instructions
        instructions_frame = tk.Frame(left_panel, bg=self.colors['white'], padx=15, pady=15)
        instructions_frame.pack(fill='x')
        
        instructions_text = "📖 Hướng dẫn:\n• Click vào ô để đánh\n• Mỗi lượt có 30 giây\n• X luôn đi trước\n• 3 ô liên tiếp để thắng"
        if mode == 'pvp':
            instructions_text += "\n• Bấm 'Cầu hòa' để đề nghị hòa"
        
        instructions_label = tk.Label(
            instructions_frame,
            text=instructions_text,
            font=('Segoe UI', 10),
            fg=self.colors['dark'],
            bg=self.colors['white'],
            justify='left'
        )
        instructions_label.pack()
        
        # Center panel - Game board
        center_panel = tk.Frame(main_container, bg=self.colors['white'], relief='raised', borderwidth=2)
        center_panel.pack(side='left', fill='both', expand=True, padx=8)
        
        # Game board frame
        board_frame = tk.Frame(center_panel, bg=self.colors['white'], padx=30, pady=30)
        board_frame.pack(expand=True)
        
        # Create game buttons with modern styling
        for i in range(3):
            for j in range(3):
                btn = tk.Button(
                    board_frame, 
                    text="", 
                    font=('Segoe UI', 36, 'bold'),
                    width=4, 
                    height=2,
                    bg=self.colors['white'],
                    fg=self.colors['dark'],
                    relief='raised',
                    borderwidth=3,
                    cursor='hand2',
                    command=lambda row=i, col=j: self.handle_click(row, col)
                )
                btn.grid(row=i, column=j, padx=10, pady=10)
                self.buttons[i][j] = btn
                
                # Add hover effect
                btn.bind('<Enter>', lambda e, b=btn: b.config(bg='#E3F2FD'))
                btn.bind('<Leave>', lambda e, b=btn: b.config(bg=self.colors['white']))
        
        # Right panel - Statistics and history
        right_panel = tk.Frame(main_container, bg=self.colors['white'], relief='raised', borderwidth=2)
        right_panel.pack(side='right', fill='y', padx=(8, 0))
        
        # Current game stats
        stats_frame = tk.Frame(right_panel, bg=self.colors['white'], padx=15, pady=15)
        stats_frame.pack(fill='x')
        
        stats_title = tk.Label(
            stats_frame,
            text="📈 Thống kê hiện tại",
            font=('Segoe UI', 14, 'bold'),
            fg=self.colors['primary'],
            bg=self.colors['white']
        )
        stats_title.pack(pady=(0, 10))
        
        # Get current mode stats
        if mode == 'pvp':
            current_stats = self.scores['pvp']
        else:
            current_stats = self.scores[f'pve_{self.ai_difficulty}']
        
        total_games = current_stats['wins'] + current_stats['losses'] + current_stats['draws']
        if total_games > 0:
            win_rate = (current_stats['wins'] / total_games) * 100
            loss_rate = (current_stats['losses'] / total_games) * 100
            draw_rate = (current_stats['draws'] / total_games) * 100
        else:
            win_rate = loss_rate = draw_rate = 0
        
        stats_text = f"""
🎮 Tổng ván: {total_games}
✅ Thắng: {current_stats['wins']} ({win_rate:.1f}%)
❌ Thua: {current_stats['losses']} ({loss_rate:.1f}%)
🤝 Hòa: {current_stats['draws']} ({draw_rate:.1f}%)
        """
        
        stats_label = tk.Label(
            stats_frame,
            text=stats_text,
            font=('Segoe UI', 11),
            fg=self.colors['dark'],
            bg=self.colors['white'],
            justify='left'
        )
        stats_label.pack()
        
        # Game mode info
        mode_frame = tk.Frame(right_panel, bg=self.colors['white'], padx=15, pady=15)
        mode_frame.pack(fill='x')
        
        mode_title = tk.Label(
            mode_frame,
            text="🎯 Thông tin chế độ",
            font=('Segoe UI', 14, 'bold'),
            fg=self.colors['primary'],
            bg=self.colors['white']
        )
        mode_title.pack(pady=(0, 10))
        
        if mode == 'pvp':
            # Hiển thị thông tin người chơi dựa trên số trận
            if self.game_count % 2 == 0:
                # Trận lẻ: X là người chơi 1, O là người chơi 2
                mode_text = "👥 Người vs Người\n• Người chơi 1 (X) đi trước\n• Người chơi 2 (O) đi sau\n• Thay phiên nhau"
            else:
                # Trận chẵn: O là người chơi 1, X là người chơi 2
                mode_text = "👥 Người vs Người\n• Người chơi 1 (O) đi trước\n• Người chơi 2 (X) đi sau\n• Thay phiên nhau"
        else:
            difficulty_map = {'easy': 'Dễ', 'medium': 'Trung bình', 'hard': 'Khó'}
            mode_text = f"🤖 Người vs Máy\n• Bạn là X\n• AI là O\n• Độ khó: {difficulty_map[self.ai_difficulty]}"
        
        mode_label = tk.Label(
            mode_frame,
            text=mode_text,
            font=('Segoe UI', 11),
            fg=self.colors['dark'],
            bg=self.colors['white'],
            justify='left'
        )
        mode_label.pack()
        
        # Quick actions
        actions_frame = tk.Frame(right_panel, bg=self.colors['white'], padx=15, pady=15)
        actions_frame.pack(fill='x')
        
        actions_title = tk.Label(
            actions_frame,
            text="⚡ Thao tác nhanh",
            font=('Segoe UI', 14, 'bold'),
            fg=self.colors['primary'],
            bg=self.colors['white']
        )
        actions_title.pack(pady=(0, 10))
        
        actions_text = """
🔄 F5: Chơi lại
📊 Ctrl+S: Xem thống kê
🔙 Esc: Quay lại menu
⏸️ Space: Tạm dừng
        """
        
        actions_label = tk.Label(
            actions_frame,
            text=actions_text,
            font=('Segoe UI', 10),
            fg=self.colors['dark'],
            bg=self.colors['white'],
            justify='left'
        )
        actions_label.pack()
        
        self.start_timer()
        
        if self.mode == 'pve' and self.current_player == 'O':
            self.root.after(500, self.computer_move)

    def start_timer(self):
        self.stop_timer()
        self.turn_time = 30
        self.update_timer_label()
        self.timer_id = self.root.after(1000, self.countdown)

    def countdown(self):
        self.turn_time -= 1
        self.update_timer_label()
        if self.turn_time <= 0:
            self.handle_timeout()
        else:
            self.timer_id = self.root.after(1000, self.countdown)

    def update_timer_label(self):
        if self.timer_label:
            self.timer_label.config(text=f"⏰ Thời gian còn lại: {self.turn_time}s")

    def stop_timer(self):
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None

    def request_draw(self):
        """Request a draw in PvP mode."""
        if self.mode != 'pvp' or self.draw_request_active:
            return
            
        # Set draw request active
        self.draw_request_active = True
        self.draw_request_player = self.current_player
        
        # Update button text
        if self.draw_request_btn:
            self.draw_request_btn.config(text="⏳ Đang chờ...", state='disabled')
        
        # Show message to current player
        messagebox.showinfo("🤝 Yêu cầu hòa", f"Đã gửi yêu cầu hòa đến người chơi {self.get_other_player()}")
        
        # Show dialog to other player
        self.show_draw_response_dialog()
    
    def get_other_player(self) -> str:
        """Get the other player's symbol."""
        return 'O' if self.current_player == 'X' else 'X'
    
    def show_draw_response_dialog(self):
        """Show dialog to the other player to accept/reject draw request."""
        other_player = self.get_other_player()
        
        # Create custom dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("🤝 Yêu cầu hòa")
        dialog.geometry("400x200")
        dialog.configure(bg=self.colors['light'])
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (dialog.winfo_screenheight() // 2) - (200 // 2)
        dialog.geometry(f"400x200+{x}+{y}")
        
        # Message
        message_label = tk.Label(
            dialog,
            text=f"Người chơi {self.draw_request_player} muốn cầu hòa.\nBạn có đồng ý không?",
            font=('Segoe UI', 14, 'bold'),
            fg=self.colors['dark'],
            bg=self.colors['light'],
            wraplength=350
        )
        message_label.pack(pady=20)
        
        # Buttons frame
        buttons_frame = tk.Frame(dialog, bg=self.colors['light'])
        buttons_frame.pack(pady=20)
        
        # Accept button
        accept_btn = ModernButton(
            buttons_frame,
            text="✅ Đồng ý",
            font=('Segoe UI', 12, 'bold'),
            bg=self.colors['success'],
            activebackground='#388E3C',
            command=lambda: self.handle_draw_response(True, dialog)
        )
        accept_btn.pack(side='left', padx=10)
        
        # Reject button
        reject_btn = ModernButton(
            buttons_frame,
            text="❌ Từ chối",
            font=('Segoe UI', 12, 'bold'),
            bg=self.colors['danger'],
            activebackground='#D32F2F',
            command=lambda: self.handle_draw_response(False, dialog)
        )
        reject_btn.pack(side='left', padx=10)
        
        # Auto-close after 30 seconds
        dialog.after(30000, lambda: self.handle_draw_response(False, dialog))
    
    def handle_draw_response(self, accepted: bool, dialog: tk.Toplevel):
        """Handle the response to draw request."""
        dialog.destroy()
        
        if accepted:
            # Draw accepted
            self.end_game_draw()
        else:
            # Draw rejected
            self.draw_request_active = False
            self.draw_request_player = None
            
            # Reset button
            if self.draw_request_btn:
                self.draw_request_btn.config(text="🤝 Cầu hòa", state='normal')
            
            # Show message
            messagebox.showinfo("❌ Từ chối", "Yêu cầu hòa đã bị từ chối. Tiếp tục chơi!")
    
    def end_game_draw(self):
        """End the game as a draw."""
        self.draw_request_active = False
        self.draw_request_player = None
        
        if self.status_label is not None:
            self.status_label.config(text="🤝 Hòa!", fg=self.colors['warning'])
        
        self.disable_all_buttons()
        self.update_score('draw')
        messagebox.showinfo("🎉 Kết quả", "Hòa!")
        self.stop_timer()
        
        # Reset draw request button
        if self.draw_request_btn:
            self.draw_request_btn.config(text="🤝 Cầu hòa", state='normal')

    def handle_timeout(self):
        # Nếu hết giờ mà chưa đi, tự động chuyển lượt
        if self.board and self.current_player:
            # Nếu là người với máy và đến lượt máy thì không timeout
            if self.mode == 'pve' and self.current_player == 'O':
                return
            # Chuyển lượt mà không đi nước nào
            self.current_player = 'O' if self.current_player == 'X' else 'X'
            if self.status_label:
                difficulty_text = ""
                player_info = ""
                if self.mode == 'pve':
                    difficulty_map = {'easy': 'Dễ', 'medium': 'Trung bình', 'hard': 'Khó'}
                    difficulty_text = f" (AI: {difficulty_map[self.ai_difficulty]})"
                else:  # pvp mode
                    # Xác định người chơi dựa trên lượt hiện tại và số trận đã chơi
                    if self.game_count % 2 == 0:
                        # Trận lẻ: X là người chơi 1, O là người chơi 2
                        player_info = f" (Người chơi {1 if self.current_player == 'X' else 2})"
                    else:
                        # Trận chẵn: O là người chơi 1, X là người chơi 2
                        player_info = f" (Người chơi {1 if self.current_player == 'O' else 2})"
                self.status_label.config(text=f"🎯 Lượt của: {self.current_player}{player_info}{difficulty_text}", fg=self.colors['primary'])
            self.start_timer()
            # Nếu là người với máy và chuyển sang máy thì gọi AI đi
            if self.mode == 'pve' and self.current_player == 'O':
                self.root.after(500, self.computer_move)

    def handle_click(self, row: int, col: int) -> None:
        """Handle button click events.
        
        Args:
            row: Row index of the clicked button
            col: Column index of the clicked button
        """
        if self.board is None or self.buttons is None:
            return
            
        if self.board[row][col] is not None:
            return
        if self.mode == 'pve' and self.current_player == 'O':
            return  # Chặn người chơi đi khi đến lượt máy
        self.make_move(row, col)
        self.start_timer()
        if self.mode == 'pve' and self.current_player == 'O':
            self.root.after(500, self.computer_move)

    def make_move(self, row: int, col: int) -> None:
        """Make a move on the board.
        
        Args:
            row: Row index for the move
            col: Column index for the move
        """
        if self.board is None or self.buttons is None or self.current_player is None:
            return
            
        self.board[row][col] = self.current_player
        button = self.buttons[row][col]
        if button is not None:
            # Set color based on player
            if self.current_player == 'X':
                button.config(text=self.current_player, state='disabled', fg=self.colors['primary'])
            else:
                button.config(text=self.current_player, state='disabled', fg=self.colors['secondary'])
        
        winner = self.check_winner()
        
        if winner:
            # Create winner message
            if self.mode == 'pvp':
                winner_text = f"🎉 Người chơi {1 if winner == 'X' else 2} ({winner}) thắng!"
            else:
                winner_text = f"🎉 {winner} thắng!"
            
            if self.status_label is not None:
                self.status_label.config(text=winner_text, fg=self.colors['success'])
            self.disable_all_buttons()
            
            # Update score
            if self.mode == 'pvp':
                # In PvP, X always goes first, so X is player 1, O is player 2
                if winner == 'X':
                    self.update_score('win')  # Player 1 wins
                else:
                    self.update_score('loss')  # Player 2 wins
            else:
                # In PvE, player is always X, AI is always O
                if winner == 'X':
                    self.update_score('win')  # Player wins
                else:
                    self.update_score('loss')  # AI wins
            
            messagebox.showinfo("🎉 Kết quả", winner_text)
            self.stop_timer()
        elif self.is_draw():
            if self.status_label is not None:
                self.status_label.config(text="🤝 Hòa!", fg=self.colors['warning'])
            self.disable_all_buttons()
            self.update_score('draw')
            messagebox.showinfo("🎉 Kết quả", "Hòa!")
            self.stop_timer()
        else:
            self.current_player = 'O' if self.current_player == 'X' else 'X'
            if self.status_label is not None:
                difficulty_text = ""
                player_info = ""
                if self.mode == 'pve':
                    difficulty_map = {'easy': 'Dễ', 'medium': 'Trung bình', 'hard': 'Khó'}
                    difficulty_text = f" (AI: {difficulty_map[self.ai_difficulty]})"
                else:  # pvp mode
                    player_info = f" (Người chơi {1 if self.current_player == 'X' else 2})"
                self.status_label.config(text=f"🎯 Lượt của: {self.current_player}{player_info}{difficulty_text}", fg=self.colors['primary'])
            self.start_timer()

    def computer_move(self) -> None:
        """Make a computer move based on AI difficulty."""
        if self.board is None:
            return
            
        empty = [(i, j) for i in range(3) for j in range(3) if self.board[i][j] is None]
        if not empty:
            return
            
        if self.ai_difficulty == 'easy':
            # Random move
            row, col = random.choice(empty)
        elif self.ai_difficulty == 'medium':
            # 70% smart, 30% random
            if random.random() < 0.7:
                row, col = self.get_best_move()
            else:
                row, col = random.choice(empty)
        else:  # hard
            # Always smart
            row, col = self.get_best_move()
            
        self.make_move(row, col)
        self.start_timer()

    def get_best_move(self) -> Tuple[int, int]:
        """Get the best move using Minimax algorithm.
        
        Returns:
            Tuple of (row, col) for the best move
        """
        if self.board is None:
            return (0, 0)
            
        best_score = float('-inf')
        best_move = (0, 0)
        
        for i in range(3):
            for j in range(3):
                if self.board[i][j] is None:
                    self.board[i][j] = 'O'
                    score = self.minimax(self.board, 0, False, float('-inf'), float('inf'))
                    self.board[i][j] = None
                    
                    if score > best_score:
                        best_score = score
                        best_move = (i, j)
        
        return best_move

    def minimax(self, board: List[List[Optional[str]]], depth: int, is_maximizing: bool, alpha: float, beta: float) -> float:
        """Minimax algorithm with Alpha-Beta pruning.
        
        Args:
            board: Current game board
            depth: Current depth in the search tree
            is_maximizing: True if maximizing player's turn
            alpha: Alpha value for pruning
            beta: Beta value for pruning
            
        Returns:
            Best score for the current position
        """
        winner = self.check_winner_on_board(board)
        
        if winner == 'O':  # AI wins
            return 1
        elif winner == 'X':  # Player wins
            return -1
        elif self.is_board_full(board):  # Draw
            return 0
            
        if is_maximizing:
            max_eval = float('-inf')
            for i in range(3):
                for j in range(3):
                    if board[i][j] is None:
                        board[i][j] = 'O'
                        eval_score = self.minimax(board, depth + 1, False, alpha, beta)
                        board[i][j] = None
                        max_eval = max(max_eval, eval_score)
                        alpha = max(alpha, eval_score)
                        if beta <= alpha:
                            break
            return max_eval
        else:
            min_eval = float('inf')
            for i in range(3):
                for j in range(3):
                    if board[i][j] is None:
                        board[i][j] = 'X'
                        eval_score = self.minimax(board, depth + 1, True, alpha, beta)
                        board[i][j] = None
                        min_eval = min(min_eval, eval_score)
                        beta = min(beta, eval_score)
                        if beta <= alpha:
                            break
            return min_eval

    def check_winner_on_board(self, board: List[List[Optional[str]]]) -> Optional[str]:
        """Check if there's a winner on a given board.
        
        Args:
            board: Board to check
            
        Returns:
            The winner symbol ('X' or 'O') or None if no winner
        """
        # Check rows
        for i in range(3):
            if board[i][0] == board[i][1] == board[i][2] and board[i][0] is not None:
                return board[i][0]
        # Check columns
        for i in range(3):
            if board[0][i] == board[1][i] == board[2][i] and board[0][i] is not None:
                return board[0][i]
        # Check diagonals
        if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
            return board[0][0]
        if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not None:
            return board[0][2]
        return None

    def is_board_full(self, board: List[List[Optional[str]]]) -> bool:
        """Check if a board is full.
        
        Args:
            board: Board to check
            
        Returns:
            True if board is full, False otherwise
        """
        return all(board[i][j] is not None for i in range(3) for j in range(3))

    def check_winner(self) -> Optional[str]:
        """Check if there's a winner.
        
        Returns:
            The winner symbol ('X' or 'O') or None if no winner
        """
        if self.board is None:
            return None
        return self.check_winner_on_board(self.board)

    def is_draw(self) -> bool:
        """Check if the game is a draw.
        
        Returns:
            True if the game is a draw, False otherwise
        """
        if self.board is None:
            return False
        return all(self.board[i][j] is not None for i in range(3) for j in range(3)) and not self.check_winner()

    def disable_all_buttons(self) -> None:
        """Disable all game buttons."""
        if self.buttons is None:
            return
        for i in range(3):
            for j in range(3):
                button = self.buttons[i][j]
                if button is not None:
                    button.config(state='disabled')

    def reset_game(self) -> None:
        """Reset the game to start a new round."""
        # Reset draw request state
        self.draw_request_active = False
        self.draw_request_player = None
        
        if self.mode:
            if self.mode == 'pve':
                self.start_game_with_ai(self.ai_difficulty)
            else:
                self.start_game(self.mode)

    def clear_window(self) -> None:
        """Clear all widgets from the main window."""
        self.stop_timer()
        for widget in self.root.winfo_children():
            widget.destroy()


def main() -> None:
    """Main function to start the game."""
    root = tk.Tk()
    app = TicTacToe(root)
    root.mainloop()


if __name__ == "__main__":
    main() 