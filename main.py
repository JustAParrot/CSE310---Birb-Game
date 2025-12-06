import arcade
import random
import math

# --- Screen Constants ---
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 700
SCREEN_TITLE = "Happy Flappy Duck - CSE310 :D"

# --- Physics ---
GRAVITY = -0.35
FLAP_STRENGTH = 7.5
MAX_FALL_SPEED = -10

# --- Pipes ---
BASE_PIPE_SPEED = 3
PIPE_WIDTH = 70
BASE_PIPE_GAP = 150
PIPE_SCALE = 0.25

BIRD_SCALE = 1.0

# --- Background ---
CLOUD_SPEED = 0.5


class GameState:
    START = "START"
    PLAYING = "PLAYING"
    GAME_OVER = "GAME_OVER"


class FlappyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Birb Game")
        arcade.set_background_color(arcade.color.SKY_BLUE)

        # --- Sounds ---
        self.flap_sound = arcade.load_sound("sounds/flap.wav")
        self.hit_sound = arcade.load_sound("sounds/hit.wav")
        self.point_sound = arcade.load_sound("sounds/point.wav")

        # --- Sprites ---
        self.all_sprites = arcade.SpriteList()
        self.pipes = arcade.SpriteList()

        self.bird = arcade.Sprite("sprites/bird.png", BIRD_SCALE)
        self.bird.center_x = SCREEN_WIDTH * 0.3
        self.bird.center_y = SCREEN_HEIGHT / 2
        self.all_sprites.append(self.bird)

        # Bird physics
        self.bird_velocity = 0

        # Game state
        self.state = GameState.START
        self.score = 0

        # Animation time 
        self.anim_time = 0.0

        # Background scrolling
        self.bg_offset = 0.0

        # Create initial pipes
        self.create_pipe_pair(SCREEN_WIDTH + 200)
        self.create_pipe_pair(SCREEN_WIDTH + 500)

    # -----------------------------
    # DIFFICULTY HELPERS
    # -----------------------------
    def get_current_gap(self):
        gap = BASE_PIPE_GAP - self.score * 5
        return max(gap, 110)

    def get_current_pipe_speed(self):
        speed = BASE_PIPE_SPEED + self.score * 0.2
        return min(speed, 8)

    # -----------------------------
    # PIPE CREATION
    # -----------------------------
    def create_pipe_pair(self, x_position):
        gap = self.get_current_gap()
        gap_y = random.randint(160, SCREEN_HEIGHT - 160)

        # ----------------------
        # BOTTOM PIPE
        # ----------------------
        bottom_pipe = arcade.Sprite("sprites/pipe_bottom.png", PIPE_SCALE)
        bottom_pipe.left = x_position

        bottom_pipe.top = gap_y - gap / 2

        bottom_pipe.is_bottom = True
        bottom_pipe.scored = False

        # ----------------------
        # TOP PIPE
        # ----------------------
        top_pipe = arcade.Sprite("sprites/pipe_top.png", PIPE_SCALE)
        top_pipe.left = x_position

        top_pipe.bottom = gap_y + gap / 2

        top_pipe.is_bottom = False

        # Add to lists
        self.pipes.append(bottom_pipe)
        self.pipes.append(top_pipe)

        self.all_sprites.append(bottom_pipe)
        self.all_sprites.append(top_pipe)


    # -----------------------------
    # RESET GAME
    # -----------------------------
    def reset_game(self):
        self.bird.center_y = SCREEN_HEIGHT / 2
        self.bird_velocity = 0

        self.pipes = arcade.SpriteList()
        self.all_sprites = arcade.SpriteList()
        self.all_sprites.append(self.bird)

        self.score = 0
        self.anim_time = 0

        self.create_pipe_pair(SCREEN_WIDTH + 200)
        self.create_pipe_pair(SCREEN_WIDTH + 500)

        self.state = GameState.START

    # -----------------------------
    # BACKGROUND DRAWING
    # -----------------------------
    def draw_background(self):
        arcade.draw_lrbt_rectangle_filled(
            0, SCREEN_WIDTH, 0, 80, arcade.color.DARK_SPRING_GREEN
)

        cloud_y = [SCREEN_HEIGHT - 150, SCREEN_HEIGHT - 220]
        for y in cloud_y:
            for i in range(3):
                x = (i * 300) - self.bg_offset
                arcade.draw_ellipse_filled(x, y, 120, 60, arcade.color.WHITE_SMOKE)
                arcade.draw_ellipse_filled(x + 40, y + 10, 90, 50, arcade.color.WHITE)

    # -----------------------------
    # DRAW LOOP
    # -----------------------------
    def on_draw(self):
        self.clear()

        self.draw_background()
        self.all_sprites.draw()

        arcade.draw_text(
            f"Score: {self.score}", 20, SCREEN_HEIGHT - 40,
            arcade.color.WHITE, 22
        )

        if self.state == GameState.START:
            arcade.draw_text(
                "Happy Flappy Duck :D",
                SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 40,
                arcade.color.WHITE, 40, anchor_x="center"
            )
            arcade.draw_text(
                "Press SPACE to Start",
                SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 10,
                arcade.color.YELLOW, 24, anchor_x="center"
            )

        elif self.state == GameState.GAME_OVER:
            arcade.draw_text(
                "GAME OVER :(",
                SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 40,
                arcade.color.RED, 40, anchor_x="center"
            )
            arcade.draw_text(
                "Press SPACE to Restart",
                SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 10,
                arcade.color.WHITE, 24, anchor_x="center"
            )

    # -----------------------------
    # UPDATE LOOP
    # -----------------------------
    def on_update(self, delta_time):
        self.anim_time += delta_time
        self.bg_offset = (self.bg_offset + CLOUD_SPEED) % SCREEN_WIDTH

        if self.state == GameState.START:
            self.bird.center_y = SCREEN_HEIGHT / 2 + 10 * math.sin(self.anim_time * 2)
            return

        if self.state == GameState.GAME_OVER:
            return

        # Bird physics
        self.bird_velocity += GRAVITY
        self.bird_velocity = max(self.bird_velocity, MAX_FALL_SPEED)
        self.bird.center_y += self.bird_velocity

        # Ground collision
        if self.bird.center_y < 80:
            self.bird.center_y = 80
            arcade.play_sound(self.hit_sound)
            self.state = GameState.GAME_OVER
            return

        # Ceiling clamp
        if self.bird.center_y > SCREEN_HEIGHT:
            self.bird.center_y = SCREEN_HEIGHT

        # Move pipes
        speed = self.get_current_pipe_speed()
        for pipe in self.pipes:
            pipe.center_x -= speed

        # Scoring & recycling
        for pipe in list(self.pipes):
            if getattr(pipe, "is_bottom", False) and not pipe.scored:
                if pipe.center_x + PIPE_WIDTH / 2 < self.bird.center_x:
                    pipe.scored = True
                    self.score += 1
                    arcade.play_sound(self.point_sound)

            if pipe.center_x < -PIPE_WIDTH:
                self.pipes.remove(pipe)
                self.all_sprites.remove(pipe)

        while len(self.pipes) < 4:
            self.create_pipe_pair(SCREEN_WIDTH + 200)

        # Collision with pipes
        if self.bird.collides_with_list(self.pipes):
            arcade.play_sound(self.hit_sound)
            self.state = GameState.GAME_OVER

    # -----------------------------
    # INPUT
    # -----------------------------
    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            if self.state == GameState.START:
                self.state = GameState.PLAYING
                self.bird_velocity = 0

            elif self.state == GameState.PLAYING:
                self.bird_velocity = FLAP_STRENGTH
                arcade.play_sound(self.flap_sound)

            elif self.state == GameState.GAME_OVER:
                self.reset_game()


def main():
    FlappyGame()
    arcade.run()


if __name__ == "__main__":
    main()
