# -*- coding: utf-8 -*-
"""
TransmissionCache Unittest Suite
================================
Unittest cases validating the functionality of the TransmissionCache. Mocks SpatialCodec.

Dependencies
------------
>>> import sys
>>> import unittest
>>> from unittest.mock import Mock
>>> from bitarray import bitarray
>>> from tcs.codec.cache import TransmissionCache

Copyright © 2020 LEAP. All Rights Reserved.
"""
import os
import sys
import unittest
from unittest.mock import Mock

from bitarray import bitarray

from tcs.codec.cache import TransmissionCache

# configure mock for SC
ap0 = bitarray('0010101011111100010111100001011000110000001001001111001010100110')  
hardware_map = bitarray('1111100001100000110110111000011101111100011001100100010010000100')
ap1 = bitarray('1111100110110110100001100001010110010101010000100000011011110100')
ap2 = bitarray('1101110000100101101000101110011110111100100011100110000000001100')
ap3 = bitarray('0001101001000101001111111100111011000000110001110101001100110000')
spatial_codec = Mock()
spatial_codec.hardware_map.return_value = hardware_map
spatial_codec.encode(ap0, 0).return_value = 0
spatial_codec.encode(ap0, 1).return_value = 1
spatial_codec.encode(ap0, 2).return_value = 2
spatial_codec.encode(ap0, 3).return_value = 3
spatial_codec.decode(0).return_value = ap0
spatial_codec.decode(1).return_value = ap1
spatial_codec.decode(2).return_value = ap2
spatial_codec.decode(3).return_value = ap3
sys.modules['SpatialCodec'] = spatial_codec

class TestCache(unittest.TestCase):

    os.environ['DIM'] = '4'

    def setUp(self):
        self.cache = TransmissionCache()
        self.cache.cache_map(ap0, 0)

    def tearDown(self):
        del self.cache

    @unittest.skip('Deprecated')
    def test_cache_miss(self):
        """Verify cache miss is correctly identified"""
        with self.assertRaises(ValueError):
            self.cache.validate(
                bitarray('1111100110100110100001100001010110010101010000100000011011110100'))
        
    @unittest.skip('Deprecated')
    def test_cache_hit(self):
        """Verify cache hit is correctly identified  at each access point"""
        assert self.cache.validate(ap0) == 0
        assert self.cache.validate(ap1) == 1
        assert self.cache.validate(ap2) == 2
        assert self.cache.validate(ap3) == 3

    def test_cache_mapping(self):
        """Verify the TransmissionCache correctly caches based on mocked input stream from SC"""
        assert self.cache._cache == [[ap0, ap1, ap2, ap3]]
        
    
if __name__ == "__main__":
    unittest.main()
