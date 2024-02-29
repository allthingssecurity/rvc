import os
import argparse
from random import shuffle

def i18n(text):
    # Assuming '是' means yes, adjust according to the function's real behavior
    return True

def click_train(exp_dir1, sr2, if_f0_3, spk_id5):
    now_dir = os.getcwd()  # Assuming now_dir is the current working directory
    exp_dir = f"{now_dir}/logs/{exp_dir1}"
    os.makedirs(exp_dir, exist_ok=True)
    gt_wavs_dir = f"{exp_dir}/0_gt_wavs"
    co256_dir = f"{exp_dir}/3_feature256"

    if (if_f0_3):
        print("entered f03")
        f0_dir = "%s/2a_f0" % (exp_dir)
        f0nsf_dir = "%s/2b-f0nsf" % (exp_dir)
        names = (
            set([name.split(".")[0] for name in os.listdir(gt_wavs_dir)])
            & set([name.split(".")[0] for name in os.listdir(co256_dir)])
            & set([name.split(".")[0] for name in os.listdir(f0_dir)])
            & set([name.split(".")[0] for name in os.listdir(f0nsf_dir)])
        )
    else:
        print("didnt enter f03")
        names = set([name.split(".")[0] for name in os.listdir(gt_wavs_dir)]) & set(
            [name.split(".")[0] for name in os.listdir(co256_dir)]
        )
    opt = []
    for name in names:
        if (if_f0_3):
            print("appending to opt")
            opt.append(
                "%s/%s.wav|%s/%s.npy|%s/%s.wav.npy|%s/%s.wav.npy|%s"
                % (
                    gt_wavs_dir.replace("\\", "\\\\"),
                    name,
                    co256_dir.replace("\\", "\\\\"),
                    name,
                    f0_dir.replace("\\", "\\\\"),
                    name,
                    f0nsf_dir.replace("\\", "\\\\"),
                    name,
                    spk_id5,
                )
            )
        else:
            print("if not f03")
            opt.append(
                "%s/%s.wav|%s/%s.npy|%s"
                % (
                    gt_wavs_dir.replace("\\", "\\\\"),
                    name,
                    co256_dir.replace("\\", "\\\\"),
                    name,
                    spk_id5,
                )
            )
    if (if_f0_3):
        print("entered f03 again")
        for _ in range(2):
            opt.append(
                "%s/logs/mute/0_gt_wavs/mute%s.wav|%s/logs/mute/3_feature256/mute.npy|%s/logs/mute/2a_f0/mute.wav.npy|%s/logs/mute/2b-f0nsf/mute.wav.npy|%s"
                % (now_dir, sr2, now_dir, now_dir, now_dir, spk_id5)
            )
    else:
        print("not f03")
        for _ in range(2):
            opt.append(
                "%s/logs/mute/0_gt_wavs/mute%s.wav|%s/logs/mute/3_feature256/mute.npy|%s"
                % (now_dir, sr2, now_dir, spk_id5)
            )
    shuffle(opt)
    print("after shuffle")
    with open(f"{exp_dir}/filelist.txt", "w") as f:
        f.write("\n".join(opt))
    print("write filelist done")
    #print("use gpus:", gpus16)

def main():
    parser = argparse.ArgumentParser(description="Process audio files for training.")
    parser.add_argument("--exp_dir1", required=True, help="Experiment directory name")
    parser.add_argument("--sr2", required=True, help="Sample rate or identifier for mute files")
    parser.add_argument("--if_f0_3", required=True, help="Flag to process F0 directories ('是' for yes)")
    parser.add_argument("--spk_id5", required=True, help="Speaker ID")
    args = parser.parse_args()
    
    click_train(args.exp_dir1, args.sr2, args.if_f0_3, args.spk_id5)

if __name__ == "__main__":
    main()


    