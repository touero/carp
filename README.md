<h1 align="center">carp</h1>

<p align="center">
  <a href="https://www.python.org/" ><img src="https://img.shields.io/badge/python_-%3E%3D3.8-blue" alt=""></a> 
  <a href="https://www.gnu.org/licenses/gpl-3.0.html" ><img src="https://img.shields.io/badge/license_-GPL3.0-blue" alt=""> 
  <a href="https://www.python.org/" ><img src="https://img.shields.io/badge/-python-grey?style=plastic&logo=python" alt=""/></a> 
  <a href="https://www.selenium.dev/"><img src="https://img.shields.io/badge/-selenium-grey?style=plastic&logo=selenium" alt=""/></a> 
  <a href="https://git-scm.com/"><img src="https://img.shields.io/badge/git-grey?style=plastic&logo=git" alt=""/></a> 
  <a href="https://www.jetbrains.com/pycharm/"><img src="https://img.shields.io/badge/-pycharm-grey?style=plastic&logo=pycharm" alt=""/></a> 
  <a href="https://www.mysql.com/"><img src="https://img.shields.io/badge/-mysql-grey?style=plastic&logo=mysql" alt=""/></a>  
</p>

<p align="center">
    <img src=.img/carp.png height="200" width="200" alt="">
</p>

## Repository Introduction

This is an integration task that encapsulates selenium twice, which allows us to crawl different websites with a set of encapsulated code and perform different task types.  
  
> Now, it has some functions:
>> 1. log 
>> 2. debug 
>> 3. can need not webdriver 
>> 4. just need to implement a func
>> 5. exception screenshot
>> 6. email api send to yourself
  
💕 If it's helpful to you or cloning it, please star it. This is maximum encouragement for open-source contributors💕
> Currently, this repository contains：
>> 1. [下厨房](https://www.xiachufang.com/) 
>> 2. [心食谱](https://www.xinshipu.com/) 
>> 3. [美食天下](https://www.meishichina.com/) 
>> 4. [果蔬网](http://www.zggswmh.com/) 
>> 5. [东方财经](https://www.eastmoney.com/) 
>> 6. [12306](https://kyfw.12306.cn/otn/resources/login.html)  
> Plus: The above URLs are not necessarily the URLs of the corresponding tasks.

## Install

This project uses [Python](https://www.python.org/) [Git](https://git-scm.com/) [Chrome](https://www.google.com/chrome/). Go check them out if you don't have them locally installed.

```shell
$ git clone https://github.com/weiensong/carp.git
```

## Usage

Recommend using Python's virtual environment

 - powershell, shell build a virtual environment

```shell
$ python 3 -m venv venv
```
 - activate virtual environment
 - - shell
```shell
$ source ./venv/bin/activate 
```
- - powershell
```powershell
> .\venv\Scripts\activate 
```
 - install packagers
```shell
$ pip install -r requriements.txt 
```


 - default_config is used to configure tasks in local_runner.py
 - default email config is in config/smtp.yaml
 - if you want to use it please build a new yaml

```shell
$ python ./local_runner.py -y smtp.yaml
```

 - quiting from virtual environment
 - - shell
```shell
$ deactivate 
```
 - - powershell
```powershell
> .\Scripts\deactivate.bat 
```
As you can see, there are relatively few crawling parts. But, contribute to this under [Python PEP-8](https://peps.python.org/pep-0008/)  

> If you want to increase your robot following: 
- please creat ***_robot.py in dir of name is rpa.
- Adding task's type and task's url in constants.py.
- Adding 1&2 in robots and urls in RpaMaster.
- Over writer your \__str\__'s and run_task's func in your robot.
- if you want to use email api [email=True] in local_runner and set your config/smtp.yaml
- Fixing task_type in local_runner and run it.

Real running instructions if using email api example:
```shell
$ python local_runner.py -y config/smtp_weiensong.yaml
```

## Related Repository

- [Python](https://github.com/TheAlgorithms/Python) — All Algorithms implemented in Python.
- [Selenium](https://github.com/SeleniumHQ/selenium) — A browser automation framework and ecosystem.

## Related Driver Download

- [Chrome](https://chromedriver.chromium.org/downloads)

- [Edge](https://developer.microsoft.com/microsoft-edge/tools/webdriver/)

- [FireFox](https://github.com/mozilla/geckodriver/releases)

Currently, there is only Chrome driver, if you have a feat with other driver please submit PRs

## Maintainers

[@weiensong](https://github.com/weiensong)



## Contributing

How I wish I could add more content in this repo !

Feel free to dive in! [Open an issue](https://github.com/weiensong/scrapySelenium/issues) or submit PRs.

Standard Python follows the [Python PEP-8](https://peps.python.org/pep-0008/) Code of Conduct.



### Contributors

This project exists thanks to all the people who contribute.  
  
<a href="https://github.com/weiensong/carp/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=weiensong/carp"  alt=""/>
</a>



## License

[GNU General Public License v3.0](https://github.com/weiensong/carp/blob/master/LICENSE) © weiensong

