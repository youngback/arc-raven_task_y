# structs_init/initialize_all_trials_info.py

from datetime import datetime

def initialize_all_trials_info():
    """
    ARC 사람 task용 trials 정보 초기화
    """

    all_trials_info = {
        "current_trial": 1,             # 현재 trial 번호
        "max_trial_num": 30,           # 총 trial 수 (변경 가능)
        "block_number": 1,              # 블록 번호 (20개씩 묶음)
        "correct_count": 0,             # 정답 개수 누적
        "trial_results": [],            # 각 trial 결과를 append해서 저장
        "stim_order": [],               # load_arc_trials()에서 채움
        "start_time": datetime.now()    # 실험 시작 시각
    }

    return all_trials_info