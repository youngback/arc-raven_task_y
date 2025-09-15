# draw_fixation.py

from psychopy import visual, event, core
import math

from psychopy import visual, core
from config import FRAME_DT  # 1/60초

def draw_fixation(visual_opt, color=None, duration=0.5):
    """
    화면 중앙에 fixation cross를 약 duration초 동안 프레임 루프로 표시.
    기본 0.5초(≈30프레임). core.wait 사용 X.
    """
    win = visual_opt["win"]
    size = visual_opt.get("fixation_size", 20)
    if color is None:
        color = visual_opt.get("text_color", "white")

    # 십자가 자극 준비(루프 밖에서 생성)
    hor_line = visual.Line(win, start=(-size, 0), end=(size, 0), lineColor=color, lineWidth=3)
    ver_line = visual.Line(win, start=(0, -size), end=(0, size), lineColor=color, lineWidth=3)

    # 정확히 N프레임 돌리기
    target_frames = int(round(duration / FRAME_DT))
    clock = core.Clock(); clock.reset()
    frame_count = 0

    while frame_count < target_frames:
        t0 = clock.getTime()

        # draw → flip
        hor_line.draw()
        ver_line.draw()
        win.flip()

        # 프레임 잔여시간(1/60초까지) 채우기
        i = 0
        while (clock.getTime() - t0) < FRAME_DT:
            i += 1

        frame_count += 1


def wait_for_fixation_hover(visual_opt, dwell=1.0, feedback=True, max_duration=None):
    """
    fixation cross 주변(hover_radius)에서 마우스를 dwell초 동안 유지하면 통과.
    - feedback=True면 hover 중 색을 바꿈.
    - max_duration이 주어지면 그 시간(초) 내에 완료 못하면 루프 종료(선택).
    core.wait 사용 X.
    """
    win = visual_opt["win"]

    # 마우스 준비
    if "mouse" not in visual_opt or visual_opt["mouse"] is None:
        visual_opt["mouse"] = event.Mouse(win=win)
    mouse = visual_opt["mouse"]
    mouse.setVisible(True)

    icon = visual.Circle(win, radius=10, units='pix', fillColor='red', lineColor='white')

    # 윈도우 단위에 따른 hover 반경
    if hasattr(win, 'units'):
        if win.units == 'pix':
            hover_radius = visual_opt.get("hover_radius", 50)
        elif win.units == 'norm':
            hover_radius = visual_opt.get("hover_radius", 0.1)
        else:
            hover_radius = visual_opt.get("hover_radius", 2.0)
    else:
        hover_radius = visual_opt.get("hover_radius", 0.1)

    # 십자가 자극(색은 프레임마다 정함)
    size = visual_opt.get("fixation_size", 20)

    clock = core.Clock(); clock.reset()
    phase_start = clock.getTime()
    hover_start = None

    frame_count = 0
    while True:
        t0 = clock.getTime()

        # (선택) 최대 대기 시간 제한
        if max_duration is not None and (t0 - phase_start) >= max_duration:
            break  # 타임아웃(원하면 여기서 반환/표시 추가)

        # 마우스 위치/hover 판정
        pos = mouse.getPos()
        dist = math.hypot(pos[0], pos[1])
        hovered = (dist <= hover_radius)

        # 색 선택
        if feedback:
            draw_color = "lightgreen" if hovered else visual_opt.get("text_color", "white")
        else:
            draw_color = visual_opt.get("text_color", "white")

        # 십자가 생성(색만 프레임마다 반영)
        hor_line = visual.Line(win, start=(-size, 0), end=(size, 0), lineColor=draw_color, lineWidth=3)
        ver_line = visual.Line(win, start=(0, -size), end=(0, size), lineColor=draw_color, lineWidth=3)

        # (선택) hover 반경 표시
        if feedback:
            hover_circle = visual.Circle(win, radius=hover_radius, lineColor='gray', fillColor=None, opacity=0.3)
            hover_circle.draw()

        # draw → flip
        hor_line.draw()
        ver_line.draw()
        icon.setPos(pos)
        icon.draw()
        win.flip()

        # dwell 판정
        if hovered:
            if hover_start is None:
                hover_start = clock.getTime()
            elif (clock.getTime() - hover_start) >= dwell:
                # 이 프레임의 잔여시간 채우고 종료 (프레임 일관성)
                i = 0
                while (clock.getTime() - t0) < FRAME_DT:
                    i += 1
                break
        else:
            hover_start = None

        # 종료 키
        if event.getKeys(["escape", "q"]):
            # 필요 시 여기서도 프레임 잔여시간 채우기
            i = 0
            while (clock.getTime() - t0) < FRAME_DT:
                i += 1
            core.quit()

        # 프레임 잔여시간(1/60초까지) 채우기
        i = 0
        while (clock.getTime() - t0) < FRAME_DT:
            i += 1

        frame_count += 1

# main.py에서 쓰는 이름과 맞추기 위한 래퍼
def draw_test_fixation(visual_opt, dwell=1.0, feedback=True):
    wait_for_fixation_hover(visual_opt, dwell=dwell, feedback=feedback)