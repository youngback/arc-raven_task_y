import os
from psychopy import visual, core, event
import numpy as np

# --- 1. 모듈 및 함수 불러오기 (Import) ---
from draw.draw_image import calc_single_image_size
from draw.draw_marker import draw_marker
from config import FRAME_HINT, WIN_WIDTH, WIN_HEIGHT
from save_func.save_frame_log import save_frame_log_hint

def phase_hint(hint_event, visual_opt, device_opt, game_opt, trial_idx, save_directory):
    win = visual_opt["win"]

    # --- 2. 데이터 준비 및 이미지 객체 생성 ---
    input_path = hint_event["input_path"]
    hint_path = hint_event["hint_path"]

    input_stim = visual.ImageStim(win, image=input_path)
    hint_stim = visual.ImageStim(win, image=hint_path)

    # --- 3. 이미지 크기 및 위치 설정 ---
    input_original_size = input_stim.size
    input_final_size = calc_single_image_size(input_original_size)
    input_stim.size = input_final_size
    input_stim.pos = (-WIN_WIDTH / 4, 0)

    hint_original_size = hint_stim.size
    hint_final_size = calc_single_image_size(hint_original_size)
    hint_stim.size = hint_final_size
    hint_stim.pos = (WIN_WIDTH / 4, 0)
    
    # --- 4. '다음 단계' 버튼 생성 ---
    button_size = WIN_WIDTH * 0.05
    button_pos_x = WIN_WIDTH / 2 - button_size * 1.5
    button_pos_y = -WIN_HEIGHT / 2 + button_size

    next_button_bg = visual.Rect(win, 
                                 width=button_size, 
                                 height=button_size, 
                                 pos=(button_pos_x, button_pos_y), 
                                 fillColor='green', 
                                 lineColor='white')
    
    arrow_vertices = np.array([
        [button_size * 0.3, 0], 
        [-button_size * 0.3, button_size * 0.3], 
        [-button_size * 0.3, -button_size * 0.3]
    ])
    next_button_arrow = visual.ShapeStim(win, 
                                         vertices=arrow_vertices, 
                                         pos=(button_pos_x, button_pos_y), 
                                         fillColor='white', 
                                         lineColor='white')

    # --- 5. 루프 설정 ---
    frame_log = []
    clock = core.Clock(); clock.reset()
    duration = float(game_opt["hint_display_time"])
    mouse = event.Mouse(visible=True)
    icon = visual.Circle(win, radius=10, units='pix', fillColor='red', lineColor='white')
    
    frame_count = 0
    rt = None

    while clock.getTime() < duration:
        t0 = clock.getTime()
        
        # --- 6. 화면 그리기 및 루프 ---
        input_stim.draw()
        hint_stim.draw()
        
        next_button_bg.draw()
        next_button_arrow.draw()

        if frame_count < FRAME_HINT:
            draw_marker(win)
        
        mouse_x, mouse_y = mouse.getPos()
        icon.setPos((mouse_x, mouse_y))
        icon.draw()

        log_entry = {
            "frame": frame_count,
            "elapsed_time": t0,
            "icon_x": mouse_x,
            "icon_y": mouse_y,
            "rt": ""
        }

        # 클릭 확인: 버튼 영역에서 클릭되면 해당 프레임에 RT 기록하고 종료
        if mouse.getPressed()[0] and next_button_bg.contains(mouse):
            rt = clock.getTime()
            log_entry["rt"] = f"{rt:.4f}"
            frame_log.append(log_entry)
            break

        # --- 로그 기록 ---
        frame_log.append(log_entry)
        frame_count += 1
        win.flip()

        # 클릭 없이 종료된 경우: 타임아웃 행 추가 (rt = duration)
    if rt is None:
        last_x, last_y = mouse.getPos()
        rt = duration
        frame_log.append({
            "frame": frame_count,
            "elapsed_time": duration,
            "icon_x": last_x,
            "icon_y": last_y,
            "rt": f"{rt:.4f}"
        })
    
    # 🔴 루프 종료 후 화면을 한 번 더 비워줍니다.
    win.flip()

    # --- CSV 저장 (이하 동일) ---
    trial_idx = hint_event.get("trial_idx", game_opt.get("trial_idx", 0))
    item_id = hint_event.get("item_id", game_opt.get("item_id", ""))
    subject_id = game_opt.get("subject_id", "")
    save_dir = save_directory

    # 저장: 프레임 로그에 rt만 포함 (헤더: frame, elapsed_time, icon_x, icon_y, rt)
    save_frame_log_hint(
        trial_idx=trial_idx,
        frame_log=frame_log,
        save_dir=save_dir,
        subject_id=subject_id,
        item_id=item_id
    )
    
    return frame_log