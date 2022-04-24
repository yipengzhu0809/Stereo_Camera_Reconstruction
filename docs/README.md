## 1. Related dependency package installation method

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

- There will be a lot of libboost_system.so.1.65.1: cannot open shared object file errors
- Use locate to locate each library
- Then softlink to the /usr/lib/x86_64-linux-gnu/ directory

```yaml
sudo ln -s /usr/lib/x86_64-linux-gnu/libboost_system.so.1.65.1 /usr/lib/x86_64-linux-gnu/libboost_system.so.1.66.0
```

- After softlinking, it's ready to use python-pcl (but testing found that there are still unknown errors)
- <Ubuntu 18.04 install python-pcl> https://blog.csdn.net/weixin_47047999/article/details/119088321 (tested and available)

## 2. Fundamentals

### (1)Parallax map

### (2) Parallax to depth map

- Parallax is expressed in pixels (pixel) and depth is often expressed in millimeters (mm).
- And based on the geometric relationship of parallel binocular vision, the following equation for the conversion of parallax to depth can be obtained.

> depth = ( f * baseline) / disp

- f denotes the normalized focal length, which is fx in the internal reference.
- baseline is the distance between the two camera optical centers, called the baseline distance.
- disp is the parallax value. The latter part of the equation is known, and the depth value can be calculated
- depth means depth map
  __
