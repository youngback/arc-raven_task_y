# structs_init/initialize_time_info.py

from datetime import datetime

def initialize_time_info():
    """
    시간 정보를 초기화하여 반환
    - 실험 시작 시점과 trial 내 시간 기록용 필드 생성
    """

    time_info = {
        "exp_start_time": datetime.now(),   # 전체 실험 시작 시간
        "trial_init_time": None,            # 각 trial 시작 시간
        "stim_on_time": None,               # 자극 제시 시간
        "response_time": None,              # 응답 시간
        "reaction_time": None               # 반응 시간 (stim_on ~ response)
    }

    return time_info