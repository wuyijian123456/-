# utils/data_loader.py
import json
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


def write_yaml(yaml_path,data):
    try:
        with open(yaml_path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f)
    except FileNotFoundError:
        print(f"错误: 数据文件未找到 at {yaml_path}")
        raise
    except yaml.YAMLError as e:
        print(f"错误: 解析 YAML 文件失败 at {yaml_path}: {e}")
        raise

def del_yaml_key(yaml_path,key):
    try:
        with open(yaml_path, 'w', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            if key in data:
                del data['key']
            write_yaml(data,f)
    except FileNotFoundError:
        print(f"错误: 数据文件未找到 at {yaml_path}")
        raise
    except yaml.YAMLError as e:
        print(f"错误: 解析 YAML 文件失败 at {yaml_path}: {e}")
        raise


def load_config(path="config.json",key=None):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    # 拼接成完整的文件路径
    full_path = os.path.join(base_dir, '..', path)
    """加载JSON配置文件"""
    if not os.path.exists(full_path):
        raise FileNotFoundError(f"配置文件不存在: {path}")

    with open(full_path, 'r', encoding='utf-8') as f:
        data= json.load(f)
        if key  is not None:
            data= data.get(key)
        # print(data)
        return data


# 全局配置对象，直接导入就能用
config = load_config()


load_yaml("config.json")



