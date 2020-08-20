import untangle
import json

class Collection:
    def __init__(self, name):
        self.name = name
        self.games = []
        self.expansions = []
        self.wish_list = []

    def __build_dict(self, p, fp):
        rank = fp.stats.rating.ranks.rank
        rank_list = []

        # Handling untangled returning single-element list containing string in dictionary format for ranks
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
            'own': p.status["own"],
            'wish_list': p.status["wishlist"],
            'num_plays': p.numplays.cdata
        }

        return _d

    def load(self):
        check = True
        no_expansion = "&excludessubtype=boardgameexpansion"
        expansion = "&subtype=boardgameexpansion"
        full_stats = "&stats=1"

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



        # TODO: combine game and expansion iteration into one function
        for i in range(len(obj_games.items)):
            path = obj_games.items.item[i]
            full_path = obj_full.items.item[i]
            game_dict = self.__build_dict(path, full_path)

            if int(game_dict['own']):
                self.games.append(game_dict)
            elif int(game_dict['wish_list']):
                self.wish_list.append(game_dict)
            else:
                pass

        for i in range(len(obj_expansion.items)):
            e_path = obj_expansion.items.item[i]
            e_full_path = obj_full.items.item[i]
            game_dict = self.__build_dict(e_path, e_full_path)

            if int(game_dict['own']):
                self.expansions.append(game_dict)
            elif int(game_dict['wish_list']):
                self.wish_list.append[game_dict]
            else:
                pass

    def out(self, subset):

        while not (subset.lower() in ['games', 'wish_list', 'expansions']):
            subset = input("Usage -- 'games' 'wish_list' 'expansions': ")

        if subset == 'games':
            subset = self.games
        elif subset == 'expansions':
            subset = self.expansions
        else:
            subset = self.wish_list

        for i in range(len(subset)):
            for keys in subset[i]:
                if type(subset[i][keys]) == list:
                    l = len(subset[i][keys])
                    for j in range(0, l, 2):
                        print(f'{subset[i][keys][j]}: {subset[i][keys][j+1]}')
                else:
                    print(f'{keys}: {subset[i][keys]}')
            print("-" * 20)

'''TODO def to_json():'''



name = input("Enter User Name: ")
x = Collection(name)
x.load()
option = input ("Type 'games' to print owned games, 'wish_list' for wishlist, 'expansions' for expansions:  ")
x.out(option)
jstr = json.dumps(x.games)
print(jstr)


'''The following didn't work:
In load function...

        self.__pre_build(obj_games, 0)
        self.__pre_build(obj_expansion, 1)


    def __pre_build(self, _obj, _exp):
        for i in range(len(_obj.items)):
            _path = _obj.items.item[i]
            _full_path = _obj.items.item[i]
            _game_dict = self.__build_dict(_path, _full_path)

            if int(_game_dict['own']):
                if _exp:
                    self.expansions.append(_game_dict)
                else:
                    self.games.append(_game_dict)
            elif int(_game_dict['wish_list']):
                self.wish_list.append(_game_dict)
            else:
                pass'''