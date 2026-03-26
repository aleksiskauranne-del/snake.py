import tkinter
import random

ROWS = 25
COL = 25
TILE_SIZE = 25

WINDOW_WIDTH = TILE_SIZE * ROWS
WINDOW_HEIGHT = TILE_SIZE * COL

class tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
#game window
window = tkinter.Tk()
window.title("mato")
window.resizable(False, False)

canvas = tkinter.Canvas(window, bg = "black", width = WINDOW_WIDTH, height = WINDOW_HEIGHT, borderwidth = 0, highlightthickness = 0)
canvas.pack()
window.update()

#center the window
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

window_x = int((screen_width/2) - (window_width/2))
window_y = int((screen_height/2) - (window_height/2))
#format "(W)x(h)+(y)"
window.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")

#initialize game
snake = tile(5*TILE_SIZE, 5*TILE_SIZE) #single tile, snake`s head
food = tile(10*TILE_SIZE, 10*TILE_SIZE)
snake_body = [] #multiple snake tiles
velocityX = 0
velocityY = 0
game_over = False
score = 0

def change_direction(e): #e = event
    # print(e)
    # print(e.keysym)
    global velocityX, velocityY, game_over
    if (game_over):
        return
    
    if (e.keysym == "Up" and velocityY != 1):
        velocityX = 0
        velocityY = -1
    elif (e.keysym == "Down" and velocityY != -1):
        velocityX = 0
        velocityY = 1
    elif (e.keysym == "Left" and velocityX != 1):
        velocityX = -1
        velocityY = 0
    elif(e.keysym == "Right"and velocityX != -1):
        velocityX = 1
        velocityY = 0
        
def move():
    global snake, food, snake_body, game_over, score
    if (game_over):
        return
    
    if (snake.x < 0 or snake.x >= WINDOW_WIDTH or snake.y < 0 or snake.y >= WINDOW_HEIGHT):
        game_over = True
        return
    
    for body_part in snake_body:
        if (snake.x == body_part.x and snake.y == body_part.y):
            game_over = True
            return
    
    #collision
    if (snake.x == food.x and snake.y == food.y):
        snake_body.append(tile(food.x, food.y))
        food.x = random.randint(0, COL-1) * TILE_SIZE
        food.y = random.randint(0, ROWS-1) * TILE_SIZE
        score += 1
        
    #update snake body
    for i in range(len(snake_body)-1, 0, -1):
        snake_body[i].x = snake_body[i-1].x
        snake_body[i].y = snake_body[i-1].y
    if len(snake_body) > 0:
        snake_body[0].x = snake.x
        snake_body[0].y = snake.y
    snake.x += velocityX * TILE_SIZE
    snake.y += velocityY * TILE_SIZE
        

def draw():
    global snake, food, snake_body, game_over, score
    move()
    canvas.delete("all")
    
    # draw food
    canvas.create_rectangle(food.x, food.y, food.x + TILE_SIZE, food.y + TILE_SIZE, fill = "white")
    
    # draw snake
    canvas.create_rectangle(snake.x, snake.y, snake.x + TILE_SIZE, snake.y + TILE_SIZE, fill = "blue")

    for tile in snake_body:
        canvas.create_rectangle(tile.x, tile.y, tile.x + TILE_SIZE, tile.y + TILE_SIZE, fill = "blue")
    
    if (game_over):
        canvas.create_text(WINDOW_WIDTH/2, WINDOW_HEIGHT/2, font = "Areial 20", text = f"Game Over: {score}", fill = "white")
    else:
        canvas.create_text(30, 20, font = "Arial 10", text = f"Score: {score}", fill = "white")
        window.after(100, draw)  # 100ms = 1/10 second, 10 frames/second
    
window.bind("<KeyRelease>", change_direction)
draw()
window.mainloop()