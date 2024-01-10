from tkinter import *
import random

game_width = 700;
game_height = 700;
speed = 200;
space_size = 50;
body_parts = 3;
snake_color = "#00FF00";
food_color = "#FF0000";
background_color = "#000000";


window = Tk()
score = 0;
direction = 'down';
label = Label(window, text="Score {}".format(score), font=('consolas', 40))
label.pack()

canvas = Canvas(window, bg=background_color, height=game_height, width=game_width)
canvas.pack()


class Snake:

    def __init__(self):

        self.coordinates = []
        self.squares = []

        for i in range(0, body_parts):
            self.coordinates.append([0,0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x,y, x+space_size,y + space_size, 
                                             fill=snake_color, 
                                             tag = "snake")
            self.squares.append(square)
class Food:

    def __init__(self):

        list_size_width = [i for i in range(0, game_width, space_size)]
        list_size_height = [i for i in range(0, game_height, space_size)]

        random_index_x = random.randint(0,len(list_size_width)-1)
        random_index_y = random.randint(0,len(list_size_height)-1)

        x = list_size_width[random_index_x]
        y = list_size_width[random_index_y]

        self.coordinates = [x, y]
        canvas.create_oval(x,y, x+space_size,y+space_size, 
                           fill=food_color, 
                           tag="food")    
class Game:
    
    def __init__(self):
        self.main()
    def next_turn(self, snake, food) -> None:
        x, y = snake.coordinates[0]

        if direction == "up":
            y -= space_size
        elif direction == "down":
            y += space_size
        elif direction == "left":
            x -= space_size
        elif direction == "right":
            x += space_size

        snake.coordinates.insert(0, (x, y))

        square = canvas.create_rectangle(x, y, x + space_size, y + space_size, fill=snake_color)

        snake.squares.insert(0, square)

        if x == food.coordinates[0] and y == food.coordinates[1]:

            global score, speed

            score += 1

            label.config(text="Score:{}".format(score))

            canvas.delete("food")

            food = Food()
            if speed != 40:
                speed -= 10

        else:

            del snake.coordinates[-1]

            canvas.delete(snake.squares[-1])

            del snake.squares[-1]


        if self.check_collisions(snake):
            self.game_over()

        else:
            window.after(speed, self.next_turn, snake, food)

    def change_direction(self, new_direction) -> None:

        global direction 

        if new_direction == 'left':
            if direction != 'right':
                direction = new_direction
        elif new_direction == 'right':
            if direction != 'left':
                direction = new_direction
        elif new_direction == 'up':
            if direction != 'down':
                direction = new_direction
        elif new_direction == 'down':
            if direction != 'up':
                direction = new_direction

    def check_collisions(self, snake) -> bool:
        x, y = snake.coordinates[0]

        if x < 0 or x >= game_width:
            return True
        elif y < 0 or y >= game_height:
            return True

        for body_part in snake.coordinates[1:]:
            if x == body_part[0] and y == body_part[1]:
                return True

        return False
    
    def game_over(self) -> None:
        canvas.delete(ALL)
        canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2,
                        font=('consolas',70), text="GAME OVER", fill="red", tag="gameover")
        
    def main(self) -> None:

        window.title("Snake Game")
        window.resizable(False, False)

        window.update()

        window_width = window.winfo_width()
        window_height = window.winfo_height()
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        x = int(screen_width / 2) - int(window_width / 2)
        y = int(screen_height / 2) - int(window_height / 2)

        window.geometry(f"{window_width}x{window_height}+{x}+{y}")

        window.bind('<Left>', lambda event: self.change_direction('left'))
        window.bind('<Right>', lambda event: self.change_direction('right'))
        window.bind('<Up>', lambda event: self.change_direction('up'))
        window.bind('<Down>', lambda event: self.change_direction('down'))

        snake = Snake()
        food = Food()

        self.next_turn(snake=snake, food=food)

        window.mainloop()

if __name__ == '__main__':
    Game()