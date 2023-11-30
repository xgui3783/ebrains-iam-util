import re

def camel_to_snake(input: str):
    return re.sub(r'([A-Z]+)', r'_\1', input).lower()
