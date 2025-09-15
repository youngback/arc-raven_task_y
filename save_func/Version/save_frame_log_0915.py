# sav_func/save_frame_log.py
import csv
import os

def save_frame_log_test(
    trial_idx: int,
    correct_idx: int,
    chosen_idx: int,
    is_correct: bool,
    rt: float,
    frame_log: list[dict],
    save_dir: str,
    subject_id: str = "",
    item_id: str = ""
):
    """
    - 파일명: trial_{trial_idx}_test.csv (덮어쓰기)
    - 메타 1블록 + 프레임 테이블
    - 좌표/시간은 그냥 문자열 포맷만 적용(결측 처리 X)
    """
    os.makedirs(save_dir, exist_ok=True)
    path = os.path.join(save_dir, f"trial_{trial_idx}_test.csv")

    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        # 메타
        w.writerow(["subject_ID","item_ID","trial","target_index","chosen_index","is_correct"])
        w.writerow([subject_id, item_id, trial_idx, correct_idx, chosen_idx, str(is_correct)])
        w.writerow([])  # 구분 빈줄

        # 헤더
        w.writerow(["frame","elapsed_time","icon_x","icon_y","event","rt"])

        # 본문
        for e in frame_log:
            w.writerow([
                f"{e['frame']:.0f}",
                f"{e['elapsed_time']:.4f}",
                f"{e['icon_x']:.2f}",
                f"{e['icon_y']:.2f}",
                e.get("event",""),
                (e.get("rt",""))
            ])


def save_frame_log_train(
    trial_idx: int,
    frame_log: list[dict],
    save_dir: str,
    subject_id: str = "",
    item_id: str = "",
    phase: str = "train"
):
    """
    Save training phase frame logs to CSV.

    Parameters:
    - trial_idx: trial number (int)
    - frame_log: list of dicts with keys ["frame", "elapsed_time", "icon_x", "icon_y"]
    - save_dir: directory to save CSV
    - subject_id: optional subject identifier
    - item_id: optional item identifier
    - phase: defaults to "train"
    
    Output CSV format:
    - trial_{trial_idx}_{phase}.csv
    - First block: meta information
    - Blank line
    - Second block: frame-by-frame log
    """
    
    os.makedirs(save_dir, exist_ok=True)
    file_path = os.path.join(save_dir, f"trial_{trial_idx}_{phase}.csv")

    with open(file_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)

        # 1) 메타 정보 작성
        writer.writerow(["subject_ID", "item_ID", "trial", "phase"])
        writer.writerow([subject_id, item_id, trial_idx, phase])
        writer.writerow([])  # 구분 빈줄

        # 2) 프레임별 로그 작성
        writer.writerow(["frame", "elapsed_time", "icon_x", "icon_y"])
        for entry in frame_log:
            writer.writerow([
                entry["frame"],
                f"{entry['elapsed_time']:.4f}",
                f"{entry['icon_x']:.2f}",
                f"{entry['icon_y']:.2f}"
            ])

import os
import csv

def save_frame_log_hint(
    trial_idx: int,
    frame_log: list[dict],
    save_dir: str,
    subject_id: str = "",
    item_id: str = "",
    rt: float | None = None
):
    """
    - 파일명: trial_{trial_idx}_hint.csv (덮어쓰기)
    - 메타 블록 + 프레임 테이블
    - 좌표/시간/RT는 문자열 포맷 적용
    - frame_log 원소에 {"frame","elapsed_time","icon_x","icon_y","event","rt"} 등이 들어있다고 가정
    """

    os.makedirs(save_dir, exist_ok=True)
    path = os.path.join(save_dir, f"trial_{trial_idx}_hint.csv")

    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        # 메타
        w.writerow(["subject_ID","item_ID","trial","phase"])
        w.writerow([subject_id, item_id, trial_idx, "hint"])
        w.writerow([])  # 구분 빈줄

        # 헤더
        w.writerow(["frame","elapsed_time","icon_x","icon_y","event","rt"])

        # 본문
        for e in frame_log:
            w.writerow([
                f"{e['frame']:.0f}",
                f"{e['elapsed_time']:.4f}",
                f"{e['icon_x']:.2f}",
                f"{e['icon_y']:.2f}",
                e.get("event",""),
                e.get("rt","")  # trial 전체 RT라면 여기서 같은 값으로 채워도 됨
            ])


def save_frame_log(trial_idx, frame_log, save_directory, phase):
    """
    간단한 프레임 로그 저장 (frame, elapsed_time만 기록)
    파일명: trial_{trial_idx}_{phase}.csv
    """
    os.makedirs(save_directory, exist_ok=True)
    file_path = os.path.join(save_directory, f"trial_{trial_idx}_{phase}.csv")

    with open(file_path, "w", newline='', encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)

        # 헤더
        writer.writerow(["frame", "elapsed_time"])

        # 내용
        for entry in frame_log:
            writer.writerow([
                entry["frame"],
                f"{entry['elapsed_time']:.4f}"
            ])