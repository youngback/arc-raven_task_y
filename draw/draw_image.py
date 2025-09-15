# draw/image.py

# 프로젝트의 설정(config) 파일에서 창 크기를 가져오는 것이 가장 좋습니다.
from config import WIN_WIDTH, WIN_HEIGHT

def calc_single_image_size(original_size):
    """
    Train Input/Output, Test Input 같이 단일 이미지의 크기를 계산합니다.
    화면 왼쪽 절반 영역을 기준으로, 그 영역의 너비 80%, 높이 80%를
    넘지 않도록 이미지 원본 비율을 유지하며 크기를 조절합니다.

    Parameters:
    - original_size: (너비, 높이) 튜플. 이미지의 원본 크기.

    Returns:
    - (최종 너비, 최종 높이) 튜플
    """
    orig_w, orig_h = original_size
    
    # 목표: 이미지가 들어갈 최대 영역(Bounding Box)의 크기를 계산합니다.
    # 너비: 전체 화면 너비의 절반(0.5) * 80%(0.8) = 전체 너비의 40%(0.4)
    target_max_w = WIN_WIDTH * 0.4
    # 높이: 전체 화면 높이의 80%(0.8)
    target_max_h = WIN_HEIGHT * 0.8
    
    # 너비와 높이를 각각 맞추기 위한 축소/확대 비율을 계산합니다.
    scale_w = target_max_w / orig_w if orig_w > 0 else float('inf')
    scale_h = target_max_h / orig_h if orig_h > 0 else float('inf')
    
    # 두 비율 중 더 작은 값을 선택해야 원본 비율이 깨지지 않습니다.
    final_scale = min(scale_w, scale_h)
    
    # 최종 크기를 계산하여 반환합니다.
    final_w = orig_w * final_scale
    final_h = orig_h * final_scale
    
    return (final_w, final_h)


def calc_choices_image(original_size, layout_opts):
    """
    Test Choices의 2x2 그리드 이미지 크기와 위치를 계산합니다.
    '상대 간격'을 기준으로 주어진 영역에 맞게 크기를 조절합니다.

    Parameters:
    - original_size: (너비, 높이) 튜플. 선택지 이미지의 원본 크기.
    - layout_opts: 레이아웃 옵션 딕셔너리.

    Returns:
    - (final_size, positions): ((최종 너비, 최종 높이), [(x1,y1), ...])
    """
    orig_w, orig_h = original_size
    
    # --- 1. 최종 이미지 크기 계산 ---
    grid_w_frac, grid_h_frac = layout_opts["grid_area_frac"]
    grid_max_w = WIN_WIDTH * grid_w_frac
    grid_max_h = WIN_HEIGHT * grid_h_frac
    spacing_frac = layout_opts["spacing_frac"]
    
    max_img_w = grid_max_w / (2 + spacing_frac)
    max_img_h = grid_max_h / (2 + spacing_frac)
    
    scale_w = max_img_w / orig_w if orig_w > 0 else float('inf')
    scale_h = max_img_h / orig_h if orig_h > 0 else float('inf')
    final_scale = min(scale_w, scale_h)
    
    final_w = orig_w * final_scale
    final_h = orig_h * final_scale
    final_size = (final_w, final_h)

    # --- 2. 이미지 위치 계산 ---
    item_w, item_h = final_size
    offset = layout_opts["grid_center_pos"]
    spacing = item_w * spacing_frac

    total_width = 2 * item_w + spacing
    total_height = 2 * item_h + spacing
    
    positions = []
    for r in range(2):
        for c in range(2):
            x = offset[0] - total_width / 2 + item_w / 2 + c * (item_w + spacing)
            y = offset[1] + total_height / 2 - item_h / 2 - r * (item_h + spacing)
            positions.append((x, y))
            
    return final_size, positions