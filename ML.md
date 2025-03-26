# 环境

## Anaconda

### 虚拟环境创建

anaconda管理虚拟环境时的一些操作:

**1.列出所有环境**

`conda env list`

```bash
C:\Users\li>conda env list
# conda environments:
#
base * C:\Users\li\anaconda3
```

**2.新建环境**
现在新建一个python3.6的虚拟环境：(叫tf1 )
`conda create -n pytorch python=3.6`

，环境就建好了，可以装其它库了

**3.删除环境**
`conda env remove -n tensorflow1.14`

```bash
C:\Users\li>conda env remove -n tensorflow1.14
Remove all packages in environment C:\Users\li\anaconda3\envs\tensorflow1.14:
```

**4.使用环境**

[^注意！]: Win Terminal无法激活环境，非要进入CMD才可以？！

激活:

`activate tf1`

```bash
C:\Users\li>activate tf1
C:\Users\li>conda.bat activate tf1
(tf1) C:\Users\li>
```

退出:

`deactivate`



换源

```shell
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/
conda config --set show_channel_urls yes

#验证
conda config --show channels
```



## CUDA

据说直接在pytorch官网复制命令行来安装，是会自动安装CUDA的。



英伟达控制面板->帮助->系统信息->组件，去官网找大于这个版本的CUDA Tool 

https://developer.nvidia.com/cuda-toolkit-archive

![image-20221106155653007](ML.assets/image-20221106155653007.png)

安装CUDA，配置环境变量

![image-20221106163522008](ML.assets/image-20221106163522008.png)



验证

```
nvcc -V

set cuda
```







# Python

## Pytorch

View（）类似resize（），可以把矩阵转换为向量 感觉这个b东西效率





**文件匹配glob**

读某个目录下的所有匹配文件

```python
file_list = [f for f in glob.glob(data_path + "**/character*", recursive=True)]  # 一个list,含所有文件
```

**抽样**

random.sample

```python
img_dirs = random.sample(file_list, n_way)  # 从所有character文件夹中选出N个
```

**enumerate()**

enumerate() 函数用于将一个可遍历的数据对象(如列表、元组或字符串)组合为一个索引序列，同时列出数据和数据下标，一般用在 for 循环当中。

```python
# 遍历一个list 
for label, img_dir in enumerate(img_dirs):

>>>seasons = ['Spring', 'Summer', 'Fall', 'Winter']
>>> list(enumerate(seasons))
[(0, 'Spring'), (1, 'Summer'), (2, 'Fall'), (3, 'Winter')]
>>> list(enumerate(seasons, start=1))       # 下标从 1 开始
[(1, 'Spring'), (2, 'Summer'), (3, 'Fall'), (4, 'Winter')]
>>> tuple(enumerate(seasons, start=1))
((1, 'Spring'), (2, 'Summer'), (3, 'Fall'), (4, 'Winter'))
```











# 数学

目标：找到一个函数解决问题。模型是函数的集合。通过损失函数作衡量指标筛选出最好的函数



#### 偏差和方差

使用过于复杂的模型（例如高次式），使得训练集ACC很高，但测试集ACC反倒降低，叫过拟合。但，错误是如何产生的？

Bias	偏差

Variance	方差

![image-20221205164654203](ML.assets/image-20221205164654203.png)

横轴是最高次项幂指数。两种极端，左侧是未拟合，右侧是过拟合。

- More data
- Regularization 正则化



#### lecture3 Gradient Descent

Loss func：L（$\theta$）

Learningrate，寻找极值点时，每次横移的幅度

Adam

SGD

只考虑某一部分样本的偏差，用它来更新参数。

Feature Scaling

可以放大特征，增大影响

#### lecture4  classification 

eg：能否找一个func：输入七种属性（10,300,20）-> 输出类别



# 有监督和无监督

有监督学习：对具有概念标记（分类）的训练样本进行学习，以尽可能对训练样本集外的数据进行标记（分类）预测。这里，所有的标记（分类）是已知的。因此，训练样本的岐义性低。

无监督学习：对没有概念标记（分类）的训练样本进行学习，以发现训练样本集中的结构性知识。这里，所有的标记（分类）是未知的。因此，训练样本的岐义性高。聚类就是典型的无监督学习





# CNN

### 1.[卷积神经网络](https://so.csdn.net/so/search?q=卷积神经网络&spm=1001.2101.3001.7020)介绍

卷积神经网络（Convolutional Neural Networks）是一类包含卷积计算且具有[深度](https://so.csdn.net/so/search?q=深度&spm=1001.2101.3001.7020)结构的前馈神经网络（Feedforward Neural Networks），是深度学习（deep learning）的代表算法之一。

### 2.卷积神经网络的结构

卷积神经网络一般包含如下几种结构，输入层，卷积层，池化层，激活函数，全链接层，输出层。

### 2.1 输入层

输入层简单说就是一个矩阵，该矩阵表示输入图片的像素点

### 2.2 卷积层

卷积层是卷积神经网络的关键所在。首先要明白几个概念，input_size表示输入的矩阵的大小，filter_size表示卷积核的大小，stride表示步长，padding表示填充。
![在这里插入图片描述](ML.assets/d08be33809b9407f8ad16365ad6f4f27.png)

卷积：与卷积核对应位置相乘再相加，填入新的矩阵的对应位置。卷积核每次向右移动stride步长




![image-20221121214652601](ML.assets/image-20221121214652601.png)

### 2.3 池化层

池化层分为两种，分别为平均池化和最大池化，最大池化目前用的更多一些，简单的说和卷积很类似，卷积是点乘求和，最大池化则是点乘求最大值，平均池化则是点乘求平均。



### 2.4全连接层



### 激活函数ReLu

```
3、ReLU 的函数表达式和导数表达式

ReLU 的函数表达式：

当 x <= 0 时，ReLU = 0

当 x > 0 时，ReLU = x



ReLU 的导数表达式：

当 x<= 0 时，导数为 0

当 x > 0 时，导数为 1

```



## **交叉熵**损失函数

https://zhuanlan.zhihu.com/p/98785902

```python
loss_func = torch.nn.CrossEntropyLoss()
```

### 什么是交叉熵？

> 回忆
>
> 信息量：它是用来衡量一个事件的不确定性的；一个事件发生的概率越大，不确定性越小，则它所携带的信息量就越小。
>
> $ I(x_0)=−log(p(x_0))$
>
> 熵：它是用来衡量一个系统的混乱程度的，代表一个系统中信息量的总和；信息量总和越大，表明这个系统不确定性就越大。

**交叉熵主要是用来判定实际的输出与期望的输出的接近程度**，为什么这么说呢，举个例子：在做分类的训练的时候，如果一个样本属于第K类，那么这个类别所对应的的输出节点的输出值应该为1，而其他节点的输出都为0，即[0,0,1,0,….0,0]，这个数组也就是样本的Label，是神经网络最期望的输出结果。也就是说用它来衡量网络的输出与标签的差异，利用这种差异经过反向传播去更新网络参数。

**交叉熵：**它主要刻画的是实际输出（概率）与期望输出（概率）的距离，也就是交叉熵的值越小，两个概率分布就越接近。假设概率分布p为期望输出，概率分布q为实际输出， H(p,q) 为交叉熵，则



$H(p,q)=−∑x(p(x)logq(x)+(1−p(x))log(1−q(x)))$



Pytorch实际使用的是另外一种方式计算：

https://blog.csdn.net/XIAOSHUCONG/article/details/123527257

# HelloWorld——MINIST

https://zhuanlan.zhihu.com/p/445381875

epoch = 10 正确率在0.7左右

model

```python
import torch.nn as nn
import torch.nn.functional as F

class Net(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Conv2d(in_channels=1,out_channels=16,
                      kernel_size=(3,3),
                      stride=(1,1),
                      padding=1                     #MNIST是1x28x28
                      ),                            #16x28x28
            nn.MaxPool2d(kernel_size=2),            #16x14x14   每两个取一个大的作代替
            nn.Conv2d(16, 32, 3, 1, 1),             #32x14x14
            nn.MaxPool2d(2),                        #32x7x7
            nn.Flatten(),                           #??
            nn.Linear(32*7*7, 16),                  #全连接
            nn.ReLU(),
            nn.Linear(16,10)                        #16->10个数字

        )

    def forward(self,x):
        return self.net(x)


```

MNIST_train

```python
import torch
import torch.optim as optim
import torchvision
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
from model import Net

# def show():
#     fig = plt.figure()
#     for i in range(20):
#         plt.subplot(5, 4, i + 1)
#         plt.tight_layout()
#         plt.imshow(example_data[i][0], cmap='gray', interpolation='none')
#         plt.title("{}".format(example_targets[i]))
#         plt.xticks([])
#         plt.yticks([])
#     plt.show()

#超参数
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

# BATCH_SIZE=512 #大概需要2G的显存
BATCH_SIZE=128
EPOCHS=10 # 总共训练批次
LEARNING_RATE = 0.1

#准备训练数据集
# train_data = torchvision.datasets.MNIST(root="data",download=True,train=True,
#                                         transform=torchvision.transforms.ToTensor())
# test_data = torchvision.datasets.MNIST(root="data",download=True,train=True,
#                                         transform=torchvision.transforms.ToTensor())
train_loader = torch.utils.data.DataLoader(
        datasets.MNIST('data', train=True, download=True,
                       transform=transforms.transforms.ToTensor()
                       ),
        batch_size=BATCH_SIZE, shuffle=True)

test_loader = torch.utils.data.DataLoader(
        datasets.MNIST('data', train=False,
                       transform=transforms.transforms.ToTensor()
                       ),
        batch_size=BATCH_SIZE, shuffle=True)


# #看看是什么东西
# examples = enumerate(train_loader)
# batch_idx, (example_data, example_targets) = next(examples)
# print(example_targets)
# print(example_data.shape)
# #绘制一下
# show()

model  = Net().to(device)#模型实例化
# model = torch.load("my_cnn.nn")
print(device)

#验证一下模型
i = torch.zeros((64, 1, 28, 28)).to(device)
o = model(i)
print(o.shape)
optimizer = optim.SGD(model.parameters(),lr=LEARNING_RATE) #简单的优化器_Adam  换成了SGD 不知道是啥
# 交叉熵损失函数
loss_func = torch.nn.CrossEntropyLoss()
#train
cnt = 0
for cnt in range (EPOCHS):
    for imgs, labels in train_loader:
        imgs = imgs.to(device)             #张量加载到显卡
        labels = labels.to(device)
        outputs = model(imgs)
        loss = loss_func(outputs, labels)
        optimizer.zero_grad()              #清空优化器梯度?
        loss.backward()
        optimizer.step()
    # 测试
    total_loss = 0
    with torch.no_grad():#不需要反向传播,不要自动求导
        for imgs, labels in test_loader:
            imgs, labels = imgs.to(device), labels.to(device)
            ouputs = model(imgs)
            loss = loss_func(ouputs, labels)
            total_loss += loss
    print("第{}次训练的Loss= {}".format(cnt+1, total_loss))

torch.save(model, "my_cnn.nn")
```

# Omniglot

![image-20221205110003046](ML.assets/image-20221205110003046.png)

共659个字母，13180张图片

读数据集生成task：随机N=5类字母，每个选5个作为训练集（support-set）5个作为测试集（qry-set）

然后把图片缩放 resize:	150^2 -> 28^2

训练，周五交差

能跑了，但是精确度只有0.2



我按顺序赋值标签的方法是不是错了，导致数据有重复的label？

测试：创建一个Task，抽中了5类

![image-20221123212412828](ML.assets/image-20221123212412828.png)



2022年11月28日00:10:29：怎么改参数都是0.2左右，是不是应该加深一下网络。

2022年12月5日08:59:47:

```python
# 参数
BATCH_SIZE = 20
LEARNING_RATE = 0.01
EPOCH = 200
#1
54925 73075
0.4291015625
34790 93210
0.271796875
#2
59338 68662
0.463578125
41287 86713
0.3225546875
#3
53729 74271
0.4197578125
39966 88034
0.312234375
#1 +
第300次训练的Loss= 101.63298797607422 0.3578125
117734 74266
0.6131979166666667
63702 128298
0.33178125
#2
第300次训练的Loss= 139.2122039794922 0.3375
103699 88301
0.5400989583333333
62434 129566
0.32517708333333334
#1 +
第400次训练的Loss= 113.33164978027344 0.3625
173060 82940
0.676015625
84156 171844
0.328734375





BATCH_SIZE = 20
LEARNING_RATE = 0.001
EPOCH = 200
#1
第200次训练的Loss= 51.43522262573242 0.2859375
33375 94625
0.2607421875
29303 98697
0.2289296875
#2
第200次训练的Loss= 51.42981719970703 0.23125
34656 93344
0.27075
29897 98103
0.2335703125
#3
第200次训练的Loss= 51.43381118774414 0.2578125
32767 95233
0.2559921875
28816 99184
0.225125
#1 +
第400次训练的Loss= 51.427276611328125 0.290625
70316 185684
0.274671875
65005 190995
0.25392578125
#2
第400次训练的Loss= 51.271080017089844 0.2875
68332 187668
0.266921875
61881 194119
0.24172265625
#3
第400次训练的Loss= 51.38982009887695 0.265625
74464 181536
0.290875
62922 193078
0.2457890625
```



```python
BATCH_SIZE = 25
LEARNING_RATE = 0.001
EPOCH = 300
第300次训练的Loss= 41.439720153808594 0.3153846153846154
66073 128927
0.3388358974358974
55373 139627
0.28396410256410254

BATCH_SIZE = 25
LEARNING_RATE = 0.01
EPOCH = 300
#1
第300次训练的Loss= 64.36944580078125 0.4676923076923077
144782 50218
0.7424717948717948
79247 115753
0.40639487179487177
#2
第300次训练的Loss= 60.239219665527344 0.47692307692307695
144263 50737
0.7398102564102564
81814 113186
0.4195589743589744
#3
第300次训练的Loss= 68.53913879394531 0.4230769230769231
134973 60027
0.6921692307692308
73660 121340
0.37774358974358974
```

为什么batch_size不能超过25呢，是不是batchsize太小了。

```python
BATCH_SIZE = 25
LEARNING_RATE = 0.02
EPOCH = 300	
#1
第300次训练的Loss= 65.05277252197266 0.4646153846153846
159561 35439
0.8182615384615385
84523 110477
0.433451282051282
#2
第300次训练的Loss= 62.387550354003906 0.4492307692307692
156770 38230
0.8039487179487179
78074 116926
0.4003794871794872
#3
第300次训练的Loss= 73.57019805908203 0.40923076923076923
155046 39954
0.7951076923076923
70876 124124
0.36346666666666666
```



```
第300次训练的Loss= 75.75947570800781 0.41384615384615386
168831 26169
0.8658
76870 118130
0.3942051282051282
```





我的判断准确率判断部分写错了，应该 * 5 而且应该记录每轮训练的准确率

在background集上测试了一下:

```
10
测试task1:Loss=2.099950	TotalLoss=2.0999	0.4400 
测试task2:Loss=3.981541	TotalLoss=6.0815	0.3200 
测试task3:Loss=3.605023	TotalLoss=9.6865	0.3467 
测试task4:Loss=2.930782	TotalLoss=12.6173	0.3500 
测试task5:Loss=5.334642	TotalLoss=17.9519	0.3120 
测试task6:Loss=5.752121	TotalLoss=23.7041	0.2867 
测试task7:Loss=4.181776	TotalLoss=27.8858	0.2800 
测试task8:Loss=3.590770	TotalLoss=31.4766	0.2700 
测试task9:Loss=4.169700	TotalLoss=35.6463	0.2667 
测试task10:Loss=2.244910	TotalLoss=37.8912	0.2760 
0.276

torch.Size([500, 50])
32
测试task1:Loss=1.744952	TotalLoss=1.7450	0.1200 
测试task2:Loss=1.469772	TotalLoss=3.2147	0.2600 
测试task3:Loss=2.061525	TotalLoss=5.2762	0.1867 
测试task4:Loss=1.706653	TotalLoss=6.9829	0.2300 
测试task5:Loss=1.782263	TotalLoss=8.7652	0.2240 
测试task6:Loss=1.703696	TotalLoss=10.4689	0.2267 
测试task7:Loss=1.768759	TotalLoss=12.2376	0.2400 
测试task8:Loss=1.960901	TotalLoss=14.1985	0.2300 
测试task9:Loss=1.702912	TotalLoss=15.9014	0.2444 
测试task10:Loss=1.774151	TotalLoss=17.6756	0.2520 
测试task11:Loss=1.518143	TotalLoss=19.1937	0.2655 
测试task12:Loss=2.101199	TotalLoss=21.2949	0.2500 
测试task13:Loss=1.730107	TotalLoss=23.0250	0.2554 
测试task14:Loss=1.812097	TotalLoss=24.8371	0.2629 
测试task15:Loss=1.767329	TotalLoss=26.6045	0.2560 
测试task16:Loss=1.428192	TotalLoss=28.0327	0.2625 
测试task17:Loss=1.780707	TotalLoss=29.8134	0.2635 
测试task18:Loss=1.651194	TotalLoss=31.4646	0.2689 
测试task19:Loss=1.851734	TotalLoss=33.3163	0.2653 
测试task20:Loss=1.388348	TotalLoss=34.7046	0.2720 
测试task21:Loss=1.777555	TotalLoss=36.4822	0.2705 
测试task22:Loss=1.370603	TotalLoss=37.8528	0.2818 
测试task23:Loss=1.605832	TotalLoss=39.4586	0.2817 
测试task24:Loss=1.601142	TotalLoss=41.0598	0.2817 
测试task25:Loss=2.068468	TotalLoss=43.1282	0.2800 
测试task26:Loss=1.751526	TotalLoss=44.8798	0.2754 
测试task27:Loss=1.882560	TotalLoss=46.7623	0.2681 
测试task28:Loss=1.648179	TotalLoss=48.4105	0.2686 
测试task29:Loss=1.558971	TotalLoss=49.9695	0.2703 
测试task30:Loss=1.679587	TotalLoss=51.6491	0.2720 
测试task31:Loss=1.784416	TotalLoss=53.4335	0.2710 
测试task32:Loss=1.602976	TotalLoss=55.0365	0.2750 
0.275

3
测试task1:Loss=3.569178	TotalLoss=3.5692	0.4000 
测试task2:Loss=10.369054	TotalLoss=13.9382	0.2400 
测试task3:Loss=8.586445	TotalLoss=22.5247	0.2533 
0.25333333333333335

3
测试task1:Loss=7.023782	TotalLoss=7.0238	0.3200 
测试task2:Loss=4.293963	TotalLoss=11.3177	0.3600 
测试task3:Loss=10.624753	TotalLoss=21.9425	0.3067 
0.30666666666666664
进程已结束，退出代码为 0

3
测试task1:Loss=11.631614	TotalLoss=11.6316	0.4400 
测试task2:Loss=12.710258	TotalLoss=24.3419	0.4600 
测试task3:Loss=10.631117	TotalLoss=34.9730	0.4133 
0.41333333333333333

```



## 超参数

train loss 下降，val loss下降，说明网络仍在学习； 奈斯，继续训练
train loss 下降，val loss上升，说明网络开始过拟合了；赶紧停止，然后数据增强、正则
train loss 不变，val loss不变，说明学习遇到瓶颈；调小学习率或批量数目
train loss 不变，val loss下降，说明数据集100%有问题；检查数据集标注有没有问题
train loss 上升，val loss上升，说明网络结构设计不当，训练超参数设置不当，数据集经过清洗等问题。

```python
# loss曲线可视化
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'validation'], loc='upper left')
plt.show()
```



## GANormaly

异常检测：（区别于分类问题）异常检测问题中NG样本通常比较少，直接学习能区分NG样本的模型是很困难的。

所以：学习能区分OK样本的模型就好，只要跟OK长得不像的就认为是NG的。

自编码器（Autoencoder）是异常检测中比较经典的一种方法。它的解决思路是采用尽可能多的OK样本去学习一个自编码模型，由于该模型见过足够多的OK样本，因此它能够很好地将OK样本重建出来，而NG样本它是没见过的，因此它没法很好地重建出来。



![img](https://pic2.zhimg.com/80/v2-cce25acc373464dfd0602fc51d58c895_1440w.webp)

同时学习“原图->重建图”和“原图的编码->重建图的编码”两个映射关系。这样，该方法不仅对生成的图片外观（图片->图片）做了的约束，也对图片内容（图片编码->图片编码）做了约束。

再加上GAN中对抗训练的思想。上述结构作为生成网络G-Net，又定义了一个判别网络D-Net，通过交替训练生成网络和对抗网络，最终学到一个比较好的生成网络。

推理时，用于推断的不是原图和重建图的差异，而是第一部分编码器产生的隐空间特征（原图的编码）和第二部分编码器产生的隐空间特征（重建图的编码）的差异。

#### 损失函数

三个网络，G-Net中的encoder1,2，D-net，需要三个损失函数。

#### 推断

用于推断的不是原图和重建图的差距，而是计算z'和z的差异。（使用编码损失进行推断：

网络收敛以后，计算所有健康样本的编码损失，取最大值作为判别阈值。推断时，给定一张图片，计算损失值，若小于这个阈值即为健康样本；反之则为异常样本。

这种方法使得模型对图片中的微小变化不敏感，减少了噪声的影响









# 什么是ZERO - SHOT 









































# Bert-VITS2 

Bert-VITS2 ：

https://github.com/Stardust-minus/Bert-VITS2 

Fish Speech：

由 [Fish Audio](https://fish.audio/) 研发的基于 VQ-GAN 和 Llama 的多语种语音合成.

启动WEBUI：

```
python -m tools.webui \
    --llama-checkpoint-path "checkpoints/fish-speech-1.4" \
    --decoder-checkpoint-path "checkpoints/fish-speech-1.4/firefly-gan-vq-fsq-8x1024-21hz-generator.pth" \
    --decoder-config-name firefly_gan_vq
```

访问：

http://127.0.0.1:7860/?__theme=light



微调：

https://speech.fish.audio/zh/finetune/#1



https://huggingface.co/spaces/XzJosh/DZ-Bert-VITS2-2.3



# GPT-SOVITS











# XGBOOST相关

