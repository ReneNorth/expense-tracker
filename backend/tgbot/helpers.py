def convert_last_element_to_number(lst):
    try:
        last_element = lst[-1]
        number = float(last_element)  # Try converting to float
        # If successful, you can also check if it's an integer
        if number.is_integer():
            number = int(number)
        return number
    except (ValueError, IndexError):
        # Handle the case when the last element is not convertible to a number
        return None
