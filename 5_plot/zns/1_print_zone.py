import os
import re
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline

config = {
    "font.family": 'serif',
    "font.size": 24,
    "mathtext.fontset": 'stix',
    "font.serif": ['Times New Roman'],
    "font.weight": 'normal'
}
plt.rcParams.update(config)

# 配置
output_dir = 'zone'
io_engines = ['sync', 'libaio', 'io_uring']
block_sizes = ['4K', '16K', '32K', '64K', '128K', '256K']
colors_nature = ['#6B9DC2', '#7FCDB8', '#C7E9B4']
colors = colors_nature


# 解析FIO输出文件中的带宽
def parse_fio_output_BW(output_file):
    with open(output_file, 'r') as f:
        content = f.read()
        match = re.search(r'bw=([0-9]+)MiB/s', content)
        if match:
            return int(match.group(1))
    return None


# 解析FIO输出文件中的IOPS
def parse_fio_output_IOPS(output_file):
    with open(output_file, 'r') as f:
        content = f.read()
        match = re.search(r'IOPS=([0-9.]+[kM]?)', content)
        if match:
            iops_str = match.group(1)
            if 'k' in iops_str:
                return float(iops_str.rstrip('k')) * 1000
            elif 'M' in iops_str:
                return float(iops_str.rstrip('M')) * 1000000
            else:
                return float(iops_str)
    return None


# 解析
bw_results = {engine: [] for engine in io_engines}
iops_results = {engine: [] for engine in io_engines}
for engine in io_engines:
    for bs in block_sizes:
        job_name = f"{engine}_{bs}"
        output_file = f"{output_dir}/{job_name}.txt"
        bw = parse_fio_output_BW(output_file)
        iops = parse_fio_output_IOPS(output_file)
        if bw is not None:
            bw_results[engine].append(bw)
        else:
            bw_results[engine].append(0)  # 如果没有找到带宽数据，设置为0
        if iops is not None:
            iops_results[engine].append(iops / 1000)  # 转换为KIOPS
        else:
            iops_results[engine].append(0)  # 如果没有找到IOPS数据，设置为0

# 绘制带宽柱状图和平滑折线图
fig, ax = plt.subplots(figsize=(10, 6))
bar_width = 0.2
index = np.arange(len(block_sizes))

for i, engine in enumerate(io_engines):
    bar_positions = index + i * bar_width
    bw_values = [bw_results[engine][j] for j in range(len(block_sizes))]
    ax.bar(bar_positions, bw_values, bar_width, label=engine, color=colors[i], edgecolor='black')

ax.set_xlabel('Block Size (KB)')
ax.set_ylabel('Bandwidth (MiB/s)')
ax.set_xticks(index + bar_width * (len(io_engines) - 1) / 2)
ax.set_xticklabels(block_sizes)
ax.set_ylim(0, 2500)

legend = ax.legend(loc=2, ncol=1, fontsize=24)
legend.get_frame().set_alpha(0)
ax.grid(True, linestyle='--', alpha=1)
plt.tight_layout(pad=0)

# 确保原点对齐
pos1 = ax.get_position()
# plt.tight_layout()

frame = plt.gca()
frame.spines['bottom'].set_linewidth(2)
frame.spines['left'].set_linewidth(2)
frame.spines['right'].set_linewidth(2)
frame.spines['top'].set_linewidth(2)
plt.subplots_adjust(left=0.15, right=0.95, top=0.95, bottom=0.15)
plt.savefig('./SVG/2_zone_bw.svg', format='svg')

# 绘制IOPS柱状图和平滑折线图
fig, ax = plt.subplots(figsize=(10, 6))
for i, engine in enumerate(io_engines):
    bar_positions = index + i * bar_width
    iops_values = [iops_results[engine][j] for j in range(len(block_sizes))]
    ax.bar(bar_positions, iops_values, bar_width, label=engine, color=colors[i], edgecolor='black')

ax.set_xlabel('Block Size (KiB)')
ax.set_ylabel('Throughput (KIOPS)')  # 修改Y轴标签
ax.set_xticks(index + bar_width * (len(io_engines) - 1) / 2)
ax.set_xticklabels(block_sizes)

ax.set_ylim(0, 80)

legend = ax.legend(loc=1, ncol=1, fontsize=24)
legend.get_frame().set_alpha(0)
ax.grid(True, linestyle='--', alpha=1)
plt.tight_layout(pad=0)

ax.set_position([pos1.x0, pos1.y0, pos1.width, pos1.height])
plt.tick_params(direction='out', width=2, length=5)

# plt.tight_layout()

# 设置边框宽度与第一张图一致
frame = plt.gca()
frame.spines['bottom'].set_linewidth(2)
frame.spines['left'].set_linewidth(2)
frame.spines['right'].set_linewidth(2)
frame.spines['top'].set_linewidth(2)

# 手动调整边距，确保图像边缘的一致性
plt.subplots_adjust(left=0.15, right=0.95, top=0.95, bottom=0.15)

plt.savefig('./SVG/3_zone_iops.svg', format='svg')

plt.show()
