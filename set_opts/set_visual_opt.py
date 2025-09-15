from psychopy import visual, event
from config import WIN_HEIGHT, WIN_WIDTH, DEFAULT_CELL_SIZE, MIN_CELL_SIZE

def set_visual_opt():

    visual_opt = {}

    visual_opt["win_size"] = (WIN_WIDTH, WIN_HEIGHT)

    visual_opt["win"] = visual.Window(
        size=visual_opt["win_size"],
        color="black",
        units="pix",
        fullscr=True,
    )

    visual_opt["color_palette"] = {
        0: "black", 1: "blue", 2: "green", 3: "yellow", 4: "red",
        5: "orange", 6: "magenta", 7: "cyan", 8: "white", 9: "gray"
    }

    visual_opt["label_grid"] = {
        # 그리드 본체 위쪽에서 레이블까지 띄울 거리: grid_height * offset_frac
        "offset_frac": 0.1,
        "height_frac": 0.05,
        "color": "white"
    }

    visual_opt["grid_width_frac"] = 0.45
    visual_opt["grid_height_frac"] = 0.8
    visual_opt["default_cell_size"] = DEFAULT_CELL_SIZE
    visual_opt["min_cell_size"] = MIN_CELL_SIZE
    visual_opt["scale"] = 1.0

    visual_opt["photodiode_box"] = {
        "size":  50,                                # 한 변 50px
        "pos":   (-WIN_WIDTH/2 + 30, WIN_HEIGHT/2 - 30),
        "color": "white"
    }

    return visual_opt
