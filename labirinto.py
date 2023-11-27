import pygame
import random
import heapq

# Definindo as cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Definindo as dimensões do labirinto
ROWS = 8
COLS = 9

# Inicializando o Pygame
pygame.init()

# Definindo o tamanho da tela
WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Labirinto sem Rato")

# Calculando o tamanho de cada célula
CELL_WIDTH = WIDTH // COLS
CELL_HEIGHT = HEIGHT // ROWS

def generate_maze(rows, cols):
    while True:
        maze = [[random.choice([0, 1]) for _ in range(cols)] for _ in range(rows)]
        maze[0][0] = 0  # Garantindo que o ponto de início seja sempre aberto
        maze[rows - 1][cols - 1] = 0  # Garantindo que o ponto final seja sempre aberto

        open_cells = get_open_cells(maze)  # Obtendo as células abertas

        # Verificando se há um caminho do ponto de início ao ponto final
        if a_star(maze, (0, 0), (rows - 1, cols - 1), open_cells):
            return maze

# Função para desenhar o labirinto
def draw_maze(maze):
    for row in range(ROWS):
        for col in range(COLS):
            if maze[row][col] == 1:
                pygame.draw.rect(screen, BLACK, (col * CELL_WIDTH, row * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT))

# Função para desenhar o ponto de início em vermelho
def draw_start(start_pos):
    pygame.draw.rect(screen, BLUE, (start_pos[1] * CELL_WIDTH, start_pos[0] * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT))

# Função para desenhar o ponto final em verde
def draw_end(end_pos):
    pygame.draw.rect(screen, GREEN, (end_pos[1] * CELL_WIDTH, end_pos[0] * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT))

# Função para desenhar o jogador
def draw_player(player_pos):
    row, col = player_pos
    if 0 <= row < ROWS and 0 <= col < COLS:
        # Desenhar jogador como um círculo
        player_center = (col * CELL_WIDTH + CELL_WIDTH // 2, row * CELL_HEIGHT + CELL_HEIGHT // 2)
        pygame.draw.circle(screen, RED, player_center, min(CELL_WIDTH, CELL_HEIGHT) // 2)

# Função para encontrar o caminho usando o algoritmo A*
def a_star(maze, start, end, open_cells, closed_cells=None):
    def heuristic(current, end):
        return abs(current[0] - end[0]) + abs(current[1] - end[1])

    queue = [(0, start, [])]
    visited = set()

    if closed_cells is None:
        closed_cells = set()

    while queue:
        cost, current, path = heapq.heappop(queue)

        if current == end:
            return path

        if current not in visited and current not in closed_cells:
            visited.add(current)

            x, y = current
            neighbors = [((x + 1, y), 'D'), ((x - 1, y), 'U'), ((x, y + 1), 'R'), ((x, y - 1), 'L')]

            for neighbor, direction in neighbors:
                nx, ny = neighbor

                if (
                    0 <= nx < len(maze) and
                    0 <= ny < len(maze[0]) and
                    maze[nx][ny] == 0 and
                    neighbor in open_cells
                ):
                    new_cost = cost + 1 + heuristic(neighbor, end)
                    heapq.heappush(queue, (new_cost, neighbor, path + [direction]))

    print("Caminho não encontrado")
    return None

# Função para extrair as coordenadas do caminho
def get_path_coordinates(path):
    return set(path)

# Função para obter as células abertas no labirinto
def get_open_cells(maze):
    open_cells = {(row, col) for row in range(ROWS) for col in range(COLS) if maze[row][col] == 0}
    return open_cells

# Função para gerar um novo labirinto
def new_maze():
    global maze
    maze = generate_maze(ROWS, COLS)

# Função principal do jogo
def main():
    global maze  # Declarando 'maze' como global para poder modificá-la dentro da função
    new_maze()  # Inicializando o labirinto
    start_pos = (0, 0)  # Definindo a posição inicial
    end_pos = (ROWS - 1, COLS - 1)  # Definindo a posição final

    # Encontrando o caminho com A* para frente
    path_forward = a_star(maze, start_pos, end_pos, get_open_cells(maze))

    if path_forward:
        print("Caminho encontrado (ida):", path_forward)
    else:
        print("Caminho não encontrado. O labirinto está bloqueado.")

    # Inicializando a posição do jogador
    player_pos = start_pos

    # Tempo inicial para verificar quando fechar o programa
    start_time = None

    # Loop principal do jogo
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Desenhando o labirinto e o jogador
        screen.fill(WHITE)
        draw_maze(maze)
        draw_start(start_pos)
        draw_end(end_pos)
        draw_player(player_pos)

        # Atualizando a tela
        pygame.display.flip()

        pygame.time.delay(500)  # Aguardando por meio segundo para melhor visualização

        # Movendo o jogador ao longo do caminho
        if path_forward:
            direction = path_forward.pop(0)
            if direction == 'U':
                player_pos = (player_pos[0] - 1, player_pos[1])
            elif direction == 'D':
                player_pos = (player_pos[0] + 1, player_pos[1])
            elif direction == 'L':
                player_pos = (player_pos[0], player_pos[1] - 1)
            elif direction == 'R':
                player_pos = (player_pos[0], player_pos[1] + 1)

        # Verificando se o jogador alcançou a posição final
        if player_pos == end_pos and not path_forward:
            print("Jogador alcançou a posição final. Voltando para o início...")
            path_backward = a_star(maze, end_pos, start_pos, get_open_cells(maze), set(get_path_coordinates(path_forward)))  # Calculando o caminho de volta

            if path_backward:
                print("Caminho de volta encontrado:", path_backward)
                path_forward = path_backward  # Invertendo o caminho para voltar ao início
                start_time = pygame.time.get_ticks()  # Atualizando o tempo de início

            else:
                print("Caminho de volta não encontrado. O labirinto está bloqueado.")
                running = False

        # Verificando se o jogador retornou ao início
        if player_pos == start_pos and start_time is not None:
            print("Jogador retornou ao início. Fechando o programa após 5 segundos.")
            current_time = pygame.time.get_ticks()
            elapsed_time = (current_time - start_time) / 1000  # Convertendo para segundos
            if elapsed_time >= 5:
                print("Fechando o programa.")
                running = False

    pygame.quit()

# Chamando a função principal
if __name__ == "__main__":
    main()

# Arquivo lobo original!