"""
tests.py
========
Comprehensive unit tests for numclassify.py
Run: python3 -m pytest tests.py -v
  or: python3 tests.py
"""

import unittest
from numclassify import *


class TestPrimes(unittest.TestCase):
    def test_basic_primes(self):
        for p in [2, 3, 5, 7, 11, 13, 17, 19, 23, 97, 101, 9973]:
            self.assertTrue(is_prime(p), f"{p} should be prime")

    def test_non_primes(self):
        for n in [0, 1, 4, 6, 8, 9, 10, 15, 25, 100]:
            self.assertFalse(is_prime(n), f"{n} should not be prime")

    def test_twin_primes(self):
        for p in [3, 5, 11, 17, 29]:
            self.assertTrue(is_twin_prime(p))

    def test_mersenne_prime(self):
        for p in [3, 7, 31, 127, 8191]:
            self.assertTrue(is_mersenne_prime(p))
        self.assertFalse(is_mersenne_prime(15))

    def test_safe_prime(self):
        for p in [5, 7, 11, 23, 47]:
            self.assertTrue(is_safe_prime(p))

    def test_sophie_germain(self):
        for p in [2, 3, 5, 11, 23, 29]:
            self.assertTrue(is_sophie_germain_prime(p))

    def test_circular_prime(self):
        self.assertTrue(is_circular_prime(197))
        self.assertTrue(is_circular_prime(11))
        self.assertFalse(is_circular_prime(15))

    def test_emirp(self):
        self.assertTrue(is_emirp(13))
        self.assertTrue(is_emirp(17))
        self.assertFalse(is_emirp(11))  # palindrome

    def test_left_right_truncatable(self):
        self.assertTrue(is_left_truncatable_prime(9137))
        self.assertTrue(is_right_truncatable_prime(2399))

    def test_prime_factors(self):
        self.assertEqual(get_prime_factors(12), [2, 2, 3])
        self.assertEqual(get_prime_factors(1729), [7, 13, 19])
        self.assertEqual(get_prime_factors(100), [2, 2, 5, 5])

    def test_carmichael(self):
        for n in [561, 1105, 1729]:
            self.assertTrue(is_carmichael(n))
        self.assertFalse(is_carmichael(15))

    def test_miller_rabin(self):
        for p in [2, 3, 5, 7, 11, 97, 1009]:
            self.assertTrue(is_prime_miller_rabin(p))
        for n in [4, 9, 15, 25, 561]:
            self.assertFalse(is_prime_miller_rabin(n))

    def test_pythagorean_prime(self):
        for p in [5, 13, 17, 29, 37]:
            self.assertTrue(is_pythagorean_prime(p))
        self.assertFalse(is_pythagorean_prime(3))

    def test_wieferich_prime(self):
        self.assertTrue(is_wieferich_prime(1093))
        self.assertTrue(is_wieferich_prime(3511))
        self.assertFalse(is_wieferich_prime(5))

    def test_cousin_prime(self):
        self.assertTrue(is_cousin_prime(7))  # 3,7
        self.assertTrue(is_cousin_prime(13))  # 13,17

    def test_sexy_prime(self):
        self.assertTrue(is_sexy_prime(5))   # 5,11
        self.assertTrue(is_sexy_prime(11))

    def test_chen_prime(self):
        self.assertTrue(is_chen_prime(3))   # 3+2=5 prime
        self.assertTrue(is_chen_prime(5))   # 5+2=7 prime

    def test_prime_next_prev(self):
        self.assertEqual(next_prime(10), 11)
        self.assertEqual(next_prime(13), 17)
        self.assertEqual(prev_prime(10), 7)


class TestArmstrong(unittest.TestCase):
    def test_armstrong(self):
        for n in [1, 2, 3, 4, 5, 6, 7, 8, 9, 153, 370, 371, 407]:
            self.assertTrue(is_armstrong(n), f"{n}")
        for n in [10, 100, 200, 154]:
            self.assertFalse(is_armstrong(n))

    def test_disarium(self):
        for n in [1, 2, 3, 89, 135, 175]:
            self.assertTrue(is_disarium(n), f"{n}")
        self.assertFalse(is_disarium(100))

    def test_munchausen(self):
        self.assertTrue(is_munchausen(1))
        self.assertTrue(is_munchausen(3435))

    def test_pdi(self):
        self.assertTrue(is_pdi_3(153))
        self.assertTrue(is_pdi_3(370))


class TestPerfectAbundant(unittest.TestCase):
    def test_perfect(self):
        for n in [6, 28, 496, 8128]:
            self.assertTrue(is_perfect(n), f"{n}")
        self.assertFalse(is_perfect(12))

    def test_abundant(self):
        for n in [12, 18, 20, 24]:
            self.assertTrue(is_abundant(n))
        self.assertFalse(is_abundant(6))

    def test_deficient(self):
        for n in [2, 3, 4, 5, 7, 8, 9, 10]:
            self.assertTrue(is_deficient(n))

    def test_semiperfect(self):
        self.assertTrue(is_semiperfect(6))
        self.assertTrue(is_semiperfect(12))

    def test_weird(self):
        self.assertTrue(is_weird(70))

    def test_amicable(self):
        self.assertTrue(is_amicable(220))
        self.assertTrue(is_amicable(284))
        self.assertFalse(is_amicable(100))

    def test_superperfect(self):
        for n in [2, 4, 16, 64]:
            self.assertTrue(is_superperfect(n))

    def test_harmonic_divisor(self):
        self.assertTrue(is_harmonic_divisor(1))
        self.assertTrue(is_harmonic_divisor(6))
        self.assertTrue(is_harmonic_divisor(28))


class TestPalindrome(unittest.TestCase):
    def test_palindrome(self):
        for n in [1, 11, 121, 1221, 12321, 99999]:
            self.assertTrue(is_palindrome(n))
        for n in [10, 12, 123, 1234]:
            self.assertFalse(is_palindrome(n))

    def test_binary_palindrome(self):
        self.assertTrue(is_binary_palindrome(9))   # 1001
        self.assertTrue(is_binary_palindrome(21))  # 10101
        self.assertFalse(is_binary_palindrome(10))

    def test_lychrel(self):
        self.assertTrue(is_lychrel(196))
        self.assertFalse(is_lychrel(56))  # 56+65=121

    def test_strobogrammatic(self):
        for n in [0, 1, 8, 11, 69, 88, 96, 101, 111, 181, 609]:
            self.assertTrue(is_strobogrammatic(n), f"{n}")
        self.assertFalse(is_strobogrammatic(2))


class TestDigitProperties(unittest.TestCase):
    def test_digit_sum(self):
        self.assertEqual(digit_sum(123), 6)
        self.assertEqual(digit_sum(999), 27)
        self.assertEqual(digit_sum(0), 0)

    def test_digital_root(self):
        self.assertEqual(digital_root(999), 9)
        self.assertEqual(digital_root(123), 6)
        self.assertEqual(digital_root(9999), 9)

    def test_additive_persistence(self):
        self.assertEqual(additive_persistence(199), 3)
        self.assertEqual(additive_persistence(0), 0)

    def test_multiplicative_persistence(self):
        self.assertEqual(multiplicative_persistence(77), 4)
        self.assertEqual(multiplicative_persistence(999), 4)

    def test_smith(self):
        self.assertTrue(is_smith(4))
        self.assertTrue(is_smith(22))
        self.assertFalse(is_smith(17))

    def test_self_number(self):
        for n in [1, 3, 5, 7, 9, 20, 31, 42]:
            self.assertTrue(is_self(n))

    def test_bouncy(self):
        self.assertTrue(is_bouncy(1543))
        self.assertFalse(is_bouncy(134))   # increasing
        self.assertFalse(is_bouncy(4321))  # decreasing

    def test_pandigital(self):
        self.assertTrue(is_pandigital(123456789))  # 1-9 pandigital
        self.assertTrue(is_pandigital(12345))       # pandigital 1-5 (by length)
        self.assertFalse(is_pandigital(11345))      # repeated digit
        self.assertTrue(is_pandigital_1_9(123456789))
        self.assertFalse(is_pandigital_1_9(12345))

    def test_repunit(self):
        for n in [1, 11, 111, 1111]:
            self.assertTrue(is_repunit(n))

    def test_repdigit(self):
        for n in [1, 22, 333, 4444, 55555]:
            self.assertTrue(is_repdigit(n))

    def test_harshad(self):
        for n in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 18, 20]:
            self.assertTrue(is_harshad(n), f"{n}")

    def test_kaprekar(self):
        for n in [1, 9, 45, 55, 99, 703, 999, 2223]:
            self.assertTrue(is_kaprekar(n), f"{n}")

    def test_metadrome(self):
        self.assertTrue(is_metadrome(1234))
        self.assertTrue(is_metadrome(159))
        self.assertFalse(is_metadrome(121))

    def test_katadrome(self):
        self.assertTrue(is_katadrome(9876))
        self.assertFalse(is_katadrome(1234))

    def test_undulating(self):
        self.assertTrue(is_undulating(12121))
        self.assertTrue(is_undulating(96969))
        self.assertFalse(is_undulating(1234))

    def test_cyclops(self):
        self.assertTrue(is_cyclops(101))    # 3 digits, single zero in middle
        self.assertTrue(is_cyclops(201))    # 3 digits, single zero in middle
        self.assertTrue(is_cyclops(11011)) # 5 digits, single zero in middle
        self.assertFalse(is_cyclops(100))   # trailing zero, not middle
        self.assertFalse(is_cyclops(10001)) # zeros at positions 1 and 3, not just middle

    def test_nude(self):
        self.assertTrue(is_nude(11))
        self.assertTrue(is_nude(12))
        self.assertTrue(is_nude(24))

    def test_polydivisible(self):
        self.assertTrue(is_polydivisible(381654729))


class TestFibonacciSequences(unittest.TestCase):
    def test_fibonacci(self):
        for n in [0, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144]:
            self.assertTrue(is_fibonacci(n), f"{n}")
        self.assertFalse(is_fibonacci(4))

    def test_lucas(self):
        for n in [2, 1, 3, 4, 7, 11, 18, 29]:
            self.assertTrue(is_lucas(n), f"{n}")

    def test_tribonacci(self):
        for n in [0, 1, 2, 4, 7, 13, 24, 44]:
            self.assertTrue(is_tribonacci(n), f"{n}")

    def test_pell(self):
        for n in [0, 1, 2, 5, 12, 29, 70]:
            self.assertTrue(is_pell(n), f"{n}")

    def test_catalan(self):
        for n in [1, 2, 5, 14, 42, 132]:
            self.assertTrue(is_catalan(n), f"{n}")
        self.assertFalse(is_catalan(6))

    def test_fibbinary(self):
        for n in [1, 2, 4, 5, 8, 10, 16, 17]:
            self.assertTrue(is_fibbinary(n), f"{n}")
        self.assertFalse(is_fibbinary(3))  # 11 in binary

    def test_padovan(self):
        for n in [1, 2, 3, 4, 5, 7, 9, 12]:
            self.assertTrue(is_padovan(n), f"{n}")


class TestFigurate(unittest.TestCase):
    def test_triangular(self):
        for n in [1, 3, 6, 10, 15, 21, 28, 36, 45, 55]:
            self.assertTrue(is_triangular(n), f"{n}")
        self.assertFalse(is_triangular(4))

    def test_pentagonal(self):
        for n in [1, 5, 12, 22, 35, 51, 70]:
            self.assertTrue(is_pentagonal(n), f"{n}")

    def test_hexagonal(self):
        for n in [1, 6, 15, 28, 45, 66]:
            self.assertTrue(is_hexagonal(n), f"{n}")

    def test_pronic(self):
        for n in [2, 6, 12, 20, 30, 42, 56]:
            self.assertTrue(is_pronic(n), f"{n}")

    def test_star(self):
        for n in [1, 13, 37, 73]:
            self.assertTrue(is_star(n), f"{n}")

    def test_centered_square(self):
        for n in [1, 5, 13, 25, 41]:
            self.assertTrue(is_centered_square(n), f"{n}")

    def test_tetrahedral(self):
        for n in [1, 4, 10, 20, 35, 56]:
            self.assertTrue(is_tetrahedral(n), f"{n}")


class TestPowers(unittest.TestCase):
    def test_perfect_square(self):
        for n in [0, 1, 4, 9, 16, 25, 36, 49, 100]:
            self.assertTrue(is_perfect_square(n), f"{n}")
        self.assertFalse(is_perfect_square(2))

    def test_perfect_cube(self):
        for n in [1, 8, 27, 64, 125, 216, 1000]:
            self.assertTrue(is_perfect_cube(n), f"{n}")

    def test_perfect_power(self):
        for n in [4, 8, 9, 16, 25, 27, 32, 36, 49]:
            self.assertTrue(is_perfect_power(n), f"{n}")

    def test_powerful(self):
        for n in [1, 4, 8, 9, 16, 25, 27, 32, 36]:
            self.assertTrue(is_powerful(n), f"{n}")

    def test_squarefree(self):
        for n in [1, 2, 3, 5, 6, 7, 10, 11, 13, 14, 15]:
            self.assertTrue(is_squarefree(n), f"{n}")
        for n in [4, 8, 9, 12, 18, 25]:
            self.assertFalse(is_squarefree(n), f"{n}")

    def test_power_of_two(self):
        for n in [1, 2, 4, 8, 16, 32, 64, 128, 1024]:
            self.assertTrue(is_power_of_two(n), f"{n}")
        self.assertFalse(is_power_of_two(3))

    def test_sum_of_two_squares(self):
        for n in [0, 1, 2, 4, 5, 8, 9, 10, 13, 16, 17, 25]:
            self.assertTrue(is_sum_of_two_squares(n), f"{n}")
        self.assertFalse(is_sum_of_two_squares(3))


class TestBinaryProperties(unittest.TestCase):
    def test_evil(self):
        for n in [0, 3, 5, 6, 9, 10, 12, 15]:
            self.assertTrue(is_evil(n), f"{n} bin={bin(n)}")

    def test_odious(self):
        for n in [1, 2, 4, 7, 8, 11, 13, 14]:
            self.assertTrue(is_odious(n), f"{n}")

    def test_pernicious(self):
        for n in [3, 5, 6, 7, 10, 11, 12, 13]:
            self.assertTrue(is_pernicious(n), f"{n}")

    def test_count_set_bits(self):
        self.assertEqual(count_set_bits(7), 3)
        self.assertEqual(count_set_bits(8), 1)
        self.assertEqual(count_set_bits(255), 8)

    def test_blum_integer(self):
        self.assertTrue(is_blum_integer(21))   # 3*7
        self.assertTrue(is_blum_integer(33))   # 3*11
        self.assertFalse(is_blum_integer(15))  # 3*5, 5≡1 mod4


class TestDivisibility(unittest.TestCase):
    def test_smooth(self):
        self.assertTrue(is_5_smooth(12))
        self.assertTrue(is_5_smooth(60))
        self.assertFalse(is_5_smooth(14))

    def test_practical(self):
        for n in [1, 2, 4, 6, 8, 12, 16, 18, 20, 24]:
            self.assertTrue(is_practical(n), f"{n}")

    def test_refactorable(self):
        for n in [1, 2, 8, 9, 12]:
            self.assertTrue(is_refactorable(n), f"{n}")

    def test_economical(self):
        self.assertTrue(is_economical(125))  # 5^3: 1 digit vs 3
        self.assertFalse(is_economical(10))  # 2*5: 2 digits == 2

    def test_sphenic(self):
        self.assertTrue(is_sphenic(30))   # 2*3*5
        self.assertTrue(is_sphenic(42))   # 2*3*7
        self.assertFalse(is_sphenic(12))

    def test_arithmetic_number(self):
        for n in [1, 3, 5, 6, 7, 11, 13, 14]:
            self.assertTrue(is_arithmetic_number(n), f"{n}")


class TestFactorial(unittest.TestCase):
    def test_factorial(self):
        for n in [1, 2, 6, 24, 120, 720, 5040]:
            self.assertTrue(is_factorial(n), f"{n}")
        self.assertFalse(is_factorial(100))

    def test_primorial(self):
        self.assertTrue(is_primorial(2))
        self.assertTrue(is_primorial(6))
        self.assertTrue(is_primorial(30))
        self.assertFalse(is_primorial(12))

    def test_hyperfactorial(self):
        self.assertTrue(is_hyperfactorial(1))
        self.assertTrue(is_hyperfactorial(4))
        self.assertTrue(is_hyperfactorial(108))

    def test_subfactorial(self):
        self.assertTrue(is_subfactorial(1))
        self.assertTrue(is_subfactorial(2))
        self.assertTrue(is_subfactorial(9))


class TestSpecialNumbers(unittest.TestCase):
    def test_taxicab_1729(self):
        self.assertTrue(is_taxicab(1729))  # 1^3+12^3 = 9^3+10^3

    def test_keith(self):
        for n in [14, 19, 28, 47, 61, 75]:
            self.assertTrue(is_keith(n), f"{n}")
        self.assertFalse(is_keith(20))

    def test_giuga(self):
        self.assertTrue(is_giuga(30))
        self.assertFalse(is_giuga(12))

    def test_vampire(self):
        self.assertTrue(is_vampire(1260))  # 21*60
        self.assertTrue(is_vampire(1395))  # 15*93
        self.assertFalse(is_vampire(100))

    def test_untouchable(self):
        for n in [2, 5, 52, 88]:
            self.assertTrue(is_untouchable(n))

    def test_zumkeller(self):
        self.assertTrue(is_zumkeller(6))
        self.assertTrue(is_zumkeller(12))

    def test_parasitic(self):
        # 142857 * 3 = 428571 (move '1' from front to back)
        self.assertTrue(is_parasitic(142857, 3))
        self.assertFalse(is_parasitic(100, 2))

    def test_spy(self):
        self.assertTrue(is_spy(22))    # 2+2=4, 2*2=4
        self.assertTrue(is_spy(1124)) # 1+1+2+4=8, 1*1*2*4=8

    def test_neon(self):
        self.assertTrue(is_neon(1))
        self.assertTrue(is_neon(9))   # 81 -> 8+1=9
        self.assertFalse(is_neon(2))

    def test_automorphic(self):
        for n in [0, 1, 5, 6, 25, 76, 376]:
            self.assertTrue(is_automorphic(n), f"{n}")


class TestConversions(unittest.TestCase):
    def test_roman(self):
        self.assertEqual(to_roman(1), 'I')
        self.assertEqual(to_roman(4), 'IV')
        self.assertEqual(to_roman(2024), 'MMXXIV')
        self.assertEqual(to_roman(1999), 'MCMXCIX')

    def test_from_roman(self):
        self.assertEqual(from_roman('XIV'), 14)
        self.assertEqual(from_roman('MCMXCIX'), 1999)

    def test_int_to_words(self):
        self.assertEqual(int_to_words(0), 'zero')
        self.assertEqual(int_to_words(1), 'one')
        self.assertEqual(int_to_words(21), 'twenty-one')
        self.assertEqual(int_to_words(100), 'one hundred')
        self.assertEqual(int_to_words(1000), 'one thousand')
        self.assertEqual(int_to_words(1_000_000), 'one million')

    def test_to_base(self):
        self.assertEqual(to_base(10, 2), '1010')
        self.assertEqual(to_base(255, 16), 'ff')
        self.assertEqual(to_base(8, 8), '10')

    def test_binary(self):
        self.assertEqual(to_binary(10), '1010')
        self.assertEqual(to_binary(0), '0')

    def test_octal(self):
        self.assertEqual(to_octal(8), '10')

    def test_hex(self):
        self.assertEqual(to_hex(255), 'ff')


class TestNumberTheory(unittest.TestCase):
    def test_euler_totient(self):
        self.assertEqual(euler_totient(1), 1)
        self.assertEqual(euler_totient(6), 2)
        self.assertEqual(euler_totient(10), 4)
        self.assertEqual(euler_totient(12), 4)

    def test_mobius(self):
        self.assertEqual(mobius(1), 1)
        self.assertEqual(mobius(6), 1)   # 2*3
        self.assertEqual(mobius(4), 0)   # 2^2
        self.assertEqual(mobius(2), -1)
        self.assertEqual(mobius(30), -1) # 2*3*5

    def test_goldbach(self):
        pairs = goldbach_pairs(28)
        self.assertIn((5, 23), pairs)
        self.assertIn((11, 17), pairs)

    def test_gcd_lcm(self):
        self.assertEqual(gcd(12, 8), 4)
        self.assertEqual(lcm(4, 6), 12)
        self.assertEqual(gcd(17, 5), 1)

    def test_sigma(self):
        self.assertEqual(sigma_0(6), 4)   # 1,2,3,6
        self.assertEqual(sigma_1(6), 12)

    def test_primitive_root(self):
        self.assertTrue(is_primitive_root(2, 5))
        self.assertFalse(is_primitive_root(4, 5))

    def test_legendre(self):
        self.assertEqual(legendre_symbol(2, 7), 1)
        self.assertEqual(legendre_symbol(3, 7), -1)

    def test_crt(self):
        # x ≡ 2 (mod 3), x ≡ 3 (mod 5) → x ≡ 8 (mod 15)
        self.assertEqual(chinese_remainder([2, 3], [3, 5]), 8)


class TestCollatz(unittest.TestCase):
    def test_collatz_steps(self):
        self.assertEqual(collatz_steps(1), 0)
        self.assertEqual(collatz_steps(2), 1)
        self.assertEqual(collatz_steps(4), 2)

    def test_collatz_sequence(self):
        self.assertEqual(collatz_sequence(6), [6, 3, 10, 5, 16, 8, 4, 2, 1])

    def test_collatz_max(self):
        self.assertEqual(collatz_max(4), 4)
        self.assertGreater(collatz_max(27), 27)


class TestRangeUtilities(unittest.TestCase):
    def test_primes_up_to(self):
        self.assertEqual(primes_up_to(20), [2, 3, 5, 7, 11, 13, 17, 19])

    def test_find_in_range_armstrong(self):
        result = find_in_range(is_armstrong, 1, 500)
        self.assertEqual(result, [1, 2, 3, 4, 5, 6, 7, 8, 9, 153, 370, 371, 407])

    def test_nth_prime(self):
        self.assertEqual(nth_prime(1), 2)
        self.assertEqual(nth_prime(5), 11)
        self.assertEqual(nth_prime(10), 29)

    def test_nth_fibonacci(self):
        self.assertEqual(nth_fibonacci(0), 0)
        self.assertEqual(nth_fibonacci(7), 13)

    def test_nth_triangular(self):
        self.assertEqual(nth_triangular(4), 10)
        self.assertEqual(nth_triangular(5), 15)

    def test_nth_catalan(self):
        self.assertEqual(nth_catalan(0), 1)
        self.assertEqual(nth_catalan(3), 5)
        self.assertEqual(nth_catalan(4), 14)


class TestGetAllProperties(unittest.TestCase):
    def test_get_all_returns_dict(self):
        props = get_all_properties(6)
        self.assertIsInstance(props, dict)
        self.assertIn('is_prime', props)
        self.assertIn('is_perfect', props)
        self.assertIn('digit_sum', props)

    def test_153_is_armstrong(self):
        props = get_all_properties(153)
        self.assertTrue(props['is_armstrong'])
        self.assertFalse(props['is_prime'])

    def test_6_is_perfect(self):
        props = get_all_properties(6)
        self.assertTrue(props['is_perfect'])

    def test_1729_is_taxicab(self):
        props = get_all_properties(1729)
        self.assertTrue(props['is_taxicab'])
        self.assertTrue(props['is_carmichael'])

    def test_get_true_properties(self):
        true_props = get_true_properties(9)
        self.assertIn('is_perfect_square', true_props)
        self.assertIn('is_perfect_power', true_props)

    def test_count_properties(self):
        self.assertGreater(count_properties(1729), 10)


class TestCalendar(unittest.TestCase):
    def test_leap_year(self):
        for y in [1600, 2000, 2004, 2024]:
            self.assertTrue(is_leap_year(y), f"{y}")
        for y in [1700, 1800, 1900, 2023]:
            self.assertFalse(is_leap_year(y), f"{y}")


class TestChecksums(unittest.TestCase):
    def test_luhn(self):
        self.assertTrue(is_luhn_valid(4532015112830366))

    def test_divisibility_11(self):
        self.assertTrue(is_divisibility_rule_11(121))
        self.assertTrue(is_divisibility_rule_11(1331))
        self.assertFalse(is_divisibility_rule_11(123))


if __name__ == '__main__':
    unittest.main(verbosity=2)
