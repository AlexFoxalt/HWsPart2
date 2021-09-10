"""HW1 Чернышов Алексей"""

# Задание: Дополнить декоратор cache поддержкой max_limit.
# Алгоритм кеширования LFU: https://en.wikipedia.org/wiki/Least_frequently_used

from functools import wraps
from requests import get
from time import sleep
from random import choice, randint


class CachedItem:
    """
    Class of data, which contain:
    :url: The URL of website as string;
    :data: The content of website as string;
    :counter: The number of mentions of each URL which were requested by the user as int.
    """

    def __init__(self, url: str, data: str, counter: int):
        self.url = url
        self.data = data
        self.counter = counter

    def __str__(self):
        """
        Admin ability. Used for monitoring the object of this class.
        """
        return f'URL ------>  {self.url}\n' \
               f'DATA ----->  {self.data}\n' \
               f'COUNTER -->  {self.counter}'

    def __eq__(self, other):
        """
        Serves to check if the DB already contains an object. Typically comparing with an URL as str.
        """
        return self.url == other


def check_existence(url: str, iterable: list):
    """
    This function will check if the DB contain an url.

    :param url: Expected a URL address as string.
    :param iterable: Expected an iterable which will contain objects of a class.
    :return: Class object if find one in the iterable, if not- None
    """
    for item in iterable:
        if item == url:
            return item


def response_shaper_from_db(obj: CachedItem):
    """
    Function will return cached data from the DB in beautiful format and increase the counter.

    :param obj: Expected the CachedItem class object to form a response as str.
    :return: Response as str.
    """
    obj.counter += 1
    return f'[from cache] {obj.data}'


def cache(limit=10):
    """
    Main function of cache shaper.
    Takes the function and arguments of one. Checking, if DB contains the result of function- it will return the cached
    data, other way- it'll remember the result and next time, if request will be repeated, return cached content.

    :param limit: The maximum size of cache database as int.
    :return: Working result of function.
    """

    def shaper(function):

        @wraps(function)
        def wrapper(*args, **kwargs):

            if args:
                if len(args) > 1:  # Notifications about minor trouble, if such exists.
                    print('!ATTENTION! Since you entered several arguments, only the first one will be processed.')

                key = args[0]
                temp_data = check_existence(key, CachedData)

                if temp_data:  # If the DB contains such URL go here.
                    return response_shaper_from_db(temp_data)

            elif kwargs:  # Same for kwargs if they were entered instead of pos.arguments.
                if len(kwargs) > 1:
                    print('!ATTENTION! Since you entered several keyword arguments, only "url" key will be processed.')

                try:  # Here we want to check if 'url' kwarg was entered.
                    key = kwargs['url']
                    temp_data = check_existence(key, CachedData)

                    if temp_data:
                        return response_shaper_from_db(temp_data)

                except KeyError:  # Notifications about major trouble, if such exists.
                    return '!Error! No argument with key "url" was found!'  # Sending Error message to the user.
            else:
                return '!Error! No arguments were given!'

            data = function(key)  # Write a content of site as str if such URL wasn't cached before.

            if isinstance(data, str):  # We don't want to write in cache error cases, so check if request was incorrect.
                return data  # Positive request will return bytes, negative - error message as string.

            if len(CachedData) >= limit:  # Check if the DB exceeds the set limit.
                # If we passed the limit, we want to spot which item should be removed.
                CachedData.sort(key=lambda i: i.counter, reverse=True)
                # Now we can remove the last one item cuz it was mentioned less times then other.
                CachedData.pop()

            fresh_counter = 1
            CachedData.append(CachedItem(key, data, fresh_counter))  # Adding the new item to the DB with fresh counter.

            return data

        return wrapper

    CachedData = []  # Creating a new database as list of CachedItem class objects.

    return shaper


@cache(limit=3)
def fetch_url(url: str, first_n=50):
    """
    Fetch a given url.

    :param url: Site address as str.
    :param first_n: Set the limit of returning data as int.
    :return: HTML content of site as str.
    """

    try:
        res = get(url)
    except Exception as e:
        print(f'Error spotted: {e}')  # Sending the info about error to admin logs.
        return '!Error! Something went wrong :('

    return res.content[:first_n]


"""~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ tests ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""


def normal_testing():
    print('~' * 20, 'normal tests next', '~' * 20, '\n\n')

    urls = [
        'https://www.google.com/',
        'https://www.youtube.com/',
        'https://www.apple.com/',
        'https://www.nasa.gov/',
        'https://stackoverflow.com/',
        'https://www.wikipedia.org/',
        'https://www.python.org/',
        'https://www.fcbarcelona.com/',
        'https://rozetka.com.ua/'
    ]

    for counter in range(len(urls)):
        address = choice(urls)
        for repeat_request in range(randint(1, 3)):
            print('-> ', fetch_url(address), '->', address)
            sleep(1)


def freak_testing():
    print('\n\n', '~' * 20, 'freak tests next', '~' * 20, '\n\n')

    print('->', fetch_url('blablabla'))
    sleep(1)
    print('->', fetch_url(abc='https://en.wikipedia.org/wiki/Welsh_Corgi',
                          xyz='https://en.wikipedia.org/wiki/Giant_panda',
                          bla='https://en.wikipedia.org/wiki/Quokka'))
    sleep(1)
    print('->', fetch_url())
    sleep(1)
    print('->', fetch_url(123123123123))
    sleep(1)
    print('->', fetch_url(True, False, None))
    sleep(1)
    print('->', fetch_url('https://123/', 'https://123/', 'https://123/'))


"""~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""

normal_testing()
freak_testing()
