from psychopy import visual

def draw_outline(
    win,
    pos,                      # ✅ 변경 1: 테두리를 그릴 중심 좌표 (x, y)
    size,                     # ✅ 변경 2: 테두리의 기준이 될 이미지 크기 (너비, 높이)
    is_correct,               # ✅ 변경 3: 정답 여부 (True/False)
    pad_frac=0.06,
    line_width=8,
    color_correct="#32CD32",
    color_incorrect="#FF4136",
):
    """
    [이미지용] 특정 위치와 크기를 기준으로 색 테두리를 그립니다.
    """
    img_w, img_h = size
    color = color_correct if is_correct else color_incorrect

    # 이미지 크기에 비례하여 테두리 크기 계산
    width  = img_w * (1 + pad_frac)
    height = img_h * (1 + pad_frac)

    # Rect 객체를 생성하고 바로 그립니다.
    visual.Rect(
        win,
        width=width,
        height=height,
        lineColor=color,
        lineWidth=line_width,
        pos=pos,
        fillColor=None,  # 테두리만 그리므로 채우기 색은 None
    ).draw()