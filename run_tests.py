# run_tests.py
# 项目的入口脚本，用于运行测试并生成报告

import os
import subprocess
import sys


PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
ALLURE_RESULTS_DIR = os.path.join(PROJECT_ROOT, "allure-results")
ALLURE_REPORT_DIR = os.path.join(PROJECT_ROOT, "allure-report")


def main():
    print("🚀 开始执行接口自动化测试...")

    # 1. 安装依赖 (如果 requirements.txt 存在)
    if os.path.exists(os.path.join(PROJECT_ROOT, "requirements.txt")):
        print("\n📦 正在安装项目依赖...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

    # 2. 运行 pytest 并生成 allure 原始数据
    print("\n🧪 正在运行 pytest 测试用例...")
    pytest_command = [
        "pytest",
        "test_cases/",  # 指定测试用例目录
        "-s",
        "-v",  # 详细输出
        "--alluredir", ALLURE_RESULTS_DIR  # 指定 allure 结果目录
    ]
    exit_code = subprocess.run(pytest_command).returncode

    if exit_code != 0:
        print(f"\n❌ 测试执行完毕，但部分用例失败。退出码: {exit_code}")

    # 3. 清理并生成 allure HTML 报告
    # print("\n📊 正在生成 Allure HTML 报告...")
    #
    # if os.path.exists(ALLURE_REPORT_DIR):
        import shutil
        shutil.rmtree(ALLURE_REPORT_DIR)  # 清理旧报告
    #
    # # generate_command = [
    # #     "allure", "generate",
    # #     ALLURE_RESULTS_DIR,
    # #     "-o", ALLURE_REPORT_DIR,
    # #     "--clean"
    # # ]
    # # subprocess.run(generate_command)
    # os.system(f"allure generate {ALLURE_RESULTS_DIR} -o {ALLURE_REPORT_DIR} --clean")
    #
    # # 4. 打开报告
    # print("\n🌐 正在打开 Allure 报告...")
    # # open_command = ["allure", "open", ALLURE_REPORT_DIR]
    # # subprocess.run(open_command)
    # os.system(f"allure open {ALLURE_REPORT_DIR} ")

    print("\n✅ 所有任务执行完毕！")


if __name__ == "__main__":
    main()