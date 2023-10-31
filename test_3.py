import tkinter as tk
import random

def create_maze():
    maze = []
    for i in range(10):
        row = []
        for j in range(10):
            if random.random() < 0.3:
                row.append('#')
            else:
                row.append('.')
        maze.append(row)

    maze[1][1] = 'S'
    maze[8][8] = 'E'

    return maze

def draw_maze():
    for i in range(10):
        for j in range(10):
            cell = maze[i][j]
            color = 'black' if cell == '#' else 'white'
            canvas.create_rectangle(j * cell_size, i * cell_size, (j + 1) * cell_size, (i + 1) * cell_size, fill=color)
            if cell == 'S':
                canvas.create_text(j * cell_size + cell_size / 2, i * cell_size + cell_size / 2, text='S')
            elif cell == 'E':
                canvas.create_text(j * cell_size + cell_size / 2, i * cell_size + cell_size / 2, text='E')
            elif cell == 'R':
                canvas.create_oval(j * cell_size + cell_size * 0.2, i * cell_size + cell_size * 0.2,
                                    (j + 1) * cell_size - cell_size * 0.2, (i + 1) * cell_size - cell_size * 0.2, fill='blue')

def solve_maze(x, y):
    if x < 0 or x >= 10 or y < 0 or y >= 10 or maze[x][y] in ['#', 'V']:
        return False

    if maze[x][y] == 'E':
        return True

    maze[x][y] = 'V'

    if (solve_maze(x + 1, y) or
        solve_maze(x - 1, y) or
        solve_maze(x, y + 1) or
        solve_maze(x, y - 1)):
        maze[x][y] = 'R'
        draw_maze()
        root.update()
        return True

    return False

def solve():
    if solve_maze(1, 1):
        print("Caminho encontrado!")
    else:
        print("Não há caminho possível.")

root = tk.Tk()
root.title("Desafio do Rato")

cell_size = 40

canvas = tk.Canvas(root, width=10 * cell_size, height=10 * cell_size)
canvas.pack()

maze = create_maze()
draw_maze()

solve_button = tk.Button(root, text="Resolver Labirinto", command=solve)
solve_button.pack()

root.mainloop()

#esse aqui funcionou! (com apenas uma interface).