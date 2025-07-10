import tkinter
import random


ROWS = 25
COLS = 25
TILE_SIZE = 25


WINDOW_WIDTH = TILE_SIZE * ROWS
WINDOW_HEIGHT = TILE_SIZE * COLS


class Tile:
   def __init__(self, x, y):
       self.x = x
       self.y = y


# Ventana
window = tkinter.Tk()
window.title("Juego de la Serpiente")
window.resizable(False, False)


canvas = tkinter.Canvas(window, bg="black", width=WINDOW_WIDTH, height=WINDOW_HEIGHT, borderwidth=0, highlightthickness=0)
canvas.pack()
window.update()


# Centrar ventana
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
window_x = int((screen_width / 2) - (window_width / 2))
window_y = int((screen_height / 2) - (window_height / 2))
window.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")


# Botón de reinicio
restart_button = tkinter.Button(window, text="Reiniciar", font=("Helvetica", 16, "bold"), command=lambda: restart_game())
restart_button.place_forget()  # Oculto al inicio


# Variables del juego
snake = None
food = None
snake_body = []
velocityX = 0
velocityY = 0
game_over = False
score = 0


def start_game():
   global snake, food, snake_body, velocityX, velocityY, game_over, score
   snake = Tile(5 * TILE_SIZE, 5 * TILE_SIZE)
   food = Tile(10 * TILE_SIZE, 10 * TILE_SIZE)
   snake_body = []
   velocityX = 0
   velocityY = 0
   game_over = False
   score = 0
   restart_button.place_forget()
   draw()


def restart_game():
   canvas.delete("all")
   start_game()


def change_direction(e):
   global velocityX, velocityY
   if game_over:
       return
   if e.keysym == "Up" and velocityY != 1:
       velocityX = 0
       velocityY = -1
   elif e.keysym == "Down" and velocityY != -1:
       velocityX = 0
       velocityY = 1
   elif e.keysym == "Left" and velocityX != 1:
       velocityX = -1
       velocityY = 0
   elif e.keysym == "Right" and velocityX != -1:
       velocityX = 1
       velocityY = 0


def move():
   global snake, food, snake_body, game_over, score
   if game_over:
       return
   if (snake.x < 0 or snake.x >= WINDOW_WIDTH or
       snake.y < 0 or snake.y >= WINDOW_HEIGHT):
       game_over = True
       return
   for tile in snake_body:
       if snake.x == tile.x and snake.y == tile.y:
           game_over = True
           return
   if snake.x == food.x and snake.y == food.y:
       snake_body.append(Tile(food.x, food.y))
       food.x = random.randint(0, COLS - 1) * TILE_SIZE
       food.y = random.randint(0, ROWS - 1) * TILE_SIZE
       score += 1
   for i in range(len(snake_body) - 1, 0, -1):
       snake_body[i].x = snake_body[i - 1].x
       snake_body[i].y = snake_body[i - 1].y
   if snake_body:
       snake_body[0].x = snake.x
       snake_body[0].y = snake.y
   snake.x += velocityX * TILE_SIZE
   snake.y += velocityY * TILE_SIZE


def draw():
   global game_over
   move()
   canvas.delete("all")


   # Comida
   canvas.create_rectangle(food.x, food.y, food.x + TILE_SIZE, food.y + TILE_SIZE, fill="red")


   # Serpiente
   canvas.create_rectangle(snake.x, snake.y, snake.x + TILE_SIZE, snake.y + TILE_SIZE, fill="lime green")
   for tile in snake_body:
       canvas.create_rectangle(tile.x, tile.y, tile.x + TILE_SIZE, tile.y + TILE_SIZE, fill="green")


   if game_over:
       canvas.create_text(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 40,
                          font=("Helvetica", 40, "bold"), text="GAME OVER", fill="red")
       canvas.create_text(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 10,
                          font=("Helvetica", 20, "bold"), text=f"Puntos: {score}", fill="white")
       restart_button.place(relx=0.5, rely=0.65, anchor="center")  # MÁS ABAJO
   else:
       canvas.create_text(90, 20, font=("Helvetica", 18, "bold"), text=f"Puntos: {score}", fill="white")
       window.after(100, draw)


# Iniciar
window.bind("<KeyRelease>", change_direction)
start_game()
window.mainloop()