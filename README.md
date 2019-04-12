# Spiders
各种爬虫练习demo

## 1. 环境

- [Miniconda With Python 3.x](https://docs.conda.io/en/latest/miniconda.html)

## 2. 安装依赖包

使用命令安装依赖包清单
```
conda env create -f conda-env.yml
```

## 3. 运行

使用`conda env list`查看已有conda环境，例如:
```
# conda environments:
#
Spiders               *  E:\work\python\env\Anaconda3\envs\Spiders
python36                 E:\work\python\env\Anaconda3\envs\python36
root                     E:\work\python\env\Anaconda3
```
使用`activate Spiders`进入[2. 安装依赖包](#2-安装依赖包)导入的环境
```
(Spiders) (E:\work\python\env\Anaconda3\envs\Spiders) E:\work\python\workspace\Spiders>
```
进入工程目录后执行`python spider.py`即可

## 4. 工程列表

- 猫眼电影top100 (requests)
- 淘宝搜索商品爬虫 (selenium+webdriver)
- vip.qiyikt易锦大学视频爬虫 (requests)