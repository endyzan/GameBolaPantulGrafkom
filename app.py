from vpython import *
import random
import time

# Buat jendela VPython dengan tema game glow hockey
scene = canvas(title='Game Bola Pantul - Glow Hockey', width=800, height=600, center=vector(0, 0, 0), background=color.black)

# Fungsi untuk menghasilkan warna acak
def random_color():
    colors = [
        vector(9 / 255, 24 / 255, 51 / 255),
        vector(19 / 255, 62 / 255, 124 / 255),
        vector(10 / 255, 189 / 255, 198 / 255),
        vector(234 / 255, 0, 217 / 255),
        vector(113 / 255, 28 / 255, 145 / 255)
    ]
    return random.choice(colors)

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
def create_sparkles(position):
    sparkles = []
    for _ in range(20):
        sparkle = sphere(pos=position, radius=0.1, color=random_color(), emissive=True)
        sparkle.velocity = random_velocity() * 2
        sparkles.append(sparkle)
    return sparkles

# Tambahkan pigora bercahaya di setiap sudut
frame_thickness = 0.2
initial_frame_color = vector(209 / 255, 247 / 255, 1)

# Pigora atas dan bawah
top_frame = box(pos=vector(0, 5 + frame_thickness / 2, 0), size=vector(10 + frame_thickness * 2, frame_thickness, 0.1), color=initial_frame_color, emissive=True)
bottom_frame = box(pos=vector(0, -5 - frame_thickness / 2, 0), size=vector(10 + frame_thickness * 2, frame_thickness, 0.1), color=initial_frame_color, emissive=True)

# Pigora kiri dan kanan
left_frame = box(pos=vector(5 + frame_thickness / 2, 0, 0), size=vector(frame_thickness, 10, 0.1), color=initial_frame_color, emissive=True)
right_frame = box(pos=vector(-5 - frame_thickness / 2, 0, 0), size=vector(frame_thickness, 10, 0.1), color=initial_frame_color, emissive=True)

# Buat bola-bola
balls = []
for i in range(3):
    ball = sphere(pos=vector(random.uniform(-5, 5), random.uniform(-5, 5), 0), radius=0.5, color=random_color(), emissive=True)
    ball.velocity = random_velocity()
    ball.mass = 1
    balls.append(ball)

# Buat bola ungu satu
purple_ball_one = sphere(pos=vector(0, 0, 0), radius=0.5, color=vector(113 / 255, 28 / 255, 145 / 255), emissive=True)
purple_ball_one.velocity = vector(0, 0, 0)
purple_ball_one.mass = 1

# Buat bola hijau dua
green_ball_two = sphere(pos=vector(random.uniform(-5, 5), random.uniform(-5, 5), 0), radius=0.5, color=vector(203 / 255, 12 / 255, 89 / 255), emissive=True)
green_ball_two.velocity = random_velocity()
green_ball_two.mass = 1

balls.append(purple_ball_one)
balls.append(green_ball_two)

# Ubah warna bola-bola lainnya
balls[0].color = vector(34 / 255, 160 / 255, 182 / 255)
balls[1].color = vector(0, 1, 159 / 255)
balls[2].color = vector(123 / 255, 19 / 255, 70 / 255)

# Menangani input keyboard
scene.bind('keydown', move_purple_ball)

# Variabel untuk waktu kembali warna pigora
frame_color_change_time = 0
color_change_duration = 0.1

# Loop untuk menggerakkan bola
dt = 0.01
sparks = []
while True:
    rate(200)  # Tentukan kecepatan animasi
    
    for ball in balls:
        ball.pos += ball.velocity * dt
        
        # Memantul dari dinding di antara sumbu x dan y
        if abs(ball.pos.x) + ball.radius > 5:
            ball.velocity.x *= -1
            ball.pos.x = 5 - ball.radius if ball.pos.x > 0 else -5 + ball.radius
            top_frame.color = bottom_frame.color = left_frame.color = right_frame.color = color.white
            frame_color_change_time = time.time()
        if abs(ball.pos.y) + ball.radius > 5:
            ball.velocity.y *= -1
            ball.pos.y = 5 - ball.radius if ball.pos.y > 0 else -5 + ball.radius
            top_frame.color = bottom_frame.color = left_frame.color = right_frame.color = color.white
            frame_color_change_time = time.time()
        
        # Tetap di sumbu x dan y
        ball.pos.z = 0
    
        # Deteksi tabrakan dengan bola lainnya
        for other_ball in balls:
            if ball != other_ball and mag(ball.pos - other_ball.pos) <= (ball.radius + other_ball.radius):
                ball.velocity, other_ball.velocity = elastic_collision(ball, other_ball)
                sparks.extend(create_sparkles(ball.pos))
                
                # Tambahkan offset untuk mencegah bola menempel
                overlap = ball.radius + other_ball.radius - mag(ball.pos - other_ball.pos)
                direction = norm(ball.pos - other_ball.pos)
                ball.pos += direction * (overlap / 2)
                other_ball.pos -= direction * (overlap / 2)

    # Kembalikan warna pigora setelah beberapa waktu
    if top_frame.color == color.white and time.time() - frame_color_change_time >= color_change_duration:
        top_frame.color = bottom_frame.color = left_frame.color = right_frame.color = initial_frame_color

    # Update percikan
    for spark in sparks:
        spark.pos += spark.velocity * dt
        spark.radius *= 0.95  # Percikan mengecil
        if spark.radius < 0.01:
            spark.visible = False
            sparks.remove(spark)
