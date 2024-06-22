from vpython import *
import random

# Buat jendela VPython dengan tema game bola pantul
scene = canvas(title='Game Bola Pantul', width=800, height=600, center=vector(0,0,0), background=color.green)

# Fungsi untuk menghasilkan warna acak
def random_color():
    return vector(random.random(), random.random(), random.random())

# Fungsi untuk menghasilkan kecepatan acak di sumbu x dan y
def random_velocity():
    return vector(random.uniform(-1, 1), random.uniform(-1, 1), 0)

# Fungsi untuk menggerakkan bola ungu satu dengan keyboard
def move_purple_ball(event):
    if event.key == 'up':
        purple_ball_one.velocity = vector(0, 1, 0)
    elif event.key == 'down':
        purple_ball_one.velocity = vector(0, -1, 0)
    elif event.key == 'left':
        purple_ball_one.velocity = vector(-1, 0, 0)
    elif event.key == 'right':
        purple_ball_one.velocity = vector(1, 0, 0)

# Fungsi untuk menghitung kecepatan baru setelah tabrakan elastis
def elastic_collision(ball1, ball2):
    v1 = ball1.velocity
    v2 = ball2.velocity
    m1 = ball1.mass
    m2 = ball2.mass
    new_v1 = v1 - (2 * m2 / (m1 + m2)) * dot(v1 - v2, ball1.pos - ball2.pos) / mag(ball1.pos - ball2.pos)**2 * (ball1.pos - ball2.pos)
    new_v2 = v2 - (2 * m1 / (m1 + m2)) * dot(v2 - v1, ball2.pos - ball1.pos) / mag(ball2.pos - ball1.pos)**2 * (ball2.pos - ball1.pos)
    return new_v1, new_v2

# Tambahkan pigora kayu di setiap sudut
frame_thickness = -5
frame_color = vector(0.55, 0.27, 0.07)  # Warna coklat seperti kayu

# Pigora atas dan bawah
box(pos=vector(0, 5 + frame_thickness/2, 0), size=vector(10 + frame_thickness*2, frame_thickness, 0.1), color=frame_color)
box(pos=vector(0, -5 - frame_thickness/2, 0), size=vector(10 + frame_thickness*2, frame_thickness, 0.1), color=frame_color)

# Pigora kiri dan kanan
box(pos=vector(5 + frame_thickness/2, 0, 0), size=vector(frame_thickness, 10, 0.1), color=frame_color)
box(pos=vector(-5 - frame_thickness/2, 0, 0), size=vector(frame_thickness, 10, 0.1), color=frame_color)

# Buat bola-bola
balls = []
for i in range(3):
    ball = sphere(pos=vector(random.uniform(-5, 5), random.uniform(-5, 5), 0), radius=0.5, color=random_color())
    ball.velocity = random_velocity()
    ball.mass = 1
    balls.append(ball)

# Buat bola ungu satu
purple_ball_one = sphere(pos=vector(0, 0, 0), radius=0.5, color=vector(1, 0, 1))
purple_ball_one.velocity = vector(0, 0, 0)
purple_ball_one.mass = 1

# Buat bola hijau dua
green_ball_two = sphere(pos=vector(random.uniform(-5, 5), random.uniform(-5, 5), 0), radius=0.5, color=vector(0, 1, 0))
green_ball_two.velocity = random_velocity()
green_ball_two.mass = 1

balls.append(purple_ball_one)
balls.append(green_ball_two)

# Menangani input keyboard
scene.bind('keydown', move_purple_ball)

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
    
        # Deteksi tabrakan dengan bola lainnya
        for other_ball in balls:
            if ball != other_ball and mag(ball.pos - other_ball.pos) <= (ball.radius + other_ball.radius):
                ball.velocity, other_ball.velocity = elastic_collision(ball, other_ball)
