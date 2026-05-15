"""Base conversion GTK application."""

from .converter import (
    ConversionError,
    MAX_SOURCE_BASE,
    MAX_TARGET_BASE,
    UNSUPPORTED_TEXT_BASE_MESSAGE,
    convert_number,
    digits_to_int,
    digits_to_string,
    int_to_digits,
    parse_digits,
)

__all__ = [
    "ConversionError",
    "MAX_SOURCE_BASE",
    "MAX_TARGET_BASE",
    "UNSUPPORTED_TEXT_BASE_MESSAGE",
    "convert_number",
    "digits_to_int",
    "digits_to_string",
    "int_to_digits",
    "parse_digits",
]
