import os
import argparse
import sys
from datetime import datetime

def rename_audio_files(folder_path, role_name, output_dir, log_prefix):
    # 创建带有时间戳的唯一输出文件名
    current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = f"{log_prefix}_文件对照表_{current_datetime}.txt"
    output_file = os.path.join(output_dir, log_filename)

    renamed_files = {}
    total_files = 0

    # 统计音频文件的总数
    for root, dirs, files in os.walk(folder_path):
        total_files += len([filename for filename in files if filename.endswith('.wav')])

    current_index = 0

    # 创建并更新进度条
    def update_progress_bar():
        nonlocal current_index
        current_index += 1
        progress = (current_index / total_files) * 100
        sys.stdout.write(f'\r[{int(progress)}%] {"#" * int(progress)}{" " * (100 - int(progress))}')
        sys.stdout.flush()

    # 遍历文件夹并重命名音频文件
    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            if filename.endswith('.wav'):
                current_index += 1
                update_progress_bar()
                new_filename = f"{role_name}_{current_index}.wav"
                while os.path.exists(os.path.join(root, new_filename)):
                    current_index += 1
                    new_filename = f"{role_name}_{current_index}.wav"
                new_filepath = os.path.join(root, new_filename)
                os.rename(os.path.join(root, filename), new_filepath)
                renamed_files[filename] = new_filename

    # 将重命名日志写入文本文件
    with open(output_file, 'w') as log_file:
        for old_name, new_name in renamed_files.items():
            log_file.write(f"{old_name} -> {new_name}\n")

    print("\n重命名完成。\n重命名日志为:", output_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="重命名音频文件")
    parser.add_argument("-n", "--name", required=True, help="角色名前缀")
    parser.add_argument("-o", "--output", default="./", help="输出的文件夹")
    parser.add_argument("-p", "--prefix", default="文件对照表", help="日志文件前缀")
    args = parser.parse_args()

    folder_path = os.path.join(os.getcwd(), 'raw_audio')  # 根据需要修改文件夹路径
    rename_audio_files(folder_path, args.name, args.output, args.prefix)
