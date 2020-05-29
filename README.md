# Python package repository template
This is a template repository for fast initialization of data science python projects.
It is based on the best practices detailed in [this post](https://medium.com/bcggamma/data-science-python-best-practices-fdb16fdedf82).

To use as a template, you can go the [repository](https://github.com/gcastella/py_ds_template) site on github and click on "Use this template".
This will create a new repository under your profile using `py_ds_template.git` as a starting point. Of course, you should rename it as you like.

## Install the package
Once you have created your own package using py_ds_template.git as a template, you can install it by doing:
```shell script
pip install git+https://github.com/gcastella/<your_package_name>.git
```
You can also add `@<branch_name>` at the end to install from a particular branch.

## Set the environment up
The file `requirements.txt` contains a list (from a `pip freeze > requirements.txt`) of the dependencies of the package.
If you want to run it once your repo has been created and cloned locally, you have to install these requirements. 
The following code creates a new conda env and installs the packages.
```shell script
conda create -n <my_env_name> python=3.7 -y
conda activate <my_env_name>
pip install -r requirements.txt
```

Also, before using the package, you should rename it since its actual name is `dsmodule`. 
To do so just replace this string (from an IDE) by whatever name you want all over the repo. 
Make sure that the setup.py file, all imports, and the module folder are correctly renamed. 
In PyCharm you can do so just by right clicking on the package folder and `refactor > rename`.

To finish with the setup, you should copy the file `.envtemplate` and name it `.env`. 
This file contains some configuration variables and can contain credentials if needed (it will be ignored once renamed).

## Structure

This repo has the following structure:

```shell script
base_repo
    ├── dsmodule                        The main python module
    │     ├── config                    Read and load configuration
    │     ├── tasks                     Task definition
    │     ├── tests                     Unit tests
    │     ├── utils                     Functions used accross the module
    │     ├── __main__.py               Calls main_cli() from run.py
    │     ├── run.py                    Only entry point (CLI) of the module
    │     └── __init__.py               Init for the package
    ├── configs                         
    │     ├── config.yaml               Overall configuration
    │     ├── logging.yaml              Logging configuration
    │     └── run.yaml                  Configuration for each run (model, algorithm, etc.)
    ├── notebooks                       Relevant notebooks for the project.
    ├── README.md                       Intro to package
    ├── setup.py                        Installing the package
    ├── requirements.txt                Lists dependencies
    ├── .gitignore                      Files/dirs to git ignore
    └── LICENSE.md                      License if needed
```

Here we document a bit deeper some relevant files.

### Entry points
This module contains only one entry point, accessible via:
```shell script
python dsmodule --task <your_task>
```
Under the hood, it is executing `__main__.py` which calls the `main_cli()` function in `run.py`, executing a task by its name.
You can add extra tasks by adding entries to the `tasks` dictionary.

### Tasks
Tasks inheriting from `BaseTask` (usually related to modelization and data):
- `extract`: Connects to the sources where data is stored to extract all data needed and save them as csv's
- `preprocess`: Load all extracted csv's and solve potential data quality issues, missings, feature engineering, selection, etc.
- `train`: Split datasets and train the model.
- `test`: Evaluate the model using different metrics.
- `predict`: Get the predictions of the model for a new dataset.

Other tasks:
- get_config: Print configuration object load from yaml files.
- version: Print version used for the files.

All tasks inheriting from `BaseTask` load and write files adding the version prefix of the run automatically at the beginning.
 You do not have to manually add it in the config files.

### Config
`config` Box object is created based on the environment variables read from `.env`.
Parameters in the `RUN_FILE` file are added to the object. 
Parameters from the correct environment (prod, pre or dev) in the `CONFIG_FILE` file are also appended.
Run version can be accessed via `config.version`.

