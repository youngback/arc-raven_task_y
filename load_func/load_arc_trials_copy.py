# load_func/load_arc_trials.py
# 기존 load_stim_order.py의 내용 포함하였음.

import os, json, random

def load_arc_trials(order_file="stim_order.txt"):
    """
    1) stim_order.txt에서 파일명(또는 task_id) 읽기
    2) evaluation/<id>.json, distractor/<id>_with_distractors.json 로드
    3) train(list), test(input/choices/correct_idx) 구성해서 trials 리스트 반환
    """
    here = os.path.dirname(os.path.abspath(__file__))
    project_root   = os.path.abspath(os.path.join(here, ".."))
    eval_dir       = os.path.join(project_root, "stimuli", "corpus", "ExtendToBoundary")
    distractor_dir = os.path.join(project_root, "stimuli", "corpus_distractor", "ExtendToBoundary_distractor")

    # 1) 순서 읽기
    order_path = os.path.join(project_root, order_file)
    with open(order_path, "r", encoding="utf-8") as f:
        names = [ln.strip() for ln in f if ln.strip()]

    trials = []
    for name in names:
        base = name if name.endswith(".json") else f"{name}.json"
        task_id = os.path.splitext(os.path.basename(base))[0]

        # 2) 본문/디스트랙터 파일 로드
        with open(os.path.join(eval_dir, base), "r", encoding="utf-8") as f:
            d_eval = json.load(f)
        with open(os.path.join(distractor_dir, f"{task_id}_with_distractors.json"), "r", encoding="utf-8") as f:
            d_dist = json.load(f)

        # 3) train(리스트), test(input) 추출  ← 네 JSON 구조 기준
        train_list = d_eval["train"]                        # [{input:2D, output:2D}, ...]
        test_input = d_eval["test"][0]["input"]             # 2D

        # 4) choices 구성(정답+오답3, 셔플)
        orig = [d_dist["output"], d_dist["distractor1"], d_dist["distractor2"], d_dist["distractor3"]]
        perm = list(range(4))
        random.shuffle(perm)
        choices = [orig[i] for i in perm]
        correct_idx = perm.index(0)  # 원래 0번이 정답이므로, 셔플 후 위치가 정답 인덱스

        # 5) trial 표준 스키마
        trials.append({
            "task_id": task_id,
            "stim_file": base,
            "distractor_file": f"{task_id}_with_distractors.json",
            "train": train_list,
            "test": {
                "input": test_input,
                "choices": choices,     # 셔플된 4개
                "correct_idx": correct_idx,
                "choices_perm": perm,   # ← 셔플 순서 보관 (원본 인덱스→현재 인덱스)
            }
        })

    return trials