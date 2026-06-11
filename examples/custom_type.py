from numclassify import register
import numclassify as nc

# Add a custom number type using the @register decorator
@register(name="Lucky Seven Multiple", category="recreational")
def is_lucky_seven_multiple(n: int) -> bool:
    return n > 0 and n % 7 == 0 and "7" in str(n)

# Now works across the entire API
print(nc.is_lucky_seven_multiple(77))   # True
print(nc.is_lucky_seven_multiple(14))   # False
print("Lucky Seven Multiples under 200:", nc.find_in_range(nc.is_lucky_seven_multiple, 1, 200))
