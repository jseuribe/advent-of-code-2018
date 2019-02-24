#https://adventofcode.com/2018/day/9

players = 400
last_marble = 71864

def establish_player_chart(players):
    player_score_card = {}
    for i in range (1, players+1):
        player_score_card[i] = 0

    return player_score_card

def determine_winner(player_card):
    print(player_card)
    c_leader = -1

    for player in player_card:
        if c_leader == -1:
            c_leader = player
            continue

        if player_card[player] > player_card[c_leader]:
            c_leader = player
    
    print("Player {0} wins, with a score of: {1}".format(c_leader, player_card[c_leader]))

def insert_at(arr, value, b_pos, a_pos):

    c_pos = 0

    if a_pos == 0:
        arr.append(value)
    else:
        arr = arr[:b_pos+1] + [value] + arr[a_pos:]

    return arr

def play_the_game(player_card):

    c_marble = 1
    playing_field = [0]
    c_pos = 0
    c_player = 1

    dbg_go_until = 23
    while c_marble < last_marble:
        #keep going until the last marble is seen
        print("Current Marble:", c_marble)
        b_point_state = False
        '''
        if dbg_go_until == 0:
            print("DEBUG STOP")
            quit()
        '''
        if (c_marble != 0) and (c_marble % 23 == 0):
            print("Player {0} just scored!".format(c_player))
            #print("C Field Len:", len(playing_field))
            #print("Field:", playing_field)
            #print("Current position:", c_pos)
            #multiple of 23 state
            #add the value to the player card
            player_card[c_player] += c_marble

            #Determine the marble to remove. Account for the looping nature
            if c_pos < 7:
                marb_to_remove = len(playing_field) - (7-c_pos)
            else:
                marb_to_remove  = c_pos-7
                
            #print("removing marble at:", marb_to_remove)
            player_card[c_player] += playing_field[marb_to_remove]
            playing_field.pop(marb_to_remove)
            if marb_to_remove == len(playing_field):
                #print("REMOVING END NODE")
                c_pos = 0
            else:
                c_pos = marb_to_remove
            #print("new start pos/val:", c_pos, playing_field[c_pos])
            b_point_state = True
        else:
            #Determine where the marble will be inserted
            if len(playing_field) != 0:
                b_pos = (c_pos + 1) % len(playing_field)
                a_pos = (c_pos + 2) % len(playing_field)
            else:
                b_pos = 0
                a_pos = 0

            #print("BPOS:", b_pos, "APOS:", a_pos)
            #Insert the marble into its appropriate position
            playing_field = insert_at(playing_field, c_marble, b_pos, a_pos)
            #print(playing_field)

        c_player = (c_player + 1)
        if c_player == players+1:
            c_player = 1

        if not b_point_state:
            c_pos = playing_field.index(c_marble)

        c_marble += 1
        dbg_go_until -= 1


if __name__ == "__main__":

    player_card = establish_player_chart(players)

    play_the_game(player_card)

    determine_winner(player_card)