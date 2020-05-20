from setuptools import setup, find_packages


with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name='python_package',
    packages=find_packages(),
    install_requires=requirements,
    include_package_data=True,
    description='Template Python package for Data Science projects.',
    version='0.1',
    url='https://github.com/gcastella/py_ds_template',
    author='Gerard Castellà Canals',
    author_email='gcastella.91@gmail.com',
    keywords=['python', 'template', 'repository', 'data', 'data-science']
    )