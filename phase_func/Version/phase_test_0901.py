import os
from psychopy import visual, core, event

# --- 1. 모듈 및 함수 불러오기 (Import) ---
from draw.draw_image import calc_single_image_size, calc_choices_image
from draw.draw_marker import draw_marker
from config import FRAME_TEST, WIN_WIDTH, WIN_HEIGHT
from save_func.save_frame_log import save_frame_log_test

def phase_test(test_event, visual_opt, game_opt, trial_idx, save_directory):
    win = visual_opt["win"]

    # --- 2. 데이터 준비 및 이미지 객체 생성 ---
    input_path = test_event["input_path"]
    choices_paths = test_event["choices_paths"]
    correct_idx = test_event["correct_idx"]

    input_stim = visual.ImageStim(win, image=input_path)
    choices_stim_list = [visual.ImageStim(win, image=path) for path in choices_paths]

    # --- 3. Input 이미지 크기 및 위치 설정 ---
    input_original_size = input_stim.size
    input_final_size = calc_single_image_size(input_original_size)
    input_stim.size = input_final_size
    input_stim.pos = (-WIN_WIDTH / 4, 0)

    # --- 4. Choice 이미지 크기 및 위치 설정 ---
    choices_original_size = choices_stim_list[0].size
    layout_options = {
        "grid_area_frac": (0.5, 0.9),
        "grid_center_pos": (WIN_WIDTH / 4, 0),
        "spacing_frac": 0.25
    }
    choices_final_size, choices_positions = calc_choices_image(
        choices_original_size, 
        layout_options
    )
    for stim, pos in zip(choices_stim_list, choices_positions):
        stim.size = choices_final_size
        stim.pos = pos
        
    # --- 5. 사용자 입력 루프 설정 ---
    # 1. 변수 초기화: frame_log와 frame_count, clock을 다시 추가합니다.
    frame_log = []
    clock = core.Clock(); clock.reset()
    duration = float(game_opt["test_display_time"])
    mouse = event.Mouse(visible=True)
    icon = visual.Circle(win, radius=10, units='pix', fillColor='red', lineColor='white')
    choice_idx, is_correct = None, None
    frame_count = 0
    
    while clock.getTime() < duration:
        t0 = clock.getTime() # 시간 기록
        
        # 화면에 모든 이미지 객체를 그립니다.
        input_stim.draw()
        for stim in choices_stim_list:
            stim.draw()
        
        # 2. draw_marker 호출: 첫 몇 프레임 동안 마커를 그립니다.
        if frame_count < FRAME_TEST:
            draw_marker(win)
            
        # 커서 아이콘을 그리고 화면을 업데이트합니다.
        mouse_x, mouse_y = mouse.getPos()
        icon.setPos((mouse_x, mouse_y))
        icon.draw()
        win.flip()
        
        # 마우스 클릭을 확인합니다.
        if mouse.getPressed()[0]:
            for i, stim in enumerate(choices_stim_list):
                if stim.contains(mouse):
                    choice_idx = i
                    is_correct = (choice_idx == correct_idx)
                    rt = clock.getTime()
                    # 클릭이 감지되면 루프를 즉시 종료합니다.
                    break
            
            # 선택이 이루어졌다면 while 루프를 빠져나옵니다.
            if choice_idx is not None:
                break
        
        if 'escape' in event.getKeys():
            break
            
        # ✅ 3. frame_log 기록: 매 프레임의 정보를 기록합니다.
        frame_log.append({
            "frame": frame_count,
            "elapsed_time": t0,
            "icon_x": mouse_x,
            "icon_y": mouse_y,
        })
        frame_count += 1

    # --- 6. 결과 반환 ---
    # 📌 루프가 끝난 후 정답 여부와 RT를 다시 확인
    # 루프가 시간 제한 때문에 끝난 경우
    if choice_idx is None:
        is_correct = False # 정답을 선택하지 못했으므로 오답으로 처리
        rt = duration      # 반응 시간을 전체 시간으로 기록
    
    subject_id = game_opt.get("subject_id", "UNKNOWN")
    item_id = test_event.get("item_id", "")
    # `save_directory`를 최상위 폴더(e.g., "logs")로 사용
    base_save_dir = save_directory 

    save_frame_log_test(
        save_dir=base_save_dir,
        subject_id=subject_id,
        trial_idx=trial_idx,
        item_id=item_id,
        correct_idx=correct_idx,
        chosen_idx=choice_idx,
        is_correct=is_correct,
        rt=rt,
        frame_log=frame_log
    )

    layout_for_feedback = {
        "input_stim": input_stim,
        "choices_stim_list": choices_stim_list,
        "choice_image_size": choices_final_size
    }

    return is_correct, choice_idx, layout_for_feedback, rt, frame_log