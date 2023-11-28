import random
import sys
import pygame as pg


WIDTH, HEIGHT = 1600, 900

delta = {  # 練習３：押下キーと移動量の辞書
    pg.K_UP: (0, -5),  # キー：移動量／値：（横方向移動量，縦方向移動量）
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0)
}


def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    オブジェクトが画面内or画面外を判定し，真理値タプルを返す関数
    引数 rct：こうかとんor爆弾SurfaceのRect
    戻り値：横方向，縦方向はみ出し判定結果（画面内：True／画面外：False）
    """
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:  # 横方向はみ出し判定
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:  # 縦方向はみ出し判定
        tate = False
    return yoko, tate

    



def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("ex02proen/fig/pg_bg.jpg")
    kk_img = pg.image.load("ex02proen/fig/3.png")
    kk_imgs = pg.image.load("ex02proen/fig/6.png")#新しい画像追加、新しく追加した爆弾に当たったとき画像切り替え用
    kk_imgs = pg.transform.rotozoom(kk_imgs, 0, 2.0)
    kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)
    

    kk_rct = kk_img.get_rect()  # 練習３：こうかとんSurfaceのRectを抽出する
    bb_imgs = pg.Surface((20, 20))   # 練習１：透明のSurfaceを作る
    bb_imgs.set_colorkey((0, 0, 0))
    kk_rct.center = 900, 400  # 練習３：こうかとんの初期座標
    bb_img = pg.Surface((20, 20))   # 練習１：透明のSurfaceを作る
    bb_img.set_colorkey((0, 0, 0))  # 練習１：黒い部分を透明にする
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)  # 練習１：赤い半径10の円を描く
    pg.draw.circle(bb_imgs, (0, 255, 0), (10, 10), 10) #緑色の赤い半径10の円を描く

    bb_rct = bb_img.get_rect()  # 練習１：爆弾SurfaceのRectを抽出する
    bb_rcts = bb_imgs.get_rect()
    bb_rct.centerx = random.randint(0, WIDTH)
    bb_rct.centery = random.randint(0, HEIGHT)
    bb_rcts.centerx = random.randint(0, WIDTH)
    bb_rcts.centery = random.randint(0, HEIGHT)
    vx, vy = +5, +5  # 練習２：爆弾の速度
    vq, vw = +5, +5#新しく追加した爆弾の速度

    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return


        if kk_rct.colliderect(bb_rct):
            print("Gmae over")
            return    
        if kk_rct.colliderect(bb_rcts):#新しく追加した爆弾は当たってもすり抜ける
            print("")
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for k, tpl in delta.items():
            if key_lst[k]:  # キーが押されたら
                sum_mv[0] += tpl[0]
                sum_mv[1] += tpl[1]
        

        screen.blit(bg_img, [0, 0])
        kk_rct.move_ip(sum_mv[0], sum_mv[1])
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])

        screen.blit(kk_img, kk_rct)  # 練習３：こうかとんを移動させる
        if  not kk_rct.colliderect(bb_rct):
            screen.blit(kk_img,kk_rct)#画像切り替え課題3
        else:
            screen.blit(kk_imgs,kk_rct)

        if  not kk_rct.colliderect(bb_rcts):
            screen.blit(kk_img,kk_rct)
        else:
            screen.blit(kk_imgs,kk_rct)
 

        bb_rct.move_ip(vx, vy)  # 練習２：爆弾を移動させる
        bb_rcts.move_ip(vq, vw)
        yoko, tate = check_bound(bb_rct)
        yoko2, tate2 = check_bound(bb_rcts)
        if not yoko:  # 横方向にはみ出たら
            vx *= -1
        if not tate:  # 縦方向にはみ出たら
            vy *= -1
        if not yoko2:  # 横方向にはみ出たら
            vq *= -1
        if not tate2:  # 縦方向にはみ出たら
            vw *= -1
        bb_rct.move_ip(vx, vy) 
        bb_rcts.move_ip(vq, vw) 
        screen.blit(bb_img, bb_rct)
        screen.blit(bb_imgs, bb_rcts)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()