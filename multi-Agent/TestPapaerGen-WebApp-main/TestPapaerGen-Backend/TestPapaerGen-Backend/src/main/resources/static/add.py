import sys
import socket
import time
def add_two_numbers(a, b):
    return a + b

if __name__ == "__main__":
    # 检查是否传入了两个参数
    if len(sys.argv) != 3:
        print("使用方法: python add.py <a> <b>")
        sys.exit(1)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # 将命令行参数转换为整数
        a = int(sys.argv[1])
        b = int(sys.argv[2])
        result = add_two_numbers(a, b)
        time.sleep(5)
        print(f"两数之和为: {result}")
    except ValueError:
        print("请输入整数作为参数。")
        sys.exit(1)