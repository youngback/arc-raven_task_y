# initialize.py

import os
import platform
import getpass
from datetime import datetime
import json

from set_opts.set_visual_opt import set_visual_opt
from set_opts.set_device_opt import set_device_opt
from set_opts.set_game_opt import set_game_opt
from set_opts.set_eyelink import set_eyelink
from save_func.define_save import define_save


def initialize():
    """
    실험 환경 전체 초기화 함수

    Returns:
        visual_opt: 시각적 설정 정보
        device_opt: 입력 장치 설정 정보
        game_opt: 게임 조건 설정 정보
        eye_opt: eye tracker 설정 정보
        save_directory: 데이터 저장 경로
    """

    # 1. 경로 설정
    current_folder = os.path.dirname(os.path.abspath(__file__))
    print(f"Current folder: {current_folder}")

    # 2. OS 및 사용자 감지
    system_name = platform.system()

    if system_name == "Darwin":
        print("Running on macOS")
        test = True
        subject_ID = input("Enter subject ID: ")
    elif system_name == "Windows":
        print("Running on Windows")
        test = False
        subject_ID = input("Enter subject ID: ")
    else:
        print("Running on other OS")
        test = False
        subject_ID = input("Enter subject ID: ")

    # 3. 저장 경로 설정
    save_directory = define_save(current_folder, subject_ID)
    os.makedirs(save_directory, exist_ok=True)
    print(f"Data will be saved to: {save_directory}")

    # 4. 각 옵션 설정
    visual_opt = set_visual_opt()
    device_opt = set_device_opt(subject_ID, test)
    game_opt = set_game_opt()
    eye_opt = set_eyelink(visual_opt, save_directory, subject_ID, test)

    # 5) 메타데이터 저장 (가벼운 요약만 JSON)
    metadata = {
        "subject_ID": subject_ID,
        "datetime": datetime.now().isoformat(timespec="seconds"),
        "os": system_name,
        "username": getpass.getuser(),
        "test_mode": test,
        # 직렬화 가능한 값들만 요약 저장
        "device_opt_summary": {k: v for k, v in device_opt.items()},
        "game_opt_summary":   {k: v for k, v in game_opt.items()},
        # visual_opt에서 큰 객체 제거(예: Window)
        "visual_opt_summary": {k: v for k, v in visual_opt.items() if k != "win"},
        "eyelink_enabled": bool(eye_opt)  # 또는 eye_opt.get("enabled", False)
    }
    metadata_path = os.path.join(save_directory, "metadata.json")
    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)

    print("Initialization complete.")
    return visual_opt, device_opt, game_opt, eye_opt, save_directory


if __name__ == "__main__":
    initialize()