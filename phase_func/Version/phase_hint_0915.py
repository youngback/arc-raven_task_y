import os
from psychopy import visual, core, event
import numpy as np

# --- 1. 모듈 및 함수 불러오기 (Import) ---
from draw.draw_image import calc_single_image_size
from draw.draw_marker import draw_marker
from config import FRAME_HINT, WIN_WIDTH, WIN_HEIGHT, FRAME_DT
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

        # 1) draw
        input_stim.draw()
        hint_stim.draw()
        next_button_bg.draw()
        next_button_arrow.draw()

        if frame_count < FRAME_HINT:
            draw_marker(win)

        # 커서 아이콘(시각화용)
        mouse_x, mouse_y = mouse.getPos()
        icon.setPos((mouse_x, mouse_y))
        icon.draw()

        # 2) 프레임 표시
        win.flip()

        # 3) flip 직후 로그 엔트리 구성
        log_entry = {
            "frame": frame_count,
            "elapsed_time": t0,   # 원하면 t_post_flip = clock.getTime()도 추가 가능
            "icon_x": mouse_x,
            "icon_y": mouse_y,
            "rt": ""
        }

        # 4) 클릭 체크 (flip 이후)
        if mouse.getPressed()[0] and next_button_bg.contains(mouse):
            rt = clock.getTime()
            log_entry["rt"] = f"{rt:.4f}"
            frame_log.append(log_entry)

            # (중요) 클릭 프레임도 1/60초 채우고 종료
            i = 0
            while (clock.getTime() - t0) < FRAME_DT:
                i += 1

            frame_count += 1
            break

        # 5) 클릭 없으면 일반 로그
        frame_log.append(log_entry)

        # 6) 프레임 잔여 시간 채우기
        i = 0
        while (clock.getTime() - t0) < FRAME_DT:
            i += 1

        frame_count += 1


    # --- CSV 저장 (이하 동일) ---
    item_id = hint_event.get("item_id", game_opt.get("item_id", ""))
    subject_id = game_opt.get("subject_id", "")
    save_dir = save_directory

    # 저장: 프레임 로그에 rt만 포함 (헤더: frame, elapsed_time, icon_x, icon_y, rt)

    save_frame_log_hint(
        trial_idx=trial_idx,
        frame_log=frame_log,
        save_dir=save_directory,
        subject_id=subject_id,
        item_id=item_id,
        rt=rt                   # ← 그냥 rt 넘기면 됨
    )
    
    return frame_log