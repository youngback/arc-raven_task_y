import os
from psychopy import visual, core, event

# --- 1. 모듈 및 함수 불러오기 (Import) ---
# 기존 그리드 관련 import는 제거하고, draw_image.py의 함수를 가져옵니다.
from draw.draw_image import calc_single_image_size
from draw.draw_marker import draw_marker
from config import FRAME_TRAIN, WIN_WIDTH, WIN_HEIGHT
from save_func.save_frame_log import save_frame_log_train

def phase_training(train_event, visual_opt, device_opt, game_opt, save_directory):
    win = visual_opt["win"]

    # --- 2. 데이터 준비 및 이미지 객체 생성 ---
    # train_event에서 숫자 배열(grid) 대신 이미지 경로(path)를 가져옵니다.

    train_input_path = train_event["train_input_path"]
    train_output_path = train_event["train_output_path"]

    # 경로를 사용해 Input/Output 이미지 객체를 생성합니다.
    input_stim = visual.ImageStim(win, image=train_input_path)
    output_stim = visual.ImageStim(win, image=train_output_path)

    # --- 3. 이미지 크기 및 위치 설정 ---
    # Input 이미지와 Output 이미지에 동일한 크기 규칙을 각각 적용합니다.

    # 1) Input 이미지의 크기를 계산하고 적용합니다.
    input_original_size = input_stim.size
    input_final_size = calc_single_image_size(input_original_size)
    input_stim.size = input_final_size
    # 2) Input 이미지의 위치를 설정합니다.
    input_stim.pos = (-WIN_WIDTH / 4, 0)

    # 3) Output 이미지의 크기를 계산하고 적용합니다.
    output_original_size = output_stim.size
    output_final_size = calc_single_image_size(output_original_size)
    output_stim.size = output_final_size
    # 4) Output 이미지의 위치를 설정합니다.
    output_stim.pos = (WIN_WIDTH / 4, 0)
    
    # --- 4. 루프 설정 ---
    # frame_log, 마커, 마우스 아이콘 등 기존 기능은 모두 유지됩니다.
    frame_log = []
    clock = core.Clock(); clock.reset()
    duration = float(game_opt["training_display_time"])
    
    mouse = event.Mouse(visible=True)
    icon = visual.Circle(win, radius=10, units='pix', fillColor='red', lineColor='white')
    
    frame_count = 0
    while clock.getTime() < duration:
        t0 = clock.getTime()
        
        # --- 5. 화면 그리기 및 루프 ---
        # 복잡한 for문 대신, 준비된 이미지 객체 두 개를 바로 그립니다.
        input_stim.draw()
        output_stim.draw()

        if frame_count < FRAME_TRAIN:
            draw_marker(win)
        
        mouse_x, mouse_y = mouse.getPos()
        icon.setPos((mouse_x, mouse_y))
        icon.draw()

        # --- 로그 기록 ---
        frame_log.append({
            "frame": frame_count,
            "elapsed_time": t0,
            "icon_x": mouse_x,
            "icon_y": mouse_y,
        })
        frame_count += 1
        win.flip()

    # --- CSV 저장 (이하 동일) ---
    trial_idx  = train_event.get("trial_idx", game_opt.get("trial_idx", 0))
    item_id    = train_event.get("item_id",  game_opt.get("item_id", ""))
    subject_id = game_opt.get("subject_id", "")
    save_dir = save_directory

    save_frame_log_train(
        trial_idx=trial_idx,
        frame_log=frame_log,
        save_dir=save_dir,
        subject_id=subject_id,
        item_id=item_id,
        phase="train"
    )
    
    return frame_log