from psychopy.hardware import joystick
from psychopy import event

def set_device_opt(subject_ID, test_requested):
    """
    ARC Task 입력 장치 설정 함수
    - 조이스틱 좌우 + 버튼 입력 방식
    - 장치 연결 안 되어 있으면 자동으로 테스트 모드로 fallback
    """

    # 1) 장치 연결 상태 확인 및 test 모드 결정
    device_opt = initialize_device_options(test_requested)

    # 2) 키보드 입력 설정
    if device_opt["KEYBOARD"]:
        device_opt = configure_keyboard(device_opt)

    # 3) 조이스틱 입력 설정
    if device_opt["JOYSTICK"]:
        device_opt = configure_joystick(device_opt)
    
    # 4) 마우스 입력 설정 (윈도우가 준비된 뒤에 실제 Mouse 객체는 외부에서 생성)
    if device_opt["MOUSE"]:
        device_opt = configure_mouse(device_opt)

    # 5) 공통 입력 파라미터 설정
    device_opt["minInput"] = 0.5          # x축 기울임 감도 임계값
    device_opt["min_t_scale"] = 1 / 1000  # 1ms 단위 시간 스케일

    return device_opt


def initialize_device_options(test_requested):
    """
    테스트 모드 여부 결정:
    - 사용자가 요청한 test 모드
    - 또는 장치 연결 실패 시 자동 test 모드 전환
    """

    # ✅ getJoysticks()는 연결된 조이스틱 리스트를 반환함
    try:
        joy_list = joystick.getJoysticks()
        has_joystick = len(joy_list) > 0
    except Exception as e:
        print(f"[WARNING] 조이스틱 확인 중 오류 발생: {e}")
        has_joystick = False

    has_eyelink = False  # eyetracker 사용 시에 추가
    test_auto = not (has_joystick and has_eyelink)
    test = test_requested or test_auto

    if test:
        print("[INFO] Test mode activated (device missing or requested).")
        return {
            "KEYBOARD": True,
            "MOUSE": True,
            "JOYSTICK": False,
            "EYELINK": False
        }
    else:
        print("[INFO] Real experiment mode activated.")
        return {
            "KEYBOARD": True,
            "MOUSE": True,
            "JOYSTICK": True,
            "EYELINK": True
        }


def configure_keyboard(device_opt):
    """
    테스트 모드에서 사용할 키보드 키 설정
    """
    device_opt["key_left"] = "left"
    device_opt["key_right"] = "right"
    device_opt["key_escape"] = "escape"
    return device_opt


def configure_joystick(device_opt):
    """
    실제 실험에서 사용할 조이스틱 설정
    - 조이스틱이 연결되어 있지 않으면 오류 발생
    """
    joystick.backend = 'pyglet'
    joy_list = joystick.getJoysticks()

    if len(joy_list) == 0:
        raise RuntimeError("[ERROR] 조이스틱이 연결되어 있지 않습니다.")

    joy = joy_list[0]  # 첫 번째 조이스틱 사용
    device_opt["joystick"] = joy
    device_opt["joy_button_select"] = 0  # 선택 확정용 버튼 번호

    return device_opt

def configure_mouse(device_opt):
    """
    마우스 관련 기본 설정. 실제 Mouse 객체는 initialize 함수 등
    win이 준비된 이후에 만들어서 visual_opt에 넣어야 함.
    """
    # 예: 버튼 매핑이 필요하면 여기서 지정
    device_opt["mouse_button_select"] = 0  # 왼쪽 버튼
    return device_opt