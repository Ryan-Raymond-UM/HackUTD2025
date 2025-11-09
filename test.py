#!/usr/bin/env python3

import NHTSA

"""
Basic workflow: Select Make, Model, Year
"""

#print('Get a list of automobile makes')
#print(NHTSA.getAllMakes())

#print('Getting all models with years for make "Honda"')
print(NHTSA.getModelYearsForMake('Honda'))

#print('Getting all years for model "Civic", make "Honda"')
print(NHTSA.getYearsForMakeAndModel('Honda', 'Civic'))

#print('Getting all variants for model "Civic", make "Honda", year "2021"')
#print(NHTSA.getVariants('Honda', 'Civic', 2021))
