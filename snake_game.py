import tkinter as tk
import random
import winsound  # For sound effects on Windows

class SnakeGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Snake Game")
        
        self.width = 600
        self.height = 400
        self.cell_size = 20
        self.score1 = 0
        self.score2 = 0
        self.high_score = 0
        self.level = 1
        self.speed = 100
        self.is_paused = False
        self.multiplayer = False
        
        self.canvas = tk.Canvas(master, width=self.width, height=self.height, bg="black")
        self.canvas.pack()

        self.show_help()

    def show_help(self):
        self.help_frame = tk.Frame(self.master)
        self.help_frame.pack()

        tk.Label(self.help_frame, text="How to Play the Snake Game", font=('Arial', 16)).pack(pady=10)
        instructions = (
            "1. Use the arrow keys to move Player 1 (Green Snake).\n"
            "2. Use WASD keys to move Player 2 (Blue Snake).\n"
            "3. Eat the red food to grow and earn points.\n"
            "4. Avoid hitting the walls and your own tail.\n"
            "5. Press 'P' to pause the game.\n"
            "6. Press 'R' to restart after game over.\n"
        )
        tk.Label(self.help_frame, text=instructions, font=('Arial', 12)).pack(pady=10)
        tk.Button(self.help_frame, text="Start Game", command=self.show_difficulty_selection).pack(pady=5)

    def show_difficulty_selection(self):
        self.help_frame.destroy()
        self.difficulty_frame = tk.Frame(self.master)
        self.difficulty_frame.pack()

        tk.Label(self.difficulty_frame, text="Select Game Mode:").pack()
        tk.Button(self.difficulty_frame, text="Single Player", command=self.setup_single_player).pack()
        tk.Button(self.difficulty_frame, text="Multiplayer", command=self.setup_multiplayer).pack(pady=5)

    def setup_single_player(self):
        self.multiplayer = False
        self.reset_game()
        self.run_game()

    def setup_multiplayer(self):
        self.multiplayer = True
        self.reset_game()
        self.run_game()

    def reset_game(self):
        self.snake1 = [(self.cell_size * 5, self.cell_size * 5)]
        self.snake2 = [(self.cell_size * 15, self.cell_size * 15)] if self.multiplayer else []
        self.snake1_dir = (self.cell_size, 0)
        self.snake2_dir = (0, -self.cell_size) if self.multiplayer else (0, 0)
        self.obstacles = self.place_obstacles()
        self.food = self.place_food()
        self.score1 = 0
        self.score2 = 0
        self.game_over = False
        self.draw_elements()
        self.master.bind("r", self.restart_game)  # Bind 'R' key for restarting
        self.master.bind("<KeyPress>", self.change_direction)  # Bind key events

    def place_food(self):
        while True:
            x = random.randint(0, (self.width // self.cell_size) - 1) * self.cell_size
            y = random.randint(0, (self.height // self.cell_size) - 1) * self.cell_size
            if (x, y) not in self.snake1 and (x, y) not in self.snake2 and (x, y) not in self.obstacles:
                return (x, y)

    def place_obstacles(self):
        obstacles = []
        for _ in range(random.randint(3, 5)):
            while True:
                x = random.randint(0, (self.width // self.cell_size) - 1) * self.cell_size
                y = random.randint(0, (self.height // self.cell_size) - 1) * self.cell_size
                if (x, y) not in self.snake1 and (x, y) not in self.snake2 and (x, y) not in obstacles:
                    obstacles.append((x, y))
                    break
        return obstacles

    def change_direction(self, event):
        if event.keysym == 'Up' and self.snake1_dir != (0, self.cell_size):
            self.snake1_dir = (0, -self.cell_size)
        elif event.keysym == 'Down' and self.snake1_dir != (0, -self.cell_size):
            self.snake1_dir = (0, self.cell_size)
        elif event.keysym == 'Left' and self.snake1_dir != (self.cell_size, 0):
            self.snake1_dir = (-self.cell_size, 0)
        elif event.keysym == 'Right' and self.snake1_dir != (-self.cell_size, 0):
            self.snake1_dir = (self.cell_size, 0)

        if self.multiplayer:
            if event.keysym == 'w' and self.snake2_dir != (0, self.cell_size):
                self.snake2_dir = (0, -self.cell_size)
            elif event.keysym == 's' and self.snake2_dir != (0, -self.cell_size):
                self.snake2_dir = (0, self.cell_size)
            elif event.keysym == 'a' and self.snake2_dir != (self.cell_size, 0):
                self.snake2_dir = (-self.cell_size, 0)
            elif event.keysym == 'd' and self.snake2_dir != (-self.cell_size, 0):
                self.snake2_dir = (self.cell_size, 0)

        if event.keysym == 'p':
            self.toggle_pause()

    def toggle_pause(self):
        self.is_paused = not self.is_paused
        if self.is_paused:
            self.canvas.create_text(self.width // 2, self.height // 2, text="PAUSED", fill="yellow", font=('Arial', 24))
        else:
            self.run_game()

    def run_game(self):
        if self.game_over:
            return
        if not self.is_paused:
            self.move_snakes()
            self.check_collisions()
            self.draw_elements()
            self.master.after(self.speed, self.run_game)

    def move_snakes(self):
        # Move Player 1
        head1_x, head1_y = self.snake1[0]
        self.new_head1 = (head1_x + self.snake1_dir[0], head1_y + self.snake1_dir[1])
        self.snake1.insert(0, self.new_head1)

        if self.new_head1 == self.food:
            winsound.Beep(1000, 100)  # Sound effect for eating food
            self.score1 += 10
            self.food = self.place_food()  # Place new food
        else:
            self.snake1.pop()

        # Move Player 2 (if in multiplayer)
        if self.multiplayer:
            head2_x, head2_y = self.snake2[0]
            self.new_head2 = (head2_x + self.snake2_dir[0], head2_y + self.snake2_dir[1])
            self.snake2.insert(0, self.new_head2)

            if self.new_head2 == self.food:
                winsound.Beep(1000, 100)  # Sound effect for eating food
                self.score2 += 10
                self.food = self.place_food()  # Place new food
            else:
                self.snake2.pop()

    def update_high_score(self, current_score):
        if current_score > self.high_score:
            self.high_score = current_score

    def check_collisions(self):
        if not self.snake1:  # Player 1 has lost
            self.game_over = True
            self.update_high_score(self.score1)
            self.handle_game_over(1)
            return

        head1_x, head1_y = self.snake1[0]
        if (head1_x < 0 or head1_x >= self.width or
                head1_y < 0 or head1_y >= self.height or
                len(self.snake1) != len(set(self.snake1)) or
                (head1_x, head1_y) in self.obstacles or
                (self.multiplayer and (head1_x, head1_y) in self.snake2)):  # Fixed collision check
            self.game_over = True
            self.handle_game_over(1)

        if self.multiplayer:
            if not self.snake2:  # Player 2 has lost
                self.game_over = True
                self.update_high_score(self.score2)
                self.handle_game_over(2)
                return
            
            head2_x, head2_y = self.snake2[0]
            if (head2_x < 0 or head2_x >= self.width or
                    head2_y < 0 or head2_y >= self.height or
                    len(self.snake2) != len(set(self.snake2)) or
                    (head2_x, head2_y) in self.obstacles or
                    (head2_x, head2_y) in self.snake1):  # Fixed collision check
                self.game_over = True
                self.update_high_score(self.score2)
                self.handle_game_over(2)

    def handle_game_over(self, player):
        self.canvas.create_text(self.width // 2, self.height // 2, text=f"Game Over! Player {player} Lost", fill="red", font=('Arial', 24))
        self.canvas.create_text(self.width // 2, self.height // 2 + 40, text="Press 'R' to Restart", fill="yellow", font=('Arial', 16))

          # Display high score
        self.canvas.create_text(self.width // 2, self.height // 2 + 80, text=f"High Score: {self.high_score}", fill="yellow", font=('Arial', 16))

    def restart_game(self, event):
        if self.game_over:
            self.reset_game()
            self.run_game()

    def draw_elements(self):
        self.canvas.delete("all")
        for segment in self.snake1:
            self.canvas.create_rectangle(segment[0], segment[1], segment[0] + self.cell_size, segment[1] + self.cell_size, fill="green")
        for segment in self.snake2:
            self.canvas.create_rectangle(segment[0], segment[1], segment[0] + self.cell_size, segment[1] + self.cell_size, fill="blue")
        for obstacle in self.obstacles:
            self.canvas.create_rectangle(obstacle[0], obstacle[1], obstacle[0] + self.cell_size, obstacle[1] + self.cell_size, fill="gray")
        self.canvas.create_oval(self.food[0], self.food[1], self.food[0] + self.cell_size, self.food[1] + self.cell_size, fill="red")

        # Display scores and level
        self.canvas.create_text(50, 20, text=f"Player 1 Score: {self.score1}", fill="white")
        if self.multiplayer:
            self.canvas.create_text(300, 20, text=f"Player 2 Score: {self.score2}", fill="white")
        self.canvas.create_text(550, 20, text=f"High Score: {self.high_score}", fill="yellow")
        self.canvas.create_text(300, 380, text=f"Level: {self.level}", fill="yellow")

if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()
