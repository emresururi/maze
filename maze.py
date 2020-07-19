from eMaze import *
import pygame as pg
import copy

n_x = n_y = 20
#n_x = 50
i_x = random.randint(0,n_x-1)
i_y = random.randint(0,n_y-1)

maze = eMaze(n_x, n_y, i_x, i_y)
maze.make_maze()
maze.write_svg("/etmp/map.svg")

pg.init()
clock = pg.time.Clock()
clock.tick(30)

res_x = res_y = 480
res_y = int(res_x * n_y / n_x)
scale_x = res_x / n_x
scale_y = res_y / n_y

disp = pg.display.set_mode((res_x, res_y))
pg.display.set_caption("Eceeeeeeee!")
# Prepare the maze surface --- 0 ---
surface_maze = pg.Surface((res_x,res_y))
color_wall = 'purple'
thickness_wall = 3
pg.draw.rect(surface_maze,color_wall,[0,0,res_x,res_y],thickness_wall)
for x in range(n_x):
    for y in range(n_y):
        walls = maze.cell_at(x,y).walls
        if(walls['S']):
            pg.draw.line(surface_maze,color_wall,[x*scale_x,(y+1)*scale_y],[(x+1)*scale_x,(y+1)*scale_y],thickness_wall)
        if(walls['E']):
            pg.draw.line(surface_maze,color_wall,[(x+1)*scale_x,(y)*scale_y],[(x+1)*scale_x,(y+1)*scale_y],thickness_wall)
# Prepare the maze surface --- 1 ---

est = pg.image.load("img/est.png")
ece = pg.image.load("img/ece.png")
bego = pg.image.load("img/bengu.png")
est=pg.transform.scale(est,(int(scale_x),int(scale_y)))
ece=pg.transform.scale(ece,(int(scale_x),int(scale_y)))
bego=pg.transform.scale(bego,(int(scale_x),int(scale_y)))

est_x = n_x - 3
est_y = 1

bego_x = 2
bego_y = 3

disp.blit(surface_maze,(0,0))
disp.blit(est,(est_x*scale_x,est_y*scale_y))
disp.blit(bego,(bego_x*scale_x,bego_y*scale_y))

ece_x = i_x
ece_y = i_y

disp.blit(ece,(ece_x*scale_x,ece_y*scale_y))
pg.display.flip()
path_from_bego_to_est  = maze.solve_from_to((bego_x,bego_y),(est_x,est_y))

surface_b2e = pg.Surface((res_x,res_y),pg.SRCALPHA,32)
path_from_bego_to_est_scaled = copy.deepcopy(path_from_bego_to_est)
path_from_bego_to_est_scaled[:,0] = path_from_bego_to_est_scaled[:,0]*scale_x+scale_x/2
path_from_bego_to_est_scaled[:,1] = path_from_bego_to_est_scaled[:,1]*scale_y+scale_y/2
pg.draw.lines(surface_b2e,'yellow',False,path_from_bego_to_est_scaled)


flag_break = False
step = 0
while not flag_break:
    # clock.tick(10)
    event = pg.event.wait()
    if event.type == pg.QUIT:
        flag_break = True
    if event.type == pg.KEYDOWN:
        if event.key == pg.K_LEFT and not maze.cell_at(ece_x,ece_y).walls['W']:
            ece_x -= 1
        elif event.key == pg.K_RIGHT and not maze.cell_at(ece_x,ece_y).walls['E']:
            ece_x += 1
        elif event.key == pg.K_UP and not maze.cell_at(ece_x,ece_y).walls['N']:
            ece_y -= 1
        elif event.key == pg.K_DOWN and not maze.cell_at(ece_x,ece_y).walls['S']:
            ece_y += 1

        disp.blit(surface_maze,(0,0))

        if(bego_x!=est_x or bego_y!=est_y):
            bego_x = path_from_bego_to_est[step][0]
            bego_y = path_from_bego_to_est[step][1]
        disp.blit(surface_b2e,(0,0))
        disp.blit(est, (est_x * scale_x, est_y * scale_y))
        disp.blit(bego,(bego_x*scale_x,bego_y*scale_y))
        disp.blit(ece,(ece_x*scale_x,ece_y*scale_y))
        pg.display.flip()
        step += 1

#disp.blit(surface,(0,0))
pg.display.flip()
print("lol")
# pg.quit()
