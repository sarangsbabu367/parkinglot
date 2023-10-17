# parkinglot
simple parkinglot simulation


## Problem description

Create a parking lot class that takes in a square footage size as input and creates an array of empty values based on the input square footage size. Assume every parking spot is 8x12 (96 ft2) for this program, but have the algorithm that calculates the array size be able to account for different parking spot sizes. For example, a parking lot of size 2000ft2 can fit 20 cars, but if the parking spots were 10x12 (120 ft2), it could only fit 16 cars. The size of the array will determine how many cars can fit in the parking lot.

Create a car class that takes in a 7 digit license plate and sets it as a property. The car will have 2 methods:

  1. A magic method to output the license plate when converting the class instance to a string.

  2. A "park" method that will take a parking lot and spot # as input and fill in the selected spot in the parking lot. If another car is parked in that spot, return a status indicating the car was not parked successfully. If no car is parked in that spot, return a status indicating the car was successfully parked.

Have a main method take an array of cars with random license plates and have them park in a random spot in the parking lot array until the input array is empty or the parking lot is full. If a car tries to park in an occupied spot, have it try to park in a different spot instead until it successfully parks. Once the parking lot is full, exit the program.

Output when a car does or does not park successfully to the terminal (Ex. "Car with license plate [LICENSE_PLATE] parked successfully in spot [SPOT #]").

OPTIONAL/BONUS - Create a method for the parking lot class that maps vehicles to parked spots in a JSON object. Call this method at the end of the program, save the object to a file, and upload the file to an input S3 bucket.

## Dependencies

Please install the below mentioned dependencies to run the project. You can copy the command as itself and run it from where you try to execute `parkinglot.py` file.

ps: Use python3 to run.

```zsh
pip install boto3 # AWS sdk for connecting with s3.
pip install pytest # For running test cases.
```
## Execution

2 sample scenarios are described in `__main__` block in `parkinglot.py` file. Running the file will show the result of these 2 scenarios. The scenarios are commented for better understanding.

2 `.json` files will be generated after you run `parkinglot.py`. These 2 files contains the result of above mentioned 2 scenarios. These files will be generated for each run.

Currently uploading to s3 part is masked by catching the exception. Once aws s3 configuration are added the `try - catch` block can be removed (In `ParkingLot` class `save` method).

ps: The output may not be the same if you try to run the file, since there is a random logic to choose the parkinglot for a car.

eg:

```zsh
(env_parkinglot) ➜  parkinglot git:(feat_parkinglot) ✗ python parkinglot.py 
*********************** Using parkinglot 1 ***********************
Car with license plate 0000001 parked successfully in spot 2
Car with license plate 0000002 parked successfully in spot 0
Car with license plate 0000003 couldnt park in spot 2
Car with license plate 0000003 couldnt park in spot 0
Car with license plate 0000003 parked successfully in spot 3
Car with license plate 0000004 parked successfully in spot 1
******************************************************************
*********************** Using parkinglot 2 ***********************
Car with license plate 0000001 parked successfully in spot 0
Car with license plate 0000002 parked successfully in spot 2
Car with license plate 0000003 parked successfully in spot 4
Car with license plate 0000004 couldnt park in spot 4
Car with license plate 0000004 couldnt park in spot 4
Car with license plate 0000004 parked successfully in spot 1
Car with license plate 0000005 couldnt park in spot 1
Car with license plate 0000005 couldnt park in spot 2
Car with license plate 0000005 couldnt park in spot 2
Car with license plate 0000005 couldnt park in spot 4
Car with license plate 0000005 couldnt park in spot 0
Car with license plate 0000005 parked successfully in spot 3
parking lot is full
******************************************************************
(env_parkinglot) ➜  parkinglot git:(feat_parkinglot) ✗ 
```

## Tests

Test cases are added strengthen the project.

```zsh
(env_parkinglot) ➜  parkinglot git:(feat_parkinglot) ✗ pytest test_parkinglot.py
====================================================== test session starts ======================================================
platform darwin -- Python 3.9.6, pytest-7.4.2, pluggy-1.3.0
rootdir: /Users/sarang/work/parkinglot
collected 11 items                                                                                                              

test_parkinglot.py ...........                                                                                            [100%]

====================================================== 11 passed in 0.17s =======================================================
(env_parkinglot) ➜  parkinglot git:(feat_parkinglot) ✗ 
```