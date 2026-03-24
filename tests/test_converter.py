import unittest

from bases_app.converter import (
    ConversionError,
    UNSUPPORTED_TEXT_BASE_MESSAGE,
    convert_number,
    digits_to_int,
    digits_to_string,
    int_to_digits,
    parse_digits,
)


class ConverterTests(unittest.TestCase):
    def test_parse_digits_accepts_mixed_case(self) -> None:
        self.assertEqual(parse_digits("1a", 16), [1, 10])

    def test_parse_digits_rejects_invalid_digit(self) -> None:
        with self.assertRaises(ConversionError) as ctx:
            parse_digits("19", 8)
        self.assertIn("not valid for base 8", str(ctx.exception))

    def test_digits_to_int_and_back(self) -> None:
        value = digits_to_int([1, 0, 1, 1], 2)
        self.assertEqual(value, 11)
        self.assertEqual(int_to_digits(value, 16), [11])

    def test_convert_zero(self) -> None:
        result = convert_number("0", 10, 2)
        self.assertEqual(result.value, 0)
        self.assertEqual(result.digits, [0])
        self.assertEqual(result.text, "0")

    def test_convert_large_number_to_base_36(self) -> None:
        result = convert_number("18446744073709551616", 10, 36)
        self.assertEqual(result.text, "3W5E11264SGSG")
        self.assertEqual(result.digits, [3, 32, 5, 14, 1, 1, 2, 6, 4, 28, 16, 28, 16])

    def test_digits_to_string(self) -> None:
        self.assertEqual(digits_to_string([1, 10, 15]), "1AF")

    def test_convert_to_base_above_36_returns_digit_list_and_message(self) -> None:
        result = convert_number("255", 10, 60)
        self.assertEqual(result.digits, [4, 15])
        self.assertEqual(result.text, UNSUPPORTED_TEXT_BASE_MESSAGE)

    def test_source_base_above_36_is_invalid(self) -> None:
        with self.assertRaises(ConversionError) as ctx:
            convert_number("10", 37, 10)
        self.assertIn("Source base must be between 2 and 36", str(ctx.exception))

    def test_empty_input_is_invalid(self) -> None:
        with self.assertRaises(ConversionError) as ctx:
            convert_number("", 10, 2)
        self.assertIn("Enter a number", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
