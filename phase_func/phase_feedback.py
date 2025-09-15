from psychopy import core, event

# --- ✅ 1. 적용: draw_outline 함수를 import 합니다. ---
from draw.draw_outline import draw_outline
from draw.draw_marker import draw_marker
from config import FRAME_FEEDBACK, FRAME_DT
from save_func.save_frame_log import save_frame_log 

def phase_feedback(is_correct, choice_idx, layout, visual_opt, game_opt, trial_idx, save_directory, global_clock=None, global_frame_log=None):
    win = visual_opt["win"]

    # --- 2. layout 정보 꺼내기 ---
    # phase_test가 전달해준 시각 객체와 크기 정보를 받습니다.
    input_stim = layout["input_stim"]
    choices_stim_list = layout["choices_stim_list"]
    choice_image_size = layout["choice_image_size"]

    # --- 피드백 루프 ---
    clock = core.Clock(); clock.reset()
    frame_count = 0
    duration = float(game_opt.get("feedback_time", 1.5))
    frame_log = []

    while clock.getTime() < duration:
        t0 = clock.getTime()
        
        # --- draw ---
        input_stim.draw()
        for stim in choices_stim_list:
            stim.draw()

        if choice_idx is not None:
            draw_outline(
                win=win,
                pos=choices_stim_list[choice_idx].pos,
                size=choice_image_size,
                is_correct=is_correct
            )

        if frame_count < FRAME_FEEDBACK:
            draw_marker(win)

        # 1) flip
        win.flip()

        if global_clock is not None and global_frame_log is not None:
            frame_abs = len(global_frame_log) + 1
            global_frame_log.append({
                "frame_abs": frame_abs,
                "time_abs": global_clock.getTime()
            })
        t1 = clock.getTime()  # flip 직후(선택: 품질 로그용)

        # 2) 로그(flip 직후가 타이밍상 가장 정확)
        frame_log.append({
            "frame": frame_count,
            "elapsed_time": t0,
            "t_frame_start": t0,
            "t_post_flip": t1,           # 선택 필드지만 강추
            "dt_draw_flip": t1 - t0,     # 선택 필드지만 강추
        })

        # 3) ESC 처리(있으면 해당 프레임도 1/60 채우고 종료)
        if 'escape' in event.getKeys():
            # 잔여시간 채우기
            i = 0
            while (clock.getTime() - t0) < FRAME_DT:
                i += 1
            frame_count += 1
            break

        # 4) 잔여시간 채우기(빠르면 no-op로 1/60 맞춤)
        i = 0
        while (clock.getTime() - t0) < FRAME_DT:
            i += 1

        # 5) 프레임이 1/60초 채워진 뒤 카운트
        frame_count += 1

    
    save_frame_log(
        trial_idx=trial_idx,
        frame_log=frame_log,
        save_directory=save_directory,
        phase="feedback"
    )
    return frame_log