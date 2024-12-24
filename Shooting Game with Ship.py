
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

screen_width = 800
screen_height = 600
ship_x = screen_width // 2
ship_y = 50
ship_width = 80
ship_height = 10
ship_speed = 10
projectile_radius = 10
projectiles = []
proj_speed = 0.5

radius = 20
circles = []
fall_speed = 0.05
score = 0
missed = 0
miss_limit = 3
game_over = False

def midpoint_line(x1, y1, x2, y2):
    dx, dy = abs(x2 - x1), abs(y2 - y1)
    if x2> x1:
        sx = 1
    else:
        sx = -1
    if y2>y1:
        sy = 1
    else:
        sy = -1
    err1 = dx - dy

    while True:
        glVertex2f(x1, y1)
        if x1 == x2 and y1 == y2:
            break
        e2 = err1 * 2
        if e2 > -dy:
            err1 -= dy
            x1 += sx
        if e2 < dx:
            err1 += dx
            y1 += sy
def midpoint_circle(x1, y1, r):
    x, y = 0, r
    d = 1 - r
    while x <= y:
        for dx, dy in [(x, y), (y, x), (-x, y), (-y, x),(-x, -y), (-y, -x), (x, -y), (y, -x)]:
            glVertex2f(x1 + dx, y1 + dy)
        if d < 0:
            d += 2 * x + 3
        else:
            d += 2 * (x - y) + 5
            y -= 1
        x += 1

def draw_ship():
    glBegin(GL_POINTS)
    midpoint_line(ship_x - ship_width // 2, ship_y, ship_x + ship_width // 2, ship_y)
    midpoint_line(ship_x - ship_width // 2, ship_y, ship_x, ship_y + ship_height)
    midpoint_line(ship_x, ship_y + ship_height, ship_x + ship_width // 2, ship_y)
    midpoint_line(ship_x - ship_width // 2, ship_y, ship_x - ship_width // 2, ship_y - ship_height)
    midpoint_line(ship_x + ship_width // 2, ship_y, ship_x + ship_width // 2, ship_y - ship_height)
    midpoint_line(ship_x - ship_width // 2, ship_y - ship_height, ship_x + ship_width // 2, ship_y - ship_height)
    glEnd()


def draw_circles():
    glBegin(GL_POINTS)
    for circle in circles:
        midpoint_circle(circle['x'], circle['y'], radius)
    glEnd()

def draw_projectiles():
    glBegin(GL_POINTS)
    for proj in projectiles:
        midpoint_circle(proj['x'], proj['y'], projectile_radius)
    glEnd()

def update_circles():
    global missed, game_over
    for circle in circles[:]:
        circle['y'] -= fall_speed
        if circle['y'] - radius <= 0:
            missed += 1
            circles.remove(circle)
            if missed >= miss_limit:
                game_over = True


def update_projectiles():
    global score
    for proj in projectiles[:]:
        proj['y'] += proj_speed
        if proj['y'] >= screen_height:
            projectiles.remove(proj)
        else:
            for circle in circles[:]:
                if (circle['x'] - proj['x'])**2 + (circle['y'] - proj['y'])**2 <= (radius + projectile_radius)**2:
                    circles.remove(circle)
                    projectiles.remove(proj)
                    score += 1
                    break

def spawn_circle():
    if not game_over:
        x = random.randint(radius, screen_width - radius)
        y = screen_height - radius
        circles.append({'x': x, 'y': y})

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    draw_ship()
    draw_circles()
    draw_projectiles()
    glutSwapBuffers()

def update_game():
    global game_over
    if not game_over:
        update_circles()
        update_projectiles()
        display()
    else:
        print(f"Game Over! YOUR SCORE: {score}")
        glutLeaveMainLoop()

def keyboard(key, x, y):
    global ship_x, projectiles
    if key == b'a' and ship_x - ship_width // 2 > 0:
        ship_x -= ship_speed
    elif key == b'd' and ship_x + ship_width // 2 < screen_width:
        ship_x += ship_speed
    elif key == b' ':
        projectiles.append({'x': ship_x, 'y': ship_y + ship_height})

def timer(value):
    if not game_over:
        spawn_circle()
        glutTimerFunc(2000, timer, 0)

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(screen_width, screen_height)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"Shoot The Circles!")
    glClearColor(0, 0, 0, 0)
    gluOrtho2D(0, screen_width, 0, screen_height)
    glutDisplayFunc(display)
    glutIdleFunc(update_game)
    glutKeyboardFunc(keyboard)
    glutTimerFunc(2000, timer, 0)
    glutMainLoop()

if __name__ == "__main__":
    main()
