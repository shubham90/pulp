from cStringIO import StringIO
import hashlib
import unittest

from pulp.plugins.util import verification

from pulp.server.exceptions import PulpCodedException


class TestSanitizeChecksumType(unittest.TestCase):
    """
    This class contains tests for the sanitize_checksum_type() function.
    """

    def test_sha_to_sha1(self):
        """
        Assert that "sha" is converted to "sha1".
        """
        checksum_type = verification.sanitize_checksum_type('sha')

        self.assertEqual(checksum_type, 'sha1')

    def test_ShA_to_sha1(self):
        """
        Assert that "ShA" is converted to "sha1".
        """
        checksum_type = verification.sanitize_checksum_type('ShA')

        self.assertEqual(checksum_type, 'sha1')

    def test_SHA256_to_sha256(self):
        """
        Assert that "SHA256" is converted to "sha256".
        """
        checksum_type = verification.sanitize_checksum_type('SHA256')

        self.assertEqual(checksum_type, 'sha256')

    def test_invalid_type_raises_coded_exception(self):
        self.assertRaises(PulpCodedException,
                          verification.sanitize_checksum_type, 'not_a_real_checksum')


class VerificationTests(unittest.TestCase):

    def test_size(self):
        # Setup
        expected_size = 9
        test_file = StringIO('Test data')

        # Test - Should not raise an exception
        verification.verify_size(test_file, expected_size)

    def test_size_incorrect(self):
        test_file = StringIO('Test data')

        # Test
        self.assertRaises(verification.VerificationException, verification.verify_size, test_file,
                          1)

    def test_checksum_sha1(self):
        # Setup
        test_file = StringIO('Test Data')
        expected_checksum = 'cae99c6102aa3596ff9b86c73881154e340c2ea8'

        # Test - Should not raise an exception
        verification.verify_checksum(test_file, verification.TYPE_SHA1, expected_checksum)

    def test_checksum_sha(self):
        # Setup (sha is an alias for sha1)
        test_file = StringIO('Test Data')
        expected_checksum = 'cae99c6102aa3596ff9b86c73881154e340c2ea8'

        # Test - Should not raise an exception
        verification.verify_checksum(test_file, verification.TYPE_SHA, expected_checksum)

    def test_checksum_sha256(self):
        # Setup
        test_file = StringIO('Test data')
        expected_checksum = 'e27c8214be8b7cf5bccc7c08247e3cb0c1514a48ee1f63197fe4ef3ef51d7e6f'

        # Test - Should not raise an exception
        verification.verify_checksum(test_file, verification.TYPE_SHA256, expected_checksum)

    def test_checksum_sha256_incorrect(self):
        # Setup
        test_file = StringIO('Test data')

        # Test
        self.assertRaises(verification.VerificationException, verification.verify_checksum,
                          test_file, verification.TYPE_SHA256, 'foo')

    def test_checksum_invalid_checksum(self):
        self.assertRaises(verification.InvalidChecksumType, verification.verify_checksum,
                          StringIO(), 'fake-type', 'irrelevant')

    def test_checksum_algorithm_mappings(self):
        self.assertEqual(4, len(verification.CHECKSUM_FUNCTIONS))
        self.assertEqual(verification.CHECKSUM_FUNCTIONS[verification.TYPE_MD5], hashlib.md5)
        self.assertEqual(verification.CHECKSUM_FUNCTIONS[verification.TYPE_SHA1], hashlib.sha1)
        self.assertEqual(verification.CHECKSUM_FUNCTIONS[verification.TYPE_SHA], hashlib.sha1)
        self.assertEqual(verification.CHECKSUM_FUNCTIONS[verification.TYPE_SHA256], hashlib.sha256)
