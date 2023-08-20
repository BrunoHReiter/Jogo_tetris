import pygame
import random

# Configurações do jogo
WIDTH, HEIGHT = 400, 400
GRID_SIZE = 30
GRID_WIDTH, GRID_HEIGHT = WIDTH // GRID_SIZE, HEIGHT // GRID_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
imagemfundo = pygame.image.load('imagem.jpg')


# Definindo as peças Tetris
pecas = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1, 1], [1, 0, 0]],  # L
    [[1, 1, 1], [0, 0, 1]],  # J
    [[1, 1, 0], [0, 1, 1]],  # S
    [[0, 1, 1], [1, 1, 0]]  # Z
]

# Função para criar uma peça aleatória
def nova_peca():
    return random.choice(pecas)

# Função para girar uma peça no sentido horário
def rodar_peca(peca):
    return [[peca[j][i] for j in range(len(peca))] for i in range(len(peca[0]) - 1, -1, -1)]

# Função para verificar se uma posição é válida para a peça atual
def is_valid_position(board, peca, x, y):
    for row in range(len(peca)):
        for col in range(len(peca[row])):
            if peca[row][col] == 1:
                if (
                    x + col < 0
                    or x + col >= GRID_WIDTH
                    or y + row >= GRID_HEIGHT
                    or board[y + row][x + col] == 1
                ):
                    return False
    return True

# Função para desenhar a grade do jogo
def draw_grid():
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            pygame.draw.rect(
                screen, WHITE, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1
            )

# Função para desenhar as peças no tabuleiro
def draw_board(board):
    for row in range(GRID_HEIGHT):
        for col in range(GRID_WIDTH):
            if board[row][col] == 1:
                pygame.draw.rect(
                    screen,
                    WHITE,
                    (
                        col * GRID_SIZE,
                        row * GRID_SIZE,
                        GRID_SIZE,
                        GRID_SIZE,
                    ),
                )

# Função para desenhar a peça Tetris atual
def desenhar_peca(peca, x, y):
    for row in range(len(peca)):
        for col in range(len(peca[row])):
            if peca[row][col] == 1:
                pygame.draw.rect(
                    screen,
                    WHITE,
                    (
                        x + col * GRID_SIZE,
                        y + row * GRID_SIZE,
                        GRID_SIZE,
                        GRID_SIZE,
                    ),
                )

# Função para remover linhas completas
def remove_complete_lines(board):
    lines_to_remove = [i for i, row in enumerate(board) if all(row)]
    for line_index in lines_to_remove:
        del board[line_index]
        board.insert(0, [0] * GRID_WIDTH)

# Função principal
def main():
    clock = pygame.time.Clock()

    board = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]
    peca = nova_peca()
    
    x, y = GRID_WIDTH // 2 - len(peca[0]) // 2, 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    peca_rodada = rodar_peca(peca)
                    if is_valid_position(board, peca_rodada, x, y):
                        peca = peca_rodada

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            if is_valid_position(board, peca, x - 1, y):
                x -= 1
        if keys[pygame.K_RIGHT]:
            if is_valid_position(board, peca, x + 1, y):
                x += 1
        if keys[pygame.K_DOWN]:
            if is_valid_position(board, peca, x, y + 1):
                y += 1

        # Mover a peça para baixo automaticamente
        if is_valid_position(board, peca, x, y + 1):
            y += 1
        else:
            # Fixar a peça no tabuleiro e pegar uma nova peça
            for row in range(len(peca)):
                for col in range(len(peca[row])):
                    if peca[row][col] == 1:
                        board[y + row][x + col] = 1
            remove_complete_lines(board)
            peca = nova_peca()
            x, y = GRID_WIDTH // 2 - len(peca[0]) // 2, 0


        screen.blit(imagemfundo, (0,0))
        draw_grid()
        draw_board(board)
        desenhar_peca(peca, x * GRID_SIZE, y * GRID_SIZE)

        pygame.display.flip()
        clock.tick(4)

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Tetris")
    main()
