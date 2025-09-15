def set_game_opt():
    """
    ARC Task용 게임 설정
    - 타이밍, trial 수, 블록 수, 피드백, 저장 전략 포함
    """

    game_opt = {
        # 전체 trial 구성
        "total_trials": 30,
        "trials_per_block": 5,
        "current_trial": 1,
        "current_block": 1,

        # 피드백 관련
        "feedback_delay": 0.3,
        "give_feedback": True,
        "feedback_time": 1.0,              # 정답 시 피드백 지속 시간 (초)

        # 점수
        "total_score": 0,                  # 초기 총점
        "points_per_correct": 1,        # 정답 시 획득 점수
        "points_per_incorrect": 0,    # 오답 시 감점 (0으로 설정 가능)

        # timing 설정
        "training_display_time": 2.0,      # training 자극 1개 제시 시간
        "hint_display_time": 5.0,          # hint 자극 1개 제시 시간
        "test_display_time": 5.0,          # test 자극 제시 최대 시간
        "fixation_time": 0.5,              # fixation 표시 시간
        "break_duration": 30.0,            # block 간 쉬는 시간 (초)
        "max_trial_duration": None,        # test phase 제한 없음

        # 데이터 저장 관련
        "save_every_trial": True,
        "save_directory": None             # 추후 initialize에서 경로 지정
    }

    return game_opt