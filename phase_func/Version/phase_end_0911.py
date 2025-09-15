#phase/phase_end.py
from psychopy import visual, core, event

def phase_end(visual_opt, duration=2.0):
    """
    ARC Task 종료 화면
    - 실험 종료 후 종료 안내 메시지를 몇 초간 표시하거나, 특정 키 입력을 기다린 뒤 종료.

    Parameters
    ----------
    visual_opt : dict          # set_visual_opt()가 만든 옵션 딕셔너리
    duration   : float         # 대기 시간(초). wait_for_key=False일 때 사용
    wait_for_key : bool        # True면 key_list 중 키 입력을 기다림
    key_list   : tuple[str]    # 기다릴 키 목록
    """
    win = visual_opt["win"]

    # 1) 텍스트 설정값: visual_opt에 없으면 안전한 기본값으로 fallback
    text       = visual_opt.get("end_text", "Thank you for your participation!")
    font       = visual_opt.get("font", "Arial")
    text_color = visual_opt.get("text_color", "white")

    # 해상도에 독립적인 크기: 창 높이의 %로 폰트 크기 잡기 (기본 ~5%)
    win_w, win_h = win.size
    font_size    = visual_opt.get("font_size", max(12, int(win_h * 0.05)))

    # 화면 폭의 80%를 줄바꿈 폭으로 사용 (기존 고정 1000 대신 반응형)
    wrap_width = int(win_w * 0.8)

    # 2) 배경 정리(검정) 후 표시
    win.color = "black"   # 또는 visual_opt.get("bg_color", "black")
    win.flip()

    end_text = visual.TextStim(
        win=win,
        text=text,
        font=font,
        color=text_color,
        height=font_size,
        wrapWidth=wrap_width,
        pos=(0, 0),
        anchorHoriz="center",
        anchorVert="center",
    )

    end_text.draw()
    win.flip()

    core.wait(duration)  # 지정된 시간 동안 유지

    # 4) 종료 시 화면 정리(선택)
    win.flip()
