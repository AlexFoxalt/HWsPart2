import random
import string
from flask import request, Flask

UPPER_LETTERS = string.ascii_uppercase
LOWER_LETTERS = string.ascii_lowercase
DIGITS = string.digits
SPECIALS = string.punctuation


def parse_params(arg: dict):
    """
    Fetch params from URL. Check all of possible errors.

    :param arg: Expected dict of params parsed from URL string.
    :return: Values of 3 options for password generator machine.
    """
    try:  # If no 'length' or some trash cases like 'length=sdsada'
        length = int(arg.get('length', 10)) if int(arg.get('length', 10)) in range(1, 101) else 10  # 1<=len<=100
    except ValueError:
        length = 10

    try:  # Same as str.18
        digits = int(arg.get('digits', 0))
    except ValueError:
        digits = 0

    try:  # Same as str.18
        specials = int(arg.get('specials', 0))
    except ValueError:
        specials = 0

    return length, digits, specials


app = Flask(__name__)


@app.route("/")
def get_password():
    """
    Take values from parse_params() function, then pass them to the password generator.

    :return: Random password as .html file.
    """
    params = request.args  # Dict of params here

    length, digits, specials = parse_params(params)  # [0]length, [1]digits, [2]specials

    string_generator = [*UPPER_LETTERS, *LOWER_LETTERS]  # Standard options for generator

    if digits:
        string_generator.extend(DIGITS)
        digits = '✔ Digits included'  # Just for informativeness of response.
    else:
        digits = '✘ Digits NOT included'

    if specials:
        string_generator.extend(SPECIALS)
        specials = '✔ Specials included'
    else:
        specials = '✘ Specials NOT included'

    password = ''.join(random.choices(string_generator, k=length))

    length = 'Length = ' + str(length)

    return '<br>'.join((length, digits, specials, password))


if __name__ == "__main__":
    app.run(debug=True)
