import pygame as pyg
import math
import time

cube_v = [
[-.5,.5,.5], #1
[.5,.5,.5],  #2
[.5,.5,-.5],   #3
[-.5,.5,-.5], #4
[-.5,-.5,.5], #5
[.5,-.5,.5], #6
[.5,-.5,-.5], #7
[-.5,-.5,-.5]] #8

cube_c = [
[1,2],
[1,4],
[1,5],
[2,3],
[2,6],
[3,4],
[3,7],
[4,8],
[5,6],
[5,8],
[6,7],
[7,8]]

camera = [[3,1,0], [0,0]] #cam_coords, [theta_cxz, theta_cy]

width = 480
height = 270
rho = width/height
tau = 2 * math.pi
fov = tau / 8
fov_offset = fov / 2
org2d = [0,0]
org3d = [0,0,0]

def normalize(theta_vec):
  return [-(theta_vec[0] / fov) * 2, -(theta_vec[1] / fov) * 2]

def float_to_coord(f_vec):
  return [(f_vec[0] + 1) * width / 2, (f_vec[1] + 1) * height / 2]

def between(num, end1, end2, inclusive):
    if inclusive:
        if (num >= end1 and num <= end2) or (num <= end1 and num >= end2):
          return True
    else:
        if (num > end1 and num < end2) or (num < end1 and num > end2):
          return True
    return False

def theta_add(theta, delta):
    new_theta = theta + delta
    if new_theta > tau:
        tau_factor = math.floor(new_theta / tau)
        return new_theta - tau_factor * tau
    elif new_theta < 0:
        tau_factor = math.floor(abs(new_theta) / tau)
        return new_theta + tau_factor * tau
    else: return new_theta

def dist(p1, p2):
    if type(p1) == list:
        acc = 0
        for i in range(len(p1)):
            acc += (p2[i] - p1[i]) ** 2
        return math.sqrt(acc)
    else: return abs(p1 - p2)

def vec_sub(vec1, vec2):
    final = []
    for i in range(len(vec1)):
        final.append(vec1[i] - vec2[i])
    return final
    
def coord2d_to_theta(coord):
    if coord[0] == 0:
        if coord[1] > 0:
            return math.pi / 2
        elif coord[1] < 0:
            return math.pi * 2 - math.pi / 2
        else:
            return 0
    return math.atan(coord[1]/coord[0])
    
def coord3d_to_theta2(coord):
    xz_vec = cart_to_vec2D([coord[0], coord[2]])
    y_theta = coord2d_to_theta([xz_vec[0], coord[1]])
    return [xz_vec[1], y_theta]
    

def cart_to_vec2D(point):
    return [dist(org2d, point), coord2d_to_theta(point)]

def cart_to_vec3D(point):
    vec = []
    theta = coord3d_to_theta2(point)
    vec.append(dist(point, org3d))
    vec.append(theta[0])
    vec.append(theta[1])
    return vec

def vec_to_cart2D(vec):
    return [vec[0] * math.cos(vec[1]), vec[0] * math.sin(vec[1])]

def vec_to_cart3D(vec):
    y = vec[0] * math.sin(vec[2])
    x = vec[0] * math.cos(vec[1])
    z = vec[0] * math.sin(vec[1])
    return [x,y,z]

def project(point):
    pt_prime = vec_sub(point, camera[0])
    pt_prime_vec = cart_to_vec3D(pt_prime)
    #print(pt_prime_vec)
    pt_prime_vec[1] = theta_add(pt_prime_vec[1], -camera[1][0])
    pt_prime_vec[2] = theta_add(pt_prime_vec[2], -camera[1][1])
    coord = normalize(pt_prime_vec[1:])
    z_fact = pt_prime_vec[0] / 2
    return [coord[0] / z_fact / rho, coord[1] / z_fact]
    
    
    
def draw_lines(v_buf, c_buf, screen):
    for line in c_buf:
        p1 = project(v_buf[line[0] - 1])
        p2 = project(v_buf[line[1] - 1])
        print(p1)
        print(p2)
        print()
        pyg.draw.line(screen, (255,255,255), float_to_coord(p1), float_to_coord(p2), 2)
    pyg.display.flip()

def calc_move(vec):
  pass


def main():
  #print(normalize([0,0]))
  #print(normalize([math.pi / 4, 0]))
  #print
  pyg.init()
  screen = pyg.display.set_mode((width, height))
  count = 0
  while True:
    #for event in pyg.events.get():
    #  if event.type() == pyg.K_w:

    draw_lines(cube_v, cube_c, screen)
    print(count)
    count += 1
    camera[1][0] = theta_add(camera[1][0], .1)
    screen.fill((0,0,0))

main()
  