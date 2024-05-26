import matplotlib.pyplot as plt
import numpy as np

# 配置样式和颜色
config = {
    "font.family": 'serif',
    "font.size": 18,
    "mathtext.fontset": 'stix',
    "font.serif": ['STSong'],
    "font.weight": 'normal'
}
plt.rcParams.update(config)

# 假设数据（请根据实际需要替换这些数据）
time = np.arange(0, 241, 10)  # 从0到240秒，每10秒一个数据点
# 创建基线数据，模拟更剧烈的波动
np.random.seed(0)
base_noise = np.random.normal(0, 10, len(time))  # 基本噪声
additional_noise1 = np.random.normal(0, 5, len(time))  # 为第一条线添加额外小幅噪声
additional_noise2 = np.random.normal(0, 5, len(time))  # 为第二条线添加额外小幅噪声
trend = np.linspace(0, -10, len(time))  # 创建一个轻微的下降趋势
data1 = 35 + trend + base_noise + additional_noise1  # 第一条线数据，基于噪声和趋势调整
data2 = 80 + trend + base_noise + additional_noise2  # 第二条线数据，与第一条线波动相似但有细微差异

# 绘图
plt.figure(figsize=(10, 6))
plt.plot(time, data1, label='NVMeVirt', color='#3C78D5', linewidth=2.5)  # 深蓝色, 线宽2.5
plt.plot(time, data2, label='Inspur NS800G2-Z', color='#C7E9B4', linewidth=2.5)  # 浅绿色, 线宽2.5

plt.xlabel('Time (s)')
plt.ylabel('RocksDB吞吐量 (KIOPS)')
plt.legend()
plt.grid(True, linestyle='-', alpha=0.7)  # 实线网格
plt.tight_layout()

# 设置边框宽度
frame = plt.gca()
frame.spines['bottom'].set_linewidth(2)
frame.spines['left'].set_linewidth(2)
frame.spines['right'].set_linewidth(2)
frame.spines['top'].set_linewidth(2)
plt.savefig('doudong.svg', format='svg')
plt.show()
