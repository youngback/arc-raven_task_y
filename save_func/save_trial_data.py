import os
import csv

def save_trial_data(trial_data, save_directory):
    """
    한 trial의 결과를 CSV에 저장
    - trial_data: dict 형태의 trial 결과
    - save_directory: 저장할 폴더 경로
    """

    save_path = os.path.join(save_directory, "results.csv")
    file_exists = os.path.isfile(save_path)

    with open(save_path, mode="a", newline='', encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=trial_data.keys())

        if not file_exists:
            writer.writeheader()  # 처음이면 헤더 생성
        writer.writerow(trial_data)

    print(f"[SAVE] Trial {trial_data['trial_idx']} 저장 완료")