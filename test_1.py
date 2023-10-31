import tkinter as tk
import random

def create_maze():
    maze = []
    for i in range(10):
        row = []
        for j in range(10):
            if random.random() < 0.3:  # 30% de chance de ser um obstáculo
                row.append('#')
            else:
                row.append('.')
        maze.append(row)

    # Defina o ponto de partida e chegada
    maze[1][1] = 'S'
    maze[8][8] = 'E'

    return maze

def draw_maze(maze):
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            cell = maze[i][j]
            color = 'black' if cell == '#' else 'white'
            canvas.create_rectangle(j * cell_size, i * cell_size, (j + 1) * cell_size, (i + 1) * cell_size, fill=color)
            if cell == 'S':
                canvas.create_text(j * cell_size + cell_size / 2, i * cell_size + cell_size / 2, text='S')
            elif cell == 'E':
                canvas.create_text(j * cell_size + cell_size / 2, i * cell_size + cell_size / 2, text='E')

def solve_maze():
    pass  # Implemente a lógica para encontrar o caminho aqui

# Configurações iniciais
root = tk.Tk()
root.title("Desafio do Rato")

cell_size = 40
maze = create_maze()

canvas = tk.Canvas(root, width=len(maze[0]) * cell_size, height=len(maze) * cell_size)
canvas.pack()

draw_maze(maze)

solve_button = tk.Button(root, text="Resolver Labirinto", command=solve_maze)
solve_button.pack()

root.mainloop()
