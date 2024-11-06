import os
import re
import matplotlib.pyplot as plt

# 定义结果目录和value sizes
result_dir = "./WAL/wal_on"  #
value_sizes = [64, 128, 256, 512, 1024, 2048, 4096]
throughputs = []

# 解析结果文件
for value_size in value_sizes:
    result_file = os.path.join(result_dir, f"results_value_size_{value_size}.txt")
    with open(result_file, "r") as f:
        content = f.read()
        # 使用正则表达式提取吞吐量（ops/sec）
        match = re.search(r'fillrandom\s*:\s*([\d.]+)\s*micros/op\s*([\d.]+)\s*ops/sec', content)
        if match:
            throughput = float(match.group(2)) / 1000  # 转换为KIOPS
            throughputs.append(throughput)
        else:
            throughputs.append(0)
            print(f"Throughput not found in {result_file}")

# 绘制图表
plt.figure(figsize=(10, 6))
plt.plot(value_sizes, throughputs, marker='o', linestyle='-', label='WAL Enabled')

plt.xlabel('Value Size (bytes)')
plt.ylabel('Throughput (KIOPS)')
plt.title('RocksDB Throughput at Different Value Sizes (WAL Enabled)')
plt.xticks(value_sizes)  # 设置横坐标为指定的值大小
plt.legend()
plt.grid(True)
plt.savefig('throughput_comparison_value_size.png')
plt.show()

print(throughputs)
