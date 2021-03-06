#!/usr/bin/env python
# coding: utf-8

from nose import main
from nose.tools import *

from msgpack import packb, unpackb

def _decode_complex(obj):
    if b'__complex__' in obj:
        return complex(obj[b'real'], obj[b'imag'])
    return obj

def _encode_complex(obj):
    if isinstance(obj, complex):
        return {b'__complex__': True, b'real': 1, b'imag': 2}
    return obj

def test_encode_hook():
    packed = packb([3, 1+2j], default=_encode_complex)
    unpacked = unpackb(packed)
    eq_(unpacked[1], {b'__complex__': True, b'real': 1, b'imag': 2})

def test_decode_hook():
    packed = packb([3, {b'__complex__': True, b'real': 1, b'imag': 2}])
    unpacked = unpackb(packed, object_hook=_decode_complex)
    eq_(unpacked[1], 1+2j)

@raises(ValueError)
def test_bad_hook():
    packed = packb([3, 1+2j], default=lambda o: o)
    unpacked = unpackb(packed)

def _arr_to_str(arr):
    return ''.join(str(c) for c in arr)

def test_array_hook():
    packed = packb([1,2,3])
    unpacked = unpackb(packed, list_hook=_arr_to_str)
    eq_(unpacked, '123')

if __name__ == '__main__':
    main()
