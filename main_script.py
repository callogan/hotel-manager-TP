import json
import os


def load_data(file_path):
    """
    Loads data from mentioned JSON-file

    Args:
        file_path (str): Path to JSON file, containing data.

    Returns:
        dict: Loaded data in dictionary format.
    """
    with open(file_path, 'r') as file:
        return json.load(file)


def find_min_price(data):
    """
    Finds room number with the lowest price and returns it.

    Args:
        data (dict): Data, containing information about rooms and prices.

    Returns:
        tuple: Room number with the lowest price and the price itself.
    """
    shown_prices = data["assignment_results"][0]["shown_price"]
    price_list = [(room, float(price)) for room, price in shown_prices.items()]

    min_price_room, min_price_value = price_list[0]
    for room, price in price_list:
        if price < min_price_value:
            min_price_value = price
            min_price_room = room

    return min_price_room, min_price_value


def get_number_of_guests(data):
    """
    Returns number of guests for the room.

    Args:
        data (dict): Data, containing the information about booking.

    Returns:
        int: Number of guests.
    """
    return data["assignment_results"][0]["number_of_guests"]


def calculate_total_prices(data):
    """
    Calculates the total price of all the rooms, including taxes.

    Args:
        data (dict): Data, containing the information about prices and taxes.

    Returns:
        list of tuple: List, containing the information about the room,
        the net price and total price with taxes.
    """
    total_prices = []
    taxes = json.loads(data["assignment_results"][0]["ext_data"]["taxes"])

    for room, price in data["assignment_results"][0]["shown_price"].items():
        price = float(price)
        tax_amount = sum(float(taxes[key]) for key in taxes)
        total_price = price + tax_amount
        total_prices.append((room, price, total_price))

    return total_prices


def display_results(
        min_price_room,
        min_price_value,
        number_of_guests,
        total_prices
):
    """
    Forms the string for reflecting results about minimal price
    and total rice all the rooms.

    Args:
        min_price_room (str): The room with the lowest price.
        min_price_value (float): The minimal price.
        number_of_guests (int): Number of guests.
        total_prices (list of tuple): Total prices all the rooms with taxes.

    Returns:
        list of str: List  of strings for outputting results.
    """
    result = []
    result.append(
        f"The lowest price: {min_price_value} USD, "
        f"room type: {min_price_room}, "
        f"number of guests: {number_of_guests}\n"
    )

    result.append("Total price for all the rooms:")
    for room, price, total_price in total_prices:
        result.append(
            f"Room: {room}, price: {price} USD, "
            f"total price (with taxes): {total_price:.2f} USD"
        )

    print("\n".join(result))

    return result


def save_results_to_file(result, file_name):
    """
    Records results in the file.

    Args:
        result (list of str): List of strings for recording in the file.
        file_name (str): Path to the file for recording.
    """
    with open(file_name, 'w') as output_file:
        output_file.write("\n".join(result))


def main():
    """
    Main function that ties all components together:

    - Initializes the correct file path for the JSON data file.
    - Loads hotel data from the specified file.
    - Finds the room with the lowest price.
    - Retrieves the number of guests.
    - Calculates the total prices for all the rooms, including taxes.
    - Displays the results and writes them to an output file.
    """
    file_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "hotel_data.json"
    )

    data = load_data(file_path)

    min_price_room, min_price_value = find_min_price(data)
    number_of_guests = get_number_of_guests(data)
    total_prices = calculate_total_prices(data)

    result = display_results(
        min_price_room,
        min_price_value,
        number_of_guests,
        total_prices
    )
    save_results_to_file(result, "hotel_results.txt")
    print("Data have been successfully recorded to 'hotel_results.txt'.")


if __name__ == "__main__":
    main()
