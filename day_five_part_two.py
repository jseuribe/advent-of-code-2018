'''
https://adventofcode.com/2018/day/5
'''
import re

inp_fname = "inp/day_five_polymers.txt"
def get_polymer():
    
    with open(inp_fname, 'r') as f:
        return f.read().rstrip()

def getUnitMap(polymer_str):
    unit_map = {}

    for char in polymer_str:
        if char.lower() not in unit_map:
            unit_map[char.lower()] = 0
    
    return unit_map

def purge_polymer_of_unit(polymer_str, unit):
    n_polymer_str = polymer_str
    n_polymer_str = re.sub(unit.lower(), '', n_polymer_str)
    n_polymer_str = re.sub(unit.upper(), '', n_polymer_str)

    return n_polymer_str

def init_reaction_chain(polymer_str):
    b_found_reaction = False
    b_nfound_first = False
    b_eof_string = False
    while b_found_reaction or not b_nfound_first:
        b_found_reaction = False

        #print("current length:", len(polymer_str))
        l_char = polymer_str[0]
        b_eof_string = False

        for index, char in enumerate(polymer_str):
            if index == 0:
                continue
            if (char.lower() == l_char or char.upper() == l_char) and char != l_char:

                n_polymer_str = polymer_str[:index-1] + polymer_str[index+1:]

                polymer_str = n_polymer_str

                if not b_nfound_first:
                    b_nfound_first = True

                b_found_reaction = True
                break
            elif index+1 == len(polymer_str):
                b_eof_string = True
            
            l_char = char
    
        if b_eof_string:
            break

    return polymer_str

if __name__ == "__main__":

    polymer_str = get_polymer()

    unit_map = getUnitMap(polymer_str)

    for unit in unit_map:
        n_polymer_str = purge_polymer_of_unit(polymer_str, unit)

        print("Determining result for polymer purged of unit:", unit)
        final_polymer_list = init_reaction_chain(n_polymer_str)
        print("RESULT OF {0} REMOVED POLYMERCHAIN: {1}".format(unit, len(final_polymer_list)))
        unit_map[unit] = len(final_polymer_list)

    print("Polymer unit list:", unit_map)

    #det the smallest chain possible
    c_min_val = 0
    c_lead_unit = ''

    for unit in unit_map:
        if c_min_val == 0:
            c_min_val = unit_map[unit]
            c_lead_unit = unit
            continue
        else:
            if unit_map[unit] < c_min_val:
                c_min_val = unit_map[unit]
                c_lead_unit = unit
    
    print("SMALLEST VAL:", c_min_val, "WHEN REMOVING THIS UNIT:", c_lead_unit)