import untangle
import json
import requests
'''
THE INTENT WITH THIS BRANCH IS TO TURN THIS CODE INTO A SCRIPT THAT WILL GET ME THE CURRENT PRICES
FOR ALL MY GAMES, AND PROVIDE A LINK - TKINTER FOR GUI
'''
class Wishlist:
    def __init__(self, name):
        self.name = name
        self.games = []
        self.expansions = []
        self.wish_list = []

    @staticmethod
    def __build_dict(p, fp):
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
            pub_year = None

        _d = {
            'name': p.name.cdata,
            'bgg_id': p['objectid'],
            'year_published': pub_year,
            'min_players': fp.stats['minplayers'],
            'max_players': fp.stats['maxplayers'],
            'min_play_time': fp.stats['minplaytime'],
            'max_play_time': fp.stats['maxplaytime'],
            'total_owned': fp.stats['numowned'],
            'rating': fp.stats.rating['value'],
            'total_ratings': fp.stats.rating.usersrated['value'],
            'average_rating': fp.stats.rating.average['value'],
            'bayes_average:': fp.stats.rating.bayesaverage['value'],
            'std_dev': fp.stats.rating.stddev['value'],
            'rank': rank_list,
            'num_plays': p.numplays.cdata,

        }

        return _d

    @staticmethod
    def __loading_display(i):
        status = "Loading"
        dot = "."
        _dots = dot * (i%5)
        del_len = len(status)+len(_dots)
        if i == 0:
            print(status + dot, end="")
        elif _dots:
            print('\b' * (del_len), end="")
            print(status + _dots, end="")
        else:
            print('\b' * (len(status) + 5), end="")
            print(status + dot, end="")




    def __pre_build(self, _obj, _full_obj, _exp):
        for i in range(len(_obj.items)):
            _path = _obj.items.item[i]
            _full_path = _full_obj.items.item[i]
            _game_dict = self.__build_dict(_path, _full_path)

            if int(_game_dict['own']):
                if _exp:
                    self.expansions.append(_game_dict)
                else:
                    self.games.append(_game_dict)
            elif int(_game_dict['wish_list']):
                self.wish_list.append(_game_dict)
            else:
                pass

    def load(self):
        check = True
        no_expansion = "&excludessubtype=boardgameexpansion"
        expansion = "&subtype=boardgameexpansion"
        full_stats = "&stats=1"

        # Three calls are necessary due to quirks in boardgamegeek.com's API - see bgg xml document tree.txt

        #TODO: adding "&wishlist=1 creates an attribute error when building the dict - creates a Nonetype object
        #TODO: add check for BGG 202 response
        while check:
            api_url = str("https://api.geekdo.com/xmlapi2/collection?username=" + self.name)
            obj_full = untangle.parse(api_url + full_stats)
            obj_games = untangle.parse(api_url + no_expansion)
            obj_expansion = untangle.parse(api_url + expansion)
            check = False
            try:
                if(obj_full.errors.error):
                    self.name = input(obj_full.errors.error.message.cdata + ".  Enter User Name: ")
                    check = True
            except AttributeError:
                pass

        self.__pre_build(obj_games, obj_full, 0)
        self.__pre_build(obj_expansion, obj_full, 1)

    def out_formatted(self):
        count = 0

        for el in self.wish_list:
            for keys in el:
                if type(el[keys]) == list:
                    for j in range(0, len(el[keys]), 2):
                        print(f'{el[keys][j]}: {el[keys][j+1]}')
                else:
                    print(f'{keys}: {el[keys]}')
            print("-" * 20)
            count = count + 1
        print(f'Total:  {count}')

    def sort_by(self, sort_type):
        while sort_type not in self.wish_list[0]:
            sort_type = input(f"Enter a key. Usage -- {self.wish_list[0].keys()}: ")
            try:
                self.wish_list = sorted(self.wish_list, key=lambda game: int(game[sort_type]))
            except TypeError:
                self.wish_list = sorted(self.wish_list, key=lambda game: game[sort_type])

    def load_price(self):
        i = 0
        # Multiple calls to BGG api to get Amazon data is needed -- multiple inline queries not supported
        # Although BGG returns its data in XML, the Amazon data is in JSON

        for el in self.wish_list:
            #name = el['name']
            el_id = el['bgg_id']
            url = ('https://www.boardgamegeek.com/api/amazon/textads?objectid=' + el_id + '&objecttype=thing')
            response = requests.get(url)
            amazon = json.loads(response.text)
            self.__loading_display(i)
            i = i + 1
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
                    if amazon_price == "(unavailable)":
                        el['msrp'] = "n/a"
                        el['price'] = "n/a"
                        el['amzlink'] = amazon_link
                        continue
                    else:
                        el['msrp'] = amazon_msrp
                        el['price'] = amazon_price
                        el['amzlink'] = amazon_link
                        #print(f"{name}: MSRP: {amazon_msrp} / Current Price: {amazon_price} - {amazon_link}")
                        continue
                except KeyError:
                     pass
            el['msrp'] = "n/a"
            el['price'] = "n/a"
            el['amzlink'] = "n/a"
            #print(f"{name} is not available on Amazon")


user_name = input("Enter User Name: ")
table = Wishlist(user_name)
table.load()
table.load_price()
table.out_formatted()