'''
https://adventofcode.com/2018/day/1
'''
import requests

day_one_input_url = "https://adventofcode.com/2018/day/1/input"
freq_f = 'freq.txt'

def get_freq():
    freq_list = []

    with open(freq_f, 'r') as freq_file:
        freq_list = [ln.rstrip() for ln in freq_file.readlines()]
        
    return freq_list


if __name__ == "__main__":

    freq_list = get_freq()

    freq_visited_map = {0: 1}
    final_freq = 0
    b_seen_second = False
    b_value_seen_second = 0

    while not b_value_seen_second:

        for freq in freq_list:
            if freq[0] == "+":
                final_freq += int(freq[1:])
            elif freq[0] == "-":
                final_freq -= int(freq[1:])

            if final_freq in freq_visited_map:
                freq_visited_map[final_freq] += 1
            else:
                freq_visited_map[final_freq] = 1
            
            print("CURRENT FREQUENCY:", final_freq)
            if freq_visited_map[final_freq] > 1:
                if not b_seen_second:
                    b_seen_second = True
                    b_value_seen_second = final_freq
                    break
                else:
                    continue

    print(freq_visited_map)
    print("FREQ SEEN SECOND FIRST:", b_value_seen_second)