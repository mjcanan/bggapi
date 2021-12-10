import bggapi
import sys
import matplotlib.pyplot as plt


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
                max_attempt -= 1
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
        filtered_collection = self.filter_by_year()
        for play in filtered_collection:
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
        self.most_played_list.sort(key=lambda x: (x[1], x[0]))
        print(f'most played game of {self.year}: {self.most_played_list[len(self.most_played_list) - 1]}')

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
        print(f"\nTwo Player Games Played In {self.year}\n|-*~.~*--*~.-~*--*~.~*--*~.~*--*~.~*--*~.~*--*~.~*-|")
        for game in two_player_by_year:
            print(f'{i}. {game}')
            i += 1

    def list_two_player_games(self):
        i = 1
        print("--------------------\nOur Two Player Games\n-----------------------")
        for game in self.two_player_collection:
            print(f"{i:>3}. {game['name']:.<40}min players: {game['min_players']}")
            i += 1

    def not_played_by_year(self):
    	i = 1
    	print(f"Games Not Played In {self.year}\n----------------------------------")
    	for game in self.collection.games:
    		played = False
    		for play in self.plays_in_year_list:
    			if game['name'] == play['game']:
    				played = True
    		if not played:
    			print(f"{i:>3}. {game['name']}")
    			i += 1

    def unique_2_player_games_not_played_in_year(self):
        temp_two = self.two_player_collection.copy()
        for game_not_played in self.two_player_collection:
            for unique_game_not_played in self.unique_games_by_year:
                if unique_game_not_played == game_not_played['name']:
                    temp_two.remove(game_not_played)
        i = 1
        print(f"|-*~.~*--*~.-~*--*~.~*--*~.~*--*~.~*--*~.~*--*~.~*-|\nGames Not Yet Played in {self.year}\n|-*~.~*--*~.-~*--*~.~*--*~.~*--*~.~*--*~.~*--*~.~*-|")
        for game_not_played in temp_two:
            print(
                f"{i:>3}. {game_not_played['name']:.<45}play time: {game_not_played['min_play_time']:>4} - {game_not_played['max_play_time']:>3} min")
            i += 1
        if len(temp_two) == 0:
            print("All 2 player games have been played!")
            
    def plays_by_weight(self):
        #TODO <1.9 is light, 2-3 is medium, 3+ is heavy (0-1 light, 1-2 medium-light, 2-3 medium, 3-4 medium-heavy, 4-5 heavy
        pass

    def wins_by_weight(self):
        #TODO call plays_by_weight, then do math.
        pass

    def first_plays(self):
        filtered_collection = self.filter_by_year()
        played = []
        first_play = []
        matt_wins = 0
        jill_wins = 0
        for play in filtered_collection:
            if play['game'] not in played:
                for player in play['players']:
                    if player['name'] == 'Matt':
                        if player['win'] == '1':
                            matt_wins += 1
                            first_play.append((play['game'], "Matt"))
                    if player['name'] == 'Jill':
                        if player['win'] == '1':
                            jill_wins += 1
                            first_play.append((play['game'], "Jill"))
                played.append(play['game'])
        print(f"Matt Wins: {matt_wins}\nJill Wins: {jill_wins}")
        ans = input('Print full list of first plays?')
        if 'y' in ans.lower():
            for game in first_play:
                print(game)


    def not_played_by_year(self):
        i = 1
        print("|-*~.~*--*~.-~*--*~.~*--*~.~*--*~.~*--*~.~*--*~.~*-|\nNot played this year\n|-*~.~*--*~.-~*--*~.~*--*~.~*--*~.~*--*~.~*--*~.~*-|")
        for game in self.collection.games:
            played = False
            for play in self.plays_in_year_list:
                if game['name'] == play['name']:
                    played = True
            if not played:
                print(f"{i}. {game['name']}")
                i += 1

    def total_plays_all_games(self):
        i = 1
        print("|-*~.~*--*~.-~*--*~.~*--*~.~*--*~.~*--*~.~*--*~.~*-|\nTotal Plays By Most Played\n|-*~.~*--*~.-~*--*~.~*--*~.~*--*~.~*--*~.~*--*~.~*-|")
        for game in self.most_played_list:
            print(f"{i:>3}. {game[0]:.<40}Total Plays: {game[1]}")
            i += 1

    #TODO take list of players instead of hardcoded
    def total_wins_per_game(self, chosen_game, full):
        game_to_display = ""
        for game in self.collection.games:
            if game['name'] == chosen_game:
                game_to_display = game

        filtered_collection = self.filter_by_year()

        if game_to_display:
            counter = 1
            matt_wins = 0
            jill_wins = 0
            matt_high = 0
            jill_high = 0
            for play in filtered_collection:
                if not chosen_game == play['game']:
                    continue
                else:
                    if full:
                        print(f"|-*~.~*--*~.-~*--*~.~*--*~.~*--*~.~*--*~.~*--*~.~*-|\n"
                              f"{' '*22}Game {counter}.\n"
                              f"|-*~.~*--*~.-~*--*~.~*--*~.~*--*~.~*--*~.~*--*~.~*-|")
                        print(f"Date Played: {play['date']}")
                    for player in play['players']:
                        if full:
                            print(f"{player['name']}: Score {player['score']} -- Win?: {player['win']}")
                        if player['name'] == "Matt":
                            if player['win'] == '1':
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
                f"|-*~.~*--*~.-~*--*~.~*--*~.~*--*~.~*--*~.~*--*~.~*-|\n{' '*15}{chosen_game} Totals"
                f"\n|-*~.~*--*~.-~*--*~.~*--*~.~*--*~.~*--*~.~*--*~.~*-|"
                f"\nMatt Wins: {matt_wins} Matt High Score: {matt_high}"
                f"\nJill Wins: {jill_wins} Jill High Score {jill_high}\n")
                show_plot = input("Show plot? Y/N: ")
            if 'y' in show_plot.lower():
                f, (b1,b2) = plt.subplots(1,2)
                wins_J = b1.bar(2 - 0.35/2, jill_wins, 0.35, label="Jill")
                wins_M = b1.bar(2 + 0.35/2, matt_wins, 0.35, label="Matt")
                b1.set_ylabel('Wins')
                b1.set_title(f"Wins")
                b1.bar_label(wins_J, padding=3)
                b1.bar_label(wins_M, padding=3)
                b1.set_xticks([],[])
                if jill_wins >= matt_wins:
                    y_ticks = list(range(0,jill_wins+1))
                else:
                    y_ticks = list(range(0,matt_wins+1))
                b1.set_yticks(y_ticks)
                b1.legend()
                b2.set_ylabel(f'High Score')
                b2.set_title(chosen_game)
                high_J = b2.bar(2-0.35/2, jill_high, 0.35, label="Jill")
                high_M = b2.bar(2+0.35/2, matt_high, 0.35, label="Matt")
                b2.bar_label(high_J, padding=3)
                b2.bar_label(high_M,padding=3)
                b2.set_xticks([],[])
                f.tight_layout()

                plt.show()
        else:
            print("Game Not Found.")

    def filter_by_year(self):
        return list(filter(lambda x: (x['date'][:4] == self.year), self.collection.play_list))

    def plot_all_game_plays(self):
        game_arr = []
        plays_arr = []
        for play in self.most_played_list:
            game_arr.append(play[0])
            plays_arr.append(play[1])
        fig, (g1, g2) = plt.subplots(1,2)
        g1.barh(game_arr[:int(len(game_arr)/2)], plays_arr[:int(len(plays_arr)/2)])
        g2.barh(game_arr[int(len(game_arr)/2):], plays_arr[int(len(plays_arr)/2):])
        g1.set_xticks([0,10,20,30,40])
        g2.set_xticks([0,10,20,30,40])
        plt.show()


    #TODO refactor to take list of players instead of hardcoded
    def total_wins_all_games(self):
        matt_wins = 0
        jill_wins = 0
        filtered_collection = self.filter_by_year()
        for el in filtered_collection:
            # if el['game'] == "My City":
            #     continue
            try:
                for i in range(len(el['players'])):
                    #TODO remove hardcoded names, take parameters instead
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

    def most_wins_per_game(self):
        most_wins_list = []
        plays_dict = {}
        #todo needs improvement - use .get()
        for play in self.plays_in_year_list:
            if play['game'] not in plays_dict.keys():
                plays_dict[play['game']] = {}

            for player in play['players']:
                if int(player['win']):
                    if player['name'] not in plays_dict[play['game']]:
                        plays_dict[play['game']][player['name']] = 1
                    else:
                        plays_dict[play['game']][player['name']] += 1
                #codenames duet phase concept zombie in my pocket are empty.

        for game in plays_dict.keys():
            if not plays_dict[game]:
                continue
            x = list(sorted(plays_dict[game].items(), key=lambda item: item[1]))
            try:
                y = [item for item in x if item[1] == x[0][1]]
                most_wins_list.append((game, y))
            except IndexError as e:
                print(f"ERROR FOR GAME {game}: {e}")
                print(f"{plays_dict[game]}")
        matt_wins = 0
        jill_wins = 0
        ties = 0
        for wins in most_wins_list:
            if "Matt" in [el[0] for el in wins[1]] and "Jill" in [el[0] for el in wins[1]]:
                ties += 1
            elif "Matt" in [el[0] for el in wins[1]]:
                matt_wins += 1
            elif "Jill" in [el[0] for el in wins[1]]:
                jill_wins += 1
            print(f"{wins[0]:.<40}{[el[0] for el in wins[1]]}")
        print(f"Matt wins: {matt_wins}")
        print(f"Jill wins: {jill_wins}")
        print(f"Ties: {ties}")

def main(args):
    #TODO add CLI argparsing instead of hardcoded
    plays = PlaysByYearForStats("flakcanon", "2021")
    plays.load_users_plays()
    plays.total_plays_all_games()
    plays.total_plays_in_year()
    plays.overview()
    plays.most_played_in_year()
    plays.most_plays_in_year_as_percentage()
    plays.most_2_player_plays_in_year_as_percentage()
    plays.unique_games_played_in_year() #TODO rename method - this is games not played
    plays.total_plays_all_games() #TODO rename method - this is games by play

    #TODO add user input
    #TODO smarter searches
    #TODO add help section
    print("Get stats by game, -q to quit, -ap for all plays plot, -t for totals, -fp for first plays, -mw most wins")
    while True:
        game = input("Select Game: ")
        if game == '-q':
            sys.exit(0)
        elif game == '-ap':
            plays.plot_all_game_plays()
        elif game == '-t':
            plays.total_wins_all_games()
        elif game == '-fp':
            plays.first_plays()
        elif game == '-mw':
            plays.most_wins_per_game()
        else:
            plays.total_wins_per_game(game, 1)


if __name__ == '__main__':
    #TODO separate this out.  BGGapi should be dao, this can be a utilities class (get particular lists, stats, etc.), and then I can have a view class
    main(sys.argv)