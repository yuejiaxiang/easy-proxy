# easy-proxy
便捷得获取**高匿代理**。爬虫任务的好帮手！

# Advantage
- **一行代码**即完成调用
- 无需额外启动数据库服务，直接import使用
- 自动从多个外部来源更新高匿代理，并自动完成可用性测试（多进程异步进行，用户几乎无感知）。


# Weakness
- 安装本库后的第一次运行会有额外的耗时（需要约几分钟时间进行初始化）。
- 需要能访问外网，在内网环境中无法使用。  


# Quick Start

## Installation
```shell script
pip install easyproxy --extra-index-url https://mirrors.tencent.com/pypi/simple/
```

## use package
```python
from easyproxy import get_proxy
for i in range(3):
    print(get_proxy())
```
> Output:
```python
{'http': '121.232.148.64:3256', 'https': '117.187.167.224:3128'}
{'http': '101.205.120.102:80', 'https': '59.124.224.180:3128'}
{'http': '182.87.136.187:9999', 'https': '203.91.121.212:3128'}
```
