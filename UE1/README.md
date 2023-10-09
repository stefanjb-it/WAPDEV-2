SWENGS - Python Programming exercise
------------------------------------

This package consists of two files. One is the main executable, main.py which 
can be run using the command

python main.py

This file MUST NOT be changed. The second file is exercises.py containing 
a number of Python function that need to be implemented. Running main.py 
will call each function with different parameters and evaluate if the 
function call succeeded or failed. At the end of the run, main.py will 
provide a score indicating how many function calls succeeded or failed. 
The maximum score is 19 points. 

The format of the output can be read as follows:

FAILED - NOT IMPLEMENTED: calculate_mean(8, 4, 10, 2) - expected output:6.0

The first part indicates the result of the function call. It can be 
"OK" (implementation is correct), "FAILED" (implementation is available 
but did not yield the expected outcome) or "FAILED - NOT IMPLEMENTED" 
indicating that that the function is not implemented yet. 

The second part - calculate_mean(8,4,10,2) - indicates the function call used 
and the expected output of the function (expected output: 6.0). 
In case the calculate_mean function was wrongly implemented 
the output would change to:

FAILED:mean_temperature([]) - Your result: 4.0 / Expected result: None

If the function is correctly implemented the output changes to:

OK:mean_temperature([]) - Your result: None / Expected result: None

If the execution of the function fails due to a programming error the 
output will give you the exception:

Execution of function call mean_temperature([]) FAILED with this error:

Traceback (most recent call last):
  File "C:/work/FH/exercise1/main.py", line 78, in <module>
    is_ok, result = _evaluate(func, param, exp_outcome, check_exception)
  File "C:/work/FH/exercise1/main.py", line 13, in _evaluate
    result = func(*param)
  File "C:\work\FH\exercise1\exercises.py", line 82, in mean_temperature
    return z
NameError: name 'z' is not defined

