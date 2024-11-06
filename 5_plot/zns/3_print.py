import matplotlib.pyplot as plt
import numpy as np

# 设置样式和颜色
config = {
    "font.family": 'serif',
    "font.size": 24,
    "mathtext.fontset": 'stix',
    "font.serif": ['Times New Roman'],
    "font.weight": 'normal'
}
plt.rcParams.update(config)

# 数据
buffer_sizes = ['4', '8', '16', '64', '256']

# 恢复时间
# zenfs_kiops = [0.5, 1.1, 4, 12, 39]
# zafs_kiops = [0.4, 0.8, 1.1, 3, 6]

# IOPS
zenfs_kiops = [10, 16, 18.5, 30, 41]
zafs_kiops = [25, 40, 61, 72, 75]

x = np.arange(len(buffer_sizes))  # 标签位置
width = 0.35  # 柱状图的宽度

# Nature期刊经典蓝绿色系
colors_nature = ['#3C78D5', '#6B9DC2', '#7FCDB8', '#95D5BB', '#C7E9B4']

fig, ax = plt.subplots(figsize=(10, 6))
rects1 = ax.bar(x - width / 2, zenfs_kiops, width, label='ZenFS', color=colors_nature[2], edgecolor='black')
rects2 = ax.bar(x + width / 2, zafs_kiops, width, label='ZAFS', color=colors_nature[4], edgecolor='black')
# 添加文本标签、标题和自定义x轴标签等

# 吞吐量

# 恢复时间
# ax.set_ylabel('Recovery Time (seconds)')
# ax.set_xlabel('WAL Size (MiB)')
ax.set_xlabel('Buffer Size (KiB)')
ax.set_ylabel('Throughput (KIOPS)')

ax.set_xticks(x)
ax.set_xticklabels(buffer_sizes)
ax.set_ylim([0, 80])
legend = ax.legend(loc=2, ncol=1, fontsize=26)
legend.get_frame().set_alpha(0)
ax.grid(True, linestyle='--', alpha=1)
plt.tight_layout(pad=0)

# 删除网格线
# ax.grid(False)

ax.set_facecolor('#f7f7f7')

# 设置边框宽度
frame = plt.gca()
frame.spines['bottom'].set_linewidth(2)
frame.spines['left'].set_linewidth(2)
frame.spines['right'].set_linewidth(2)
frame.spines['top'].set_linewidth(2)
# 手动调整边距
plt.subplots_adjust(left=0.15, right=0.95, top=0.95, bottom=0.15)

# plt.tight_layout()
plt.savefig('./SVG/7_IOPS.svg', format='svg')
plt.show()
