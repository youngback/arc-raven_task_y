# phases/phase_training.py

import os
from psychopy import visual, core, event
# [변경] create_labeled_grid_stim 함수를 import 합니다.
from draw.draw_labeled_grid import create_labeled_grid_stim, calc_grid_size
from draw.draw_marker import draw_marker
from config import FRAME_TRAIN
from save_func.save_frame_log import save_frame_log_train

def phase_training(train_event, visual_opt, device_opt, game_opt):
    input_grid  = train_event["input"]
    output_grid = train_event["output"]

    win          = visual_opt["win"]
    palette      = visual_opt["color_palette"]
    label_opts   = visual_opt["label_grid"]
    win_w, win_h = visual_opt["win_size"]
    width_frac   = visual_opt["grid_width_frac"]
    height_frac  = visual_opt["grid_height_frac"]
    default_cell = visual_opt["default_cell_size"]
    scale        = visual_opt["scale"]

    ri, ci = len(input_grid),  len(input_grid[0])
    ro, co = len(output_grid), len(output_grid[0])

    label_of = label_opts["offset_frac"]
    label_hf = label_opts["height_frac"]
    effective_h = height_frac / (1 + label_of + label_hf)

    # [변경] phase_test와 동일하게 너비 계산 방식을 맞추어 일관성을 유지합니다.
    cell_i, _, _ = calc_grid_size(ri, ci, width_frac, effective_h, default_cell, scale)
    cell_o, _, _ = calc_grid_size(ro, co, width_frac, effective_h, default_cell, scale)

    pos_left  = (-win_w / 4, 0)
    pos_right = (win_w / 4, 0)

    # ===================================================================
    # ✅ 1. 루프 시작 전: 모든 시각 객체를 '미리' 생성합니다.
    # ===================================================================
    input_stimuli = create_labeled_grid_stim(win, input_grid, "Input", pos_left, cell_i, palette, label_opts)
    output_stimuli = create_labeled_grid_stim(win, output_grid, "Output", pos_right, cell_o, palette, label_opts)

    # --- 루프 설정 ---
    frame_log = []
    clock = core.Clock(); clock.reset()
    duration = float(game_opt["training_display_time"])
    
    # [추가] 마우스 아이콘을 추가하고, 기본 커서를 숨깁니다.
    mouse = event.Mouse(visible=True)
    icon = visual.Circle(win, radius=10, units='pix', fillColor='red', lineColor='white')
    
    frame_count = 0
    while clock.getTime() < duration:
        t0 = clock.getTime()
        
        # ===================================================================
        # ✅ 2. 루프 안: 미리 만든 객체들을 '그리기만' 합니다.
        # ===================================================================
        for stim in input_stimuli:
            stim.draw()
            
        for stim in output_stimuli:
            stim.draw()

        # [기존 create_labeled_grid_stim 호출 부분은 삭제되었습니다]

        if frame_count < FRAME_TRAIN:
            draw_marker(win)
        
        # [추가] 마우스 아이콘 위치를 업데이트하고 그립니다.
        mouse_x, mouse_y = mouse.getPos()
        icon.setPos((mouse_x, mouse_y))
        icon.draw()

        win.flip()

        # --- 로그 기록 ---
        frame_log.append({
            "frame": frame_count,
            "elapsed_time": t0,
            "icon_x": mouse_x,
            "icon_y": mouse_y,
        })
        frame_count += 1

    # --- CSV 저장 (이하 동일) ---
    trial_idx  = train_event.get("trial_idx", game_opt.get("trial_idx", 0))
    item_id    = train_event.get("item_id",  game_opt.get("item_id", ""))
    subject_id = game_opt.get("subject_id", "")
    save_dir   = game_opt.get("save_dir", os.path.join("logs", "train"))

    save_frame_log_train(
        trial_idx=trial_idx,
        frame_log=frame_log,
        save_dir=save_dir,
        subject_id=subject_id,
        item_id=item_id,
        phase="train"
    )
    
    return frame_log