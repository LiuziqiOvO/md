import matplotlib.pyplot as plt
import numpy as np

# 配置样式和颜色
config = {
    "font.family": 'serif',
    "font.size": 24,
    "mathtext.fontset": 'stix',
    "font.serif": ['Times New Roman'],
    "font.weight": 'normal'
}
plt.rcParams.update(config)

# 假设数据（请根据实际需要替换这些数据）
time = np.arange(0, 241, 10)  # 从0到240秒，每10秒一个数据点
# 创建基线数据，模拟更剧烈的波动
np.random.seed(0)
base_noise = np.random.normal(0, 8, len(time))  # 基本噪声
additional_noise1 = np.random.normal(0, 5, len(time))  # 为第一条线添加额外小幅噪声
additional_noise2 = np.random.normal(0, 5, len(time))  # 为第二条线添加额外小幅噪声
trend = np.linspace(0, -10, len(time))  # 创建一个轻微的下降趋势
data1 = 35 + trend + base_noise + additional_noise1  # 第一条线数据，基于噪声和趋势调整
data2 = 80 + trend + base_noise + additional_noise2  # 第二条线数据，与第一条线波动相似但有细微差异

# 绘图
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(time, data1, label='NVMeVirt', color='#3C78D5', linewidth=2.5)  # 深蓝色, 线宽2.5
ax.plot(time, data2, label='Inspur NS800G2-Z', color='#C7E9B4', linewidth=2.5)  # 浅绿色, 线宽2.5

# 设置坐标轴标签
ax.set_xlabel('Time (s)')
ax.set_ylabel('Throughput (KIOPS)')

# 设置固定的坐标轴范围
ax.set_xlim([0, 240])
ax.set_ylim([0, 100])

# 添加网格线
ax.grid(True, linestyle='-', alpha=0.7)  # 实线网格

# 设置图例
legend = ax.legend(loc=1, ncol=1, fontsize=26)
legend.get_frame().set_alpha(0)
# 设置边框宽度
for spine in ax.spines.values():
    spine.set_linewidth(2)

# 自动调整布局
# plt.tight_layout()

frame = plt.gca()
frame.spines['bottom'].set_linewidth(2)
frame.spines['left'].set_linewidth(2)
frame.spines['right'].set_linewidth(2)
frame.spines['top'].set_linewidth(2)

plt.grid(linestyle='--', linewidth=1)
plt.tight_layout(pad=0)

# 手动调整边距，确保图像边缘的一致性
plt.subplots_adjust(left=0.1, right=0.95, top=0.95, bottom=0.15)

# 保存图像
plt.savefig('./SVG/1_NVMevirt.svg', format='svg')
plt.show()
