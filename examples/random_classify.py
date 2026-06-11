import numclassify as nc

# Classify 5 random numbers
for _ in range(5):
    result = nc.random_number(max_n=100000)
    print(f"{result['number']}: {result['score']} properties \u2014 {result['true_properties'][:3]}")
