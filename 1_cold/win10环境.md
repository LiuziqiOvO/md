

# WeChat miniprogram

[云开发](https://www.cloudbase.net/community/guides/handbook/tcb21.html)

## Node.js

<img src="win10%E7%8E%AF%E5%A2%83.assets/image-20220426205445721.png" alt="image-20220426205445721" style="zoom:33%;" />![image-20220426205649891](win10%E7%8E%AF%E5%A2%83.assets/image-20220426205649891.png)

<img src="win10%E7%8E%AF%E5%A2%83.assets/image-20220426205659554.png" alt="image-20220426205659554" style="zoom:33%;" />

# Anaconda

装到D盘environment里了

Python:3.9

## TensorFlow:2.5.0

```bash
pip install tensorflow==2.5.0 -i https://pypi.mirrors.ustc.edu.cn/simple

pip install tensorflow-gpu==2.5.0 -i https://pypi.mirrors.ustc.edu.cn/simple
```



## Pytorch:1.11

![image-20220313150200779](%E5%85%B6%E4%BB%96.assets/image-20220313150200779.png)



```bash
conda install pytorch torchvision torchaudio cudatoolkit=11.3 -c pytorch
```



## CUDA:那就11.3吧

https://developer.nvidia.com/cuda-toolkit-archive

![image-20220313151031034](%E5%85%B6%E4%BB%96.assets/image-20220313151031034.png)

## cudnn:11.3

https://developer.nvidia.com/rdp/cudnn-archive

解压出cuda文件夹放入 刚才安装cuda的文件夹

C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.3

![image-20220313152938145](%E5%85%B6%E4%BB%96.assets/image-20220313152938145.png)



## 环境变量

![image-20220313153142615](%E5%85%B6%E4%BB%96.assets/image-20220313153142615.png)

## Test

```python
import torch
torch.cuda.is_available()
```

![](%E5%85%B6%E4%BB%96.assets/image-20220313153850029.png)



```python
import tensorflow as tf
tf.test.is_gpu_available()
```

![](%E5%85%B6%E4%BB%96.assets/image-20220313153923541.png)





# JDK8

官网登陆下载:https://www.oracle.com/java/technologies/downloads/#java11-windows

下载需要账号:http://bugmenot.com/view/oracle.com

## 配置环境变量:

添加JAVA_HOME

![image-20220421231534815](win10%E7%8E%AF%E5%A2%83.assets/image-20220421231534815.png)

增加系统变量:

![image-20220421231626393](win10%E7%8E%AF%E5%A2%83.assets/image-20220421231626393.png)

# WSL

[^]: https://blog.csdn.net/qq_35333978/article/details/113177819

## 安装WSL1

**启用windows功能**

**微软商店下载Ubuntu**

## WSL1 -> WSL2

**下载升级包**

https://wslstorestorage.blob.core.windows.net/wslblob/wsl_update_x64.msi

## 启动管理员身份的powershell:

打开powershell,输入
`Start-Process powershell -Verb runAs`



将WSL 2设置为默认版本，以后下载安装的ubnutu默认就是wsl2，也可以不执行这条命令

```bash
wsl --set-default-version 2
```

![img](环境.assets/20210126125555821.png)

看系统和版本信息

```bash
wsl -l -v
```

![img](环境.assets/20210126125656606.png)

**升级指令+验证**

```bash
wsl --set-version Ubuntu-20.04 2
wsl -l -v
```

## 美化

https://blog.csdn.net/huiruwei1020/article/details/107663355

Windows Terminal的配置文件

```json
"defaults":

   {

     // Put settings here that you want to apply to all profiles.

     "acrylicOpacity": 0.8, //背景透明度

      "useAcrylic": true, // 启用毛玻璃

     //"backgroundImage": "C:\\Users\\Liu\\Pictures\\ubuntu.jpg", //背景图片

     // "backgroundImageOpacity": 0.5, //图片透明度

     "backgroundImageStretchMode": "fill", //填充模式

     //"icon": "C:\\Users\\Liu\\Pictures\\最近\\1121490.png", //图标

     "fontFace": "JetBrainsMono NF", //字体

     "fontSize": 13, //文字大小

      //"colorScheme": "Solarized Light", //主题

     "cursorColor": "#FFFFFF", //光标颜色

     "cursorShape": "bar" //光标形状

    },
```









# VS code

**有的时候添加不上断点?**

​	好像也是因为文件名中英文问题



**调试的时候报错,找不到路径?No such file...**

​	含中文的路径不能调试



任务栏图标不见了



# Typora

修改字体：





# 其他



一个在线网站:compiler explorer, 可以把C语言转成汇编语言

21/8/17		我在services.msc里禁用了windows更新

21/11/22	  因为VsCode控制台总报异常,按照一篇博客, 更新并激活 PSReadline

如果有非常重要的事情没有处理完，不希望关机，那么可以打开cmd.exe命令行工具，在里面输入命令：shutdown -a这样就可以取消关机了。

`shutdown -a`	





