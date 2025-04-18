# Hello Python and Jupyter 👋

## Setup
1. Open up : https://jupyter.nsls2.bnl.gov
2. Log in with your BNL credentials and accept DUO push
3. Start My Server
4. Select Job Profile: Scientific Python, Start
5. Open a notebook
6. Make a fork of this repository (if you have not done so already)
7. Copy the HTTP clone link
8. In the first cell of your notebook try:
```
!git clone https://github.com/<username>/bluesky-training-2025-2.git
```
9. You should see a new folder “bluesky-training-2025-2” appear in the file explorer
10. Open the folder and find “hello-python-and-jupyter.ipynb” in the `Week2` folder

## Types of Jupyter Notebook Cells
**Markdown**
* Cells for text using Markdown which is like HTML (but easier)
* Headings, bold, italics, lists
* https://daringfireball.net/projects/markdown/
* https://jupyter-notebook.readthedocs.io/en/stable/examples/Notebook/Working%20With%20Markdown%20Cells.html

**Code**
* Allows you to enter and run code
* Run each code cell using Shift-Enter or pressing the play button in the tool bar
* https://jupyter-notebook.readthedocs.io/en/stable/examples/Notebook/Running%20Code.html

**List of toolbar shortcuts:** https://gist.github.com/discdiver/9e00618756d120a8c9fa344ac1c375ac

## Other Python Interfaces
* IPython – terminal based with magic by typing `ipython`
* Terminal – simple python shell by typing `python`
* IDEs 
  * Visual Studio Code - https://code.visualstudio.com
  * PyCharm - https://www.jetbrains.com/pycharm/

## Python Environments
**Conda** - Cross-platform package manager 
* We use custom conda environments in DSSI to deploy necessary packages and python version on the experimental floor
* https://github.com/conda/conda

**venv** – virtual environments
* Module supports lightweight virtual environments each with their own independent set of python packages installed in their site directories
* Common install tool is pip
* https://docs.python.org/3/library/venv.html

**pixi** – new package management workspace
* https://pixi.sh/latest/

## Testing in Python
* **pytest**: helps you write better programs
* Makes it easy to write small, readable tests, but also scales to complex functional testing for applications
* https://docs.pytest.org/en/stable/


## Challenge Problems: **Credit to Tiny Python Projects by Ken Youens-Clark**
* https://github.com/kyclark/tiny_python_projects
* https://github.com/kyclark/tiny_python_projects/tree/master/02_crowsnest
  
