import numclassify as nc

# Memory-safe streaming over large range
# Print any number with score > 30
for result in nc.stream(1, 10000):
    if result["score"] > 30:
        print(f"{result['number']}: score={result['score']}, types={result['true_properties'][:5]}")
