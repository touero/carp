# 封装了selenium的集成任务
<img src="https://img.shields.io/badge/python_-%3E%3D3.8-green" alt=""> <img src="https://img.shields.io/badge/license_-MIT-green" alt=""> <img src="https://img.shields.io/badge/pymysql-blue" alt=""> <img src="https://img.shields.io/badge/Selenium-blue" alt="">


仓库介绍

这是一个二次封装了selenium的集成任务, 它能使得我们能用一套封装好的代码爬取不同的网站而进行不同的任务类型.

本仓库包含以下内容的爬虫：

1. [下厨房](https://www.xiachufang.com/) 
2. [心食谱](https://www.xinshipu.com/) 
3. [美食天下](https://www.meishichina.com/) 
4. [果蔬网](http://www.zggswmh.com/) 
5. [东方财经](https://www.eastmoney.com/) 

Plus: 以上url并不一定为对应任务的url

## 安装

这个项目使用 [Python](https://www.python.org/) [Git](https://git-scm.com/) [Chrome](https://www.google.com/chrome/)。请确保你本地安装了它们。

```sh
$ git clone https://github.com/weiensong/scrapySelenium.git
```

## 运行

```sh
$ pip install -r requriements.txt

# local_runner.py中的default_config用以配置任务
$ python3 ./local_runner.py
```

## 相关仓库

- [Python](https://github.com/TheAlgorithms/Python) — All Algorithms implemented in Python.
- [Selenium](https://github.com/SeleniumHQ/selenium) — A browser automation framework and ecosystem.

## 相关Driver下载

- [Chrome](https://chromedriver.chromium.org/downloads)

- [Edge](https://developer.microsoft.com/microsoft-edge/tools/webdriver/)

- [FireFox](https://github.com/mozilla/geckodriver/releases)

## 维护者

[@weiensong](https://github.com/weiensong)



## 如何贡献

非常欢迎你的加入！[提一个 Issue](https://github.com/weiensong/scrapySelenium/issues) 或者提交一个 Pull Request。


标准 Python 遵循 [Python PEP-8](https://peps.python.org/pep-0008/) 行为规范。



### 贡献者

感谢参与项目的所有人



## 使用许可

[MIT](LICENSE) © weiensong

