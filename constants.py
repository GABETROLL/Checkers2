ROWS = COLUMNS = 8
WIDTH = HEIGHT = 800
BLOCK_WIDTH = WIDTH // ROWS

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)
LIGHT_BLUE = (128, 128, 255)
LIGHT_YELLOW = (255, 255, 128)

FPS = 60

if __name__ == "__main__":
    d = {"piece": {"vm #0": ["captured #0"], "vm #1": ["captured #0", ["captured #1"]]}}
    valid_moves = []
    for piece in d:
        for vm in d[piece]:
            valid_moves.append(vm)
    print(valid_moves)
