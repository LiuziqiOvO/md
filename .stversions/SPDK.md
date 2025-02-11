# SPDK



## OCF

(Open CAS Framework)

> https://www.cnblogs.com/whl320124/articles/12409621.html

SPDK 在 19.01 的release中，引入了新的bdev模块OCF（全称：Open CAS Framework）
CAS （Intel Cache Acceleration Software）相当于企业版的OCF library + Linux Adapter。OCF 其实就是CAS 的cache engine的开源库。



欢迎访问OCF 官方网站：
https://open-cas.github.io 以获得更加详细的文档和资料。
OCF代码库：
https://github.com/Open-CAS/ocf 



## SPDK及OCF安装配置 (v22.01)

下载和准备

```bash
git clone <https://github.com/spdk/spdk.git>
cd spdk
git checkout v22.01

# 初始化子模块
git submodule update --init

# 切换ocf版本
cd ocf
git checkout v21.6.4

# 查看当前分支
git status
```

编译配置

```bash
cd ..
cp scripts/pkgdep/centos.sh scripts/pkgdep/openeuler.sh
vim scripts/pkgdep/openeuler.sh

# 修改第104行
# 将 yum install -y python3-configshell python3-pexpect
# 改为
yum install -y python3-configshell # python3-pexpect
sh scripts/pkgdep.sh

# configure
./configure --with-ocf --with-rbd --with-vfio-user
```

尝试编译`make -j`

不通过，继续依赖安装

- 基本编译工具
  - gcc gcc-c++ make cmake
- Python相关工具和模块
  - python3-pip
  - meson
  - ninja
  - pyelftools
- 开发库
  - json-c-devel
  - libcmocka-devel
  - openssl-devel
- Ceph相关库
  - librados-devel
  - librbd-devel
  - libradospp-devel
- 自动工具
  - autoconf
  - automake
  - libtool
- DPDK依赖
  - numactl-devel
  - libarchive-devel
  - libbsd-devel
  - jansson-devel
  - libpcap-devel
- libuuid-devel
- libaio-devel
- libarchive-devel
- CUnit-devel
- ncurses-devel

`make install` 一下，Installed to /usr/local




