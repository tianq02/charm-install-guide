# charm安装指北

> 2025-04-20, tianq02:  
> 本文基于[这篇教程](https://blog.csdn.net/weixin_63468703/article/details/146476693)，对一些错误作了修正  
> 下面的流程ubuntu22.04上通过测试, 理论上也适合debian12

## 1. 准备源码包：

[gmp-5.1.3](https://gmplib.org/download/gmp/gmp-5.1.3.tar.xz)  
[pbc-0.5.14](https://crypto.stanford.edu/pbc/files/pbc-0.5.14.tar.gz)  
[charm(下载dev分支源码)](https://github.com/JHUISI/charm)  

## 2. 安装系统依赖项

不要在这里安装libgmp-dev, 稍后我们会自己编译安装对应版本的gmp到虚拟环境中
```bash
sudo apt install build-essential m4 flex bison libssl-dev
```

## 3. 设置conda虚拟环境

[miniforge安装教程](https://mirror.nju.edu.cn/help/miniforge)

### 安装miniforge

下载[最新版本miniforge安装包(x64)](https://mirror.nju.edu.cn/github-release/conda-forge/miniforge/LatestRelease/Miniforge3-Linux-x86_64.sh), 之后在下载目录中`bash Miniforge3-Linux-x86_64.sh`, 一路enter安装。安装后, 重新打开终端。

### 设置conda镜像站

懒人脚本
```bash
echo 'channels:
  - defaults
show_channel_urls: true
default_channels:
  - https://mirror.nju.edu.cn/anaconda/cloud/conda-forge/
' | sudo tee ~/.condarc
```

### 创建虚拟环境

```bash
# charm很老了, 建议搭配老版本python使用, 例如这里的3.6
conda create -n py36 python=3.6 pyparsing=2.4.6
```

### 进入虚拟环境, 验证python版本

```bash
conda activate py36
python --version
```

## 4. 编译安装GMP, PBC, charm

*注意顺序要求*

### 配置环境变量

```bash
conda activate py36
# 在激活的虚拟环境中设置编译路径
export C_INCLUDE_PATH=$CONDA_PREFIX/include:$C_INCLUDE_PATH
export LIBRARY_PATH=$CONDA_PREFIX/lib:$LIBRARY_PATH
export LD_LIBRARY_PATH=$CONDA_PREFIX/lib:$LD_LIBRARY_PATH
```

### 编译安装GMP

```bash
# 解压 GMP
tar -xf gmp-5.1.3.tar.gz
cd gmp-5.1.3

# 配置并安装到虚拟环境目录
./configure --prefix=$CONDA_PREFIX
make && make check && make install
cd ..
```

### 编译安装PBC

> 如果没配置环境变量, 此处configure找不到GMP

```bash
# 解压 PBC
tar -xvf pbc-0.5.14.tar.gz
cd pbc-0.5.14

# 配置并安装到虚拟环境目录
./configure --prefix=$CONDA_PREFIX
make && make install
cd ..
```

### 检查GMP和PBC的安装

每个命令都应该有输出

```bash
# 验证GMP
ls $CONDA_PREFIX/include/gmp.h
ls $CONDA_PREFIX/lib | grep libgmp
# 验证PBC
ls $CONDA_PREFIX/include/pbc/pbc.h
ls $CONDA_PREFIX/lib | grep libpbc
```

### 编译安装charm

make过程中会从网上下载python依赖, 如果前面没有配置好镜像站, 这一步会很慢

> 如果make出错形如`benchmarkmodule.h:60: multiple definition of 'BenchmarkError'`
> 去下载最新的charm-dev, 修复补丁已经合并

```bash
#解压charm的源代码
unzip charm-dev.zip
cd charm-dev

# 下面的配置命令在我的机器上通过，可能可以简化
./configure.sh --prefix=$CONDA_PREFIX --enable-pairing-pbc --enable-integer-gmp --extra-cflags="-I$CONDA_PREFIX/include -I$CONDA_PREFIX/include/pbc" --extra-ldflags="-L$CONDA_PREFIX/lib -lpbc -lgmp"

make && make install
```

成功安装后，末尾提示

```plaintext
Finished processing dependencies for Charm-Crypto==0.50
```

## 5. 测试charm安装

随便写点用上charm的代码看看能不能跑

> 如果运行时integer导入失败, 说明python版本太高，请从[设置conda环境](#3-设置conda虚拟环境)重新开始

```python
from charm.toolbox.pairinggroup import PairingGroup, ZR, G1, G2, GT
def main():
    # 初始化配对群
    group = PairingGroup('MNT224')

    # 生成两个随机元素
    a = group.random(ZR)
    b = group.random(ZR)

    # 计算两个元素的乘积
    result = a * b

    print(f"随机元素 a: {a}")
    print(f"随机元素 b: {b}")
    print(f"a 和 b 的乘积: {result}")

if __name__ == "__main__":
    main()
```

保存为`test.py`后，测试运行结果

```bash
python test.py
```

输出类似：

```plaintext
(py36) tianq@tianq-charm:/tmp/apps/charm2$ python ./test.py 
随机元素 a: 10087302322155781615109627050530113104575862683813810626881790445688
随机元素 b: 12803826869553815185965561501190434416208398704389683979554212481887
a 和 b 的乘积: 13537376690695691051453641432633615238840167108378827226149116308343
```

大功告成！
