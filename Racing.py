"""A small top-down arcade racer built with Pygame."""

import json
import random
import sys
from pathlib import Path

import pygame



pygame.init()

WIDTH, HEIGHT = 900, 700
FPS = 60
ROAD_WIDTH = 500
ROAD_LEFT = (WIDTH - ROAD_WIDTH) // 2
ROAD_RIGHT = ROAD_LEFT + ROAD_WIDTH
CAR_WIDTH, CAR_HEIGHT = 46, 78

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Velocity | Arcade Racing")
clock = pygame.time.Clock()

FONT = pygame.font.Font(None, 30)
SMALL_FONT = pygame.font.Font(None, 23)
CONTROL_FONT = pygame.font.Font(None, 20)
KEY_FONT = pygame.font.Font(None, 19)
TITLE_FONT = pygame.font.Font(None, 68)

BACKGROUND = (19, 29, 39)
ASPHALT = (43, 49, 56)
ROAD_EDGE = (234, 239, 235)
LANE_MARK = (222, 207, 151)
TEXT = (241, 245, 242)
MUTED = (166, 180, 187)
ACCENT = (80, 224, 184)

CARS = [
	{"name": "LIME GT", "body": (107, 220, 135), "accent": (238, 250, 193)},
	{"name": "SKYLINE", "body": (93, 177, 242), "accent": (218, 241, 255)},
	{"name": "SUNSET", "body": (245, 132, 91), "accent": (255, 220, 157)},
	{"name": "VIOLET", "body": (184, 145, 239), "accent": (239, 222, 255)},
]
TRAFFIC_COLORS = [(234, 100, 104), (245, 191, 91), (107, 194, 203), (196, 205, 214)]
LANES = [ROAD_LEFT + 105, ROAD_LEFT + 250, ROAD_LEFT + 395]
HIGH_SCORE_PATH = Path(__file__).with_name("racing_high_score.json")


def load_high_score():
	try:
		with HIGH_SCORE_PATH.open(encoding="utf-8") as score_file:
			score_data = json.load(score_file)
			if not isinstance(score_data, dict):
				return 0
			return max(0, int(score_data.get("distance", 0)))
	except (OSError, ValueError, TypeError, json.JSONDecodeError):
		return 0


def save_high_score(score):
	try:
		with HIGH_SCORE_PATH.open("w", encoding="utf-8") as score_file:
			json.dump({"distance": score}, score_file)
		return True
	except OSError:
		return False


def draw_text(text, font, color, position, *, center=False):
	image = font.render(text, True, color)
	rect = image.get_rect(center=position) if center else image.get_rect(topleft=position)
	screen.blit(image, rect)


def draw_control_hint(x, y, key, label):
	key_rect = pygame.Rect(x, y, 28, 24)
	pygame.draw.rect(screen, (38, 53, 61), key_rect, border_radius=5)
	pygame.draw.rect(screen, (82, 105, 111), key_rect, width=1, border_radius=5)
	draw_text(key, KEY_FONT, TEXT, key_rect.center, center=True)
	draw_text(label, CONTROL_FONT, MUTED, (x + 36, y + 4))


def draw_car(rect, color, accent, player=False):
	"""Draw a compact top-down car from clean geometric shapes."""
	x, y, width, height = rect
	shadow = pygame.Rect(x + 4, y + 7, width, height)
	pygame.draw.rect(screen, (20, 24, 28), shadow, border_radius=11)
	body = pygame.Rect(x, y, width, height)
	pygame.draw.rect(screen, color, body, border_radius=11)

	# Wheels sit slightly outside the body for a clear racing-car silhouette.
	wheel_color = (23, 27, 31)
	for wheel_y in (y + 13, y + height - 25):
		pygame.draw.rect(screen, wheel_color, (x - 4, wheel_y, 7, 17), border_radius=3)
		pygame.draw.rect(screen, wheel_color, (x + width - 3, wheel_y, 7, 17), border_radius=3)

	windshield = pygame.Rect(x + 8, y + 15, width - 16, 20)
	pygame.draw.rect(screen, (48, 72, 82), windshield, border_radius=6)
	rear_window = pygame.Rect(x + 10, y + 43, width - 20, 12)
	pygame.draw.rect(screen, (57, 77, 84), rear_window, border_radius=4)
	pygame.draw.line(screen, accent, (x + 9, y + 9), (x + width - 9, y + 9), 3)
	pygame.draw.rect(screen, (255, 245, 190), (x + 6, y + 3, 9, 4), border_radius=2)
	pygame.draw.rect(screen, (255, 245, 190), (x + width - 15, y + 3, 9, 4), border_radius=2)
	pygame.draw.rect(screen, (229, 75, 72), (x + 6, y + height - 7, 9, 4), border_radius=2)
	pygame.draw.rect(screen, (229, 75, 72), (x + width - 15, y + height - 7, 9, 4), border_radius=2)
	if player:
		pygame.draw.rect(screen, accent, body, width=2, border_radius=11)


def reset_game():
	player_x = WIDTH / 2 - CAR_WIDTH / 2
	return player_x, [], 0.0, 0.0, 0.0, False


def accelerate_speed(speed, elapsed_seconds):
	return min(speed + 28 * elapsed_seconds, 560)


def difficulty_level(distance):
	return min(max(distance / 4000, 0), 1)


def draw_road(line_offset):
	screen.fill(BACKGROUND)
	pygame.draw.rect(screen, (28, 55, 50), (0, 0, ROAD_LEFT, HEIGHT))
	pygame.draw.rect(screen, (28, 55, 50), (ROAD_RIGHT, 0, WIDTH - ROAD_RIGHT, HEIGHT))
	pygame.draw.rect(screen, ASPHALT, (ROAD_LEFT, 0, ROAD_WIDTH, HEIGHT))
	pygame.draw.rect(screen, ROAD_EDGE, (ROAD_LEFT + 12, 0, 5, HEIGHT))
	pygame.draw.rect(screen, ROAD_EDGE, (ROAD_RIGHT - 17, 0, 5, HEIGHT))

	dash_height, gap = 38, 34
	for lane_x in (ROAD_LEFT + ROAD_WIDTH // 3, ROAD_LEFT + 2 * ROAD_WIDTH // 3):
		for y in range(-dash_height, HEIGHT + dash_height, dash_height + gap):
			pygame.draw.rect(screen, LANE_MARK, (lane_x - 2, y + line_offset, 4, dash_height), border_radius=2)

	# Sparse roadside markers add depth without competing with the cars.
	for y in range(-20, HEIGHT + 40, 90):
		marker_y = (y + int(line_offset * 0.55)) % (HEIGHT + 40) - 20
		for side_x in (ROAD_LEFT - 30, ROAD_RIGHT + 20):
			pygame.draw.circle(screen, (75, 116, 88), (side_x, marker_y), 7)


def main():
	player_x, traffic, distance, spawn_timer, road_offset, crashed = reset_game()
	speed = 300.0
	high_score = load_high_score()
	new_record = False
	selected_car = 0
	paused = False
	running = True

	while running:
		dt = min(clock.tick(FPS) / 1000, 0.04)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			elif event.type == pygame.KEYDOWN:
				if event.key in (pygame.K_ESCAPE, pygame.K_q):
					running = False
				elif event.key == pygame.K_c and not crashed:
					selected_car = (selected_car + 1) % len(CARS)
				elif event.key == pygame.K_p and not crashed:
					paused = not paused
				elif event.key == pygame.K_r:
					player_x, traffic, distance, spawn_timer, road_offset, crashed = reset_game()
					speed = 300.0
					paused = False
					new_record = False

		keys = pygame.key.get_pressed()
		if not paused and not crashed:
			steering = int(keys[pygame.K_RIGHT] or keys[pygame.K_d]) - int(keys[pygame.K_LEFT] or keys[pygame.K_a])
			player_x += steering * 360 * dt
			player_x = max(ROAD_LEFT + 28, min(ROAD_RIGHT - CAR_WIDTH - 28, player_x))

			speed = accelerate_speed(speed, dt)
			distance += speed * dt / 12
			difficulty = difficulty_level(distance)
			road_offset = (road_offset + speed * dt) % 72
			spawn_timer += dt
			spawn_interval = 0.95 - 0.60 * difficulty
			if spawn_timer >= spawn_interval:
				spawn_timer = 0
				lane_x = random.choice(LANES)
				if all(abs(lane_x - car[0]) > 90 for car in traffic if car[1] < 150):
					traffic.append([lane_x - CAR_WIDTH / 2, -CAR_HEIGHT, random.choice(TRAFFIC_COLORS)])

			player_rect = pygame.Rect(round(player_x), HEIGHT - 135, CAR_WIDTH, CAR_HEIGHT)
			for car in traffic:
				car[1] += speed * (1 + 0.4 * difficulty) * dt
				traffic_rect = pygame.Rect(round(car[0]), round(car[1]), CAR_WIDTH, CAR_HEIGHT)
				if player_rect.inflate(8, 12).colliderect(traffic_rect.inflate(8, 12)):
					if not crashed:
						crashed = True
						run_score = int(distance)
						if run_score > high_score:
							new_record = save_high_score(run_score)
							if new_record:
								high_score = run_score
			traffic = [car for car in traffic if car[1] < HEIGHT + CAR_HEIGHT]

		draw_road(road_offset)

		# Side panels keep the playfield open while making controls and stats easy to scan.
		pygame.draw.rect(screen, (21, 34, 42), (22, 24, ROAD_LEFT - 44, 210), border_radius=10)
		draw_text("VELOCITY", FONT, ACCENT, (40, 38))
		draw_text("ARCADE RACING", SMALL_FONT, MUTED, (40, 64))
		draw_text("SPEED", SMALL_FONT, MUTED, (40, 94))
		draw_text(f"{int(speed):03d} km/h", FONT, TEXT, (40, 111))
		meter_rect = pygame.Rect(40, 143, ROAD_LEFT - 84, 6)
		pygame.draw.rect(screen, (48, 65, 72), meter_rect, border_radius=3)
		pygame.draw.rect(screen, ACCENT, (meter_rect.x, meter_rect.y, int(meter_rect.width * speed / 560), meter_rect.height), border_radius=3)
		draw_text("DISTANCE", SMALL_FONT, MUTED, (40, 158))
		draw_text(f"{int(distance):05d} m", FONT, TEXT, (40, 174))
		draw_text(f"BEST  {high_score:05d} m", SMALL_FONT, ACCENT, (40, 208))

		pygame.draw.rect(screen, (21, 34, 42), (ROAD_RIGHT + 22, 24, WIDTH - ROAD_RIGHT - 44, 146), border_radius=10)
		draw_text("YOUR CAR", SMALL_FONT, MUTED, (ROAD_RIGHT + 40, 42))
		draw_text(CARS[selected_car]["name"], FONT, CARS[selected_car]["body"], (ROAD_RIGHT + 40, 68))
		draw_car((ROAD_RIGHT + 32, 105, 35, 58), CARS[selected_car]["body"], CARS[selected_car]["accent"])
		draw_control_hint(ROAD_RIGHT + 78, 122, "C", "CHANGE")

		for car_x, car_y, car_color in traffic:
			draw_car((round(car_x), round(car_y), CAR_WIDTH, CAR_HEIGHT), car_color, (248, 247, 229))
		player_y = HEIGHT - 135
		draw_car((round(player_x), player_y, CAR_WIDTH, CAR_HEIGHT), CARS[selected_car]["body"], CARS[selected_car]["accent"], player=True)

		pygame.draw.rect(screen, (21, 34, 42), (22, HEIGHT - 77, WIDTH - 44, 52), border_radius=9)
		draw_text("STEER  ← → / A D", CONTROL_FONT, TEXT, (42, HEIGHT - 59))
		for separator_x in (225, 420, 615):
			pygame.draw.line(screen, (48, 65, 72), (separator_x, HEIGHT - 64), (separator_x, HEIGHT - 39), 1)
		draw_control_hint(250, HEIGHT - 63, "C", "CHANGE")
		draw_control_hint(445, HEIGHT - 63, "R", "RESTART")
		draw_control_hint(640, HEIGHT - 63, "ESC", "QUIT")

		if paused or crashed:
			veil = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
			veil.fill((9, 16, 22, 175))
			screen.blit(veil, (0, 0))
			title = "CRASHED" if crashed else "PAUSED"
			draw_text(title, TITLE_FONT, TEXT, (WIDTH // 2, HEIGHT // 2 - 28), center=True)
			if crashed:
				draw_text(f"DISTANCE {int(distance):05d} m   |   BEST {high_score:05d} m", FONT, ACCENT, (WIDTH // 2, HEIGHT // 2 + 22), center=True)
				draw_text("NEW RECORD!" if new_record else "Press R to race again", SMALL_FONT, TEXT, (WIDTH // 2, HEIGHT // 2 + 55), center=True)
			else:
				draw_text("Press P to continue", FONT, ACCENT, (WIDTH // 2, HEIGHT // 2 + 25), center=True)
			draw_text("ESC to quit", SMALL_FONT, MUTED, (WIDTH // 2, HEIGHT // 2 + 87), center=True)

		pygame.display.flip()

	pygame.quit()
	sys.exit()


if __name__ == "__main__":
	main()
