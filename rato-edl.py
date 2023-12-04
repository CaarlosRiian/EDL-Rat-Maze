import pygame
import sys

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLOCK_SIZE = 30

def load_maze(file_path):
    maze = []
    start_pos = None
    exit_pos = None
    with open(file_path, 'r') as file:
        for row_index, line in enumerate(file):
            row = [char for char in line.strip()]
            maze.append(row)
            for col_index, cell in enumerate(row):
                if cell == 'm':
                    start_pos = (row_index, col_index)
                elif cell == 'e':
                    exit_pos = (row_index, col_index)
    return maze, start_pos, exit_pos

def load_and_resize_image(image_path):
    return pygame.transform.scale(pygame.image.load(image_path), (BLOCK_SIZE, BLOCK_SIZE))

ground_image = load_and_resize_image('imgs/fundo.png')
wall_image = load_and_resize_image('imgs/muro.png')
exit_image = load_and_resize_image('imgs/queijo.webp')
mouse_image = load_and_resize_image('imgs/rato.webp')

def draw_maze(screen, maze):
    for row_index, row in enumerate(maze):
        for col_index, cell in enumerate(row):
            rect = pygame.Rect(col_index * BLOCK_SIZE, row_index * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
            if cell == '0':  
                screen.blit(ground_image, rect)
            elif cell == '1':  
                screen.blit(wall_image, rect)
            elif cell == 'e':  
                screen.blit(ground_image, rect)  
                screen.blit(exit_image, rect)     
            elif cell == 'm':  
                screen.blit(ground_image, rect)  
                screen.blit(mouse_image, rect)   

    for row_index, row in enumerate(maze):
        for col_index, cell in enumerate(row):
            if cell == 'm':  # Rato
                rect = pygame.Rect(col_index * BLOCK_SIZE, row_index * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                screen.blit(ground_image, rect) 
                screen.blit(mouse_image, rect)   

# algoritmo do busca e profundidade
def depth_first_search(maze, start_pos, exit_pos, screen):
    stack = [start_pos]
    visited = set()

    while stack:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        current_pos = stack.pop()
        if current_pos in visited:
            continue

        visited.add(current_pos)

        row, col = current_pos
        if current_pos == exit_pos: 
            return current_pos  

        neighbors = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]
        for neighbor in neighbors:
            n_row, n_col = neighbor
            if (
                0 <= n_row < len(maze)
                and 0 <= n_col < len(maze[0])
                and maze[n_row][n_col] != '1'
                and neighbor not in visited
            ):
                stack.append(neighbor)

                maze[row][col] = '0' 
                maze[n_row][n_col] = 'm' 

                draw_maze(screen, maze)

                pygame.display.flip()
                pygame.time.delay(200)  

    return None  

# Função principal
def main():
    pygame.init()
    maze, start_pos, exit_pos = load_maze('labirinto.txt')

    window_width = len(maze[0]) * BLOCK_SIZE
    window_height = len(maze) * BLOCK_SIZE
    screen = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption('Labirinto do rato mais dificil')

    clock = pygame.time.Clock()
    current_pos = start_pos

    final_pos = depth_first_search(maze, start_pos, exit_pos, screen)

    if final_pos == exit_pos:
        print("Rato encontrou a saída!")
    else:
        print("Rato não encontrou a saída.")

   # Loop de encerramento
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_RETURN:  
                    return  

if __name__ == '__main__':
    main()
