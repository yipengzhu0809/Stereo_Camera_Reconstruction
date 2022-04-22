## 1.相关依赖包安装方法

#### opencv-contrib-python

```bash
pip install opencv-contrib-python # ximgproc
```

#### PCL-Python

- https://zhuanlan.zhihu.com/p/162277657

```bash
sudo apt-get install libpcl-dev -y
conda install -c sirokujira python-pcl --channel conda-forge
```

- 会出现很多libboost_system.so.1.65.1: cannot open shared object file的错误
- 使用locate定位每个库的位置
- 再通过软链接到/usr/lib/x86_64-linux-gnu/目录下

```yaml
sudo ln -s /usr/lib/x86_64-linux-gnu/libboost_system.so.1.65.1  /usr/lib/x86_64-linux-gnu/libboost_system.so.1.66.0
```

- 软链接完后，就可以使用python-pcl了(但测试发现，还是有未知的错误)
- <Ubuntu 18.04安装python-pcl> https://blog.csdn.net/weixin_47047999/article/details/119088321 (亲测可用)

## 2.基本原理

### (1)视差图

### (2)视差图转换为深度图

- 视差的单位是像素（pixel），深度的单位往往是毫米（mm）表示。
- 而根据平行双目视觉的几何关系，可以得到下面的视差与深度的转换公式：

> depth = ( f * baseline) / disp

- f表示归一化的焦距，也就是内参中的fx；
- baseline是两个相机光心之间的距离，称作基线距离；
- disp是视差值。等式后面的均已知，深度值即可算出
- depth表示深度图
  __