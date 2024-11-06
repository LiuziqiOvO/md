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
output_dir = 'disk'
io_engines = ['io_uring']
block_sizes = ['4k', '16k', '32k', '64k', '128k', '256k']
thread_counts = [1, 2, 4, 8, 16]
# Nature期刊经典蓝绿色系
colors_nature = ['#3C78D5', '#6B9DC2', '#7FCDB8', '#95D5BB', '#C7E9B4']

# Nature Communications期刊配色
colors_ncomms = ['#0072B2', '#009E73', '#D55E00', '#CC79A7', '#F0E442']

# Nature Medicine期刊配色
# colors_nmed = ['#0072B2', '#56B4E9', '#009E73', '#E69F00', '#F0E442']

# Nature Biotechnology期刊配色
# colors_nbio = ['#0072B2', '#009E73', '#CC79A7', '#D55E00', '#F0E442']

# Nature Physics期刊配色
# colors_nphys = ['#56B4E9', '#009E73', '#CC79A7', '#D55E00', '#F0E442']

colors = colors_nature
# 解析FIO输出文件中的带宽、IOPS和延迟
def parse_fio_output(output_file):
    with open(output_file, 'r') as f:
        content = f.read()
        bw_match = re.search(r'bw=([0-9]+)MiB/s', content)
        iops_match = re.search(r'IOPS=([0-9.]+[kM]?)', content)
        lat_match = re.search(r'avg=([0-9.]+)([mu]sec)', content)

        bw = int(bw_match.group(1)) if bw_match else None
        if iops_match:
            iops_str = iops_match.group(1)
            if 'k' in iops_str:
                iops = float(iops_str.rstrip('k')) * 1000
            elif 'M' in iops_str:
                iops = float(iops_str.rstrip('M')) * 1000000
            else:
                iops = float(iops_str)
        else:
            iops = None

        if lat_match:
            lat = float(lat_match.group(1))
            if lat_match.group(2) == 'msec':
                lat *= 1000  # 转换为usec
        else:
            lat = None

        return bw, iops, lat

# 收集数据
bw_results = {bs: [] for bs in block_sizes}
iops_results = {bs: [] for bs in block_sizes}
lat_results = {bs: [] for bs in block_sizes}

for bs in block_sizes:
    for num_threads in thread_counts:
        job_name = f"io_uring_{bs}_{num_threads}threads"
        output_file = f"{output_dir}/{job_name}.txt"
        bw, iops, lat = parse_fio_output(output_file)
        if bw is not None:
            bw_results[bs].append(bw)
        else:
            bw_results[bs].append(0)
        if iops is not None:
            iops_results[bs].append(iops / 1000)  # 转换为KIOPS
        else:
            iops_results[bs].append(0)
        if lat is not None:
            lat_results[bs].append(lat)
        else:
            lat_results[bs].append(0)

# 绘制带宽柱状图和平滑折线图
fig, ax = plt.subplots(figsize=(10, 6))
bar_width = 0.15
index = np.arange(len(block_sizes))


for i, num_threads in enumerate(thread_counts):
    bar_positions = index + i * bar_width
    bw_values = [bw_results[bs][i] for bs in block_sizes]
    ax.bar(bar_positions, bw_values, bar_width, label=f'{num_threads} threads', color=colors[i], edgecolor='black')  # 添加黑色边框

ax.set_xlabel('Block Size (KB)')
ax.set_ylabel('Bandwidth (MiB/s)')
ax.set_xticks(index + bar_width * (len(thread_counts) - 1) / 2)
ax.set_xticklabels(block_sizes)

legend = ax.legend(loc=2, ncol=1, fontsize=18)
legend.get_frame().set_alpha(0)
ax.grid(True, linestyle='--', alpha=1)
plt.tight_layout(pad=0)

ax.set_facecolor('#f7f7f7')
ax.set_ylim(0, 6000)
# 设置边框宽度与第一个图一致
frame = plt.gca()
frame.spines['bottom'].set_linewidth(2)
frame.spines['left'].set_linewidth(2)
frame.spines['right'].set_linewidth(2)
frame.spines['top'].set_linewidth(2)

plt.subplots_adjust(left=0.15, right=0.95, top=0.95, bottom=0.15)
pos1 = ax.get_position()
plt.savefig('./SVG/4_bw_vs_bs.svg', format='svg')

# 绘制IOPS柱状图和平滑折线图
fig, ax = plt.subplots(figsize=(10, 6))
for i, num_threads in enumerate(thread_counts):
    bar_positions = index + i * bar_width
    iops_values = [iops_results[bs][i] for bs in block_sizes]
    ax.bar(bar_positions, iops_values, bar_width, label=f'{num_threads} threads', color=colors[i], edgecolor='black')  # 添加黑色边框

ax.set_xlabel('Block Size (KB)')
ax.set_ylabel('Throughput (KIOPS)')
ax.set_xticks(index + bar_width * (len(thread_counts) - 1) / 2)
ax.set_xticklabels(block_sizes)

legend = ax.legend(loc=1, ncol=1, fontsize=26)
legend.get_frame().set_alpha(0)
ax.grid(True, linestyle='--', alpha=1)
plt.tight_layout(pad=0)
ax.set_facecolor('#f7f7f7')

# 设置边框宽度与第一个图一致
frame = plt.gca()
frame.spines['bottom'].set_linewidth(2)
frame.spines['left'].set_linewidth(2)
frame.spines['right'].set_linewidth(2)
frame.spines['top'].set_linewidth(2)

# 手动调整边距，确保图像边缘的一致性
plt.subplots_adjust(left=0.15, right=0.95, top=0.95, bottom=0.15)
ax.set_position([pos1.x0, pos1.y0, pos1.width, pos1.height])
ax.set_ylim(0, 1000)
plt.savefig('./SVG/5_iops_vs_bs.svg', format='svg')

plt.show()
