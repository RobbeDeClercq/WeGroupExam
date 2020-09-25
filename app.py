numbers = [1, 1, 2, 3, 3, 1, 3, 1, 1, 1, 2]
grouped_numbers = []
same_numbs = []

for numb in numbers:
    if len(same_numbs) != 0 and numb not in same_numbs:
        grouped_numbers.append(same_numbs)
        same_numbs = []

    same_numbs.append(numb)

grouped_numbers.append(same_numbs)
print(grouped_numbers)