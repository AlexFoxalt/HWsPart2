""" 
1. 
Problem: In Teacher Creating form (forms.py -54) there are two validators that contradict each other
(first one in models.py -29). So creating a new teacher is unable, because validation will not pass anyway.

Solution: Get rid of one of these validators.

2.
Problem: No input form in Student Creating form (forms.py -9) for birthday. Unable to set birthday so all students
are 0 y.o.

Solution: Add form and set datetime choice widget for convenience.
"""
