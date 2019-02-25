from collections import deque

players = 400
last_marble = 71864*100

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

def play_the_game(player_card):

    c_marble = 1
    playing_field = deque([0])
    c_pos = 0
    c_player = 1

    dbg_stop = 2
    while c_marble < last_marble:
        print("cmarble", c_marble)
        if c_marble % 23 == 0 and c_marble != 0:
            print("Player {0} just scored!".format(c_player))
            player_card[c_player] += c_marble

            #Move the deque 7 steps backwards
            playing_field.rotate(7)
            print("Player {0} got: {1} points".format(c_player, playing_field[0]))
            player_card[c_player] += playing_field.popleft()

        else:
            '''
            The insertion point is always 2 nodes after the current position
            deques so generously account for this when treating it as a circular buffer!
            '''
            playing_field.insert(2, c_marble)
            #when inserted, the new start point will be moved to the new element
            playing_field.rotate(-2)

        c_player += 1
        if c_player > players:
            c_player = 1
        c_marble += 1

        #print(playing_field)

        dbg_stop -= 1

if __name__ == "__main__":

    player_card = establish_player_chart(players)

    play_the_game(player_card)

    determine_winner(player_card)