import unittest
import json
import os

from main_script import (
    load_data,
    find_min_price,
    get_number_of_guests,
    calculate_total_prices,
    display_results,
    save_results_to_file
)


# Test data in JSON format
test_data = {
    "assignment_results": [
        {
            "shown_price": {
                "King Studio Suite - Hearing Accessible/Non-Smoking": "113.05",
                "King Studio Suite - Non Smoking": "90",
                "King Room - Mobility/Hearing Accessible - "
                "Non-Smoking": "115.05",
                "Queen Suite with Two Queen Beds - "
                "Non-Smoking": "112.05"
            },
            "number_of_guests": 4,
            "ext_data": {
                "taxes": "{ \"TAX\":\"14.70\", \"City tax\":\"4.01\"}"
            }
        }
    ]
}


class TestHotelFunctions(unittest.TestCase):

    # Test for load_data function with a temporary file creation
    def test_load_data(self):
        file_path = "test_hotel_data.json"
        with open(file_path, 'w') as file:
            json.dump(test_data, file)

        data = load_data(file_path)
        self.assertEqual(data["assignment_results"][0]["number_of_guests"], 4)
        self.assertIn(
            "King Studio Suite - Hearing Accessible/Non-Smoking",
            data["assignment_results"][0]["shown_price"]
        )

        os.remove(file_path)

    # Test for find_min_price function
    def test_find_min_price(self):
        data = test_data
        min_price_room, min_price_value = find_min_price(data)
        self.assertEqual(min_price_room, "King Studio Suite - Non Smoking")
        self.assertEqual(min_price_value, 90.0)

    # Test for get_number_of_guests function
    def test_get_number_of_guests(self):
        data = test_data
        number_of_guests = get_number_of_guests(data)
        self.assertEqual(number_of_guests, 4)

    # Test for calculate_total_prices function
    def test_calculate_total_prices(self):
        data = test_data
        total_prices = calculate_total_prices(data)
        self.assertEqual(len(total_prices), 4)
        self.assertEqual(total_prices[0][2], 131.76)

    # Test for display_results function
    def test_display_results(self):
        data = test_data
        min_price_room, min_price_value = find_min_price(data)
        number_of_guests = get_number_of_guests(data)
        total_prices = calculate_total_prices(data)

        result = display_results(
            min_price_room,
            min_price_value,
            number_of_guests,
            total_prices
        )

        self.assertIn(f"The lowest price: {min_price_value} USD", result[0])

        expected_room_info = f"Room: {min_price_room}, " \
                             f"price: {min_price_value} USD, " \
                             f"total price (with taxes): " \
                             f"{total_prices[1][2]:.2f} USD"
        for room, price, total_price in total_prices:
            if room == min_price_room:
                expected_room_info = f"Room: {room}, price: {price} USD, " \
                                     f"total price (with taxes): " \
                                     f"{total_price:.2f} USD"
                break

        self.assertIn(expected_room_info, result)

    # Test for save_results_to_file function with a temporary file
    def test_save_results_to_file(self):
        result = ["Line 1", "Line 2", "Line 3"]
        file_name = "test_hotel_results.txt"

        save_results_to_file(result, file_name)

        with open(file_name, 'r') as file:
            content = file.read()
            self.assertEqual(content, "Line 1\nLine 2\nLine 3")

        os.remove(file_name)


if __name__ == '__main__':
    unittest.main()
