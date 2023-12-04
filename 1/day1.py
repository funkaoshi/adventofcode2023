import re

p1_regex = re.compile(r"(?:\d)")
p2_regex = re.compile(
    r"(?:\d)|(?:one)|(?:two)|(?:three)|(?:four)|(?:five)|(?:six)|(?:seven)|(?:eight)|(?:nine)"
)

string_to_digit = {
    "1": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}

def extract_digits(line, regex):
    """Pull out the first and last numeric values found in line"""
    matches = regex.findall(line)
    first = matches[0]
    second = matches[-1]
    value = string_to_digit[first] * 10 + string_to_digit[second]
    return value

with open("input.txt") as f:
    inputs = f.readlines()

print(sum([extract_digits(line, p1_regex) for line in inputs]))
print(sum([extract_digits(line, p2_regex) for line in inputs]))
