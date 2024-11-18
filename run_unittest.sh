#!/bin/bash
export MODE=local_unittest

pytest -ra -s -x ./tests
