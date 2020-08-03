from graphics import *
import time,keyboard,random
from pymsgbox import *

size = [50, 50]
sizeWin = [size[0]*10 + 50, size[1]*10]


time_step_snake = 0.07 #Время одного перемещения тела змеи
time_gen_food = 5 #Время генерации еды


snake_body = [[2,2]] #first x second y
dir_inc = [1,0]
rotate = 4
food_pos = []
save_snake_body = 0
big_food = False
last_time = time.time()
last_time_move = time.time()
update_label = True
game_over = False


win = GraphWin("Змейка", sizeWin[0], sizeWin[1])
win.setBackground("white")


def clear_main():
	global win

	vertices = [Point(0,0), Point(sizeWin[0],0), Point(sizeWin[0],sizeWin[1]), Point(0, sizeWin[1])]
	triangle = Polygon(vertices)
	triangle.setFill('white')
	triangle.setOutline('black')
	triangle.draw(win)


def print_score():
	global snake_body

	vertices = [Point(sizeWin[0]-49,0), Point(sizeWin[0],0), Point(sizeWin[0],sizeWin[1]), Point(sizeWin[0]-49, sizeWin[1])]
	triangle = Polygon(vertices)
	triangle.setFill('white')
	triangle.setOutline('black')
	triangle.draw(win)

	message = Text(Point(sizeWin[0]-20, 50), len(snake_body)-1)
	message.setTextColor('black')
	message.setStyle('italic')
	message.setSize(20)
	message.draw(win)


def print_pixel(x,y, color='black'):
	global win

	vertices = [Point(x*10+1,y*10+1), Point(x*10+8, y*10+1), Point(x*10+8, y*10+8), Point(x*10+1, y*10+8)]
	triangle = Polygon(vertices)
	triangle.setFill(color)
	triangle.setOutline('white')
	triangle.draw(win)


def gen_food(type):
	global food_pos
	global big_food

	x = random.randint(0, size[0]-2)
	y = random.randint(0, size[1]-2)
	food_pos = [x,y]

	print_pixel(x,y,'red' if not big_food else 'green')


def change_direct(direct = -1):
	global size
	global snake_body
	global dir_inc
	global food_pos
	global win
	global save_snake_body
	global big_food
	global update_label
	global game_over

	last_index = len(snake_body)-1 

	snake_body.append([snake_body[last_index][0] + dir_inc[0], snake_body[last_index][1] + dir_inc[1]])

	if snake_body[last_index+1][0] <= 0 or snake_body[last_index+1][0] > size[0]-2:
		game_over = True
	elif snake_body[last_index+1][1] <= 0 or snake_body[last_index+1][1] > size[1]-2:
		game_over = True

	snake_eat_body = False

	for i in range(0, last_index+1):
		if snake_body[i] == snake_body[last_index+1]:
			snake_eat_body = True
			break

	if snake_body[last_index+1] == food_pos:
		print_pixel(food_pos[0], food_pos[1])

		if not big_food:
			save_snake_body = 1
		else:
			save_snake_body = 3
			big_food = False

		update_label = True

		food_pos = []

	if snake_eat_body:
		game_over = True

	if direct == 1:
		dir_inc[0] = 0
		dir_inc[1] = 1
	elif direct == 3:
		dir_inc[0] = 0
		dir_inc[1] = -1
	elif direct == 2:
		dir_inc[0] = -1
		dir_inc[1] = 0
	elif direct == 4:
		dir_inc[0] = 1
		dir_inc[1] = 0


def del_snake_body():
	global snake_body

	snake_body_del = []

	for i in range(0, len(snake_body)):
		snake_body_del.append([snake_body[i][0], snake_body[i][1]])

	snake_body = []
	snake_body = snake_body_del


def set_rotate(direction):
	global rotate

	if abs(rotate - direction) != 2:
		rotate = direction



keyboard.add_hotkey('up', lambda: set_rotate(3))
keyboard.add_hotkey('left', lambda: set_rotate(2))
keyboard.add_hotkey('down', lambda: set_rotate(1))
keyboard.add_hotkey('right', lambda: set_rotate(4))

try:
	clear_main()

	while True:
		if game_over:
			box = confirm(text='Score: ' + str(len(snake_body)-1), title='Game Over', buttons=['Close', 'Restart'])
			
			if (box == 'Close'):
				win.close()
			else:
				snake_body = [[2,2]] #first x second y
				dir_inc = [1,0]
				rotate = 4
				food_pos = []
				save_snake_body = 0
				big_food = False
				last_time = time.time()
				last_time_move = time.time()
				update_label = True
				game_over = False

				clear_main()


		if update_label:
			print_score()
			update_label = False

		if len(food_pos) != 2 and time.time() - last_time >= time_gen_food:
			last_time = int(time.time())

			chance = random.randint(0,99)
			if (chance < 15):
				big_food = True

			gen_food(big_food)

		if time.time() - last_time_move >= time_step_snake:
			last_time_move = time.time()

			change_direct(rotate)

			last_index = len(snake_body)-1

			print_pixel(snake_body[last_index][0], snake_body[last_index][1])

			print_pixel(snake_body[0][0], snake_body[0][1], 'white')

			if save_snake_body == 0:
				del snake_body[0]
			else:
				save_snake_body -= 1
				update_label = True
finally:
	win.getMouse()
	win.close()