import pygame
import random
import sys

# 初始化pygame
pygame.init()

# 游戏常量
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 600
FPS = 60

# 颜色定义
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)


class Player(pygame.sprite.Sprite):
    """玩家飞机类"""
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 40))
        self.image.fill(GREEN)
        # 绘制三角形飞机
        pygame.draw.polygon(self.image, GREEN, [(25, 0), (0, 40), (50, 40)])
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 10
        self.speed_x = 0
        self.shoot_delay = 250  # 射击间隔（毫秒）
        self.last_shot = pygame.time.get_ticks()

    def update(self):
        """更新玩家位置"""
        self.speed_x = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.speed_x = -8
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.speed_x = 8
        
        self.rect.x += self.speed_x
        
        # 边界检测
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        """发射子弹"""
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = Bullet(self.rect.centerx, self.rect.top)
            return bullet
        return None


class Enemy(pygame.sprite.Sprite):
    """敌机类"""
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 30))
        self.image.fill(RED)
        # 绘制倒三角形敌机
        pygame.draw.polygon(self.image, RED, [(20, 30), (0, 0), (40, 0)])
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speed_y = random.randrange(2, 6)
        self.speed_x = random.randrange(-2, 2)

    def update(self):
        """更新敌机位置"""
        self.rect.y += self.speed_y
        self.rect.x += self.speed_x
        
        # 如果敌机飞出屏幕，重新生成
        if self.rect.top > SCREEN_HEIGHT + 10 or \
           self.rect.left < -25 or self.rect.right > SCREEN_WIDTH + 20:
            self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speed_y = random.randrange(2, 6)


class Bullet(pygame.sprite.Sprite):
    """子弹类"""
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 15))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed_y = -10

    def update(self):
        """更新子弹位置"""
        self.rect.y += self.speed_y
        # 如果子弹飞出屏幕，删除
        if self.rect.bottom < 0:
            self.kill()


class Game:
    """游戏主类"""
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("飞机大战")
        self.clock = pygame.time.Clock()
        self.running = True
        self.score = 0
        self.font = pygame.font.Font(None, 36)
        
        # 创建精灵组
        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        
        # 创建玩家
        self.player = Player()
        self.all_sprites.add(self.player)
        
        # 创建敌机
        for i in range(8):
            enemy = Enemy()
            self.all_sprites.add(enemy)
            self.enemies.add(enemy)

    def handle_events(self):
        """处理事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullet = self.player.shoot()
                    if bullet:
                        self.all_sprites.add(bullet)
                        self.bullets.add(bullet)

    def update(self):
        """更新游戏状态"""
        self.all_sprites.update()
        
        # 检测子弹击中敌机
        hits = pygame.sprite.groupcollide(self.enemies, self.bullets, True, True)
        for hit in hits:
            self.score += 10
            # 重新生成敌机
            enemy = Enemy()
            self.all_sprites.add(enemy)
            self.enemies.add(enemy)
        
        # 检测敌机撞击玩家
        hits = pygame.sprite.spritecollide(self.player, self.enemies, False)
        if hits:
            self.running = False

    def draw(self):
        """绘制游戏画面"""
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        
        # 绘制分数
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        pygame.display.flip()

    def run(self):
        """运行游戏主循环"""
        while self.running:
            self.clock.tick(FPS)
            self.handle_events()
            self.update()
            self.draw()
        
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()
