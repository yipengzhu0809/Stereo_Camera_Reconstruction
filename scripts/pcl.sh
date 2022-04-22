#!/usr/bin/env bash
sudo apt install libpcl-dev
sudo apt-get update
sudo apt-get install git build-essential linux-libc-dev
sudo apt-get install cmake cmake-gui
sudo apt-get install libusb-1.0-0-dev libusb-dev libudev-dev
sudo apt-get install mpi-default-dev openmpi-bin openmpi-common
sudo apt-get install libflann1.8 libflann-dev
sudo apt-get install libeigen3-dev 这个需要自己下载正确版本安装
sudo apt-get install libboost-all-dev
sudo apt-get install libvtk7.1-qt libvtk7.1 libvtk7-qt-dev
sudo apt-get install libqhull* libgtest-dev
sudo apt-get install freeglut3-dev pkg-config
sudo apt-get install libxmu-dev libxi-dev
sudo apt-get install mono-complete
sudo apt-get install openjdk-8-jdk openjdk-8-jre
# build pcl
cd libs
git clone https://github.com/PointCloudLibrary/pcl.git
cd pcl
mkdir build && cd build
cmake -DCMAKE_BUILD_TYPE=Release -D CMAKE_INSTALL_PREFIX=/usr/local ..
sudo make -j2 install
cd ../../
## 安装python-pcl
#git clone https://github.com/strawlab/python-pcl.git
#cd python-pcl
#python setup.py install