# phase/phase_score.py
from psychopy import core, visual
from draw.draw_marker import draw_marker
from config import FRAME_SCORE, FRAME_DT
from save_func.save_frame_log import save_frame_log

def phase_score(trial_idx, visual_opt, total_correct, save_dir, duration=2.0):
    """
    화면 중앙에 'Total score'와 실제 점수를 중첩 정렬하여 표시한 뒤,
    duration(초) 동안 60Hz 프레임 루프로 표시합니다.
    """
    win = visual_opt["win"]

    # 윈도우 크기 (pix)
    win_w, win_h = win.size

    # 텍스트 크기/위치
    title_height = win_h * 0.03
    score_height = win_h * 0.06
    y_offset = win_h * 0.10

    title_stim = visual.TextStim(
        win=win,
        text="Total score",
        pos=(0,  y_offset),
        height=title_height,
        anchorHoriz='center',
        anchorVert='bottom'
    )
    score_stim = visual.TextStim(
        win=win,
        text=str(total_correct),
        pos=(0, -y_offset),
        height=score_height,
        anchorHoriz='center',
        anchorVert='top'
    )

    # 프레임 로그
    clock = core.Clock(); clock.reset()
    frame_count = 0
    frame_log = []

    # duration 동안 루프
    while clock.getTime() < duration:
        t0 = clock.getTime()

        # draw
        title_stim.draw()
        score_stim.draw()

        # 포토다이오드: 시작 직후 N프레임만
        if frame_count < FRAME_SCORE:
            draw_marker(win)

        # flip
        win.flip()
        t1 = clock.getTime()  # flip 직후

        # 로그 (flip 직후 시각 기반)
        frame_log.append({
            "frame": frame_count,
            "elapsed_time": t0,
            "t_frame_start": t0,
            "t_post_flip": t1,           # 선택 필드지만 강추
            "dt_draw_flip": t1 - t0,     # 선택 필드지만 강추
        })

        # 프레임 잔여 시간 채우기 (빠르면 no-op로 1/60초 맞춤)
        i = 0
        while (clock.getTime() - t0) < FRAME_DT:
            i += 1  # no-op

        # 프레임 카운트는 채운 뒤 증가
        frame_count += 1

    save_frame_log(
        trial_idx=trial_idx,
        frame_log=frame_log,
        save_directory=save_dir,
        phase="score"
    )
    return frame_log