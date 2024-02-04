# Welcome to Carp wiki

## Usage

Recommend using Python's [venv](https://docs.python.org//3.10/library/venv.html).  

Install dependency
```shell
pip install -r requriements.txt
```

## Run
> [!Important]
> 1. `default_config` is a dict, which used to configure tasks in `run.py`. 
> 2. default email config is in `config/smtp.yaml`. 
> 3. if you want to use it please build a new yaml.

and then: 
```shell
python run.py
```
Real running instructions if using email api example:
```shell
python run.py -y config/smtp.yaml
```

## How increase your robot
- Please creating `***_robot.py` in `/robots`.
- Adding task's type and task's url in `constants.py`.
- Adding your robot to dicts `self.robots` and `self.urls` in `src/robot_master.py`.
- Over writing your robot's `def __str__(self)` and `def run_task(self)` in your robot.
- Setting your task type in `run.py` and run it.
- If you want to use email api `email: bool = True` in `run.py` and set your `smtp_config.yaml` in config. 

> [!Important]
> Standard Python follows the [Python PEP-8](https://peps.python.org/pep-0008/) Code of Conduct.  

and then you can new pull request.