"""One-liner knapsack problem solution"""

from collections import namedtuple
import csv
from itertools import accumulate
from itertools import takewhile
from itertools import tee


thing = namedtuple('thing', 'item weight value')
knapsack_capacity = 400

# data preparation
with open('knapsack_items_data', newline='') as data_file:
    items = [thing(x[0], int(x[1]), int(x[2]))
             for x in csv.reader(data_file, delimiter=',')]

# First approach
# Can be shorter in case of prepared ordered things list
things = ([y.item for y in sorted(
    items, key=lambda x: x.value / x.weight, reverse=True)[
        :len([x for x in takewhile(
            lambda x: x < knapsack_capacity,
            accumulate(
                [item.weight for item in sorted(
                    items, key=lambda k: k.value / k.weight,
                    reverse=True)]))])]])

print(things)

# Second approach
things = [r[1].item for r in [
    zip(takewhile(lambda y: y < knapsack_capacity,
                  accumulate(item.weight for item in x[0])), x[1])
    for x in [tee(sorted(items, key=lambda k: k.value / k.weight,
                         reverse=True), 2)]][0]]

print(things)
