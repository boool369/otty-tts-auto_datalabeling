import subprocess
import os


# 获取当前文件所在文件夹的绝对路径
current_directory = os.path.dirname(os.path.abspath(__file__))


# 构建虚拟环境的路径
env_path = os.path.join(current_directory, "envs")

env_name = "autolabeling"

envs_path = os.path.join(env_path, env_name)

# model path
model_path = os.path.join(current_directory, "Model")


def create_conda_env():
    try:
        # 创建Conda虚拟环境
        subprocess.check_call(
            ["conda", "create", "--prefix", envs_path, "python=3.8"])
        print(f"Conda虚拟环境 创建成功！")
        subprocess.check_call(
            ["conda", "config", "--append", "envs_dirs", env_path])
        print("conda 环境已添加")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Conda虚拟环境创建失败: {e}")
        return False


def install_requirements(requirements_file):
    try:
        # 激活虚拟环境
        subprocess.run(f"conda activate {env_name} && pip install -r {requirements_file}", shell=True, executable="/bin/bash")

        print("依赖安装成功！")

    except subprocess.CalledProcessError as e:
        print(f"依赖安装失败: {e}")
        return False


def install_model(model_url):
    try:
        subprocess.check_call(["git", "clone", model_url, model_path])
        print("模型安装成功")
    except subprocess.CalledProcessError as e:
        print(f"model安装失败: {e}")
        return False


if __name__ == "__main__":
    current_directory = os.path.dirname(__file__)  # 获取当前文件所在的文件夹绝对路径
    requirements_file = current_directory + \
        "/requirements.txt"
    # 创建Conda虚拟环境
    if create_conda_env():
        # 安装依赖
        install_requirements(requirements_file)
    # 安装模型
    model_url = "https://huggingface.co/hezhaoqia/speech_paraformer-large_asr_nat-zh-cn-16k-common-vocab8404-pytorch"
    install_model(model_url)
