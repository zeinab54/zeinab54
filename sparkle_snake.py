import random
from PIL import Image, ImageDraw

# 🐍 Settings
CELL = 15
ROWS = 11
COLS = 20
WIDTH = COLS * CELL
HEIGHT = ROWS * CELL
BACKGROUND = (255, 230, 245)  # baby pink
WALL_COLOR = (255, 105, 180)   # hot pink walls
SNAKE_COLOR = (255, 182, 193)  # light pink snake
SPARKLE_COLOR = (255, 255, 255)
HEART_COLOR = (255, 20, 147)
SNAKE_LENGTH = 6
FRAME_DELAY = 180

frames = []

# Maze layout: 1 = wall, 0 = path
maze = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,1,0,0,0,0,0,1,0,0,0,1,0,0,0,0,1],
    [1,0,1,0,1,0,1,1,1,0,1,0,1,0,1,1,1,1,0,1],
    [1,0,1,0,0,0,0,0,1,0,0,0,1,0,0,0,0,1,0,1],
    [1,0,1,1,1,1,1,0,1,1,1,0,1,1,1,1,0,1,0,1],
    [1,0,0,0,0,0,1,0,0,0,1,0,0,0,0,1,0,1,0,1],
    [1,1,1,1,1,0,1,1,1,0,1,1,1,1,0,1,0,1,0,1],
    [1,0,0,0,1,0,0,0,1,0,0,0,0,1,0,1,0,0,0,1],
    [1,0,1,0,1,1,1,0,1,1,1,1,0,1,0,1,1,1,0,1],
    [1,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
]

dirs = [(-1,0),(1,0),(0,-1),(0,1)]

# DFS traversal to generate snake path
def dfs(r, c, visited, path):
    visited.add((r,c))
    path.append((r,c))
    random.shuffle(dirs)
    for dr, dc in dirs:
        nr, nc = r+dr, c+dc
        if 0 <= nr < ROWS and 0 <= nc < COLS:
            if maze[nr][nc] == 0 and (nr,nc) not in visited:
                dfs(nr, nc, visited, path)

visited = set()
snake_path = []
dfs(1,1,visited,snake_path)

# Hearts along the path
num_hearts = max(5, len(snake_path)//8)
heart_positions = random.sample(snake_path, num_hearts)

# Animate snake
for frame_index in range(len(snake_path)):
    img = Image.new("RGB", (WIDTH, HEIGHT), BACKGROUND)
    draw = ImageDraw.Draw(img)

    # Draw maze walls
    for r in range(ROWS):
        for c in range(COLS):
            if maze[r][c]==1:
                x0, y0 = c*CELL, r*CELL
                x1, y1 = x0+CELL, y0+CELL
                draw.rectangle([x0, y0, x1, y1], fill=WALL_COLOR)

    # Draw hearts
    for hr, hc in heart_positions:
        hx = hc*CELL + CELL//4
        hy = hr*CELL + CELL//4
        draw.ellipse([hx, hy, hx+CELL//2, hy+CELL//2], fill=HEART_COLOR)

    # Draw snake body as capsules with sparkles
    snake_head_index = frame_index
    snake_body_indices = range(max(0, snake_head_index-SNAKE_LENGTH+1), snake_head_index+1)
    for idx in snake_body_indices:
        r, c = snake_path[idx]
        x0, y0 = c*CELL, r*CELL
        x1, y1 = x0+CELL, y0+CELL
        # Rounded rectangle (capsule)
        draw.rounded_rectangle([x0, y0, x1, y1], radius=CELL//2, fill=SNAKE_COLOR)
        # Sparkles on body
        for _ in range(4):
            sx = x0 + random.randint(0, CELL-3)
            sy = y0 + random.randint(0, CELL-3)
            draw.ellipse([sx, sy, sx+2, sy+2], fill=SPARKLE_COLOR)

    # Remove heart if eaten
    head_pos = snake_path[snake_head_index]
    if head_pos in heart_positions:
        heart_positions.remove(head_pos)

    frames.append(img)

# Save GIF
frames[0].save(
    "maze_sparkle_snake_capsule.gif",
    save_all=True,
    append_images=frames[1:],
    optimize=True,
    duration=180,
    loop=0
)

print("✨ Done! maze_sparkle_snake_capsule.gif generated — snake is now rounded and sparkling! ✨")