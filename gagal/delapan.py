#final

from vpython import *
import random

# Buat jendela VPython dengan tema game glow hockey
scene = canvas(title='Game Bola Pantul - Glow Hockey', width=800, height=600, center=vector(0,0,0), background=color.black)

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

# Fungsi untuk membuat percikan
def create_sparkles(position, color):
    sparkles = []
    for _ in range(20):
        sparkle = sphere(pos=position, radius=0.1, color=color, emissive=True)
        sparkle.velocity = random_velocity() * 2
        sparkles.append(sparkle)
    return sparkles

# Fungsi untuk membuat garis pigora
def create_frame_lines():
    lines = []
    segment_length = 2.5
    num_segments = 4
    
    for i in range(num_segments):
        lines.append(box(pos=vector(-5 + i * segment_length + segment_length / 2, 5, 0), size=vector(segment_length, 0.2, 0.1), color=color.white, emissive=True))
        lines.append(box(pos=vector(-5 + i * segment_length + segment_length / 2, -5, 0), size=vector(segment_length, 0.2, 0.1), color=color.white, emissive=True))
        lines.append(box(pos=vector(5, -5 + i * segment_length + segment_length / 2, 0), size=vector(0.2, segment_length, 0.1), color=color.white, emissive=True))
        lines.append(box(pos=vector(-5, -5 + i * segment_length + segment_length / 2, 0), size=vector(0.2, segment_length, 0.1), color=color.white, emissive=True))
    
    return lines

# Buat garis pigora
frame_lines = create_frame_lines()

# Buat bola-bola
balls = []
for i in range(3):
    ball = sphere(pos=vector(random.uniform(-5, 5), random.uniform(-5, 5), 0), radius=0.5, color=random_color(), emissive=True)
    ball.velocity = random_velocity()
    ball.mass = 1
    balls.append(ball)

# Buat bola ungu satu
purple_ball_one = sphere(pos=vector(0, 0, 0), radius=0.5, color=color.purple, emissive=True)
purple_ball_one.velocity = vector(0, 0, 0)
purple_ball_one.mass = 1

# Buat bola hijau dua
green_ball_two = sphere(pos=vector(random.uniform(-5, 5), random.uniform(-5, 5), 0), radius=0.5, color=color.green, emissive=True)
green_ball_two.velocity = random_velocity()
green_ball_two.mass = 1

balls.append(purple_ball_one)
balls.append(green_ball_two)

# Menangani input keyboard
scene.bind('keydown', move_purple_ball)

# Loop untuk menggerakkan bola
dt = 0.01
sparks = []
while True:
    rate(200)  # Tentukan kecepatan animasi
    
    for ball in balls:
        ball.pos += ball.velocity * dt
        
        # Memantul dari dinding di antara sumbu x dan y
        if abs(ball.pos.x) >= 5:
            ball.velocity.x *= -1
            # Ubah warna garis pigora
            for line in frame_lines:
                if line.pos.y == 5 or line.pos.y == -5:
                    line.color = ball.color
                    sparks.extend(create_sparkles(ball.pos, ball.color))
            
        if abs(ball.pos.y) >= 5:
            ball.velocity.y *= -1
            # Ubah warna garis pigora
            for line in frame_lines:
                if line.pos.x == 5 or line.pos.x == -5:
                    line.color = ball.color
                    sparks.extend(create_sparkles(ball.pos, ball.color))
        
        # Tetap di sumbu x dan y
        ball.pos.z = 0
    
        # Deteksi tabrakan dengan bola lainnya
        for other_ball in balls:
            if ball != other_ball and mag(ball.pos - other_ball.pos) <= (ball.radius + other_ball.radius):
                ball.velocity, other_ball.velocity = elastic_collision(ball, other_ball)
                sparks.extend(create_sparkles(ball.pos, ball.color))

    # Update percikan
    for spark in sparks:
        spark.pos += spark.velocity * dt
        spark.radius *= 0.95  # Percikan mengecil
        if spark.radius < 0.01:
            spark.visible = False
            sparks.remove(spark)
