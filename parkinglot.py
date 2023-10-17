"""Parking lot simulation."""
from typing import List, Optional, Dict
from random import randrange
import json
import boto3
from botocore.exceptions import NoCredentialsError


_S3 = boto3.client("s3")
_BUCKET_NAME: str = "parkinglot"
_DEFAULT_SPOT_SIZE: int = 96  # 8x12 ft.


class ParkingLot:
    """Handles the parking lot."""

    def __init__(
        self, parking_lot_size: int, spot_size: int = _DEFAULT_SPOT_SIZE
    ) -> None:
        self._parking_lot_size: int = parking_lot_size // spot_size
        self._parking_lots: List[Optional[str]] = [None] * self._parking_lot_size
        self._parked_car_count: int = 0

    @property
    def total_spots(self) -> int:
        """Total parking spots."""
        return self._parking_lot_size

    def is_vacant(self, spot_position: int) -> bool:
        """Return true, if spot is vacant."""
        if spot_position < 0 or spot_position >= self.total_spots:
            raise ValueError(
                f"spot position must be in range of [0, {self.total_spots - 1}]"
            )

        return self._parking_lots[spot_position] is None

    def is_full(self) -> bool:
        """Return true if parkinglot is fully occupied."""
        return self._parking_lot_size == self._parked_car_count

    def park(self, spot_position: int, car_number_plate: str) -> None:
        """Park the car in given spot."""
        if not self.is_vacant(spot_position):
            raise ValueError(f"spot '{spot_position}' is already occupied")

        self._parking_lots[spot_position] = car_number_plate
        self._parked_car_count += 1

    def save(self) -> None:
        """Save the parkinglot to a file and then upload to s3.

        NOTE: Since s3 credentials are not configured, masking the upload to s3 part.
              Remove catching exception while uploading to s3 once credentials are
              configured.
        """
        parking_lot: Dict[str, int] = {}
        # Attaching object's 'id' at end to make unique file name.
        file_name: str = "parkinglot_" + str(id(self)) + ".json"
        for spot, number_plate in enumerate(self._parking_lots):
            if number_plate is None:
                continue
            parking_lot[number_plate] = spot

        # Save to file.
        with open(file_name, "w") as dest:
            json.dump(parking_lot, dest)

        # Upload to s3.
        with open(file_name, "rb") as source:
            # NOTE: Remove this exception catching once AWS s3 credentials are
            #       configured.
            try:
                _S3.upload_fileobj(source, _BUCKET_NAME, file_name)
            except NoCredentialsError:
                pass


class Car:
    """A car with parking option."""

    def __init__(self, number_plate: str) -> None:
        self._number_plate: str = number_plate

    def __str__(self) -> str:
        return self._number_plate

    def park(self, parking_lot: ParkingLot, spot: int) -> bool:
        """Return true, if car is parked successfully else false."""
        try:
            parking_lot.park(spot, self._number_plate)
        except ValueError:
            return False
        return True


def _park_cars(cars: List[Car], parking_lot: ParkingLot) -> None:
    """Park the given cars in parkinglot."""
    for car in cars:
        if parking_lot.is_full():
            print("parking lot is full")
            break

        # Infinite loop to get available spot randomly.
        while True:
            random_spot: int = randrange(parking_lot.total_spots)
            if car.park(parking_lot, random_spot) is True:
                print(
                    "Car with license plate "
                    + str(car)
                    + f" parked successfully in spot {random_spot}"
                )
                break
            print(
                "Car with license plate "
                + str(car)
                + f" couldnt park in spot {random_spot}"
            )


if __name__ == "__main__":
    parking_lot1: ParkingLot = ParkingLot(480)  # 96*5 for simplicity.
    parking_lot2: ParkingLot = ParkingLot(480)  # 96*5 for simplicity.

    car1: Car = Car("0000001")
    car2: Car = Car("0000002")
    car3: Car = Car("0000003")
    car4: Car = Car("0000004")
    car5: Car = Car("0000005")
    car6: Car = Car("0000006")

    case_less_cars_than_spots: List[Car] = [car1, car2, car3, car4]
    case_more_cars_than_spots: List[Car] = [car1, car2, car3, car4, car5, car6]

    # uses parkinglot1.
    print("*********************** Using parkinglot 1 ***********************")
    _park_cars(case_less_cars_than_spots, parking_lot1)
    parking_lot1.save()
    print("******************************************************************")
    # uses parkinglot2
    print("*********************** Using parkinglot 2 ***********************")
    _park_cars(case_more_cars_than_spots, parking_lot2)
    parking_lot2.save()
    print("******************************************************************")
