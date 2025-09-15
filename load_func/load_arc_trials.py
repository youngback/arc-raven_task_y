import os, random, glob

def load_arc_trials(order_file="stim_order.txt"):
    # ... (project_root, train_dir 등 경로 설정은 동일) ...
    here = os.path.dirname(os.path.abspath(__file__))
    project_root   = os.path.abspath(os.path.join(here, ".."))

    train_dir = os.path.join(project_root, "stimuli", "png", "train")
    test_dir = os.path.join(project_root, "stimuli", "png", "test")
    hint_dir = os.path.join(project_root, "stimuli", "png", "hint")
    choices_dir = os.path.join(project_root, "stimuli", "png", "choices")

    order_path = os.path.join(project_root, order_file)
    with open(order_path, "r", encoding="utf-8") as f:
        names = [ln.strip() for ln in f if ln.strip()]

    random.shuffle(names)

    trials = []
    for name in names:
        base = name if name.endswith(".json") else f"{name}.json"
        task_id = os.path.splitext(os.path.basename(base))[0]

        test_hint_path = os.path.join(hint_dir, "question_mark.png")
        
        # 3) train 세트의 '경로' 구성
        # [고정] 학습 세트 개수를 3으로 고정합니다.
        train_input_files = glob.glob(os.path.join(train_dir, f"{task_id}_train_input_*.png"))
        train_input_files.sort() # 파일 순서대로 정렬

        num_train_pairs = len(train_input_files) # 파일의 개수만큼 반복 횟수 설정

        train_list = []
        for i in range(1, num_train_pairs + 1):
            train_list.append({
                "train_input_path":  os.path.join(train_dir, f"{task_id}_train_input_{i}.png"),
                "train_output_path": os.path.join(train_dir, f"{task_id}_train_output_{i}.png"),
            })

        # test input (번호 붙는 경우)
        # 수정된 코드
        # test input (번호 붙는 경우)
        print(f"현재 작업 중인 task_id: {task_id}")
        test_input_path = glob.glob(os.path.join(test_dir, f"{task_id}_test_input_*.png"))[0]

        # phase_test의 choices (output은 번호 붙음)
        test_output_path = glob.glob(os.path.join(choices_dir, f"{task_id}_test_output_*.png"))[0]

        orig_paths = [
            test_output_path,
            os.path.join(choices_dir, f"{task_id}_choices_distractor1.png"),
            os.path.join(choices_dir, f"{task_id}_choices_distractor2.png"),
            os.path.join(choices_dir, f"{task_id}_choices_distractor3.png"),
        ]
        
        perm = list(range(4))
        random.shuffle(perm)
        shuffled_choice_paths = [orig_paths[i] for i in perm]
        correct_idx = perm.index(0)

        trials.append({
            "task_id": task_id,
            "train": train_list,
            "test": {
                "input_path": test_input_path,
                "choices_paths": shuffled_choice_paths,
                "correct_idx": correct_idx,
                "choices_perm": perm,  # 셔플 순서 보관
                "hint_path": test_hint_path,
            }
        })
        
    return trials