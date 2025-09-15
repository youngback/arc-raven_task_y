def set_eyelink(visual_opt, save_directory, subject_ID=None, test=False):
    """
    ARC Task용 EyeLink 설정 함수
    - 실험 모드(test=False)일 때만 EyeLink 연결 시도
    - 추후 실제 장비와 연동 시 pylink 코드 추가 가능
    """

    eye_opt = {
        "eye_side": 2,          # 1: left, 2: right (오른쪽 눈 기본값)
        "eyelink_on": False     # 기본값: off
    }

    if not test:
        try:
            # 추후 실험 장비 붙일 때 여기에 pylink 관련 초기화 삽입
            # 예: import pylink, tracker = pylink.EyeLink()
            # tracker.openDataFile(f"{subject_ID}.edf")
            # tracker.sendCommand("screen_pixel_coords = 0 0 1919 1079")
            # tracker.startRecording()

            eye_opt["eyelink_on"] = True
            print("[INFO] EyeLink initialized and recording started.")

        except Exception as e:
            eye_opt["eyelink_on"] = False
            print(f"[WARNING] EyeLink initialization failed: {e}")

    else:
        print("[INFO] EyeLink not used (test mode).")

    return eye_opt