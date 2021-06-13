import bggapi
import sys


#TODO: two errors - first time I call it either returns an error and cdata, or it returns double the results
class PlaysByYearForStats:
    def __init__(self, username, year):
        self.username = username
        self.year = year
        self.collection = bggapi.Collection(username)
        self.most_plays_list = []
        self.plays_in_year_count = 0
        self.unique_games_by_year = []
        self.most_played_list = []
        self.plays_in_year_list = []
        self.two_player_collection = []

    #TODO refactor to load all lists
    def load_users_plays(self):
        #For testing
        max_attempt = 3

        while len(self.collection.games) == 0 and max_attempt:
            try:
                self.collection.load()
                self.collection.load_plays()
                # need different except clause -- returning 0 collection due to 202 error -- this should have been handled in bggapi...
            except AttributeError:
                print("202 Error - retrying:")
                max_attempt -= 1;
            except Exception:
                print("No user found. Exiting.")
                sys.exit()

        if not max_attempt:
            print("Max attempts exceeded.  Please try again later.")
            sys.exit()

    def overview(self):
        print(f"games owned: {self.collection.total_owned}")
        print(f"games/expansions on wishlist: {self.collection .total_wish_list}")
        print(f"expansions owned: {self.collection.total_exp}")
        print(f"total plays logged: {len(self.collection.play_list)}")

    def total_plays_in_year(self):

        for play in self.collection.play_list:
            if play['date'][0:4] == self.year:
                self.plays_in_year_count += 1
                self.plays_in_year_list.append(play)

        print(f'total games played in 2021: {self.plays_in_year_count}')

    def most_played_in_year(self):
        for play in self.plays_in_year_list:
            if play['game'] not in self.unique_games_by_year:
                self.unique_games_by_year.append(play['game'])
        print(f'total unique games played in {self.year}: {len(self.unique_games_by_year)}')
        # super inefficient but it works sooooooooooo good enough for now!
        for game in self.unique_games_by_year:
            i = 0
            for play in self.plays_in_year_list:
                if game == play['game']:
                    i += 1
            temp_tup = (game, i)
            self.most_played_list.append(temp_tup)
        self.most_played_list.sort(key=lambda x: x[1], reverse=True)
        print(f'most played game of {self.year}: {self.most_played_list[0]}')

    def most_plays_in_year_as_percentage(self):
        collection_played_percent = float(len(self.unique_games_by_year) / self.collection.total_owned)
        print(f'percentage of collection played in {self.year}: {collection_played_percent * 100:.2f}%')

    def most_2_player_plays_in_year_as_percentage(self):
        #TODO - extract to separate method - load, then display
        u_two_player_collection_by_year = []
        for game_2 in self.collection.games:
            min = game_2['min_players']
            if int(min) <= 2:
                self.two_player_collection.append(game_2)

        for game in self.collection.games:
            for unique_game in self.unique_games_by_year:
                if unique_game == game['name'] and int(game['min_players']) <= 2:
                    u_two_player_collection_by_year.append(unique_game)
        collection_two_player_played = float(len(u_two_player_collection_by_year) / len(self.two_player_collection))
        print(f'Total two player games played in {self.year}: {len(u_two_player_collection_by_year)}')
        print(f'Total two player games played in collection: {len(self.two_player_collection)}')
        print(f'percentage of two-player supported games played in {self.year}: {collection_two_player_played * 100:.2f}%')
        self.total_two_player_games_played_in_year(u_two_player_collection_by_year)

    def total_two_player_games_played_in_year(self, two_player_by_year):
        i = 1
        print(f"\nTwo Player Games Played In {self.year}\n----------------------")
        for game in two_player_by_year:
            print(f'{i}. {game}')
            i += 1

    def list_two_player_games(self):
        i = 1
        for game in self.two_player_collection:
            print(f"{i:>3}. {game['name']:.<40}min players: {game['min_players']}")
            i += 1

    def unique_games_played_in_year(self):
        temp_two = self.two_player_collection.copy()
        for game_not_played in self.two_player_collection:
            for unique_game_not_played in self.unique_games_by_year:
                if unique_game_not_played == game_not_played['name']:
                    temp_two.remove(game_not_played)
        i = 1
        for game_not_played in temp_two:
            print(
                f"{i:>3}. {game_not_played['name']:.<45}play time: {game_not_played['min_play_time']:>4} - {game_not_played['max_play_time']:>3} min")
            i += 1

    def total_plays_all_games(self):
        i = 1
        for game in self.most_played_list:
            print(f"{i:>3}. {game[0]:.<40}Total Plays: {game[1]}")
            i += 1

    def total_wins_per_game(self, chosen_game, full):
        game_to_display = ""
        for game in self.collection.games:
            if game['name'] == chosen_game:
                game_to_display = game

        if game_to_display:
            counter = 1
            matt_wins = 0
            jill_wins = 0
            matt_high = 0
            jill_high = 0
            for play in self.collection.play_list:
                if not chosen_game == play['game']:
                    continue
                else:
                    if full:
                        print(f"----------------------------------\nGame {counter}.\n----------------------------------\n")
                    for player in play['players']:
                        if full:
                            print(f"{player['name']}: {player['score']}")
                        if player['name'] == "Matt":
                            if int(player['win']) == 1:
                                matt_wins += 1
                            try:
                                # Note: No Thanks is Low Score -- must account for these
                                if int(player['score']) > matt_high:
                                    matt_high = int(player['score'])
                            except Exception:
                                pass
                        if player['name'] == "Jill":
                            if int(player['win']) == 1:
                                jill_wins += 1
                            try:
                                if int(player['score']) > jill_high:
                                    jill_high = int(player['score'])
                            except Exception:
                                pass
                    counter += 1
            print(
                f"---------------------------\n{chosen_game} Totals\n---------------------------\nMatt Wins: {matt_wins} Matt High Score: {matt_high}"
                f"\nJill Wins: {jill_wins} Jill High Score {jill_high}\n")
        else:
            print("Game Not Found.")

    #TODO refactor to take list of players instead of hardcoded
    def total_wins_all_games(self):
        matt_wins = 0
        jill_wins = 0
        for el in self.collection.play_list:
            # if el['game'] == "My City":
            #     continue
            try:
                for i in range(len(el['players'])):
                    if el['players'][i]['name'] == "Matt":
                        matt_wins += int(el['players'][i]['win'])
                    if el['players'][i]['name'] == "Jill":
                        jill_wins += int(el['players'][i]['win'])
            except KeyError as e:
                print(e)
            except IndexError as e:
                print(e)
            except AttributeError as e:
                print(e)
        print(f"Matt's Wins: {matt_wins}\nJill's Wins: {jill_wins}")


def main(args):
    #TODO add CLI argparsing instead of hardcoded
    plays = PlaysByYearForStats("flakcanon", "2021")
    plays.load_users_plays()
    plays.overview()
    plays.total_plays_in_year()

    if len(plays.collection.play_list) > 0:

        plays.total_wins_per_game("Star Realms", 0)
        plays.total_wins_all_games()

if __name__ == '__main__':
    main(sys.argv)