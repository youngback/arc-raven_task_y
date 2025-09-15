# phase_func/phase_test.py
import os
from psychopy import visual, core, event
from draw.draw_labeled_grid import create_labeled_grid_stim, calc_grid_size, calc_grid_positions
from draw.draw_marker import draw_marker
from draw.draw_fixation import draw_fixation
from config import FRAME_TEST
from save_func.save_frame_log import save_frame_log_test

def phase_test(trial, visual_opt, device_opt, game_opt):
    win          = visual_opt["win"]
    palette      = visual_opt["color_palette"]
    label_opts   = visual_opt["label_grid"]
    win_w, win_h = visual_opt["win_size"]

    width_frac   = visual_opt["grid_width_frac"]
    height_frac  = visual_opt["grid_height_frac"]
    default_cell = visual_opt["default_cell_size"]
    scale        = visual_opt["scale"]

    label_of    = label_opts.get("offset_frac", 0.1)
    label_hf    = label_opts.get("height_frac", 0.05)
    effective_h = height_frac / (1 + label_of + label_hf)

    inp         = trial["test"]["input"]
    choices     = trial["test"]["choices"]
    correct_idx = trial["test"]["correct_idx"]

    ri, ci = len(inp), len(inp[0])
    cell_i, _, _ = calc_grid_size(ri, ci, width_frac, effective_h, default_cell, scale)
    pos_left  = (-win_w / 4, 0)

    rows, cols = len(choices[0]), len(choices[0][0])
    assert all(len(g)==rows and len(g[0])==cols for g in choices), "choices 크기가 서로 다릅니다."
    cell_c, gw, gh = calc_grid_size(rows, cols, width_frac / 2, effective_h, default_cell, scale)

    offset_right = (win_w / 4, 0)
    positions = calc_grid_positions(2, 2, gw, gh, cell_c, offset=offset_right)
    hitboxes = [visual.Rect(win, width=gw, height=gh, pos=pos, opacity=0.0) for pos in positions]

    # --- 시각 객체 미리 생성 ---
    input_stimuli = create_labeled_grid_stim(win, inp, "Input", pos_left, cell_i, palette, label_opts)
    choices_stimuli = []
    for i, grid_data in enumerate(choices):
        pos = positions[i]
        label = f"Choice {i+1}"
        stim_list = create_labeled_grid_stim(win, grid_data, label, pos, cell_c, palette, label_opts)
        choices_stimuli.append(stim_list)

    # --- 선택 루프 (프레임 기반) ---
    # [변경] 아이콘이 커서 역할을 하므로 기본 마우스는 숨김 처리
    mouse = event.Mouse(visible=True, win=win) 
    icon = visual.Circle(win, radius=10, units='pix', fillColor='red', lineColor='white')

    clock       = core.Clock(); clock.reset()
    frame_count = 0
    choice_idx  = None
    frame_log = []

    while choice_idx is None:
        mx, my = mouse.getPos()

        # --- 화면 그리기 ---
        for stim in input_stimuli:
            stim.draw()
        for stim_list in choices_stimuli:
            for stim in stim_list:
                stim.draw()

        if frame_count < FRAME_TEST:
            draw_marker(win)

        # --- 아이콘 위치 업데이트 및 그리기 ---
        icon.setPos((mx, my))
        icon.draw()

        win.flip()

        # [추가] 마우스 클릭 감지 로직
        if mouse.getPressed()[0]: # 왼쪽 마우스 버튼이 클릭되었는지 확인
            for i, hb in enumerate(hitboxes):
                if hb.contains((mx, my)):
                    choice_idx = i
                    rt = clock.getTime()
                    break # 선택이 확정되면 더 이상 확인할 필요 없으므로 중단
        
        # --- 로그 및 종료 처리 ---
        frame_log.append({
            "frame": frame_count,
            "elapsed_time": clock.getTime(),
            "icon_x": mx, "icon_y": my,
        })
        
        if 'escape' in event.getKeys():
            choice_idx = -1
            rt = clock.getTime()
            break

        frame_count += 1

        if 'escape' in event.getKeys():
            core.quit()

    # --- 결과 저장 (이하 동일) ---
    layout = {
        "inp": inp, "choices": choices,
        "pos_left": pos_left, "cell_i": cell_i, "positions": positions,
        "cell_sizes": [cell_c] * len(choices), "gw": gw, "gh": gh,
        "correct_idx": correct_idx,
    }
    trial_idx  = trial.get("trial_idx", 0)
    item_id    = trial.get("item_id", "")
    subject_id = trial.get("subject_id", "")
    save_dir   = trial.get("save_dir", os.path.join("logs", "test"))
    save_frame_log_test(
        trial_idx=trial_idx, correct_idx=correct_idx, chosen_idx=choice_idx,
        is_correct=(choice_idx == correct_idx), rt=rt, frame_log=frame_log,
        save_dir=save_dir, subject_id=subject_id, item_id=item_id
    )
    return choice_idx, rt, layout, frame_log