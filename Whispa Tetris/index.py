import pygame
import random
import time
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

pygame.init()

#COLORS
PURPLE_DARK_SCREEN = (0, 0, 0)
PURPLE_LIGHT_PLAYFIELD = (20, 20, 40)
PURPLE_GRID = (30, 50, 70)  # Grid Lines
PURPLE_ACCENT_PINK = (255, 105, 180)#BORDER
PURPLE_GRADIENT_END = (5, 0, 15) #Sa playfield

WHITE = (255, 255, 255)
RED_GAME_OVER = (255, 50, 50)
BLACK = (0, 0, 0)

# Colors ng Blocks
COLOR_MAP = [
    (255, 105, 180),  # T Pink
    (0, 200, 255),  # I Cyan
    (255, 180, 0),  # L Orange
    (100, 255, 100),  # S Lime Green
    (255, 255, 0),  # O Yellow
    (150, 0, 255),  # J Violet
    (255, 50, 150)  # Z Dark Pink
]
SHAPE_COLORS = {i: COLOR_MAP[i % len(COLOR_MAP)] for i in range(len(COLOR_MAP))}

# Grids and screens
GRID_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20
PLAYFIELD_WIDTH = GRID_WIDTH * GRID_SIZE
PLAYFIELD_HEIGHT = GRID_HEIGHT * GRID_SIZE
SIDE_PANEL_WIDTH = 200
WIDTH = PLAYFIELD_WIDTH + 2 * SIDE_PANEL_WIDTH
HEIGHT = PLAYFIELD_HEIGHT

# Shaping ng blocks
SHAPES_RAW = [
    # I (Index 0)
    [['.....', '.....', 'OOOO.', '.....', '.....'],
     ['..O..', '..O..', '..O..', '..O..', '.....']],
    # T Tetromino (Index 1) - Custom rotation order
    [['.....', '..O..', '.OOO.', '.....', '.....'],
     ['..O..', '..OO.', '..O..', '.....', '.....'],
     ['.....', '.OOO.', '..O..', '.....', '.....'],
     ['..O..', '.OO..', '..O..', '.....', '.....']] ,
    # L (Index 2)
    [['.....', '...O.', '.OOO.', '.....', '.....'],
     ['..O..', '..O..', '..OO.', '.....', '.....'],
     ['.....', '.OOO.', '.O...', '.....', '.....'],
     ['.OO..', '..O..', '..O..', '.....', '.....']],
    # J (Index 3)
    [['.....', '.O...', '.OOO.', '.....', '.....'],
     ['..OO.', '..O..', '..O..', '.....', '.....'],
     ['.....', '.OOO.', '...O.', '.....', '.....'],
     ['..O..', '..O..', '.OO..', '.....', '.....']],
    # S (Index 4)
    [['.....', '..OO.', '.OO..', '.....', '.....'],
     ['.O...', '.OO..', '..O..', '.....', '.....']],
    # Z (Index 5)
    [['.....', '.OO..', '..OO.', '.....', '.....'],
     ['..O..', '.OO..', '.O...', '.....', '.....']],
    # O (Index 6)
    [['.....', '..OO.', '..OO.', '.....', '.....']]
]


class Tetromino:
    def __init__(self, x, y, shape_index):
        self.x = x
        self.y = y
        self.shape_index = shape_index
        self.shape = SHAPES_RAW[shape_index]
        self.color = SHAPE_COLORS[shape_index]
        self.rotation = 0


class Tetris:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[PURPLE_DARK_SCREEN for _ in range(width)] for _ in range(height)]

        # Game State
        self.game_over = False
        self.score = 0
        self.lines_cleared = 0
        self.held_piece_index = None
        self.can_hold = True
        self.line_clear_flash_time = 0

        # Piece Management
        self.next_piece_index = random.randint(0, len(SHAPES_RAW) - 1)
        self.current_piece = self._new_piece_from_next()

    def _new_piece_from_next(self):
        #create piece n generate new piece
        current_index = self.next_piece_index
        new_piece = Tetromino(self.width // 2 - 2, 0, current_index)
        self.next_piece_index = random.randint(0, len(SHAPES_RAW) - 1)
        return new_piece

    def new_piece(self):
        #Used when a piece is locked
        return self._new_piece_from_next()

    # check if the piece can move sa offset
    def valid_move(self, piece, x_offset, y_offset, rotation_offset):

        # Calculate the new rotation
        new_rotation = (piece.rotation + rotation_offset) % len(piece.shape)
        new_shape = piece.shape[new_rotation]

        for i, row in enumerate(new_shape):
            for j, cell in enumerate(row):
                if cell == 'O':
                    new_x = piece.x + j + x_offset
                    new_y = piece.y + i + y_offset

                    # Check boundaries
                    if new_x < 0 or new_x >= self.width or new_y >= self.height:
                        return False

                    # Check for collision with the locked grid
                    # Only check grid cells if y is within bounds (prevents error when piece is high up)
                    if new_y >= 0 and self.grid[new_y][new_x] != PURPLE_DARK_SCREEN:
                        return False
        return True

    # Calculates the lowest valid y-coordinate for the current piece.
    def _get_ghost_y(self, piece):
        y = piece.y
        for _ in range(self.height + 1):
            if self.valid_move(piece, 0, y + 1 - piece.y, 0):
                y += 1
            else:
                break
        return y

    def get_level(self):
        #Calculates the current level based on lines cleared.
        if self.lines_cleared < 5:
            return 1
        else:
            return (self.lines_cleared - 5) // 10 + 2

    def get_fall_speed(self):
        #Calculates the fall speed in milliseconds based on level.
        level = self.get_level()
        speed = max(50, 250 - (level - 1) * 70)
        return speed

    def clear_lines(self):
        full_rows = 0
        new_grid = []

        # if there is background color, row is not full
        for i, row in enumerate(self.grid):
            if PURPLE_DARK_SCREEN in row:
                new_grid.append(row)
            else:
                full_rows += 1

        # Add new empty rows to the top
        for _ in range(full_rows):
            new_grid.insert(0, [PURPLE_DARK_SCREEN for _ in range(self.width)])

        self.grid = new_grid

        if full_rows > 0:
            self.line_clear_flash_time = time.time()

        return full_rows

    def lock_piece(self, piece):
        #lock piece, clear lines, udpate score, spawn new piece
        current_shape = piece.shape[piece.rotation % len(piece.shape)]

        for i, row in enumerate(current_shape):
            for j, cell in enumerate(row):
                if cell == 'O':
                    lock_y = piece.y + i
                    lock_x = piece.x + j

                    # Check for game over (locking above the visible field)
                    if lock_y < 0:
                        self.game_over = True
                        return

                    self.grid[lock_y][lock_x] = piece.color

        self.can_hold = True

        lines_cleared = self.clear_lines()
        self.lines_cleared += lines_cleared

        current_level = self.get_level()
        #scoring
        if lines_cleared == 1:
            self.score += 100 * current_level
        elif lines_cleared == 2:
            self.score += 300 * current_level
        elif lines_cleared == 3:
            self.score += 500 * current_level
        elif lines_cleared == 4:
            self.score += 800 * current_level

        self.current_piece = self.new_piece()

        # Check for immediate game over on spawn
        if not self.valid_move(self.current_piece, 0, 0, 0):
            self.game_over = True

    def hold_piece(self):
        # hold (c) - swapping piece
        if not self.can_hold:
            return

        current_index = self.current_piece.shape_index

        if self.held_piece_index is None:
            self.held_piece_index = current_index
            self.current_piece = self.new_piece()
        else:
            temp_held_index = self.held_piece_index
            self.held_piece_index = current_index
            # Spawn the held piece at the top center
            self.current_piece = Tetromino(self.width // 2 - 2, 0, temp_held_index)

        self.can_hold = False

    def update(self):
        # move piece down automatically
        if not self.game_over:
            if self.valid_move(self.current_piece, 0, 1, 0):
                self.current_piece.y += 1
            else:
                self.lock_piece(self.current_piece)

    def draw_block(self, screen, x, y, color):
        # ui design for drawing blocks
        block_rect = pygame.Rect(x, y, GRID_SIZE - 1, GRID_SIZE - 1)

        # 1. Main Block (Darker base)
        r, g, b = color
        darker_color = (max(0, r - 50), max(0, g - 50), max(0, b - 50))
        pygame.draw.rect(screen, darker_color, block_rect, border_radius=4)

        # 2. Inner Highlight (Main color)
        inner_rect = pygame.Rect(x + 1, y + 1, GRID_SIZE - 3, GRID_SIZE - 3)
        pygame.draw.rect(screen, color, inner_rect, border_radius=3)

        # 3. Top-Left Light Edge
        light_color = (min(255, r + 50), min(255, g + 50), min(255, b + 50))
        pygame.draw.circle(screen, light_color, (x + 3, y + 3), 1)

        # 4. Subtle Shadow
        pygame.draw.rect(screen, BLACK, block_rect, 1, border_radius=4)

    def draw_playfield_gradient(self, screen, rect):
        #drawing playfield
        color_start = PURPLE_LIGHT_PLAYFIELD
        color_end = PURPLE_GRADIENT_END

        r1, g1, b1 = color_start
        r2, g2, b2 = color_end
        h = rect.height

        for i in range(h):
            r = r1 + (r2 - r1) * i // h
            g = g1 + (g2 - g1) * i // h
            b = b1 + (b2 - b1) * i // h

            line_color = (r, g, b)
            pygame.draw.line(screen, line_color, (rect.x, rect.y + i), (rect.right, rect.y + i))

    def draw(self, screen, x_offset, y_offset):
        #drawing grid, ghost piece, current piece

        # grid
        playfield_rect = pygame.Rect(x_offset, y_offset, PLAYFIELD_WIDTH, PLAYFIELD_HEIGHT)
        self.draw_playfield_gradient(screen, playfield_rect)

        # line clear effect
        flash_duration = 0.1
        if self.line_clear_flash_time and time.time() - self.line_clear_flash_time < flash_duration:
            flash_surface = pygame.Surface((PLAYFIELD_WIDTH, PLAYFIELD_HEIGHT), pygame.SRCALPHA)
            flash_surface.fill((255, 255, 255, 100))
            screen.blit(flash_surface, (x_offset, y_offset))
        else:
            self.line_clear_flash_time = 0

        # Draw locked grid
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if cell != PURPLE_DARK_SCREEN:
                    self.draw_block(screen, x_offset + x * GRID_SIZE, y_offset + y * GRID_SIZE, cell)

        # Draw the grid lines
        for x in range(self.width):
            pygame.draw.line(screen, PURPLE_GRID,
                             (x_offset + x * GRID_SIZE, y_offset),
                             (x_offset + x * GRID_SIZE, y_offset + self.height * GRID_SIZE), 1)
        for y in range(self.height):
            pygame.draw.line(screen, PURPLE_GRID,
                             (x_offset, y_offset + y * GRID_SIZE),
                             (x_offset + self.width * GRID_SIZE, y_offset + y * GRID_SIZE), 1)

        if self.current_piece and not self.game_over:
            # ghost piece
            ghost_y = self._get_ghost_y(self.current_piece)
            current_shape = self.current_piece.shape[self.current_piece.rotation % len(self.current_piece.shape)]

            ghost_color = self.current_piece.color

            for i, row in enumerate(current_shape):
                for j, cell in enumerate(row):
                    if cell == 'O':
                        x_coord = x_offset + (self.current_piece.x + j) * GRID_SIZE
                        y_coord = y_offset + (ghost_y + i) * GRID_SIZE

                        if y_coord >= y_offset:
                            # Draw simple outline for ghost
                            pygame.draw.rect(screen, ghost_color,
                                             (x_coord, y_coord, GRID_SIZE - 1, GRID_SIZE - 1), 2, border_radius=4)
                            # Draw inner X
                            pygame.draw.line(screen, ghost_color, (x_coord + 5, y_coord + 5),
                                             (x_coord + GRID_SIZE - 6, y_coord + GRID_SIZE - 6), 1)
                            pygame.draw.line(screen, ghost_color, (x_coord + GRID_SIZE - 6, y_coord + 5),
                                             (x_coord + 5, y_coord + GRID_SIZE - 6), 1)

            # current piece
            for i, row in enumerate(current_shape):
                for j, cell in enumerate(row):
                    if cell == 'O':
                        x_coord = x_offset + (self.current_piece.x + j) * GRID_SIZE
                        y_coord = y_offset + (self.current_piece.y + i) * GRID_SIZE

                        if y_coord >= y_offset:
                            self.draw_block(screen, x_coord, y_coord, self.current_piece.color)


#global drawing functions
PREVIEW_PANEL_WIDTH = 150
PREVIEW_PANEL_HEIGHT = 110


def draw_info_panel(screen, game, side_x, side_y, title, piece_index):
    #draw hold/next panel

    panel_rect = pygame.Rect(side_x, side_y, PREVIEW_PANEL_WIDTH, PREVIEW_PANEL_HEIGHT)

    # 1. Background (Solid Black)
    pygame.draw.rect(screen, BLACK, panel_rect, border_radius=8)

    # 2. Clean, thick border (Pink)
    pygame.draw.rect(screen, PURPLE_ACCENT_PINK, panel_rect, 4, border_radius=8)

    # 3. Title Text (White on black for high visibility)
    font_title = pygame.font.Font(None, 30)
    text_title = font_title.render(title, True, WHITE)

    # Center the title horizontally
    title_x = side_x + (PREVIEW_PANEL_WIDTH - text_title.get_width()) // 2
    screen.blit(text_title, (title_x, side_y + 8))

    if piece_index is not None:
        piece_color = SHAPE_COLORS[piece_index]
        piece_shape = SHAPES_RAW[piece_index][0]

        preview_grid_size = 18

        # Calculate centering for the piece inside the box
        offset_x = side_x + 30
        offset_y = side_y + 35

        for i, row in enumerate(piece_shape):
            for j, cell in enumerate(row):
                if cell == 'O':
                    block_x = offset_x + j * preview_grid_size
                    block_y = offset_y + i * preview_grid_size

                    # Draw a simplified block for preview
                    block_rect = pygame.Rect(block_x, block_y, preview_grid_size - 1, preview_grid_size - 1)
                    pygame.draw.rect(screen, piece_color, block_rect, border_radius=2)


def draw_text_with_shadow(screen, text, font, color, shadow_color, x, y):
    text_shadow = font.render(text, True, shadow_color)
    screen.blit(text_shadow, (x + 1, y + 1))

    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))


def draw_score(screen, game, x, y):
#draw score, lines and level

    panel_width = 160
    panel_height = 280
    panel_rect = pygame.Rect(x, y, panel_width, panel_height)

    # 1. Outer Border and Background
    pygame.draw.rect(screen, BLACK, panel_rect, border_radius=8)
    pygame.draw.rect(screen, PURPLE_ACCENT_PINK, panel_rect, 4, border_radius=8)

    font_label = pygame.font.Font(None, 28)
    font_value = pygame.font.Font(None, 60)

    shadow_color = (10, 10, 10)

    #Draw all 3 sections (Level, Score, Lines)
    sections = [
        ("LEVEL", f"{game.get_level()}"),
        ("SCORE", f"{game.score}"),
        ("LINES", f"{game.lines_cleared}"),
    ]

    padding = 20
    line_thickness = 2

    for i, (label, value) in enumerate(sections):

        label_surf = font_label.render(label, True, PURPLE_ACCENT_PINK)
        label_x = x + (panel_width - label_surf.get_width()) // 2
        screen.blit(label_surf, (label_x, y + padding))

        padding += 25

        value_surf = font_value.render(value, True, WHITE)
        value_x = x + (panel_width - value_surf.get_width()) // 2
        draw_text_with_shadow(screen, value, font_value, WHITE, shadow_color, value_x, y + padding)

        padding += 60

        if i < len(sections) - 1:
            divider_y = y + padding
            pygame.draw.line(screen, PURPLE_ACCENT_PINK, (x + 15, divider_y), (x + panel_width - 15, divider_y),
                             line_thickness)
            padding += 10  # Extra spacing after divider


def draw_game_over(screen):
    center_x = WIDTH // 2
    center_y = HEIGHT // 2

    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((255, 105, 180, 50))
    screen.blit(overlay, (0, 0))

    container_width = 600
    container_height = 240
    container_x = center_x - container_width // 2
    container_y = center_y - container_height // 2

    pygame.draw.rect(screen, (0, 0, 0, 200), (container_x, container_y, container_width, container_height),
                     border_radius=20)
    pygame.draw.rect(screen, RED_GAME_OVER, (container_x, container_y, container_width, container_height), 5,
                     border_radius=20)

    font_large = pygame.font.Font(None, 100)
    font_small = pygame.font.Font(None, 40)

    # GAME OVER Text
    text_over = font_large.render("GAME OVER", True, RED_GAME_OVER)
    text_rect = text_over.get_rect(center=(center_x, center_y - 40))
    screen.blit(text_over, text_rect)

    # Restart Text
    restart_text = font_small.render("Press any key to restart", True, WHITE)
    restart_rect = restart_text.get_rect(center=(center_x, center_y + 40))
    screen.blit(restart_text, restart_rect)


def draw_pause_screen(screen):
    center_x = WIDTH // 2
    center_y = HEIGHT // 2

    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))
    screen.blit(overlay, (0, 0))

    font_large = pygame.font.Font(None, 120)
    font_small = pygame.font.Font(None, 40)

    text_paused = font_large.render("PAUSED", True, PURPLE_ACCENT_PINK)
    text_rect = text_paused.get_rect(center=(center_x, center_y - 30))

    draw_text_with_shadow(screen, "PAUSED", font_large, PURPLE_ACCENT_PINK, BLACK, text_rect.x, text_rect.y)

    text_instruction = font_small.render("Press P to Resume", True, WHITE)
    instruction_rect = text_instruction.get_rect(center=(center_x, center_y + 50))
    screen.blit(text_instruction, instruction_rect)


# main game loop
def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Whispa Tetris')
    clock = pygame.time.Clock()
    game = Tetris(GRID_WIDTH, GRID_HEIGHT)

    fall_time = 0
    fall_speed_soft_drop = 50

    DAS_DELAY = 200
    ARR_RATE = 40
    horizontal_move_time = 0
    key_pressed_time = 0
    current_key = None

    paused = False

    PLAYFIELD_X = SIDE_PANEL_WIDTH
    PLAYFIELD_Y = 0

    LEFT_PANEL_X = 25
    RIGHT_PANEL_X = PLAYFIELD_X + PLAYFIELD_WIDTH + 25

    SCORE_PANEL_Y = HEIGHT - 280 - 20

    while True:
        fall_speed_base = game.get_fall_speed()
        fall_speed_current = fall_speed_base

        # event handlers
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                # Global handlers (Restart, Pause)
                if game.game_over:
                    game = Tetris(GRID_WIDTH, GRID_HEIGHT)
                    paused = False
                    fall_time = 0
                    current_key = None
                    key_pressed_time = 0
                    horizontal_move_time = 0
                    continue

                if event.key == pygame.K_p:
                    paused = not paused
                    horizontal_move_time = pygame.time.get_ticks()
                    continue

                if not game.game_over and not paused:
                    if event.key == pygame.K_UP:
                        if game.valid_move(game.current_piece, 0, 0, 1):
                            game.current_piece.rotation = (game.current_piece.rotation + 1) % len(
                                game.current_piece.shape)
                        else:
                            wall_kicks = [
                                (-1, 0),
                                (1, 0),
                                (-2, 0),
                                (2, 0),
                                (0, -1)
                            ]

                            next_rotation = (game.current_piece.rotation + 1) % len(game.current_piece.shape)
                            kick_successful = False

                            for dx, dy in wall_kicks:
                                if game.valid_move(game.current_piece, dx, dy, 1):
                                    game.current_piece.rotation = next_rotation
                                    game.current_piece.x += dx
                                    game.current_piece.y += dy
                                    kick_successful = True
                                    break

                    elif event.key == pygame.K_SPACE:
                        # Hard Drop
                        while game.valid_move(game.current_piece, 0, 1, 0):
                            game.current_piece.y += 1
                        game.lock_piece(game.current_piece)
                        fall_time = 0
                    elif event.key == pygame.K_c:
                        # Hold piece
                        game.hold_piece()

                    elif event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        direction = -1 if event.key == pygame.K_LEFT else 1

                        if game.valid_move(game.current_piece, direction, 0, 0):
                            game.current_piece.x += direction

                        if current_key != event.key:
                            current_key = event.key
                            key_pressed_time = pygame.time.get_ticks()
                            horizontal_move_time = key_pressed_time

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    if event.key == current_key:
                        current_key = None
                        key_pressed_time = 0
                        horizontal_move_time = 0

        keys = pygame.key.get_pressed()

        # speed check, running while not paused
        if not game.game_over and not paused and keys[pygame.K_DOWN]:
            fall_speed_current = fall_speed_soft_drop
        else:
            fall_speed_current = fall_speed_base

        if not game.game_over and not paused:
            current_time = pygame.time.get_ticks()

            if current_key is not None:
                if current_time - key_pressed_time >= DAS_DELAY:
                    if current_time - horizontal_move_time >= ARR_RATE:

                        direction = -1 if current_key == pygame.K_LEFT else 1

                        if game.valid_move(game.current_piece, direction, 0, 0):
                            game.current_piece.x += direction
                            horizontal_move_time = current_time


            delta_time = clock.get_rawtime()
            fall_time += delta_time

            if fall_time >= fall_speed_current:
                game.update()
                fall_time = 0

        # drawing
        screen.fill(PURPLE_DARK_SCREEN)

        pygame.draw.rect(screen, PURPLE_ACCENT_PINK,
                         (PLAYFIELD_X - 5, PLAYFIELD_Y - 5, PLAYFIELD_WIDTH + 10, PLAYFIELD_HEIGHT + 10), 5,
                         border_radius=15)

        # Draw the game elements
        game.draw(screen, PLAYFIELD_X, PLAYFIELD_Y)

        draw_info_panel(screen, game, LEFT_PANEL_X, 20, "HOLD (C)", game.held_piece_index)

        draw_info_panel(screen, game, RIGHT_PANEL_X, 20, "NEXT", game.next_piece_index)

        draw_score(screen, game, RIGHT_PANEL_X, SCORE_PANEL_Y)

        # pause and game over screen
        if paused and not game.game_over:
            draw_pause_screen(screen)

        if game.game_over:
            draw_game_over(screen)

        font_small = pygame.font.Font(None, 28)
        esc_text = font_small.render("Press ESC to exit", True, WHITE)
        screen.blit(esc_text, (LEFT_PANEL_X, HEIGHT - 40))

        pygame.display.flip()

        clock.tick(60)


if __name__ == "__main__":
    main()