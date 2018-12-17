'''
https://adventofcode.com/2018/day/2
'''
boxcodes_fname = "boxcodes.txt"

def get_codes():
    boxcodes_map = {}

    boxcodes_list = []
    with open(boxcodes_fname, 'r') as boxcode_f:
        boxcodes_list = [ln.rstrip() for ln in boxcode_f.readlines()]

    for boxcode in boxcodes_list:
        boxcodes_map[boxcode] = {}
        
    return boxcodes_map, boxcodes_list

if __name__ == "__main__":

    print("////////CALCULATING")
    boxcodes_map, boxcodes_list = get_codes()

    for c_code in boxcodes_map:

        for this_code in boxcodes_list:

            if c_code == this_code:
                continue
            if c_code in boxcodes_map[this_code]:
                continue

            c_index = 0
            boxcodes_map[c_code][this_code] = []
            for char_one, char_two in zip(c_code, this_code):

                if char_one != char_two:
                    boxcodes_map[c_code][this_code].append((char_two, c_index))

                c_index += 1

    
    #print(boxcodes_map)

    rec_first_code = ''
    rec_second_code = ''
    rec_tuple_diff = None

    for c_code in boxcodes_map:
        print("RESULTS FOR", c_code)
        for comp_code in boxcodes_map[c_code]:
            diffs = boxcodes_map[c_code][comp_code]
            #print("COMP-CODE:", comp_code, "DIFFS", diffs)
            if len(diffs) == 1:
                print("POSSIBLE MATCH FOUND", c_code, comp_code, diffs)
                rec_first_code = c_code
                rec_second_code = comp_code
                rec_tuple_diff = diffs

    skip_index = rec_tuple_diff[0][1]

    result_str = ''
    for c_index, char in enumerate(rec_first_code):
        if c_index == skip_index:
            continue
        else:
            result_str += char

    print("FINAL RESULT:", result_str)