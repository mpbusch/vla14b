# vla14b
Script for VLA 14B-429.222 data reductions 

## Making PyCharm Recognize casapy Task for Easy Scripting
1. Download the MacOS X version of CASA binary and unpack it
2. Point PyCharm project interpreter to `CASA.app/Contents/MacOS/python`
3. Add `CASA.app/Contents/Resources/python` to the interpreter paths 
from within PyCharm. (From Project Interpreter Preferences, 
Click the gear icon -> More ... 
-> Click "show paths for the selected interpreter")

Now you should be able to import casapy high-level tasks to your 
scripts and PyCharm should recognize them. For example:

    from gaincal import gaincal
    
    gaincal(...)
    ...

Note that altough this import line is a legit import in `casapy` 
(it replaces the interactive version of the task with its own function), 
you still have to execute the actual script with `casapy`. We simply 
point PyCharm to CASA libraries to retrieve information from docstrings 
of casapy tasks here.