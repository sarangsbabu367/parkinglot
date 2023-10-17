import pytest
import os
import json

from parkinglot import ParkingLot, Car

_BASIC_PARKING_LOT_SIZE: int = 96


class TestParkingLot:
    def test_total_spots_default_size(self):
        assert ParkingLot(_BASIC_PARKING_LOT_SIZE * 5).total_spots == 5
        assert ParkingLot(_BASIC_PARKING_LOT_SIZE * 6).total_spots == 6

    def test_total_spots_custom_size(self):
        assert ParkingLot(120 * 5, 10).total_spots == (120 * 5) // 10
        assert ParkingLot(120 * 6, 10).total_spots == (120 * 6) // 10

    def test_is_vacant_invalid_index(self):
        with pytest.raises(ValueError):
            ParkingLot(_BASIC_PARKING_LOT_SIZE).is_vacant(-10)

        with pytest.raises(ValueError):
            ParkingLot(_BASIC_PARKING_LOT_SIZE).is_vacant(10)

    def test_is_vacant(self):
        assert ParkingLot(_BASIC_PARKING_LOT_SIZE).is_vacant(0) is True

    def test_is_full(self):
        parking_lot: ParkingLot = ParkingLot(_BASIC_PARKING_LOT_SIZE)

        assert parking_lot.is_full() is False

        parking_lot.park(0, "0000001")
        assert parking_lot.is_full() is True

    def test_park_occupied_spot(self):
        parking_lot: ParkingLot = ParkingLot(_BASIC_PARKING_LOT_SIZE)
        parking_lot.park(0, "0000001")

        with pytest.raises(ValueError):
            parking_lot.park(0, "0000001")

    def test_park(self):
        parking_lot: ParkingLot = ParkingLot(_BASIC_PARKING_LOT_SIZE)
        assert parking_lot.park(0, "0000001") is None

    def test_save(self):
        parking_lot: ParkingLot = ParkingLot(_BASIC_PARKING_LOT_SIZE)
        parking_lot.park(0, "0000001")

        assert parking_lot.save() is None

        for file_name in [f for f in os.listdir() if not os.path.isdir(f)]:
            if file_name != f"parkinglot_{id(parking_lot)}.json":
                continue
            with open(file_name, "r") as source:
                assert json.load(source) == {"0000001": 0}
            # Deleting file created for test.
            os.remove(file_name)
            break
        else:
            assert False, "file not found"


class TestCar:
    def test_number_plate(self):
        assert str(Car("0000001")) == "0000001"
        assert str(Car("0000002")) == "0000002"

    def test_park_occupied_spot(self):
        parking_lot: ParkingLot = ParkingLot(_BASIC_PARKING_LOT_SIZE)
        car: Car = Car("0000001")
        car.park(parking_lot, 0)

        assert car.park(parking_lot, 0) is False

    def test_park(self):
        parking_lot: ParkingLot = ParkingLot(_BASIC_PARKING_LOT_SIZE)
        car: Car = Car("0000001")

        assert car.park(parking_lot, 0) is True
