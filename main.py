import pygame
import sys
import random

# 초기화
pygame.init()

# 화면 크기 설정
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("벽돌깨기 게임")

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# 공 속성
BALL_RADIUS = 10
ball_x = SCREEN_WIDTH // 2
ball_y = SCREEN_HEIGHT // 2
ball_dx = 4 * random.choice((1, -1))
ball_dy = -4

# 패들 속성
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 10
paddle_x = (SCREEN_WIDTH - PADDLE_WIDTH) // 2
paddle_y = SCREEN_HEIGHT - 30
paddle_speed = 6

# 벽돌 속성
BRICK_ROWS = 5
BRICK_COLUMNS = 8
BRICK_WIDTH = 75
BRICK_HEIGHT = 20
BRICK_PADDING = 10
BRICK_OFFSET_TOP = 50
BRICK_OFFSET_LEFT = 35

# 벽돌 생성
bricks = []
for row in range(BRICK_ROWS):
    for col in range(BRICK_COLUMNS):
        brick_x = BRICK_OFFSET_LEFT + col * (BRICK_WIDTH + BRICK_PADDING)
        brick_y = BRICK_OFFSET_TOP + row * (BRICK_HEIGHT + BRICK_PADDING)
        bricks.append(pygame.Rect(brick_x, brick_y, BRICK_WIDTH, BRICK_HEIGHT))

# 게임 루프
clock = pygame.time.Clock()
running = True

while running:
    screen.fill(BLACK)

    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 키 입력 처리
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle_x > 0:
        paddle_x -= paddle_speed
    if keys[pygame.K_RIGHT] and paddle_x < SCREEN_WIDTH - PADDLE_WIDTH:
        paddle_x += paddle_speed

    # 공 이동
    ball_x += ball_dx
    ball_y += ball_dy

    # 공 벽 충돌
    if ball_x <= 0 or ball_x >= SCREEN_WIDTH - BALL_RADIUS:
        ball_dx *= -1
    if ball_y <= 0:
        ball_dy *= -1

    # 공 패들 충돌
    paddle_rect = pygame.Rect(paddle_x, paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT)
    if paddle_rect.collidepoint(ball_x, ball_y + BALL_RADIUS):
        ball_dy *= -1

    # 공 벽돌 충돌
    for brick in bricks[:]:
        if brick.collidepoint(ball_x, ball_y):
            bricks.remove(brick)
            ball_dy *= -1
            break

    # 공이 바닥에 닿았을 때
    if ball_y > SCREEN_HEIGHT:
        print("Game Over!")
        running = False

    # 벽돌이 모두 깨졌을 때
    if not bricks:
        print("You Win!")
        running = False

    # 화면 그리기
    pygame.draw.circle(screen, WHITE, (ball_x, ball_y), BALL_RADIUS)
    pygame.draw.rect(screen, BLUE, paddle_rect)
    for brick in bricks:
        pygame.draw.rect(screen, RED, brick)

    # 화면 업데이트
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()