from psychopy import core, visual, event
from initialize import initialize
from load_func.load_arc_trials import load_arc_trials
from phase_func.phase_training import phase_training
from phase_func.phase_hint import phase_hint
from phase_func.phase_test import phase_test
from phase_func.phase_feedback import phase_feedback
from phase_func.phase_start import phase_start
from phase_func.phase_end import phase_end
from phase_func.phase_score import phase_score
from draw.draw_fixation import draw_fixation, wait_for_fixation_hover
from save_func.save_trial_data import save_trial_data
from save_func.save_frame_log import save_frame_log_total
import os

def main():
    visual_opt, device_opt, game_opt, _, save_directory = initialize()

    global_frame_log = []
    global_frame_count = 0
    global_clock = core.Clock()

    trial_list = load_arc_trials("stimuli/stim_order.txt")

    phase_start(visual_opt, device_opt, global_clock=global_clock, global_frame_log=global_frame_log)

    total_correct = 0
    for trial_idx, trial in enumerate(trial_list):

        # 1) Training
        for i, train_event in enumerate(trial["train"]):
            train_event['item_id'] = trial['task_id']
            train_event['trial_idx'] = i
            phase_training(train_event, visual_opt, device_opt, game_opt, save_directory, global_clock=global_clock, global_frame_log=global_frame_log)

        # Training 종료 후 십자선 표시 (frame loop 0.5초)
        draw_fixation(visual_opt, duration=0.5, global_clock=global_clock, global_frame_log=global_frame_log)

        # 2) Hint
        phase_hint( 
            hint_event=trial["test"],
            visual_opt=visual_opt,
            device_opt=device_opt,
            game_opt=game_opt,
            trial_idx=trial_idx,
            save_directory=save_directory,
            global_clock=global_clock,
            global_frame_log=global_frame_log
        )

        # Hint 종료 후 십자선 표시 (frame loop 0.5초)
        draw_fixation(visual_opt, duration=0.5, global_clock=global_clock, global_frame_log=global_frame_log)

        # 3) Test
        is_correct, choice_idx, layout, _, _ = phase_test(
            test_event=trial["test"],
            visual_opt=visual_opt,
            game_opt=game_opt,
            trial_idx=trial_idx,
            save_directory=save_directory,
            global_clock=global_clock,
            global_frame_log=global_frame_log
        )

        # 4) Feedback
        phase_feedback(
            is_correct=is_correct,
            choice_idx=choice_idx,
            layout=layout,
            visual_opt=visual_opt,
            game_opt=game_opt,
            trial_idx=trial_idx,
            save_directory=save_directory,
            global_clock=global_clock,
            global_frame_log=global_frame_log
        )

        # Feedback 종료 후 십자선 표시 (frame loop 0.5초)
        draw_fixation(visual_opt, duration=0.5, global_clock=global_clock, global_frame_log=global_frame_log)

        # 5) Score (내부가 프레임 루프면 그대로 사용)
        if is_correct:
            total_correct += 1
        phase_score(trial_idx, visual_opt, total_correct, save_directory, duration=2.0, global_clock=global_clock, global_frame_log=global_frame_log)

        # 6) Fixation 대기 (hover 프레임 루프)
        wait_for_fixation_hover(visual_opt, dwell=0.1, feedback=True, global_clock=global_clock, global_frame_log=global_frame_log)

        # 7) 결과 저장
        trial_result = {
            "trial_idx":     trial_idx + 1,
            "task_id":       trial["task_id"],
            "choices_perm":  trial["test"]["choices_perm"],
            "choice_idx":    choice_idx,
            "is_correct":    is_correct,
        }
        save_trial_data(trial_result, save_directory)

    phase_end(visual_opt)

    global_frame_count = len(global_frame_log)                                  # ★ NEW
    save_frame_log_total(
        trial_idx=len(trial_list),
        global_frame_log=global_frame_log,
        save_directory=save_directory,
        phase="total",
        total_frames=global_frame_count                                         # ★ NEW
    )
    core.quit()

if __name__ == '__main__':
    main()
