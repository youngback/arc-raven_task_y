import os
from datetime import datetime

def define_save(base_path, subject_ID):
    """
    저장 경로를 생성하고 반환
    - base_path: 실험 루트 폴더 (예: 현재 실행 위치)
    - subject_ID: 참가자 이름/ID
    """

    # 현재 날짜-시간 문자열 생성 (예: 2025-07-28_21-37-52)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # 저장 디렉토리 경로 생성
    save_dir = os.path.join(base_path, "data", f"{subject_ID}_{timestamp}")

    # 디렉토리 생성 (중복 방지)
    os.makedirs(save_dir, exist_ok=True)

    print(f"[INFO] Data will be saved to: {save_dir}")

    return save_dir