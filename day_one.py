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

    final_freq = 0
    for freq in freq_list:
        if freq[0] == '+':
            final_freq += int(freq[1:])
        elif freq[0] == '-':
            final_freq -= int(freq[1:])

    print("FINAL FREQUENCY:", final_freq)

