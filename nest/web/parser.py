# -*- coding: utf8 -*-
from webargs.flaskparser import FlaskParser

parser = FlaskParser()


@parser.error_handler
def _handle_error(error, req, schema, *, error_status_code, error_headers):
    raise error
