from eMaze import *
import pygame as pg
import copy

n_x = n_y = 10
#n_x = 50
i_x = random.randint(0,n_x-1)
i_y = random.randint(0,n_y-1)

maze = eMaze(n_x, n_y, i_x, i_y)
maze.make_maze()
maze.write_svg("map.svg")

pg.init()
clock = pg.time.Clock()
clock.tick(30)

res_x = res_y = 480
res_y = int(res_x * n_y / n_x)
scale_x = int(res_x / n_x)
scale_y = int(res_y / n_y)

disp = pg.display.set_mode((res_x, res_y))
pg.display.set_caption("MAZE!")
# Prepare the maze surface --- 0 ---
surface_maze = pg.Surface((res_x,res_y))
color_wall = pg.Color('purple')
thickness_wall = 3
pg.draw.rect(surface_maze,color_wall,[0,0,res_x,res_y],thickness_wall+5)
for x in range(n_x):
    for y in range(n_y):
        walls = maze.cell_at(x,y).walls
        if(walls['S']):
            pg.draw.line(surface_maze,color_wall,[x*scale_x,(y+1)*scale_y],[(x+1)*scale_x,(y+1)*scale_y],thickness_wall)
        if(walls['E']):
            pg.draw.line(surface_maze,color_wall,[(x+1)*scale_x,(y)*scale_y],[(x+1)*scale_x,(y+1)*scale_y],thickness_wall)
# Prepare the maze surface --- 1 ---

gate = pg.image.load("img/gate.png")
wanderer = pg.image.load("img/wanderer.png")
pathfinder = pg.image.load("img/pathfinder.png")
gate=pg.transform.scale(gate,(int(scale_x),int(scale_y)))
wanderer=pg.transform.scale(wanderer,(int(scale_x),int(scale_y)))
pathfinder=pg.transform.scale(pathfinder,(int(scale_x),int(scale_y)))

gate_x = n_x - 3
gate_y = 1

pathfinder_x = 1
pathfinder_y = n_y - 3

disp.blit(surface_maze,(0,0))
disp.blit(gate,(gate_x*scale_x,gate_y*scale_y))
disp.blit(pathfinder,(pathfinder_x*scale_x,pathfinder_y*scale_y))

wanderer_x = i_x
wanderer_y = i_y

disp.blit(wanderer,(wanderer_x*scale_x,wanderer_y*scale_y))
pg.display.flip()
path_from_pathfinder_to_gate  = maze.solve_from_to((pathfinder_x,pathfinder_y),(gate_x,gate_y))

surface_b2e = pg.Surface((res_x,res_y),pg.SRCALPHA,32)
path_from_pathfinder_to_gate_scaled = copy.deepcopy(path_from_pathfinder_to_gate)
path_from_pathfinder_to_gate_scaled[:,0] = path_from_pathfinder_to_gate_scaled[:,0]*scale_x+scale_x/2
path_from_pathfinder_to_gate_scaled[:,1] = path_from_pathfinder_to_gate_scaled[:,1]*scale_y+scale_y/2
pg.draw.lines(surface_b2e,pg.Color('yellow'),False,path_from_pathfinder_to_gate_scaled)


flag_break = False
step = 0
while not flag_break:
    # clock.tick(10)
    event = pg.event.wait()
    if event.type == pg.QUIT:
        flag_break = True
    if event.type == pg.KEYDOWN:
        if event.key == pg.K_LEFT:
            if not maze.cell_at(wanderer_x,wanderer_y).walls['W']:
                wanderer_x -= 1
            else:
                pg.draw.line(surface_maze, pg.Color('red'), [(wanderer_x) * scale_x, (wanderer_y) * scale_y],
                             [(wanderer_x) * scale_x, (wanderer_y + 1) * scale_y], thickness_wall)
                maze.update_wall(wanderer_x, wanderer_y, 'W', False)
        elif event.key == pg.K_RIGHT:
            if not maze.cell_at(wanderer_x,wanderer_y).walls['E']:
                wanderer_x += 1
            else:
                pg.draw.line(surface_maze, pg.Color('red'), [(wanderer_x + 1) * scale_x, (wanderer_y) * scale_y],
                             [(wanderer_x + 1) * scale_x, (wanderer_y + 1) * scale_y], thickness_wall)
                maze.update_wall(wanderer_x,wanderer_y,'E',False)
        elif event.key == pg.K_UP:
            if not maze.cell_at(wanderer_x,wanderer_y).walls['N']:
                wanderer_y -= 1
            else:
                pg.draw.line(surface_maze, pg.Color('red'), [(wanderer_x) * scale_x, (wanderer_y) * scale_y],
                 [(wanderer_x+1) * scale_x, (wanderer_y) * scale_y], thickness_wall)
                maze.update_wall(wanderer_x, wanderer_y, 'N', False)
        elif event.key == pg.K_DOWN:
            if not maze.cell_at(wanderer_x,wanderer_y).walls['S']:
                wanderer_y += 1
            else:
                pg.draw.line(surface_maze, pg.Color('red'), [(wanderer_x) * scale_x, (wanderer_y+1) * scale_y],
                 [(wanderer_x+1) * scale_x, (wanderer_y+1) * scale_y], thickness_wall)
                maze.update_wall(wanderer_x, wanderer_y, 'S', False)
        elif event.key == pg.K_r and pathfinder_x!=gate_x and pathfinder_y!=gate_y:
            # Re-calculate the path (include broken walls, if any)
            path_from_pathfinder_to_gate = maze.solve_from_to((pathfinder_x, pathfinder_y), (gate_x, gate_y))

            surface_b2e = pg.Surface((res_x, res_y), pg.SRCALPHA, 32)
            path_from_pathfinder_to_gate_scaled = copy.deepcopy(path_from_pathfinder_to_gate)
            path_from_pathfinder_to_gate_scaled[:, 0] = path_from_pathfinder_to_gate_scaled[:,
                                                        0] * scale_x + scale_x / 2
            path_from_pathfinder_to_gate_scaled[:, 1] = path_from_pathfinder_to_gate_scaled[:,
                                                        1] * scale_y + scale_y / 2
            pg.draw.lines(surface_b2e, pg.Color('yellow'), False, path_from_pathfinder_to_gate_scaled)
            step = 0

        disp.blit(surface_maze,(0,0))

        if(pathfinder_x!=gate_x or pathfinder_y!=gate_y):
            pathfinder_x = path_from_pathfinder_to_gate[step][0]
            pathfinder_y = path_from_pathfinder_to_gate[step][1]
        disp.blit(surface_b2e,(0,0))
        disp.blit(gate, (gate_x * scale_x, gate_y * scale_y))
        disp.blit(pathfinder,(pathfinder_x*scale_x,pathfinder_y*scale_y))
        disp.blit(wanderer,(wanderer_x*scale_x,wanderer_y*scale_y))
        pg.display.flip()
        step += 1

#disp.blit(surface,(0,0))
pg.display.flip()
print("lol")
# pg.quit()
