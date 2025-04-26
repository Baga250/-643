def combination_sum(candidates, target):
    candidates.sort()
    result = []
    
    def backtrack(start, target, path):
        if target == 0:
            result.append(path.copy())
            return
        for i in range(start, len(candidates)):
            if i > start and candidates[i] == candidates[i-1]:
                continue
            if candidates[i] > target:
                break
            path.append(candidates[i])
            backtrack(i+1, target - candidates[i], path)
            path.pop()
    
    backtrack(0, target, [])
    return result

print(combination_sum([2,5,2,1,2], 5))
print(combination_sum([10,1,2,7,6,1,5], 8))