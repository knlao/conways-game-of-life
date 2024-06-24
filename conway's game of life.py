import pygame
from copy import deepcopy
from random import randint

### CHANGE THE VALUES BELOW ###
BOX_W = 10
BOX_H = 10
BOX_X = 32
BOX_Y = 32

FPS = 600
### CHANGE THE VALUES ABOVE ###

PADDING = 3

INFO_HEIGHT = 20

COLOR = [(255, 255, 255), (0, 0, 0)]

boxes = [[randint(0, 1) for x in range(BOX_X)] for y in range(BOX_Y)]
boxes_tmp = [[0 for x in range(BOX_X)] for y in range(BOX_Y)]
boxes_history = []
boxes_history.append(deepcopy(boxes))

pygame.init()
pygame.font.init()

pygame.display.set_caption("Conway's Game of Life")
screen = pygame.display.set_mode([BOX_X*BOX_W+PADDING, BOX_Y*BOX_H+PADDING+INFO_HEIGHT])

info_font = pygame.font.SysFont("MingLiU", 20)

running = True
iterations = 0
first_repeat_iter = -1

screen.fill((222, 222, 222))


def count_neighbours(x, y):
	cnt = 0
	if y-1 >= 0 and x-1 >= 0:
		cnt += boxes[y-1][x-1]
	if y-1 >= 0:
		cnt += boxes[y-1][x]
	if y-1 >= 0 and x+1 < BOX_X:
		cnt += boxes[y-1][x+1]
	if x-1 >= 0:
		cnt += boxes[y][x-1]
	if x+1 < BOX_X:
		cnt += boxes[y][x+1]
	if y+1 < BOX_Y and x-1 >= 0:
		cnt += boxes[y+1][x-1]
	if y+1 < BOX_Y:
		cnt += boxes[y+1][x]
	if y+1 < BOX_Y and x+1 < BOX_X:
		cnt += boxes[y+1][x+1]
	return cnt


# Main code

while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
			continue
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_r:		
				boxes = [[randint(0, 1) for x in range(BOX_X)] for y in range(BOX_Y)]
				boxes_tmp = [[0 for x in range(BOX_X)] for y in range(BOX_Y)]
				iterations = 0
				first_repeat_iter = -1
				boxes_history.clear()
				screen.fill((222, 222, 222))
				continue
			if event.key == pygame.K_q:
				running = False
				continue

	for x in range(BOX_X):
		for y in range(BOX_Y):
			n = count_neighbours(x, y)
			if boxes_tmp[y][x] == 1:
				if n < 2:
					boxes_tmp[y][x] = 0
				if n == 2 or n == 3:
					boxes_tmp[y][x] = 1
				if n > 3:
					boxes_tmp[y][x] = 0
			elif n == 3:
				boxes_tmp[y][x] = 1

	screen.fill((222, 222, 222))

	if boxes_tmp in boxes_history:
		if first_repeat_iter == -1:
			first_repeat_iter = iterations
		info2 = info_font.render(f"Repeated at {first_repeat_iter}", True, (0, 0, 0))
		screen.blit(info2, (BOX_X*BOX_W/2, BOX_Y*BOX_H+PADDING))

	boxes = deepcopy(boxes_tmp)
	boxes_history.append(deepcopy(boxes))

	iterations += 1

	for x in range(BOX_X):
		for y in range(BOX_Y):
			pygame.draw.rect(screen, COLOR[boxes[y][x]], pygame.Rect(x*BOX_W+PADDING, y*BOX_H+PADDING, BOX_W-PADDING, BOX_H-PADDING))

	info = info_font.render(f"Iterations: {iterations}", True, (0, 0, 0))
	screen.blit(info, (0, BOX_Y*BOX_H+PADDING))

	pygame.display.flip()

	pygame.time.wait(int(1000/FPS))

pygame.quit()
