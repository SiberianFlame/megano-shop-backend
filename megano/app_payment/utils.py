def is_card_number_valid(card_number: str) -> bool:
    """
    Checks whether the last number in the account number is even, not zero,
    and whether there are 16 characters in the account number
    :param card_number: Card number to check
    :return: True (valid), False (not valid)
    """

    if int(card_number[-1]) % 2 != 0 or len(card_number) != 16 or int(card_number[-1]) == 0:
        return False
    else:
        return True