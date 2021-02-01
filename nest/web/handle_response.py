# -*- coding: utf8 -*-
import functools

from webargs.core import ValidationError

from nest.app.use_case.authentication_plugin import InvalidCertificateError


def _extract_first_error_message(messages):
    if isinstance(messages, str):
        return messages
    if isinstance(messages, list):
        return _extract_first_error_message(messages[0])
    else:
        assert isinstance(messages, dict)
        # TODO: 只需要第一对key-value即可，这里应该可以改写为更好的形式。
        for field, sub_messages in messages.items():
            sub_message = _extract_first_error_message(sub_messages)
            return '{}: {}'.format(field, sub_message)


def wrap_response(func):
    @functools.wraps(func)
    def wrapper(*args, **kw):
        try:
            return func(*args, **kw)
        except InvalidCertificateError:
            return {
                'message': '请先登录'
            }, 401
        except ValidationError as e:
            message = _extract_first_error_message(e.messages)
            return {
                'message': message,
            }, 422

    return wrapper
