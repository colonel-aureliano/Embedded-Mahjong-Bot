# assume t1 - t9 are 0 - 8
# assume w1 - w9 are 9 - 17
# assume b1 - b9 are 18 - 26
# flowers is 27 - 30
# honors east - white is 31 - 37
# seasons is 38 - 41

class HandPartitioner:
  def __init__(self):
    pass
  
  def find_patterns(self,numbers):
    results = {
        "seq-complete": [],
        "triplet": [],
        "couplet": [],
        "quadruplet": [],
    }

    # Helper to check if any three numbers are consecutive and in the same window
    def check_consecutive_in_window(nums):
        temp_nums : list = nums.copy()
        temp_nums.sort()
        i = 0
        while (i < len(nums)):
            i2 = temp_nums.index(temp_nums[i] + 1) if (temp_nums[i] + 1) in temp_nums else -1
            i3 = temp_nums.index(temp_nums[i] + 2) if (temp_nums[i] + 2) in temp_nums else -1
            if (i2 != -1 and i3 != -1):
                results["seq-complete"].append(temp_nums[i])
                temp_nums[i2] = -1
                temp_nums[i3] = -1
            else:
                i += 1
        
    # Collect numbers by windows
    window1 = [x for x in numbers if 0 <= x <= 8]
    window2 = [x for x in numbers if 9 <= x <= 17]
    window3 = [x for x in numbers if 18 <= x <= 26]

    # Check each window for consecutive numbers
    check_consecutive_in_window(window1)
    check_consecutive_in_window(window2)
    check_consecutive_in_window(window3)

    # Check for triplets
    from collections import Counter
    count = Counter(numbers)
    for num, cnt in count.items():
        if cnt >= 4:
            results["quadruplet"].append(num)
        elif cnt >= 3:
            results["triplet"].append(num)
        elif cnt >= 2:
            results["couplet"].append(num)

    return results
