from cgitb import text
import pygame 

class SudokuGame:
    def __init__(self, board):
        self.board = board
        self.solved = False
        self.solved_board = board # solve board
        self.diff = 50*board.size / board.size 
        
    def instructions(self):
        msg1 = "Welcome to Sudoku!"
        msg2 = "The objective of the game is to fill a NxN grid with digits so that each column, each row, and each of the nine sqrt(N)xsqrt(N) sub-grids that compose the grid contains all of the digits from 1 to N."
        screen.blit(font1.render(msg1, False, (0, 0, 0)), (0, 0))
        screen.blit(font1.render(msg2, False, (0, 0, 0)), (0, 50))
        
    def draw_grid(self):
        for i in range(self.board.size):
            for j in range(self.board.size):
                pygame.draw.rect(screen, (255, 255, 255), (x, y, diff, diff))
                if grid[i][j] != 0:
                    text = font2.render(str(grid[i][j]), False, (0, 0, 0))
                    screen.blit(text, (x + diff / 2 - text.get_width() / 2, y + diff / 2 - text.get_height() / 2))
                x += diff
            y += diff
            x = 0
            
        # draw the lines
        for i in range(self.board.size + 1):
            if i % sqrt(self.board.size) == 0:
                pygame.draw.line(screen, (0, 0, 0), (0, i * diff), (self.board.size * diff, i * diff), 3)
                pygame.draw.line(screen, (0, 0, 0), (i * diff, 0), (i * diff, self.board.size * diff), 3)
            else:
                pygame.draw.line(screen, (0, 0, 0), (0, i * diff), (self.board.size * diff, i * diff), 1)
                pygame.draw.line(screen, (0, 0, 0), (i * diff, 0), (i * diff, self.board.size * diff), 1)
                
        pygame.display.update()

    def visualize(self):
        pygame.font.init()
        font1 = pygame.font.SysFont('Comic Sans MS', 30)
        font2 = pygame.font.SysFont('Comic Sans MS', 20)
    
        screen = pygame.display.set_mode((self.board.size * 50, self.board.size * 50))
        
        # Title and Icon
        pygame.display.set_caption("Sudoku")
        icon = pygame.image.load('sudoku.png')
        pygame.display.set_icon(icon)
        
        x = 0
        y = 0
        val = 0
        
        grid = self.board
        run = True
        
        # Game loop
        while run:
            screen.fill((255, 255, 255))
            self.draw_grid()
            pygame.display.update()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    x = pos[0] // diff
                    y = pos[1] // diff
                    val = 0
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        val = 1
                    if event.key == pygame.K_2:
                        val = 2
                    if event.key == pygame.K_3:
                        val = 3
                    if event.key == pygame.K_4:
                        val = 4
                    if event.key == pygame.K_5:
                        val = 5
                    if event.key == pygame.K_6:
                        val = 6
                    if event.key == pygame.K_7:
                        val = 7
                    if event.key == pygame.K_8:
                        val = 8
                    if event.key == pygame.K_9:
                        val = 9
                    if event.key == pygame.K_BACKSPACE:
                        val = 0
                    if event.key == pygame.K_RETURN:
                        i, j = get_row_col_from_mouse(pos)
                        if valid(grid, i, j, val):
                            grid[i][j] = val
                        val = 0
                    if event.key == pygame.K_SPACE:
                        solve_gui(grid)
                        val = 0
                    if event.key == pygame.K_c:
                        grid = [[0 for x in range(self.board.size)] for y in range(self.board.size)]
                        val = 0
                    if event.key == pygame.K_s:
                        find = find_empty(grid)
                        if not find:
                            print_board(grid)
                        else:
                            i, j = find
                            for val in range(1, 10):
                                if valid(grid, i, j, val):
                                    grid[i][j] = val
                                    solve_gui(grid)
                                    grid[i][j] = 0
                        val = 0
                    if event.key == pygame.K_ESCAPE:
                        run = False
            if val != 0:
                draw_val(screen, val)