from sys import argv
from collections import OrderedDict
from helpers import pick_player, describe_stage, do_coin_toss, print_stats
from players import BruceLeeds, SerenaWilliamson, JCVanDime

def initiate_game(num_of_matches_to_play):
    matches_played = 0
    player_roaster = OrderedDict([
        (1, BruceLeeds),
        (2, SerenaWilliamson),
        (3, JCVanDime),
    ])
    unavil_choices = []

    describe_stage("Let's play a simple game of ping pong..")
    player_one_choice = pick_player(player_roaster, unavil_choices, "FIRST")
    unavil_choices.append(player_one_choice)
    player_two_choice = pick_player(player_roaster, unavil_choices, "SECOND")
    player_one        = player_roaster[player_one_choice]()
    player_two        = player_roaster[player_two_choice]()
    match_pair        = [player_one, player_two]

    describe_stage("Preparing a match between: '{}' vs '{}'"\
                   .format(player_one.pretty_name, player_two.pretty_name))

    while True:
        if num_of_matches_to_play and (num_of_matches_to_play == matches_played):
            break
        serve_index    = do_coin_toss() # Return 0 or 1
        first_to_serve = match_pair[serve_index]
        print ""
        print "Player '{}' will be serving first.".format(first_to_serve.pretty_name)

        describe_stage("Match begins..")
        start_match(match_pair, serve_index)
        matches_played += 1

        player_one_result = match_pair[0].check_if_stats_stablized()
        player_two_result = match_pair[1].check_if_stats_stablized()
        if player_one_result and player_two_result:
            break

        print "Current stats..."
        print_stats(match_pair[0], match_pair[0].return_shots_history())
        print_stats(match_pair[1], match_pair[1].return_shots_history())
        print "Preparing a rematch..."

    describe_stage("Showing match stats.. ")
    print "Total number of matches played: {}".format(matches_played)
    print "{} wins {} ({:.0f}%)".format(match_pair[0].pretty_name, match_pair[0].matches_won,
                                        match_pair[0].matches_won / float(matches_played) * 100)
    print "{} wins {} ({:.0f}%)".format(match_pair[1].pretty_name, match_pair[1].matches_won,
                                        match_pair[1].matches_won / float(matches_played) * 100)
    print_stats(match_pair[0], match_pair[0].return_shots_history())
    print_stats(match_pair[1], match_pair[1].return_shots_history())


def start_match(match_pair, serve_index):
    serve_count   = 0
    match_pair[0].pts_in_match = 0
    match_pair[1].pts_in_match = 0
    serve_and_start(match_pair, serve_index, serve_count)

def serve_and_start(match_pair, serve_index, serve_count):
    while True:
        print "---------- {} | {} vs {} | {} ----------".format(match_pair[0].pretty_name,
                                                                match_pair[0].pts_in_match,
                                                                match_pair[1].pts_in_match,
                                                                match_pair[1].pretty_name)

        if match_pair[0].pts_in_match == 21:
            match_pair[0].matches_won += 1
            print "MATCH OVER: {} wins.".format(match_pair[0].pretty_name)
            break
        if match_pair[1].pts_in_match == 21:
            match_pair[1].matches_won += 1
            print "MATCH OVER: {} wins.".format(match_pair[1].pretty_name)
            break

        if serve_count == 5:
            serve_count = 0
            serve_index = abs(serve_index - 1) #flip btwn 0 and 1
        serve_count += 1
        shooter = match_pair[serve_index]
        receiver = match_pair[abs(serve_index - 1)]

        print "({} to serve to {}.)".format(shooter.pretty_name, receiver.pretty_name)
        fire_shot(shooter, receiver, is_serve=True)

def fire_shot(shooter, receiver, is_serve=False):
    shot_type = shooter.determine_shot_type()
    print "{} successfully hit a {} to {}.".format(shooter.pretty_name,
                                                   shot_type, receiver.pretty_name)
    was_able_to_hit = receiver.try_hitting_back(shot_type, is_serve)
    if was_able_to_hit:
        fire_shot(receiver, shooter) # Receiver becomes a shooter now and vice versa
    else:
        shooter.pts_in_match += 1
        print ".... {} unable to return {}'s {}.".format(receiver.pretty_name,
                                                         shooter.pretty_name, shot_type)
        print "{} scores a point!".format(shooter.pretty_name)
        print ""
    return


if __name__ == "__main__":
    try:
        script, num_of_matches_to_play = argv
        num_of_matches_to_play = int(num_of_matches_to_play)
    except ValueError:
        num_of_matches_to_play = 0
    initiate_game(num_of_matches_to_play)

