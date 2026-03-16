# utils/data_loader.py
import yaml
import os


def load_yaml(file_path):
    """
    从指定路径加载并返回 YAML 文件的内容。

    :param file_path: YAML 文件的相对或绝对路径
    :return: 解析后的 Python 对象 (通常是 dict 或 list)
    """
    # 获取当前脚本所在目录的绝对路径
    base_dir = os.path.dirname(os.path.abspath(__file__))
    # 拼接成完整的文件路径
    full_path = os.path.join(base_dir, '..', file_path)

    try:
        with open(full_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        return data
    except FileNotFoundError:
        print(f"错误: 数据文件未找到 at {full_path}")
        raise
    except yaml.YAMLError as e:
        print(f"错误: 解析 YAML 文件失败 at {full_path}: {e}")
        raise