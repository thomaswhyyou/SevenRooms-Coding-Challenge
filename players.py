import random

class Player(object):
    def __init__(self):
        self.pretty_name  = "Player"
        self.matches_won  = 0
        self.pts_in_match = 0
        self.shots_fired_count = {
            'flat': 0,
            'slice': 0,
            'topspin': 0,
            'unreturnable': 0,
            'total': 0,
        }

        self.shots_returned_count = {
            'flat': 0,
            'slice': 0,
            'topspin': 0,
            'total': 0,
        }

        # Placeholder values to be overwritten by subclass
        self.prob_of_hitting_shot_type = {}
        self.prob_of_return_shot_type = {}

    def try_hitting_back(self, shot_type, is_serve):
        if shot_type == 'unreturnable':
            return False

        prob_hitting_back = self.prob_of_return_shot_type[shot_type]
        if is_serve:
            prob_hitting_back -= 0.1
        random_float = random.uniform(0, 1)
        if random_float < prob_hitting_back:
            self.shots_returned_count[shot_type] += 1
            self.shots_returned_count['total']   += 1
            return True
        else:
            return False

    def determine_shot_type(self):
        cutoff_prob   = 0.0
        types         = self.prob_of_hitting_shot_type.keys()
        probabilities = self.prob_of_hitting_shot_type.values()

        random_float  = random.uniform(0, 1)
        for shot_type, prob_per_type in zip(types, probabilities):
            cutoff_prob += prob_per_type
            if random_float < cutoff_prob:
                break
        self.shots_fired_count[shot_type] += 1
        self.shots_fired_count['total']   += 1
        return shot_type

    def return_shots_history(self):
        total_shots    = float(self.shots_fired_count['total'])
        flat_ratio     = self.shots_fired_count['flat'] / total_shots
        slice_ratio    = self.shots_fired_count['slice'] / total_shots
        topspin_ratio  = self.shots_fired_count['topspin'] /total_shots
        unreturn_ratio = self.shots_fired_count['unreturnable'] / total_shots
        return (total_shots, flat_ratio, slice_ratio, topspin_ratio, unreturn_ratio)

    def check_if_stats_stablized(self):
        '''
        Check if the actual spread of hitting shot type (as a % of total) matches
        the initialized probability within the given threshold for each shot type.
        If so, return True; if not, False.
        '''
        threshold = 0.001
        total_shots, flat_ratio, slice_ratio, topspin_ratio, unreturn_ratio = self.return_shots_history()
        counter = 0
        counter += 1 if abs(self.prob_of_hitting_shot_type['flat'] - flat_ratio) < threshold else 0
        counter += 1 if abs(self.prob_of_hitting_shot_type['slice'] - slice_ratio) < threshold else 0
        counter += 1 if abs(self.prob_of_hitting_shot_type['topspin'] - topspin_ratio) < threshold else 0
        counter += 1 if abs(self.prob_of_hitting_shot_type['unreturnable'] - unreturn_ratio) < threshold else 0
        if counter < 4:
            return False
        else:
            return True

class BruceLeeds(Player):
    def __init__(self):
        super(BruceLeeds, self).__init__()
        self.pretty_name = "Bruce Leeds"
        self.prob_of_hitting_shot_type = {
            'flat': 0.47,
            'slice': 0.25,
            'topspin': 0.25,
            'unreturnable': 0.03,
        }
        self.prob_of_return_shot_type = {
            'flat': 0.80,
            'slice': 0.45,
            'topspin': 0.75,
        }


class SerenaWilliamson(Player):
    def __init__(self):
        super(SerenaWilliamson, self).__init__()
        self.pretty_name = "Serena Williamson"
        self.prob_of_hitting_shot_type = {
            'flat': 0.10,
            'slice': 0.20,
            'topspin': 0.66,
            'unreturnable': 0.04,
        }
        self.prob_of_return_shot_type = {
            'flat': 0.65,
            'slice': 0.50,
            'topspin': 0.85,
        }


class JCVanDime(Player):
    def __init__(self):
        super(JCVanDime, self).__init__()
        self.pretty_name = "JC Van Dime"
        self.prob_of_hitting_shot_type = {
            'flat': 0.70,
            'slice': 0.10,
            'topspin': 0.15,
            'unreturnable': 0.05,
        }
        self.prob_of_return_shot_type = {
            'flat': 0.90,
            'slice': 0.25,
            'topspin': 0.85,
        }
