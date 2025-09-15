#phase/phase_start.py
from psychopy import core, visual, event

def phase_start(visual_opt, device_opt):
    """
    ARC Task 시작 화면
    - 키보드 입력 대기
    """
    win = visual_opt["win"]

    # 1) 텍스트 설정값: visual_opt에 없으면 안전한 기본값으로 fallback
    text       = visual_opt.get("start_text", "Click the screen to start.")
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

    start_text = visual.TextStim(
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

    start_text.draw()
    win.flip()

    # 3) 입력 대기: 마우스 클릭 또는 키보드 입력

    # - 1) 마우스 준비: 이전 클릭을 리셋하고, 눌린 상태가 있으면 먼저 뗄 때까지 기다림
    mouse = event.Mouse(win=win, visible=True)
    mouse.clickReset()

    # 이미 눌려있는 상태(드래그·버튼 고정 등) 방지: 버튼이 모두 올라갈 때까지
    while any(mouse.getPressed()):
        core.wait(0.01)

    # - 2) 대기 루프: 마우스 클릭 또는 키보드 입력 감지
    while True:
        # a) 종료 키(ESC)
        if "escape" in event.getKeys():
            core.quit()

        # b) 마우스 클릭(좌/우/가운데 아무거나)
        buttons, times = mouse.getPressed(getTime=True)
        if any(buttons):
            # 디바운싱: 실제로 눌린 시점이 0.03초 이상이면 인정
            if max(times) > 0.03:
                break

        # 너무 바쁘지 않게 살짝 쉼
        core.wait(0.01)

    # → 여기 도달하면 클릭/키 입력이 발생한 것
    # 다음 phase를 호출하거나 True/상태값을 반환하는 등 네가 원하는 흐름으로 마무리!
    return True