import pygame
import sys
import random

# ウィンドウの大きさ
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 1200

# 宇宙船の大きさと速度
SHIP_WIDTH = 50
SHIP_HEIGHT = 50
SHIP_SPEED = 2

# 小惑星の大きさと速度
ASTEROID_WIDTH = 50
ASTEROID_HEIGHT = 50
ASTEROID_SPEED = 2

# 弾の大きさと速度
BULLET_WIDTH = 10
BULLET_HEIGHT = 10
BULLET_SPEED = 10

# Pygameを初期化
pygame.init()

# フォントを設定
font = pygame.font.Font(None, 72)  # 大きいフォント
small_font = pygame.font.Font(None, 36)  # 小さいフォント

# ウィンドウを作成
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# 宇宙船と小惑星のスプライトを作成
ship = pygame.image.load('ship.png')
ship = pygame.transform.scale(ship, (SHIP_WIDTH, SHIP_HEIGHT))
ship_rect = ship.get_rect(center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

asteroid = pygame.image.load('asteroid.jpeg')
asteroid = pygame.transform.scale(asteroid, (ASTEROID_WIDTH, ASTEROID_HEIGHT))
asteroid_rect = asteroid.get_rect(center = (random.randrange(0, SCREEN_WIDTH - ASTEROID_WIDTH), -ASTEROID_HEIGHT))

bullets = []

# 破壊した小惑星の数
destroyed_asteroids = 0

# ゲームのループ
while True:
    # イベントを処理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # 弾を撃つ
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # 左クリック
                bullet = pygame.Rect(ship_rect.centerx, ship_rect.centery, BULLET_WIDTH, BULLET_HEIGHT)
                bullets.append(bullet)

    # 宇宙船を操作
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        ship_rect.left -= SHIP_SPEED
    if keys[pygame.K_RIGHT]:
        ship_rect.right += SHIP_SPEED
    if keys[pygame.K_UP]:
        ship_rect.top -= SHIP_SPEED
    if keys[pygame.K_DOWN]:
        ship_rect.bottom += SHIP_SPEED

    # 小惑星を移動
    asteroid_rect.y += ASTEROID_SPEED

    # 小惑星が画面から出たら新たに生成
    if asteroid_rect.top > SCREEN_HEIGHT:
        asteroid_rect = pygame.Rect(random.randrange(0, SCREEN_WIDTH - ASTEROID_WIDTH), -ASTEROID_HEIGHT, ASTEROID_WIDTH, ASTEROID_HEIGHT)

    # 弾を移動
    for bullet in bullets:
        bullet.y -= BULLET_SPEED
        if bullet.bottom < 0:
            bullets.remove(bullet)

    # 弾と小惑星の衝突判定
    for bullet in bullets:
        if asteroid_rect.colliderect(bullet):
            bullets.remove(bullet)
            asteroid_rect = pygame.Rect(random.randrange(0, SCREEN_WIDTH - ASTEROID_WIDTH), -ASTEROID_HEIGHT, ASTEROID_WIDTH, ASTEROID_HEIGHT)
            destroyed_asteroids += 1

    # 宇宙船と小惑星の衝突判定
    if asteroid_rect.colliderect(ship_rect):
        pygame.quit()
        sys.exit()

    # 画面をクリア
    screen.fill((0, 0, 0))

    # スプライトを描画
    screen.blit(ship, ship_rect)
    screen.blit(asteroid, asteroid_rect)

    # 弾を描画
    for bullet in bullets:
        pygame.draw.rect(screen, (255, 255, 255), bullet)

    # 破壊した小惑星の数を表示
    score_text = small_font.render(f"Asteroids destroyed: {destroyed_asteroids}", True, (255, 255, 255))
    screen.blit(score_text, (SCREEN_WIDTH - score_text.get_width() - 10, 10))

    # ゲームクリア条件をチェック
    if destroyed_asteroids >= 10:
        text = font.render("Game Clear", True, (255, 0, 0))  # 赤色で表示
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))

    # 画面を更新
    pygame.display.flip()
