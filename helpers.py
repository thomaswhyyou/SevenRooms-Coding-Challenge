import random
from time import sleep

def pick_player(player_roaster, unavil_choices, draft_round_str):
    while True:
        prompt_text = "Pick your {} player (Enter player's number):\n".format(draft_round_str)
        for key, val in player_roaster.iteritems():
            if key in unavil_choices:
                continue
            prompt_text += "{}: {}\n".format(key, val.__name__)
        prompt_text += ">> "
        user_input = raw_input(prompt_text)
        try:
            player_choice = int(user_input)
        except ValueError:
            print "\n"
            print "ERROR: Please enter a number, please try again.\n"
            sleep(0.25)
            continue

        if (player_choice in unavil_choices) or (player_choice not in player_roaster.keys()):
            print "\n"
            print "ERROR: Invalid choice, please try again.\n"
            sleep(0.25)
        else:
            print "\n"
            print "'{}' picked.\n".format(player_roaster[player_choice].__name__)
            sleep(0.25)
            break
    return player_choice

def describe_stage(description):
    print "\n"
    print "--" * 30
    print description
    print "--" * 30

def do_coin_toss():
    print "Coin toss to determine the first player to serve.."
    return random.randint(0, 1)

def print_stats(player, stats_tuple):
    total_shots, flat_ratio, slice_ratio, topspin_ratio, unreturn_ratio = stats_tuple

    print ""
    print "{} (Total shots taken: {:.0f})".format(player.pretty_name.upper(), total_shots)
    print "of total"
    print "... flat: {:.0f}%".format(flat_ratio * 100)
    print "... slice: {:.0f}%".format(slice_ratio * 100)
    print "... topspin: {:.0f}%".format(topspin_ratio * 100)
    print "... unreturnable: {:.0f}%".format(unreturn_ratio * 100)

