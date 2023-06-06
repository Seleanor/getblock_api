from functools import wraps
import allure


class AllureMessage:
    CHECK_STATUS_CODE = 'Status code must be {}'
    CHECK_KEY_RESPONSE_BODY = 'Check the following keys in response body: {}'
    CHECK_VALUE_RESPONSE_BODY = 'Check value from key in response body: {}'
    REPEAT_REQUEST = 'Repeat following request: {}'


def allure_step(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        with allure.step(f"{self.__module__.split('.')[-2].capitalize()}.{self.__class__.__name__}.{func.__name__} {args}"):
            pass
            action = func(self, *args, **kwargs)
            with allure.step(f"Returning {action}"):
                pass
        return action
    return wrapper
