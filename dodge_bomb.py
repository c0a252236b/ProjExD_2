import os
import pygame as pg
import random
import sys
import time



WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP:(0,-5),
    pg.K_DOWN:(0,5),
    pg.K_LEFT:(-5,0),
    pg.K_RIGHT:(5,0),
    }
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rct: pg.Rect) -> tuple[bool,bool]:
    """
    引数:pygame.Rect
    戻り値:タプル(横方向判定結果,縦方向判定結果)
    画面内であればTrue
    """
    return rct.left >= 0 and rct.right <= WIDTH,rct.top >= 0 and rct.bottom <= HEIGHT


def gameOver(screen: pg.surface) -> None:
    bg_black = pg.Surface((WIDTH,HEIGHT))
    pg.draw.rect(bg_black,(0,0,0),bg_black.get_rect())
    bg_black.set_alpha(200)
    fonto = pg.font.Font(None,100)
    txt = fonto.render("GameOver",True,(255,255,255))
    kk_img8 = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 0.9)
    kk_rct8 = kk_img8.get_rect()
    bg_black.blit(txt,[WIDTH*1/3,HEIGHT*1/2])
    bg_black.blit(kk_img8,[WIDTH*3/4,HEIGHT*1/2])
    bg_black.blit(kk_img8,[WIDTH*1/4,HEIGHT*1/2])
    screen.blit(bg_black,[0,0])
    pg.display.update()
    time.sleep(5)
    
    


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")

    bb_img = pg.Surface((20,20))
    pg.draw.circle(bb_img,(255,0,0),(10,10),10)
    bb_img.set_colorkey((0,0,0))
    bb_rct = bb_img.get_rect()
    bb_rct.center = (random.randint(0,WIDTH),random.randint(0,HEIGHT))

    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200

    clock = pg.time.Clock()
    tmr = 0
    vx,vy = 5,5  # 爆弾の初期速度

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
        screen.blit(bg_img, [0, 0])

        # 衝突判定
        if kk_rct.colliderect(bb_rct):
            print("Game Over")
            gameOver(screen)
            return

        # 爆弾の移動
        if not (check_bound(bb_rct)[0]):
            vx *= -1
        if not (check_bound(bb_rct)[1]):
            vy *= -1
        bb_rct.move_ip(vx,vy)

        key_lst = pg.key.get_pressed()
        
        # こうかとんの移動
        sum_mv = [0, 0]
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]  #左右
                sum_mv[1] += mv[1]  #上下
        kk_rct.move_ip(sum_mv)
        if not (check_bound(kk_rct) == (True,True)):
            kk_rct.move_ip(-sum_mv[0],-sum_mv[1])

        screen.blit(kk_img, kk_rct)
        screen.blit(bb_img,bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
