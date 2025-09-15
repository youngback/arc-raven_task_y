# phase/phase_score.py
from psychopy import core, visual
from draw.draw_marker import draw_marker
from config import FRAME_SCORE

def phase_score(trial_idx, visual_opt, total_correct, save_dir, duration=2.0):
    """
    화면 중앙에 'Total score'와 실제 점수를 중첩 정렬하여 표시한 뒤,
    duration(초)만큼 유지합니다.
    
    Parameters
    ----------
    win : psychopy.visual.Window
        PsychoPy 윈도우 객체
    score : int or str
        표시할 점수
    duration : float
        유지 시간(초)
    """
    win = visual_opt["win"]

    # 윈도우 크기 가져오기 (pix 단위)
    win_w, win_h = win.size
    
    # 텍스트 크기를 윈도우 높이의 8%로 설정
    title_height = win_h * 0.02
    score_height = win_h * 0.05
    
    # 위아래 간격 비율
    y_offset = win_h * 0.10
    
    # 1) 제목
    title_stim = visual.TextStim(
        win=win,
        text="Total score",
        pos=(0,  y_offset),
        height=title_height,
        anchorHoriz='center',
        anchorVert='bottom'
    )
    # 2) 점수
    score_stim = visual.TextStim(
        win=win,
        text=str(total_correct),
        pos=(0, -y_offset),
        height=score_height,
        anchorHoriz='center',
        anchorVert='top'
    )
    
    # 프레임 로그 기록 준비
    clock = core.Clock(); clock.reset()
    frame_count = 0
    frame_log = []
    
    # duration 동안 루프
    while clock.getTime() < duration:
        title_stim.draw()
        score_stim.draw()

        # 포토다이오드: 시작 직후 N프레임만
        if frame_count < FRAME_SCORE:
            draw_marker(win)

        win.flip()
        
        frame_log.append({
            "frame": frame_count,
            "elapsed_time": clock.getTime()
        })
        
        frame_count += 1
    
    # 저장
    return frame_log