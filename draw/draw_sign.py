from psychopy import visual

def draw_sign(win, choice_position, is_correct, win_width, win_height):
    """
    정답 여부에 따라 Choice 자극 옆에 초록 원(정답) 또는 빨간 X(오답) 표시

    Parameters:
    - win: PsychoPy Window 객체
    - choice_position: "right_top_left", "right_top_right",
                       "right_bottom_left", "right_bottom_right"
    - is_correct: True이면 초록 원, False이면 빨간 X
    - win_width, win_height: 화면 크기
    """

    # 기본 offset 값 (원본 대비)
    base_x = win_width // 4
    base_y = win_height // 4
    margin_x = 120
    margin_y = 150

    # 위치별 offset 계산
    if choice_position == "right_top_left":
        offset_x = base_x - margin_x
        offset_y = base_y + margin_y

    elif choice_position == "right_top_right":
        offset_x = base_x + margin_x
        offset_y = base_y + margin_y

    elif choice_position == "right_bottom_left":
        offset_x = base_x - margin_x
        offset_y = -base_y - margin_y

    elif choice_position == "right_bottom_right":
        offset_x = base_x + margin_x
        offset_y = -base_y - margin_y

    # (구버전) 아래 두 키도 호환 유지
    elif choice_position == "right_top":
        offset_x = base_x + margin_x
        offset_y =  margin_y
    elif choice_position == "right_bottom":
        offset_x = base_x + margin_x
        offset_y = -margin_y

    else:
        # 안전장치: 중앙 우측
        offset_x = base_x + margin_x
        offset_y = 0

    pos = (offset_x, offset_y)

    # 정답/오답 심볼 그리기
    if is_correct:
        circle = visual.Circle(
            win,
            radius=30,
            edges=64,
            lineColor="green",
            lineWidth=12,
            fillColor=None,
            pos=pos
        )
        circle.draw()
    else:
        # X 표시
        line1 = visual.Line(
            win,
            start=(-20, -20),
            end=(20, 20),
            lineColor="red",
            lineWidth=12,
            pos=pos
        )
        line2 = visual.Line(
            win,
            start=(-20, 20),
            end=(20, -20),
            lineColor="red",
            lineWidth=12,
            pos=pos
        )
        line1.draw()
        line2.draw()