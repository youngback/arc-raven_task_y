from psychopy import visual
from config import WIN_WIDTH, WIN_HEIGHT

#2차원 그리드의 크기를 계산하는 코드
def calc_grid_size(rows, cols, width_frac, height_frac, default_cell_size, scale):
    """
    그리드 하나(cell) 크기와 전체 그리드 크기를 계산해 주는 공통 함수
    """
    #frac 파라미터를 비율에 맞게 수정해서 사용하면 됨
    #셀 크기는 1)그리드 높이 기준 최댓값, 2)그리드 너비 기준 최댓값, 3)디폴드 셀 크기 중 가장 작은 값을 선택함
    max_w = (WIN_WIDTH  * width_frac) // cols
    max_h = (WIN_HEIGHT * height_frac) // rows
    cell_size = scale * min(default_cell_size, max_w, max_h)
    grid_w = cols * cell_size
    grid_h = rows * cell_size
    return cell_size, grid_w, grid_h

#2차원 그리드의 위치 코드
def calc_grid_positions(arr_rows, arr_cols, grid_w, grid_h, cell_size, offset=(0,0), spacing_unit=2.0):
    """
    그리드를 몇 행×몇 열 배열로 배치할 때,
    각 셀(그리드)의 중심 좌표 리스트를 반환하는 함수.

    Parameters:
    - arr_rows, arr_cols: 몇 행×몇 열 배열로 배치할지 (예: 2×2 → arr_rows=2, arr_cols=2)
    - grid_w, grid_h:     그리드 하나(격자 전체)가 차지하는 너비·높이 (픽셀)
    - offset:             (x, y) 추가 이동값. 예: (100, 0)이면 오른쪽으로 100px 이동

    Returns:
    - positions:          [(x1, y1), (x2, y2), …] 형태의 중심 좌표 리스트
    """
    positions = []
    ox, oy = offset

    # cell_size를 기준으로 grid 간 간격 변화
    spacing_px = cell_size * spacing_unit

    # 전체 배열의 너비와 높이 계산 (새로운 간격 포함)
    total_width = arr_cols * grid_w + (arr_cols - 1) * spacing_px
    total_height = arr_rows * grid_h + (arr_rows - 1) * spacing_px

    # for loop로 각 그리드의 중심 좌표 계산
    for r in range(arr_rows):
        for c in range(arr_cols):
            # 각 그리드의 위치를 계산할 때 spacing_px를 사용합니다.
            x = (c * (grid_w + spacing_px)) - (total_width / 2) + (grid_w / 2) + ox
            y = ((total_height / 2) - (grid_h / 2)) - (r * (grid_h + spacing_px)) + oy
            positions.append((x, y))

    return positions

def calc_label_params(grid_h, label_opts):
    """
    grid_h: 그리드 전체 높이(px)
    label_opts: {"offset_frac": float, "height_frac": float, "color": str, ...}
    반환: (레이블 오프셋 px, 텍스트 높이 px)
    """
    offset_frac = label_opts.get("offset_frac", 0.1)
    height_frac = label_opts.get("height_frac", 0.05)
    offset_px = grid_h * offset_frac
    height_px = max(1, grid_h * height_frac)  # 최소 높이는 1px
    return offset_px, height_px

# [새로운 '설계' 함수]
# 이 함수는 draw_labeled_grid.py 파일에 추가하거나, 별도 파일로 관리할 수 있습니다.

def create_labeled_grid_stim(win, grid_data, label, pos, cell_size, color_palette, label_opts, line_color="white", line_width=2):
    """
    [리팩토링된 함수]
    그리드를 표시하는 데 필요한 모든 시각 자극(stimuli) 객체를
    '생성만' 해서 하나의 리스트에 담아 반환합니다.
    이 함수는 루프 밖에서 한 번만 호출됩니다.
    """
    
    # ------------------------------------------------------------------
    # ▼▼▼▼▼ 기존 draw_labeled_grid 함수의 로직을 거의 그대로 사용 ▼▼▼▼▼
    # ------------------------------------------------------------------
    
    stimuli_list = [] # 생성된 모든 객체를 담을 빈 리스트

    rows, cols = len(grid_data), len(grid_data[0])
    grid_w = cols * cell_size
    grid_h = rows * cell_size

    # 1) 레이블 오프셋/높이 계산
    label_offset, label_height = calc_label_params(grid_h, label_opts)

    # 2) 레이블 객체 '생성'
    label_stim = visual.TextStim(
        win,
        text=label,
        pos=(pos[0], pos[1] + grid_h / 2 + label_offset),
        color=label_opts.get("color", "white"),
        height=label_height,
    )
    # [변경점] .draw() 대신 리스트에 추가
    stimuli_list.append(label_stim)

    # 3) 셀들(사각형) 객체 '생성'
    half_rows, half_cols = rows / 2.0, cols / 2.0
    for r in range(rows):
        for c in range(cols):
            val = grid_data[r][c]
            fill = color_palette.get(val, "black")
            x = pos[0] + (c - half_cols + 0.5) * cell_size
            y = pos[1] - (r - half_rows + 0.5) * cell_size
            
            # 사각형 객체 '생성'
            rect = visual.Rect(
                win,
                width=cell_size,
                height=cell_size,
                fillColor=fill,
                lineColor=line_color,
                lineWidth=line_width,
                pos=(x, y),
            )
            # [변경점] .draw() 대신 리스트에 추가
            stimuli_list.append(rect)

    # ------------------------------------------------------------------
    # ▲▲▲▲▲ 여기까지 기존 로직과 거의 동일 ▲▲▲▲▲
    # ------------------------------------------------------------------

    # 모든 객체가 담긴 리스트를 반환
    return stimuli_list