# Flappy Bird in Python (Pygame)

A 2D arcade Flappy Bird game built from scratch in Python using the **Pygame** library. This project demonstrates core game development principles, including frame-rate-governed game loops, 2D physics simulation, dynamic obstacle generation, AABB collision detection, and state management.

---

## Table of Contents
1. [Project Overview](#project-overview)
2. [How the Game Works](#how-the-game-works)
3. [Architecture & Flow](#architecture--flow)
4. [Step-by-Step Implementation Guide](#step-by-step-implementation-guide)
5. [In-Depth Code Breakdown](#in-depth-code-breakdown)
6. [Controls](#controls)
7. [Installation and How to Run](#installation-and-how-to-run)
8. [Optional: Untracking `venv` from Git](#optional-untracking-venv-from-git)
9. [Future Enhancements](#future-enhancements)

---

## Project Overview

This game replicates the mechanics of the iconic mobile game **Flappy Bird**.
- **Player Character**: A bird that falls under simulated gravity and jumps when the user presses `Space`.
- **Obstacles**: Randomly generated top and bottom pipe pairs that scroll horizontally across the screen from right to left.
- **Objective**: Navigate the bird safely through the pipe gaps to accumulate points.
- **Game Over & Restart**: Hitting the ground, ceiling, or any pipe triggers the "GAME OVER" screen with an option to restart instantly using `R`.

### Key Specifications
| Parameter | Value | Description |
| :--- | :--- | :--- |
| **Window Dimensions** | 400 × 600 px | Portrait arcade aspect ratio |
| **Target Frame Rate** | 60 FPS | Smooth rendering and stable physics updates |
| **Physics** | Gravity = `0.5`, Jump = `-8` | Vertical velocity and displacement calculation |
| **Pipes** | Width = `60px`, Gap = `170px`, Speed = `3px/frame` | Obstacle dimensions and pacing |

---

## How the Game Works

The game runs inside a continuous **Game Loop** ticking at 60 iterations per second:

```
[ Process Input Events ] -> [ Update Physics & State ] -> [ Check Collisions & Score ] -> [ Render / Draw ] -> [ Tick Clock ]
```

1. **Coordinate System**:
   - The origin `(0, 0)` is at the **top-left corner**.
   - `x` increases to the **right**.
   - `y` increases **downwards**.
2. **Physics Engine**:
   - Every frame, `bird_velocity` increases by `gravity` (downward acceleration).
   - The bird's vertical position (`bird_y`) increases by `bird_velocity`.
   - When the user presses `Space`, `bird_velocity` is set to `jump_strength` (`-8`), propelling the bird upward.
3. **Obstacle Spawning & Scrolling**:
   - Pipes are spawned off the right edge of the screen (`x = WIDTH`).
   - Each pipe obstacle contains both a **top pipe** and a **bottom pipe**, separated by a constant gap (`pipe_gap = 170px`).
   - The vertical center of this gap (`gap_y`) is randomly chosen between `150` and `400` pixels.
   - Pipes move left by `pipe_speed` each frame. When a pipe leaves the screen on the left, it is removed from memory.
4. **Collision Detection**:
   - The bird's circular hitbox is approximated using an Axis-Aligned Bounding Box (`pygame.Rect`).
   - The engine checks for intersections between the bird rect and both pipe rectangles using `colliderect()`.
   - It also checks boundary conditions: if the bird flies above the ceiling (`y < 0`) or touches the ground (`y > HEIGHT`), the game ends.
5. **Score Tracking**:
   - Each pipe structure has a boolean flag: `"scored": False`.
   - When a pipe's trailing edge passes the bird's horizontal position (`pipe["x"] + pipe_width < bird_x`), the score increments by `1` and `"scored"` is set to `True`.

---

## Architecture & Flow

```
                      +-------------------+
                      |   pygame.init()   |
                      | Window & Settings |
                      +---------+---------+
                                |
                                v
                      +-------------------+
                      |  Main Game Loop   | <-------------------------+
                      |    (60 FPS)       |                           |
                      +---------+---------+                           |
                                |                                     |
               +----------------+---------------+                     |
               |                                |                     |
     [ Event Handling ]                [ State Check ]                |
     - QUIT: exit()                    - Is game_over == True?        |
     - SPACE: jump                     +--------+-------------+       |
     - R: restart                               |             |       |
                                                v (No)        v (Yes) |
                               +--------------------+     +-----------+---------+
                               | Update Physics     |     | Render Game Over UI |
                               | Move Pipes         |     | Listen for 'R'      |
                               | Check Collisions   |     +-----------+---------+
                               | Update Score       |                 |
                               +--------+-----------+                 |
                                        |                             |
                                        v                             |
                               +--------------------+                 |
                               | Render Frame       |                 |
                               | - Sky Background   |                 |
                               | - Green Pipes      |                 |
                               | - Bird Body & Eyes |                 |
                               | - Current Score    |                 |
                               +--------+-----------+                 |
                                        |                             |
                                        +-----------------------------+
```

---

## Step-by-Step Implementation Guide

### Step 1: Environment & Display Initialization
We initialize Pygame, establish the window size (400 × 600), set the window caption, and instantiate a clock object (`pygame.time.Clock()`) to lock execution to 60 frames per second.

### Step 2: Defining Game Constants & Color Palette
Color tuples in RGB format define the visual identity:
- Sky Blue: `(135, 206, 235)`
- Pipe Green: `(34, 177, 76)`
- Bird Yellow: `(255, 220, 0)`
- White & Black: `(255, 255, 255)` & `(0, 0, 0)`

### Step 3: Modeling the Player (Bird)
The bird is configured by its position `(bird_x, bird_y)`, size (`bird_radius`), downward acceleration (`gravity = 0.5`), and instantaneous upward impulse (`jump_strength = -8`).

### Step 4: Procedural Pipe Generation
A helper function `create_pipe()` computes a random vertical gap center:
```python
def create_pipe():
    gap_y = random.randint(150, 400)
    return {"x": WIDTH, "gap_y": gap_y, "scored": False}
```
Pipes are dynamically spawned when the newest pipe travels far enough into the screen (`WIDTH - 220`).

### Step 5: Collision and Boundary Logic
We construct bounding rectangles for the bird, upper pipe, and lower pipe:
- Top pipe rect: `(pipe["x"], 0, pipe_width, gap_y - pipe_gap // 2)`
- Bottom pipe rect: `(pipe["x"], gap_y + pipe_gap // 2, pipe_width, HEIGHT - bottom_y)`

If `bird_rect.colliderect()` returns true for either, or if `bird_y` exceeds `0` or `HEIGHT`, `game_over` becomes `True`.

### Step 6: Rendering Pipeline
Every frame, the screen is wiped with the background color (`screen.fill(SKY)`), and geometric primitives are drawn in order (back to front):
1. Top and bottom green pipe rectangles (`pygame.draw.rect`)
2. Yellow bird circle (`pygame.draw.circle`)
3. Bird eye details (outer white circle, inner black pupil)
4. Score and Game Over text surfaces blitted onto the screen
5. `pygame.display.update()` pushes the drawn frame to the monitor.

---

## In-Depth Code Breakdown

Here is an analysis of each section of [app.py](file:///c:/Users/cozme/Desktop/flappy_bird/app.py):

### 1. Initialization and Configuration (Lines 1–36)
```python
import pygame
import random
import sys

pygame.init()
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")
```
- `pygame.init()` boots all Pygame submodules (display, font, event system).
- `set_mode((WIDTH, HEIGHT))` creates the graphics surface representing the application window.

### 2. Game Variables and Object State (Lines 21–36)
```python
bird_x = 80
bird_y = 300
bird_radius = 15
bird_velocity = 0
gravity = 0.5
jump_strength = -8

pipe_width = 60
pipe_gap = 170
pipe_speed = 3
pipes = []
score = 0
font = pygame.font.SysFont(None, 36)
clock = pygame.time.Clock()
```
- `bird_velocity`: Holds current vertical speed. Starts at 0 and changes based on gravity or jump events.
- `pipe_gap = 170`: The vertical clearance the bird must fly through.
- `pipes`: An in-memory list tracking active pipe pairs.

### 3. Event Loop (Lines 54–69)
```python
for event in pygame.event.get():
    if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE and not game_over:
            bird_velocity = jump_strength

        if event.key == pygame.K_R and game_over:
            # Reset game variables
            bird_y = 300
            bird_velocity = 0
            pipes = [create_pipe()]
            score = 0
            game_over = False
```
- Reads OS inputs (keyboard, close window).
- When `Space` is pressed, `bird_velocity` is reset to `-8` (moving up).
- When `R` is pressed while game over, it resets the player, obstacles, and score.

### 4. Physics and Pipe Mechanics (Lines 71–86)
```python
# Bird physics
bird_velocity += gravity
bird_y += bird_velocity

# Create new pipes
if pipes[-1]["x"] < WIDTH - 220:
    pipes.append(create_pipe())

# Move pipes
for pipe in pipes:
    pipe["x"] -= pipe_speed

# Remove off-screen pipes
pipes = [pipe for pipe in pipes if pipe["x"] + pipe_width > 0]
```
- Euler integration for physics: Acceleration alters velocity, velocity alters position.
- Memory management: List comprehension discards pipes that have moved completely past the left edge of the screen (`x + width <= 0`).

### 5. Collision and Scoring (Lines 88–120)
```python
bird_rect = pygame.Rect(
    bird_x - bird_radius,
    int(bird_y) - bird_radius,
    bird_radius * 2,
    bird_radius * 2
)
for pipe in pipes:
    top_height = pipe["gap_y"] - pipe_gap // 2
    bottom_y = pipe["gap_y"] + pipe_gap // 2
    top_rect = pygame.Rect(pipe["x"], 0, pipe_width, top_height)
    bottom_rect = pygame.Rect(pipe["x"], bottom_y, pipe_width, HEIGHT - bottom_y)

    if bird_rect.colliderect(top_rect) or bird_rect.colliderect(bottom_rect):
        game_over = True

    if not pipe["scored"] and pipe["x"] + pipe_width < bird_x:
        score += 1
        pipe["scored"] = True
```
- Calculates precise bounding boxes for both top and bottom pipes and evaluates collision with `bird_rect`.
- Awards a point as soon as the back edge of the pipe passes `bird_x`.

### 6. Graphics Rendering & Display Refresh (Lines 122–176)
- Renders the sky background, pipes, bird, eye, and UI text onto the back buffer.
- `pygame.display.update()` performs buffer flipping to render the frame cleanly on screen without tearing.

---

## Controls

| Key | Action | Context |
| :--- | :--- | :--- |
| **`Space`** | Flap / Jump | In-game |
| **`R`** | Restart Game | On Game Over screen |
| **`Close (X)`** | Exit Game | Any time |

---

## Installation and How to Run

### Prerequisites
- Python 3.8+ installed on your system.

### Running Locally
1. **Clone the repository:**
   ```bash
   git clone https://github.com/HABIBI-001-10/Flappy-bird.git
   cd Flappy-bird
   ```

2. **Create and activate a virtual environment (recommended):**
   - **Windows:**
     ```powershell
     python -m venv venv
     .\venv\Scripts\activate
     ```
   - **macOS / Linux:**
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the game:**
   ```bash
   python app.py
   ```

---

## Optional: Untracking `venv` from Git

If your `venv/` folder was accidentally committed to your GitHub repository, you can remove it from Git while keeping it on your local computer:

```bash
git rm -r --cached venv
git commit -m "Remove venv from git tracking"
git push origin main
```

---

## Future Enhancements
- [ ] Add sound effects for jumping, scoring, and collisions.
- [ ] Implement persistent high score tracking using a local file or `sqlite3`.
- [ ] Add sprite animations for the bird and textured pipes.
- [ ] Add parallax scrolling background clouds and ground tiles.
