def is_this_a_token(token: str) -> bool:
    response_valid = False

    while not response_valid:
        print(f"During type/token counting we found {token}, is this a valid token?")
        response = _response_to_bool(input("(y/n): "))

        if response != None:
            response_valid = True
        else:
            print("The only valid response is `y` or `n` letter and enter.")

    return response


def _response_to_bool(response: str) -> bool | None:
    response = response.strip().lower()
    if response == "y":
        return True
    elif response == "n":
        return False
    return None
