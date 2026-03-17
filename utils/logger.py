import os
import json
import logging
import logging.handlers
import sys


from utils.data_loader import load_config


class ColoredFormatter(logging.Formatter):
    """带颜色的日志格式化器"""

    COLORS = {
        'DEBUG': '\033[36m',  # 青色
        'INFO': '\033[32m',  # 绿色
        'WARNING': '\033[33m',  # 黄色
        'ERROR': '\033[31m',  # 红色
        'CRITICAL': '\033[35m',  # 紫色
        'RESET': '\033[0m'  # 重置颜色
    }

    def __init__(self, fmt: str, datefmt: str, use_color: bool = True):
        super().__init__(fmt, datefmt)
        self.use_color = use_color

    def format(self, record):
        # 保存原始信息
        original_msg = record.msg
        levelname = record.levelname

        if self.use_color and levelname in self.COLORS:
            # 为不同级别添加颜色
            colored_levelname = f"{self.COLORS[levelname]}{levelname}{self.COLORS['RESET']}"
            record.levelname = colored_levelname

            # 为消息添加颜色
            # colored_msg = f"{self.COLORS[levelname]}{original_msg}{self.COLORS['RESET']}"
            # record.msg = colored_msg

        # 调用父类的 format 方法
        result = super().format(record)

        # 恢复原始信息
        record.msg = original_msg
        record.levelname = levelname

        return result


class LoggerConfig:
    """日志配置类，负责加载和验证配置文件"""

    @staticmethod
    def load_config(config_path: str = "config.json"):
        """加载 JSON 配置文件"""
        try:
            # with open(config_path, 'r', encoding='utf-8') as f:
            #     config = json.load(f)
            #
            # # 验证配置结构
            # if 'logger' not in config:
            #     raise ValueError("配置文件中缺少 'logger' 部分")
            config =load_config(config_path)

            logger_config = config['logger']

            # 验证必要字段
            required_fields = ['level', 'format']
            for field in required_fields:
                if field not in logger_config:
                    raise ValueError(f"配置文件中缺少必要的 '{field}' 字段")

            # 转换字符串级别为 logging 常量
            level_map = {
                'DEBUG': logging.DEBUG,
                'INFO': logging.INFO,
                'WARNING': logging.WARNING,
                'ERROR': logging.ERROR,
                'CRITICAL': logging.CRITICAL
            }

            if logger_config['level'].upper() in level_map:
                logger_config['level'] = level_map[logger_config['level'].upper()]
            else:
                raise ValueError(f"不支持的日志级别: {logger_config['level']}")

            return config

        except FileNotFoundError:
            raise FileNotFoundError(f"配置文件不存在: {config_path}")
        except json.JSONDecodeError as e:
            raise ValueError(f"JSON 配置文件格式错误: {e}")


class Logger:
    """应用程序日志类，封装日志功能"""
    _instance = None

    def __new__(cls, config_path: str = "config.json"):
        """单例模式，确保整个应用只有一个日志实例"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, config_path: str = "config.json"):
        """初始化日志器"""
        if self._initialized:
            return

        # 加载配置
        self.config = LoggerConfig.load_config(config_path)
        self.logger = logging.getLogger('AppLogger')
        self.logger.setLevel(self.config['logger']['level'])

        # 清除已有的处理器
        self.logger.handlers.clear()

        # 创建格式化器
        formatter = ColoredFormatter(
            fmt=self.config['logger']['format']['pattern'],
            datefmt=self.config['logger']['format']['date_format'],
            use_color=self.config['logger']['color']
        )

        # 添加控制台处理器
        if self.config['logger']['console']['enabled']:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)

        # 添加文件处理器
        if self.config['logger']['file']['enabled']:
            log_path = self.config['logger']['file']['path']
            # 确保日志目录存在
            log_dir = os.path.dirname(log_path)
            if log_dir and not os.path.exists(log_dir):
                os.makedirs(log_dir)

            file_handler = logging.handlers.RotatingFileHandler(
                filename=log_path,
                maxBytes=self.config['logger']['file']['max_size'],
                backupCount=self.config['logger']['file']['backup_count'],
                encoding='utf-8'
            )
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

        self._initialized = True

    def get_logger(self) -> logging.Logger:
        """获取日志器实例"""
        return self.logger

    def debug(self, msg: str, *args, **kwargs):
        """记录 DEBUG 级别日志"""
        self.logger.debug(msg, *args, **kwargs)

    def info(self, msg: str, *args, **kwargs):
        """记录 INFO 级别日志"""
        self.logger.info(msg, *args, **kwargs)

    def warning(self, msg: str, *args, **kwargs):
        """记录 WARNING 级别日志"""
        self.logger.warning(msg, *args, **kwargs)

    def error(self, msg: str, *args, **kwargs):
        """记录 ERROR 级别日志"""
        self.logger.error(msg, *args, **kwargs)

    # def critical(self, msg: str, *args, **kwargs):
    #     """记录 CRITICAL 级别日志"""
    #     self.logger.critical(msg, *args, **kwargs)

    def log(self, level: int, msg: str, *args, **kwargs):
        """记录指定级别的日志"""
        self.logger.log(level, msg, *args, **kwargs)


# 创建全局日志实例
logger = Logger()

# 使用示例
if __name__ == "__main__":
    # 获取日志器
    logger = logger.get_logger()

    # 记录不同级别的日志
    logger.debug("这是一条调试信息")
    logger.info("这是一条信息")
    logger.warning("这是一条警告")
    logger.error("这是一条错误")
    # logger.critical("这是一条严重错误")

    # 也可以直接使用实例方法
    logger.info("使用实例方法记录信息")