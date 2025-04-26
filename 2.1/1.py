def count_jewels(j, s):
    jewels = set(j)
    return sum(1 for char in s if char in jewels)

print(count_jewels("ab", "aabbccd")) 