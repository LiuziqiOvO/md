> 各种小工具
>
> 各种编辑器的插件配置。





# Vscode

## vscdoe.Clang-format

在服务器安装：

```bash
sudo apt install clang-format 
```

记得在vscode配置 format on save

![image-20241104163653707](Tool.assets/image-20241104163653707.png)



# Jetbrain系列





# Typora

> 直接copy现有的主题文件夹就行了

显示宽度，



修改汉字、英文的字体样式，





# EasyN2N——虚拟局域网



windows端用EasyN2N客户端



服务器用apt-get install n2n  



# Syncthing——文件P2P同步器

Linux版:

[https://apt.syncthing.net/](https://apt.syncthing.net/)



```
tmux new-session -d -s split_session \; \
    new-window -d -n "split_11" "./split 1577808000000046 1580486400000000 11" \; \
    new-window -d -n "split_12" "./split 1577808000000046 1580486400000000 12" \; \
    new-window -d -n "split_13" "./split 1577808000000046 1580486400000000 13" \; \
    new-window -d -n "split_14" "./split 1577808000000046 1580486400000000 14" \; \
    new-window -d -n "split_15" "./split 1577808000000046 1580486400000000 1" \; \
    attach-session -t split_session

```



```bash
tmux new-session -d -s split_session \; \ 
	new-window -d -n "split_11" "./split 1577808000000046 1580486400000000 11" \; \ 
    new-window -d -n "split_12" "./split 1577808000000046 1580486400000000 12" \; \    
    new-window -d -n "split_13" "./split 1577808000000046 1580486400000000 13" \; \
    new-window -d -n "split_14" "./split 1577808000000046 1580486400000000 14" \; \
    new-window -d -n "split_15" "./split 1577808000000046 1580486400000000 15" \; \
    attach-session -t split_session  
```







tmux new-session -d -s split_session \; \    new-window -d -n "split_16" "./split 1577808000000046 1580486400000000 16" \; \    new-window -d -n "split_17" "./split 1577808000000046 1580486400000000 17" \; \    new-window -d -n "split_18" "./split 1577808000000046 1580486400000000 18" \; \    new-window -d -n "split_19" "./split 1577808000000046 1580486400000000 19" \; \    new-window -d -n "split_20" "./split 1577808000000046 1580486400000000 20" \; \    attach-session -t split_session
