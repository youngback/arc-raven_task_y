from psychopy import core, event

# --- ✅ 1. 적용: draw_outline 함수를 import 합니다. ---
from draw.draw_outline import draw_outline
from draw.draw_marker import draw_marker
from config import FRAME_FEEDBACK

def phase_feedback(is_correct, choice_idx, layout, visual_opt, game_opt, trial_idx, save_directory):
    win = visual_opt["win"]

    # --- 2. layout 정보 꺼내기 ---
    # phase_test가 전달해준 시각 객체와 크기 정보를 받습니다.
    input_stim = layout["input_stim"]
    choices_stim_list = layout["choices_stim_list"]
    choice_image_size = layout["choice_image_size"]

    # --- 피드백 루프 ---
    clock = core.Clock(); clock.reset()
    frame_count = 0
    fb_time = float(game_opt.get("feedback_time", 1.5))
    frame_log = []

    while clock.getTime() < fb_time:
        # --- 화면에 그리기 ---
        # 1. Input과 Choice 이미지들을 먼저 그립니다.
        input_stim.draw()
        for stim in choices_stim_list:
            stim.draw()

        # --- 3. 적용: draw_outline 함수를 호출하여 테두리를 그립니다. ---
        # 2. 사용자가 선택한 것이 있다면 (choice_idx is not None), 그 위에 테두리를 덧그립니다.
        if choice_idx is not None:
            draw_outline(
                win=win,
                pos=choices_stim_list[choice_idx].pos, # 선택된 이미지의 위치
                size=choice_image_size,                # 선택지 이미지의 크기
                is_correct=is_correct                  # 정답 여부
            )
        
        if frame_count < FRAME_FEEDBACK:
            draw_marker(win)

        win.flip()

        # 프레임 정보를 기록합니다.
        frame_log.append({
            "frame": frame_count,
            "elapsed_time": clock.getTime()
        })
        if 'escape' in event.getKeys(): break
        frame_count += 1
    
    return frame_log