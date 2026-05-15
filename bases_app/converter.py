"""Pure helpers for base conversion."""

from __future__ import annotations

from dataclasses import dataclass

MIN_BASE = 2
MAX_SOURCE_BASE = 36
MAX_TARGET_BASE = 10_000
UNSUPPORTED_TEXT_BASE_MESSAGE = "Not supported"
_DIGITS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"


class ConversionError(ValueError):
    """Raised when an input cannot be converted."""


@dataclass(frozen=True)
class ConversionResult:
    value: int
    digits: list[int]
    text: str


def _validate_source_base(base: int) -> None:
    if not MIN_BASE <= base <= MAX_SOURCE_BASE:
        raise ConversionError(f"Source base must be between {MIN_BASE} and {MAX_SOURCE_BASE}.")


def _validate_target_base(base: int) -> None:
    if not MIN_BASE <= base <= MAX_TARGET_BASE:
        raise ConversionError(f"Target base must be between {MIN_BASE} and {MAX_TARGET_BASE}.")


def parse_digits(text: str, base: int) -> list[int]:
    _validate_source_base(base)
    normalized = text.strip().upper()
    if not normalized:
        raise ConversionError("Enter a number to convert.")

    digits: list[int] = []
    for char in normalized:
        if char not in _DIGITS:
            raise ConversionError(f"Unsupported digit '{char}'.")
        value = _DIGITS.index(char)
        if value >= base:
            raise ConversionError(f"Digit '{char}' is not valid for base {base}.")
        digits.append(value)
    return digits


def digits_to_int(digits: list[int], base: int) -> int:
    _validate_source_base(base)
    if not digits:
        raise ConversionError("At least one digit is required.")

    value = 0
    for digit in digits:
        if digit < 0 or digit >= base:
            raise ConversionError(f"Digit value {digit} is not valid for base {base}.")
        value = (value * base) + digit
    return value


def int_to_digits(value: int, base: int) -> list[int]:
    _validate_target_base(base)
    if value < 0:
        raise ConversionError("Only non-negative integers are supported.")
    if value == 0:
        return [0]

    digits: list[int] = []
    current = value
    while current:
        current, remainder = divmod(current, base)
        digits.append(remainder)
    digits.reverse()
    return digits


def digits_to_string(digits: list[int]) -> str:
    if not digits:
        raise ConversionError("At least one digit is required.")
    try:
        return "".join(_DIGITS[digit] for digit in digits)
    except IndexError as exc:
        raise ConversionError("Digit list contains values that cannot be rendered.") from exc


def convert_number(text: str, source_base: int, target_base: int) -> ConversionResult:
    source_digits = parse_digits(text, source_base)
    integer_value = digits_to_int(source_digits, source_base)
    target_digits = int_to_digits(integer_value, target_base)
    if target_base > MAX_SOURCE_BASE:
        text_output = UNSUPPORTED_TEXT_BASE_MESSAGE
    else:
        text_output = digits_to_string(target_digits)
    return ConversionResult(
        value=integer_value,
        digits=target_digits,
        text=text_output,
    )
