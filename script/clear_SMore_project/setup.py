# @Author: Pbihao
# @Time  : 22/10/2021 6:18 PM
from setuptools import setup

"""
use:
    pip install -e $path_to_script_folder
    
For Example:
    pip install -e /home/pbihao/SMore/github/SMore/script/clear_SMore_project

to install script, and then you can directly use this script in command
"""

setup(
    name="clear_SMore_project",
    version='1.0',
    entry_points={
        'console_scripts': [
            'clear_SMore_project=clear_SMore_project:main'
        ]
    }
)
