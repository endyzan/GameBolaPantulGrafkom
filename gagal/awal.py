from vpython import *
import random

# Buat jendela VPython
scene = canvas(title='Five Randomly Moving Balls', width=800, height=600, center=vector(0,0,0))

# Fungsi untuk menghasilkan warna acak
def random_color():
    return vector(random.random(), random.random(), random.random())

# Fungsi untuk menghasilkan kecepatan acak di sumbu x dan y
def random_velocity():
    return vector(random.uniform(-1, 1), random.uniform(-1, 1), 0)

# Fungsi untuk menggerakkan bola hijau satu dengan keyboard
def move_green_ball(event):
    if event.key == 'up':
        green_ball_one.velocity = vector(0, 1, 0)
    elif event.key == 'down':
        green_ball_one.velocity = vector(0, -1, 0)
    elif event.key == 'left':
        green_ball_one.velocity = vector(-1, 0, 0)
    elif event.key == 'right':
        green_ball_one.velocity = vector(1, 0, 0)

# Buat bola-bola
balls = []
for i in range(3):
    ball = sphere(pos=vector(random.uniform(-5, 5), random.uniform(-5, 5), 0), radius=0.5, color=random_color())
    ball.velocity = random_velocity()
    balls.append(ball)

# Buat bola hijau satu
green_ball_one = sphere(pos=vector(0, 0, 0), radius=0.5, color=vector(0, 1, 0))
green_ball_one.velocity = vector(0, 0, 0)

# Buat bola hijau dua
green_ball_two = sphere(pos=vector(random.uniform(-5, 5), random.uniform(-5, 5), 0), radius=0.5, color=vector(0, 1, 0))
green_ball_two.velocity = random_velocity()

balls.append(green_ball_one)
balls.append(green_ball_two)

# Menangani input keyboard
scene.bind('keydown', move_green_ball)

# Loop untuk menggerakkan bola
dt = 0.01
while True:
    rate(200)  # Tentukan kecepatan animasi
    
    for ball in balls:
        ball.pos += ball.velocity * dt
        
        # Memantul dari dinding di antara sumbu x dan y
        if abs(ball.pos.x) >= 5:
            ball.velocity.x *= -1
        if abs(ball.pos.y) >= 5:
            ball.velocity.y *= -1
        
        # Tetap di sumbu x dan y
        ball.pos.z = 0
    
        # Deteksi tabrakan dengan bola hijau satu
        if ball != green_ball_one and mag(ball.pos - green_ball_one.pos) <= (ball.radius + green_ball_one.radius):
            if ball == green_ball_two:
                # Menghitung kecepatan baru setelah tabrakan elastis
                v1 = green_ball_one.velocity
                v2 = green_ball_two.velocity
                green_ball_one.velocity, green_ball_two.velocity = v2, v1
            else:
                ball.velocity = vector(0, 0, 0)  # Bola lainnya berhenti