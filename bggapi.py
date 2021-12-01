import untangle
import json
import requests
import time
import sys
import math
#import argparse
'''
THE INTENT WITH THIS BRANCH IS TO TURN THIS CODE INTO A SCRIPT THAT WILL GET ME THE CURRENT PRICES
FOR ALL MY GAMES, AND PROVIDE A LINK - TKINTER FOR GUI
'''


class Collection:
    def __init__(self, name):
        self.name = name
        self.games = []
        self.expansions = []
        self.wish_list = []
        self.play_list = []
        # TODO: have a total_owned and a total_games to account for 1. all objects owned and 2. all base games owned
        self.total_owned = 0
        self.total_wish_list = 0
        self.total_exp = 0

    def __build_dict(self, p, fp):
        rank = fp.stats.rating.ranks.rank
        rank_list = []

        # Handling untangle returning single-element list containing string in dictionary format for ranks
        for i in range(len(rank)):
            temp = str(rank[i])
            arr = temp.split(sep="'")
            n_index = arr.index("friendlyname")
            r_index = arr.index("value")
            rank_list.append(arr[n_index+2])
            rank_list.append(arr[r_index+2])

        # Handling unpublished games
        try:
            pub_year = p.yearpublished.cdata
        except AttributeError:
            pub_year = -1

        if fp.stats.rating['value'] == 'N/A':
            rating = -1
        else:
            rating = fp.stats.rating['value']

        # turning bgg untangled xml data in a dictionary for use by user
        _d = {
            'name': p.name.cdata,
            'bgg_id': p['objectid'],
            'year_published': pub_year,
            'min_players': fp.stats['minplayers'],
            'max_players': self.__check_none(fp.stats['maxplayers']),
            'min_play_time': fp.stats['minplaytime'],
            'max_play_time': self.__check_none(fp.stats['maxplaytime']),
            'total_owned': fp.stats['numowned'],
            'rating': rating,
            'total_ratings': fp.stats.rating.usersrated['value'],
            'average_rating': fp.stats.rating.average['value'],
            'bayes_average': fp.stats.rating.bayesaverage['value'],
            'std_dev': fp.stats.rating.stddev['value'],
            'rank': rank_list,
            'own': p.status['own'],
            'wish_list': p.status['wishlist'],
            'num_plays': p.numplays.cdata,
            'msrp': 0,
            'price': 0,
            'amzlink': ""
        }

        return _d

    def __check_none(self, value):
        # a function for handling None values for games with no maximum players and/or no maximum play time
        if value is None:
            return -1
        else:
            return value

    def __loading_display(self, i, total):
        status = str("Loading " + str(i) + " of " + str(total))
        if i == total:
            print("\b" * len(status), end="")
            print(status)
        elif i > 0:
            print("\b" * len(status), end="")
            print(status, end="")
        else:
            print(status, end="")

    def __pre_build(self, _obj, _full_obj, _exp):
        try:
            for i in range(len(_obj.items)):

                _path = _obj.items.item[i]
                _full_path = _full_obj.items.item[i]

                _game_dict = self.__build_dict(_path, _full_path)

                if int(_game_dict['own']):
                    if _exp:
                        self.expansions.append(_game_dict)
                        self.total_exp += 1
                    else:
                        self.games.append(_game_dict)
                        self.total_owned += 1
                elif int(_game_dict['wish_list']):
                    self.wish_list.append(_game_dict)
                    self.total_wish_list += 1
                else:
                    pass
        except AttributeError:
            print("Something went wrong...")
            print(_obj)
            print(type(_obj))
            sys.exit()

    def load(self):

        no_expansion = "&excludessubtype=boardgameexpansion"
        expansion = "&subtype=boardgameexpansion"
        full_stats = "&stats=1"
        check_202 = 0

        # Three calls are necessary due to quirks in boardgamegeek.com's API - see bgg xml document tree.txt
        # Some expansions still make it in to the games list due to mislabeling by BGG
        while True:
            if check_202 > 3:
                if __name__ == '__main__':
                    print("Too many retries.  Exiting.")
                    sys.exit(4)

            api_url = str("https://api.geekdo.com/xmlapi2/collection?username=" + self.name)
            obj_full = untangle.parse(api_url + full_stats)
            # TODO: excludesubstype does not work?  getting expansions in my game list...
            obj_games = untangle.parse(api_url + no_expansion)
            obj_expansion = untangle.parse(api_url + expansion)
            # all_plays = untangle.parse("https://api.geekdo.com/xmlapi2/plays?username=" + self.name)

            # test for invalid username
            try:
                if obj_full.errors.error:
                    if __name__ == '__main__':
                        self.name = input(obj_full.errors.error.message.cdata + ".  Enter User Name: ")
                    else:
                        return 1

                    if self.name == 'q':
                        sys.exit()
                    elif self.name == '-h':
                        Collection.usage(True)

                    continue
            except AttributeError:
                # if no "error" attribute then there were no errors
                pass

            # Test for 202 response
            try:
                if obj_games.items['totalitems'] == '0':
                    if __name__ == '__main__':
                        print("User has no collection data")
                        self.name = input(".  Enter User Name: ")
                        continue
                    else:
                        return 3

                self.__pre_build(obj_games, obj_full, 0)
                self.__pre_build(obj_expansion, obj_full, 1)
            except AttributeError:
                # 202 Response produces AttributeError -- 202 is common on your first call to a given username in a day
                if __name__ == '__main__':
                    print("Response 202.  Retrying in 3 seconds...")
                    time.sleep(3)
                    check_202 += 1
                    continue
                else:
                    return 2
            break
        # TODO: Hack to get expansions out of game list -- need to fix later!
        to_remove = []
        for game in self.games:
            for expansion in self.expansions:
                if game['name'] == expansion['name']:
                    to_remove.append(game)
                    break
        for game in to_remove:
            self.games.remove(game)
            self.total_owned -= 1

        if not __name__ == '__main__':
            return 0

    def out_formatted(self, f_list, f, s, g):
        # Outputs your games/wishlist/expansions in an easier to read format
        # if "g", then this function will output a single game
        # if "f", prints out the full list of details for your lists, otherwise prints abridged information
        # if "s", will call sort_by method and sort your list
        count = 0
        no_game_found = True
        if s:
            f_list = self.sort_by(f_list)
            if f_list[1] == 4:
                print(f_list[0])
                return
        if g:
            temp_list = []
            for el in f_list:
                # returns multiple results -- better chance of getting something returned this way
                if g.lower() in el['name'].lower():
                    temp_list.append(el)
                    f = True
                    no_game_found = False
            if no_game_found:
                print("No game found.  Please check your spelling and try again")
                return
            else:
                f_list = temp_list

        if f:
            # prints all data in the dictionary
            for el in f_list:
                print("-" * 40)
                for keys in el:
                    if type(el[keys]) == list:
                        for j in range(0, len(el[keys]), 2):
                            print(f'{el[keys][j]}: {el[keys][j+1]}')
                    else:
                        print(f'{keys}: {el[keys]}')
                count += 1
            print("-" * 40)
            print(f'Total:  {count}')
        else:
            # printing only abridge info unless "f" - name, msrp, price and amazon link
            for i in range(len(f_list)):
                print("-" * 40)
                print(f"name: {f_list[i]['name']}\nmsrp: {f_list[i]['msrp']}\nprice: {f_list[i]['price']}\n" +
                      f"link: {f_list[i]['amzlink']}")
                count += 1
            print("-" * 40)
            print(f'Total:  {count}')

    @staticmethod
    def usage(t):
        # "t" for usage on the command, not "t" for usage while in __main__
        if t:
            print("Usage: bggapi.py [user name] [-h]")
        else:
            print('''Usage:
             g: output your owned games's name, msrp, price and amazon link
             w: output your wish list
             e: output your expansions
             n: output all games with number of plays
             Flags:
                -f: output full information (ex: g -f)
                -s: sort list by a key before output (ex: w -s)
                    -f and -s can be combined.
                -g: outputs information for an individual user-chosen game
             q: quit
            -h: help''')

# TODO: more elaborate search - should not allow searches for all values - error when searching by amzlink
    def sort_by(self, col_list, sort_type=""):
        i = 0
        while sort_type not in col_list[0]:
            sort_type = input(f"Enter a key. Press k for keys: ")
            if sort_type == 'k':
                for key in col_list[0].keys():
                    print(f"{key} | ", end="")
                    i += 1
                    if not i % 5:
                        print("")
        try:
            col_list = sorted(col_list, key=lambda game: float(game[sort_type]))
        except:
            col_list = sorted(col_list, key=lambda game: game[sort_type])
        #     col_list.sort(key=lambda game: game[sort_type])
        # except ValueError as err:
        #     return [err, 4]

        return col_list

    def plays(self, g):
        t = time.time()
        any_games = False
        if not g:
            # TODO use self.plays instead of self.games 'num_plays'
            play_list = self.sort_by(self.games, 'num_plays')
            print("-" * 40 + f"\nNumber of Plays as of {time.strftime('%m-%d-%Y %H:%M %Z', time.localtime(t))}\n"
                  + "-" * 40)
            for i in range(len(play_list)):
                print(f"{play_list[i]['num_plays']} - {play_list[i]['name']}")
        else:
            for game in self.games:
                if g.lower() in game['name'].lower():
                    print(f"{game['name']} - Total Plays: {game['num_plays']}")
                    any_games = True
            if not any_games:
                print("No games found.  Please check your spelling and try again")

            return

    def load_price(self, sub_list=None):
        i = 1

        # Loading prices separated into a different function due to API call issues:
        # Multiple calls to BGG API to get Amazon data are needed -- multiple inline queries not supported
        # Although BGG returns its data in XML, the Amazon data is in JSON
        if sub_list is None:
            sub_list = self.games

        for el in sub_list:
            el_id = el['bgg_id']
            url = ('https://www.boardgamegeek.com/api/amazon/textads?objectid=' + el_id + '&objecttype=thing')
            response = requests.get(url)
            # Handling decoding error (occurred only once in testing)
            try:
                amazon = json.loads(response.text)
                # TODO: error handle for 202 responses at this time?
            except json.decoder.JSONDecodeError:
                el['msrp'] = -1
                el['price'] = -1
                el['amzlink'] = "n/a"
                continue

            # Visual Output for Command Line
            if __name__ == "__main__":
                self.__loading_display(i, len(sub_list))
                i += 1

            try:
                keys = list(amazon.keys())
                # return the first key in list, as this is the primary source used by BGG for pricing
                region = keys[0]
            except AttributeError:
                pass

            if not amazon:
                pass
            else:
                try:
                    amazon_price = amazon[region]['defaultprice']
                    amazon_msrp = amazon[region]['listprice']
                    amazon_link = amazon[region]['url']

                    # Handling different data types and non-uniform return values
                    if amazon_msrp is None:
                        amazon_msrp = 0
                    if amazon_price == "(unavailable)":
                        el['msrp'] = 0
                        el['price'] = 0
                        el['amzlink'] = amazon_link
                        continue
                    else:
                        # Removing money symbols to avoid errors during sort
                        # (using replace method to avoid importing re)
                        amazon_msrp = str(amazon_msrp).replace("$", "").replace("£", "")\
                            .replace(",", ".").replace("€", "").replace("CDN", "")
                        amazon_price = str(amazon_price).replace("$", "").replace("£", "")\
                            .replace(",", ".").replace("€", "").replace("CDN", "")
                        el['msrp'] = float(amazon_msrp)
                        try:
                            el['price'] = float(amazon_price)
                        except ValueError as e:
                            el['price'] = -1
                        el['amzlink'] = amazon_link
                        continue
                except KeyError:
                    pass
            el['msrp'] = -1
            el['price'] = -1
            el['amzlink'] = "n/a"

    def load_plays(self):
        # only returns 100 results per page
        page = 1
        plays_url = str("http://api.geekdo.com/xmlapi2/plays?username=" + self.name + "&page=" + str(page))
        plays_list = untangle.parse(plays_url)

        # would like to avoid importing math if possible - this determines number of pages
        page_num = math.ceil(int(plays_list.plays['total'])/100)

        while page_num > 0:
            if plays_list.plays['total'] == '0':
                return

            for i in range(len(plays_list.plays)):
                play_path = plays_list.plays.play[i]

                # Handling when no comments are entered
                try:
                    comment = play_path.comments.cdata
                except AttributeError:
                    comment = 'no comment'

                # Handling when no players are added
                try:
                    players_temp = play_path.players
                    players = []
                    #TODO THIS DOESN'T WORK - NEED NEW OBJECTS EACH TIME.
                    #this doesn't work, because I need a new object each time, this is just dealing with the same object.
                    for p in players_temp:
                        for n in range(len(p.player)):
                            players.append(self._generate_scoresheet(p.player[n]))

                except AttributeError:
                    players = []
                #TODO -> players needs to be parsed more!
                _play = {
                    'id': play_path['id'],
                    'date': play_path['date'],
                    'quantity': play_path['quantity'],
                    'game': play_path.item['name'],
                    'comment': comment,
                    'players': players
                }
                self.play_list.append(_play)
            # If page_num > 0, make another api call to get the next page of play results
            page += 1
            page_num -= 1
            #TODO: error handle for 429 and 202 errors
            plays_url = str("http://api.geekdo.com/xmlapi2/plays?username=" + self.name + "&page=" + str(page))
            # TODO: make the untangle part here a separate function returning results -- include 429 and 202 error handling there.
            plays_list = untangle.parse(plays_url)

    def _generate_scoresheet(self, score_sheet):
        return {
            "name": score_sheet['name'],
            "score": score_sheet['score'],
            "win": score_sheet['win']
        }

    def get_weight(self, game):
        game_id = game['bgg_id']
        weight_url = str(f"http://api.geekdo.com/xmlapi2/thing?id={game_id}&stats=1")

        game_stats = untangle.parse(weight_url)
        return game_stats.items.item.statistics.ratings.averageweight['value']


def main(argv):

    # TODO: argparse instead of sys.argv
    try:
        if len(argv) < 2 or '-h' in argv:
            Collection.usage(True)
            sys.exit()
        else:
            user_name = argv[1]
            print('''
                        *-*-*-*-*-*-BOARD GAME GEEK COLLECTION PRICE LIST-*-*-*-*-*-*
                        * This program will load your BoardGameGeek collection and  *
                        * create a list of all your owned games, wish list games,   *
                        * and expansions, with all data associated therewith,       *
                        * including MSRP, list price and an Amazon link.            *
                        * Enter -h for help using the program.                      *
                        *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*\n''')
    except IndexError:
        Collection.usage(True)
        sys.exit(1)

# TODO: change "Collection" to "Player" and have Collection and Plays inherit from Player class
    table = Collection(user_name)
    table.load()
    table.load_plays()
    table.get_weight({'bgg_id': '118048'})
  #  print(f"LOADING GAME LIST PRICES FOR {len(table.games)} GAMES...")
   # table.load_price()
   # print(f"LOADING WISH LIST PRICES FOR {len(table.wish_list)} GAMES...")
   # table.load_price(table.wish_list)
   # print(f"LOADING EXPANSIONS PRICES FOR {len(table.expansions)} EXPANSIONS...")
   # table.load_price(table.expansions)

    while False:
        to_sort = False
        print("-" * 40)
        cmd = input("Command: ").lower()
        c_f = cmd.split(" ")

        if len(c_f) > 3:
            c_f = "-h"

        if "-f" in c_f:
            full = 1
        else:
            full = 0

        if "-s" in c_f:
            to_sort = True

        if 'w' in c_f:
            if '-g' in c_f:
                g = input("Choose a game: ")
                table.out_formatted(table.wish_list, full, to_sort, g)
            else:
                table.out_formatted(table.wish_list, full, to_sort, False)
        elif 'g' in c_f:
            if '-g' in c_f:
                g = input("Choose a game: ")
                table.out_formatted(table.games, full, to_sort, g)
            else:
                table.out_formatted(table.games, full, to_sort, False)
        elif 'n' in c_f:
            if '-g' in c_f:
                g = input("Choose a game: ")
                table.plays(g)
            else:
                table.plays(False)
        elif 'e' in c_f:
            if '-g' in c_f:
                g = input("Choose a game: ")
                table.out_formatted(table.expansions, full, to_sort, g)
            else:
                table.out_formatted(table.expansions, full, to_sort, False)
        elif 'q' in c_f:
            sys.exit()
        elif '-h' in c_f:
            Collection.usage(False)
        else:
            print("Enter -h for help")


if __name__ == '__main__':
    main(sys.argv)

