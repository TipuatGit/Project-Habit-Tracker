# Project: Habit Tracker Application
Habit Tracker program for my University course.

Start here:

```Habit Tracker.py``` 

This is the main file that runs the program. Best to run it as a CLI because some functionality is not possible in IDLE.

```functions.py``` file contains various functions that enable the program to work such as the different interactive interfaces, help features and database data management.

```habit_class.py``` defines the Habit class and contains a few methods.

## Installation

```shell
python -r requirements.txt
```

The program is complete and fully developed.

## Tests

To test the program, you need to install ```pytest``` then follow these exact steps:
1) open ```command-prompt``` in the directory of the program and type:
```shell
pytest test_program.py -s
```

2) press Enter
3) type ```main``` and press Enter
4) repeat step 3 three more times

Users can use the program during testing like normal too, go around and select different options or give wrong inputs to see if there is any change. Following these steps above is just faster.

The ```-s``` handle is reqired because the input cannot be docked and so must be entered manually by users, the handle allows for that otherwise the testing fails.

   
