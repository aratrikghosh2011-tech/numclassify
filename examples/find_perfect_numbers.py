import numclassify as nc

# Find all perfect numbers under 10000
perfect = nc.find_by_property(start=1, end=10000, Perfect=True)
print("Perfect numbers:", perfect)

# Find numbers that are both perfect and odious
perfect_odious = nc.find_by_property(start=1, end=10000, Perfect=True, Odious=True)
print("Perfect and Odious:", perfect_odious)
