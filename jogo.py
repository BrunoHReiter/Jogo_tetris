import pygame
import random

# Configurações do jogo
WIDTH, HEIGHT = 400, 800
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

# Função para remover linhas completas e ganhar pontos
def remove_complete_lines(board):
    lines_to_remove = [i for i, row in enumerate(board) if all(row)]
    points_earned = len(lines_to_remove) * 20  # Ganha 20 pontos para cada linha removida
    for line_index in lines_to_remove:
        del board[line_index]
        board.insert(0, [0] * GRID_WIDTH)
    return points_earned

# Função principal
# Função principal
def main():
    clock = pygame.time.Clock()

    # Inicialização do tabuleiro vazio e da primeira peça
    board = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]
    peca = nova_peca()

    # Posição inicial da peça
    x, y = GRID_WIDTH // 2 - len(peca[0]) // 2, 0
    score = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    # Tentativa de girar a peça
                    peca_rodada = rodar_peca(peca)
                    nova_x = x
                    if is_valid_position(board, peca_rodada, nova_x, y):
                        peca = peca_rodada

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            # Tentativa de mover a peça para a esquerda
            nova_x = x - 1
            if is_valid_position(board, peca, nova_x, y):
                x = nova_x
        if keys[pygame.K_RIGHT]:
            # Tentativa de mover a peça para a direita
            nova_x = x + 1
            if is_valid_position(board, peca, nova_x, y):
                x = nova_x

        nova_y = y + 1
        if is_valid_position(board, peca, x, nova_y):
            # Tentativa de mover a peça para baixo
            y = nova_y
        else:
            # Fixar a peça no tabuleiro e pegar uma nova peça
            for row in range(len(peca)):
                for col in range(len(peca[row])):
                    if peca[row][col] == 1:
                        board[y + row][x + col] = 1

            # Verificar e remover linhas completas, atualizar pontuação
            lines_removed = remove_complete_lines(board)
            score += lines_removed

            # Pegar uma nova peça e definir sua posição inicial
            peca = nova_peca()
            x, y = GRID_WIDTH // 2 - len(peca[0]) // 2, 0

        if keys[pygame.K_DOWN]:
            # Tentativa de mover a peça para baixo manualmente
            nova_y = y + 1
            if is_valid_position(board, peca, x, nova_y):
                y = nova_y

        if any(board[row + y][col + x] == 1 for row in range(len(peca)) for col in range(len(peca[row])) if peca[row][col] == 1):
            # Verificar se a peça atingiu o topo do tabuleiro
            font = pygame.font.Font(None, 72)
            game_over_text = font.render("Game Over", True, WHITE)
            text_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(game_over_text, text_rect)
            pygame.display.flip()
            pygame.time.delay(1000)
            pygame.quit()
            exit()

        # Limpar a tela, desenhar o tabuleiro, peça e informações
        screen.fill(BLACK)
        draw_grid()
        draw_board(board)
        desenhar_peca(peca, x * GRID_SIZE, y * GRID_SIZE)

        font = pygame.font.Font(None, 36)
        score_text = font.render("Pontuação: " + str(score), True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(4)

# Inicialização do pygame e configuração da tela
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Tetris")
    main()
