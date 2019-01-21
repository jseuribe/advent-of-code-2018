'''
https://adventofcode.com/2018/day/2
'''
from collections import defaultdict

boxcodes_fname = "inp\\boxcodes.txt"

def get_codes():
    boxcodes_map = {}

    boxcodes_list = []
    with open(boxcodes_fname, 'r') as boxcode_f:
        boxcodes_list = [ln.rstrip() for ln in boxcode_f.readlines()]

    for boxcode in boxcodes_list:
        boxcodes_map[boxcode] = {}

        boxcodes_map[boxcode]['two_counts'] = 0
        boxcodes_map[boxcode]['three_counts'] = 0
    return boxcodes_map

if __name__ == "__main__":
    print("Getting map!")
    boxcodes_map = get_codes()

    print(boxcodes_map)
    codes_with_two_sat = 0
    codes_with_three_sat = 0

    for code in boxcodes_map:
        char_map = defaultdict(int)

        for char in code:
            if char in char_map:
                char_map[char] += 1
            else:
                char_map[char] = 1

        b_two_sat = False
        b_three_sat = False

        for char in char_map:
            if char_map[char] == 2 and not b_two_sat:
                b_two_sat = True
                codes_with_two_sat += 1
            elif char_map[char] == 3 and not b_three_sat:
                b_three_sat = True
                codes_with_three_sat += 1

    print("CODES WITH TWO SAT:", codes_with_two_sat)
    print("CODES WITH THREE SAT:", codes_with_three_sat)
    print("FINAL CHECKSUM:", codes_with_two_sat * codes_with_three_sat)
