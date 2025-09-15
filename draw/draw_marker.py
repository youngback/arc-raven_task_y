# draw/draw_marker.py
from psychopy import visual
from config import WIN_HEIGHT, WIN_WIDTH

# --- 마커 설정 ---

# 1. 크기 설정 (화면 너비의 5%)
MARKER_SIZE_FRAC = 0.05

def draw_marker(win):
    """
    화면 왼쪽 아래에 고정된 크기의 하얀 정사각형 마커를 그립니다.
    """
    # 위치를 화면 왼쪽 아래로 고정
    pos = (-WIN_WIDTH / 1.5, -WIN_HEIGHT / 1.5)

    # 설정된 비율로 크기 계산
    side = WIN_WIDTH * MARKER_SIZE_FRAC

    # 마커 생성 및 그리기
    marker = visual.Rect(
        win=win,
        pos=pos,
        width=side,
        height=side,
        fillColor='white',
        lineColor='white',
        units='pix'
    )
    marker.draw()