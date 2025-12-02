import dataclasses
import functools
import itertools
from collections import defaultdict
from itertools import permutations, pairwise

import numpy as np
import re
from enum import StrEnum

@dataclasses.dataclass(frozen=True)
class Ingredient:
    name: str
    stats: dict[str, int]

def parse(s):
    """Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8"""
    name, stats_str = s.split(": ")
    stats = {stats_str.split()[0]: int(stats_str.split()[1]) for stats_str in stats_str.split(", ")}
    return Ingredient(name=name, stats=stats)

butterscotch = parse("Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8")
cinnamon = parse("Cinnamon: capacity 2, durability 3, flavor -2, texture -1, calories 3")
assert butterscotch == Ingredient("Butterscotch", {"capacity": -1, "durability": -2, "flavor": 6, "texture": 3, "calories": 8})

def score(ingredients: list[Ingredient], recipe, require_500_calories=False):
    ingredients_dict = {i.name: i.stats for i in ingredients}
    properties = ["calories", "capacity", "durability", "flavor", "texture"]
    def property_score(p):
        s = max(0, sum((recipe[k] * ingredients_dict[k][p]) for k in recipe))
        if p == 'calories':
            return 0 if require_500_calories and s != 500 else 1
        return s
    return functools.reduce(lambda acc, p: acc * property_score(p), properties, 1)

def partitions(total, count):
    if count == 0:
        yield []
    elif count == 1:
        yield [total]
    else:
        for x in range(0, total + 1):
            for p in partitions(total - x, count - 1):
                yield [x] + p
assert list(partitions(0, 0)) == [[]], list(partitions(0, 0))
assert list(partitions(0, 1)) == [[0]], list(partitions(0, 1))
assert list(partitions(1, 1)) == [[1]], list(partitions(1, 1))
assert list(partitions(1, 2)) == [[0, 1], [1, 0]], list(partitions(1, 2))

def ab(ingredients: list[Ingredient], require_500_calories):
    def get_recipe(partition):
        return {ingredients[k].name: partition[k] for k in range(len(ingredients))}
    return max(score(ingredients, get_recipe(p), require_500_calories=require_500_calories) for p in partitions(100, len(ingredients)))

assert(score([butterscotch, cinnamon], {butterscotch.name: 44, cinnamon.name: 56})) == 62842880, score([butterscotch, cinnamon], {butterscotch[0]: 44, cinnamon[0]: 56})
input = open('input/15').read()
ingredients = [parse(line) for line in input.splitlines()]
print(ab(ingredients, require_500_calories=False))
print(ab(ingredients, require_500_calories=True))