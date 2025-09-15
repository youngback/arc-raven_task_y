# phase_func/phase_feedback.py

from psychopy import core, event, visual # [추가] visual import
# [변경] create_labeled_grid_stim 함수를 import 합니다.
from draw.draw_labeled_grid import create_labeled_grid_stim 
from draw.draw_marker import draw_marker
from config import FRAME_FEEDBACK
from save_func.save_frame_log import save_frame_log

def phase_feedback(is_correct, choice_idx, layout, visual_opt, game_opt, trial_idx, save_directory):
    """
    phase_test에서 생성된 layout 정보를 받아 화면을 그리고 피드백을 제시합니다.
    (리팩토링됨: 모든 시각 객체를 미리 생성하여 성능 최적화)
    """
    win = visual_opt["win"]
    palette = visual_opt["color_palette"]
    label_opts = visual_opt["label_grid"]

    inp = layout["inp"]
    choices = layout["choices"]
    pos_left = layout["pos_left"]
    cell_i = layout["cell_i"]
    positions = layout["positions"]
    cell_sizes = layout["cell_sizes"]
    gw = layout["gw"]
    gh = layout["gh"]

    # ===================================================================
    # ✅ 1. 루프 시작 전: 모든 시각 객체를 '미리' 생성합니다.
    # ===================================================================
    
    # Input 그리드 객체 생성
    input_stimuli = create_labeled_grid_stim(win, inp, "Input", pos_left, cell_i, palette, label_opts)
    
    # 4개의 Choice 그리드 객체 생성
    choices_stimuli = []
    for i, (grid_data, pos) in enumerate(zip(choices, positions)):
        # phase_test에서 사용된 실제 셀 크기를 그대로 전달
        stim_list = create_labeled_grid_stim(win, grid_data, f"Choice {i+1}", pos, cell_sizes[i], palette, label_opts)
        choices_stimuli.append(stim_list)

    # 피드백 테두리(outline) 객체도 미리 생성
    outline_stim = None
    if choice_idx is not None and choice_idx >= 0:
        pad_frac = 0.06
        line_width = 6
        color = "#32CD32" if is_correct else "#FF4136" # 밝은 색상 사용
        
        outline_stim = visual.Rect(
            win,
            width=gw * (1 + pad_frac),
            height=gh * (1 + pad_frac),
            lineColor=color,
            lineWidth=line_width,
            fillColor=None,
            pos=positions[choice_idx] # 선택된 위치에 생성
        )
        
    # --- 피드백 루프 설정 ---
    clock = core.Clock(); clock.reset()
    frame_count = 0
    fb_time = float(game_opt.get("feedback_time", 1.0))
    frame_log = []

    while clock.getTime() < fb_time:
        # ===================================================================
        # ✅ 2. 루프 안: 미리 만든 객체들을 '그리기만' 합니다.
        # ===================================================================
        
        # Input 그리드 그리기
        for stim in input_stimuli:
            stim.draw()
            
        # Choice 그리드들 그리기
        for stim_list in choices_stimuli:
            for stim in stim_list:
                stim.draw()

        # 피드백 테두리 그리기
        if outline_stim:
            outline_stim.draw()

        # [기존 draw_labeled_grid 및 draw_outline 호출은 삭제되었습니다]

        if frame_count < FRAME_FEEDBACK:
            draw_marker(win)

        win.flip()

        frame_log.append({
            "frame": frame_count,
            "elapsed_time": clock.getTime()
        })

        if 'escape' in event.getKeys():
            break

        frame_count += 1

    save_frame_log(trial_idx, frame_log, save_directory, "feedback")