import os
import subprocess

# 设置参数
zoned_block_device = "nvme0n1"  # 替换为ZNS设备名称
key_size = 16  # 键的大小，单位为字节
value_size = 2048  # 值的大小，单位为字节（4KiB）
kv_num = 1000000  #
thread_counts = [1, 2, 4, 8, 16, 32, 64]  # 并发写入线程数量的列表
result_dir = "./wal_on"  # 存储结果文件的目录

# 创建或清理目录
if not os.path.exists(result_dir):
    os.makedirs(result_dir)

# 运行测试
for threads in thread_counts:
    print(f"Running db_bench with {threads} threads and WAL disabled...")
    result_file = os.path.join(result_dir, f"results_{threads}_threads.txt")
    command = [
        "sudo", "../db_bench",  # 使用sudo权限运行db_bench工具
        f"--fs_uri=zenfs://dev:{zoned_block_device}",  # 指定ZNS设备URI
        "--benchmarks=fillrandom",  # 基准测试类型为fillrandom
        f"--key_size={key_size}",  # 键的大小
        f"--value_size={value_size}",  # 值的大小
        f"--num={kv_num}",  # 写入键值对数量
        f"--threads={threads}",  # 并发写入线程数量
        "--compression_type=none",  # 不使用压缩
        "--write_buffer_size=67108864",  # 写缓冲区大小设置为64MB
        "--max_write_buffer_number=3",  # 最多三个写缓冲区
        "--target_file_size_base=67108864",  # 目标文件大小设置为64MB
        "--max_background_compactions=4",  # 后台压缩任务的最大数量
        "--max_background_flushes=2",  # 后台刷新的最大数量
        "--sync=0",  # 禁用同步写
        "--statistics=1",  # 启用统计信息
        "--use_direct_io_for_flush_and_compaction"
    ]
    # 运行命令并将结果保存到文件中
    with open(result_file, "w") as f:
        subprocess.run(command, stdout=f)
    print(f"Benchmark completed for [{threads}] threads. Results saved to {result_file}")

print("All benchmarks completed.")