import matplotlib.pyplot as plt
import numpy as np

# 设置样式和颜色
config = {
    "font.family": 'serif',
    "font.size": 24,
    "mathtext.fontset": 'stix',
    "font.serif": ['STSong'],
    "font.weight": 'normal'
}
plt.rcParams.update(config)

# 数据
buffer_sizes = ['4', '8', '16', '64', '256']
# zenfs_kiops = [10, 15, 18, 30, 40]
# zafs_kiops = [25, 40, 60, 70, 75]

zenfs_kiops = [0.5, 1.1, 4, 12, 40]
zafs_kiops = [0.4, 0.8, 1.1, 3, 6]


x = np.arange(len(buffer_sizes))  # 标签位置
width = 0.35  # 柱状图的宽度

# Nature期刊经典蓝绿色系
colors_nature = ['#3C78D5', '#6B9DC2', '#7FCDB8', '#95D5BB', '#C7E9B4']

# Nature Communications期刊配色
colors_ncomms = ['#0072B2', '#009E73', '#D55E00', '#3C78D5', '#F0E442']

# 009E73

fig, ax = plt.subplots(figsize=(12, 8))
rects1 = ax.bar(x - width/2, zenfs_kiops, width, label='ZenFS', color='#3C78D5', edgecolor='black')
rects2 = ax.bar(x + width/2, zafs_kiops, width, label='ZAFS', color='#95D5BB', edgecolor='black')

# 添加文本标签、标题和自定义x轴标签等
# ax.set_ylabel('吞吐量 (KIOPS)')
# ax.set_xlabel('Buffer Size(KiB)')
ax.set_ylabel('数据恢复时间(sec)')
ax.set_xlabel('WAL size(MiB)')

# ax.set_title('ZAFS 和 ZenFS 性能测试 (db_bench, fillrandom, 4KiB requests)')
ax.set_xticks(x)
ax.set_xticklabels(buffer_sizes)
ax.legend()

ax.grid(True, linestyle='-', alpha=0.7)
ax.set_facecolor('#f7f7f7')

# 设置边框宽度
frame = plt.gca()
frame.spines['bottom'].set_linewidth(2)
frame.spines['left'].set_linewidth(2)
frame.spines['right'].set_linewidth(2)
frame.spines['top'].set_linewidth(2)

plt.tight_layout()
plt.savefig('recovery_time.svg', format='svg')
plt.show()
