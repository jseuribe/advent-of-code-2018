'''
https://adventofcode.com/2018/day/5
'''
inp_fname = "inp/day_five_polymers.txt"
def get_polymer():
    
    with open(inp_fname, 'r') as f:
        return f.read().rstrip()

if __name__ == "__main__":

    polymer_str = get_polymer()

    b_found_reaction = False
    b_nfound_first = False
    b_eof_string = False
    while b_found_reaction or not b_nfound_first:
        b_found_reaction = False

        print("current length:", len(polymer_str))
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

    print("FINAL LENGTH:", len(polymer_str))
