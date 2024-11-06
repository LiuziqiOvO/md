import os
import re
import matplotlib.pyplot as plt

# 定义结果目录和线程数量
result_dirs = {
    "WAL_disabled": "./WAL/wal_off",
    "WAL_enabled": "./WAL/wal_on"
}
thread_counts = [1, 2, 4, 8, 16, 32]
throughputs = {
    "WAL_enabled": [],
    "WAL_disabled": []
}

# 解析结果文件
for wal_status, result_dir in result_dirs.items():
    for threads in thread_counts:
        result_file = os.path.join(result_dir, f"results_{threads}_threads.txt")
        with open(result_file, "r") as f:
            content = f.read()
            # 使用正则表达式提取吞吐量（ops/sec）
            match = re.search(r'fillrandom\s*:\s*([\d.]+)\s*micros/op\s*([\d.]+)\s*ops/sec', content)
            if match:
                throughput = float(match.group(2)) / 1000  # 转换为KIOPS
                throughputs[wal_status].append(throughput)
            else:
                throughputs[wal_status].append(0)
                print(f"Throughput not found in {result_file}")

# 绘制图表
plt.figure(figsize=(10, 6))
for wal_status, throughput_values in throughputs.items():
    plt.plot(thread_counts, throughput_values, marker='o', linestyle='-', label=wal_status)

plt.xlabel('Number of Threads')
plt.ylabel('Throughput (KIOPS)')
plt.title('RocksDB Throughput: WAL Enabled vs. Disabled')
plt.legend()
plt.grid(True)
plt.savefig('throughput_comparison.png')
plt.show()

print(throughputs)