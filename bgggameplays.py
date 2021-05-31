import bggapi
import sys
#TODO: two errors - first time I call it either returns an error and cdata, or it returns double the results
user = 'flakcanon'
collection = bggapi.Collection(user)
year = '2021'
max_attempt = 3

while len(collection.games) == 0 and max_attempt:
    try:
        collection.load()
        collection.load_plays()
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


print(f"games owned: {collection.total_owned}")
print(f"games/expansions on wishlist: {collection.total_wish_list}")
print(f"expansions owned: {collection.total_exp}")
print(f"total plays logged: {len(collection.play_list)}")

if len(collection.play_list) > 0:
    plays_in_year_count = 0
    plays_in_year_list = []
    unique_games_by_year = []
    most_played_list = []


    '''Total plays in year'''
    for play in collection.play_list:
        if play['date'][0:4] == year:
            plays_in_year_count += 1
            plays_in_year_list.append(play)

    print(f'total games played in 2021: {plays_in_year_count}')

    '''Most played game of the year'''
    for play in plays_in_year_list:
        if play['game'] not in unique_games_by_year:
            unique_games_by_year.append(play['game'])
    print(f'total unique games played in 2021: {len(unique_games_by_year)}')
        # super inefficient but it works sooooooooooo good enough for now!
    for game in unique_games_by_year:
        i = 0
        for play in plays_in_year_list:
            if game == play['game']:
                i += 1
        temp_tup = (game, i)
        most_played_list.append(temp_tup)
    most_played_list.sort(key=lambda x:x[1],reverse=True)

    print(f'most played game of 2021: {most_played_list[0]}')

    '''Total games in collection played as a percentage'''
    collection_played_percent = float(len(unique_games_by_year)/collection.total_owned)
    print(f'percentage of collection played in 2021: {collection_played_percent*100:.2f}%')

    '''Total 2-player games in collection played as a percentage'''
    two_player_collection = []
    u_two_player_collection_2020 = []
    for game_2 in collection.games:
        min = game_2['min_players']
        if int(min) <= 2:
            two_player_collection.append(game_2)

    for g in collection.games:
        for u_g in unique_games_by_year:
            if u_g == g['name'] and int(g['min_players']) <= 2:
                u_two_player_collection_2020.append(u_g)
    collection_two_player_played = float(len(u_two_player_collection_2020)/len(two_player_collection))
    print(f'Total two player games played in 2021: {len(u_two_player_collection_2020)}')
    print(f'Total two player games played in collection: {len(two_player_collection)}')
    print(f'percentage of two-player supported games played in 2021: {collection_two_player_played*100:.2f}%')

    print("\nOur two player games\n-----------------------")
    i = 1
    for game in two_player_collection:
        print(f"{i:>3}. {game['name']:.<40}min players: {game['min_players']}")
        i+=1
    i = 1
    print(f"\nTwo Player Games Played In {year}\n----------------------")
    for game in u_two_player_collection_2020:
        print(f'{i}. {game}')
        i+=1
    print(f"\nTwo Player Games Not Played in {year}\n-----------------------")
    temp_two = two_player_collection.copy()
    for g_not in two_player_collection:
        for u_g_not in unique_games_by_year:
            if u_g_not == g_not['name']:
                temp_two.remove(g_not)
    i = 1
    for g_not_p in temp_two:
        print(f"{i:>3}. {g_not_p['name']:.<45}play time: {g_not_p['min_play_time']:>4} - {g_not_p['max_play_time']:>3} min")
        i+=1

    print(f"\nTotal Plays In {year}: All games\n------------------------------")
    i = 1
    for game in most_played_list:
        print(f"{i:>3}. {game[0]:.<40}Total Plays: {game[1]}")
        i += 1

    print(f"\nTotal Wins: All games\n-----------------------------")
    i = 1
    matt_wins = 0
    jill_wins = 0
    for el in collection.play_list:
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

#TODO refactor because slllloooowwww
    print(f"\nTotal Wins: Per Game")
    for game in collection.games:
        counter = 1
        matt_wins = 0
        jill_wins = 0
        matt_high = 0
        jill_high = 0
        print(f"{game['name']}")
        for play in collection.play_list:
            if not game['name'] == play['game']:
                continue
            else:
                print(f"----------------------------------\nGame {counter}.\n----------------------------------\n")
                for player in play['players']:
                    print(f"{player['name']}: {player['score']}")
                    if player['name'] == "Matt":
                        if int(player['win']) == 1:
                            matt_wins += 1
                        try:
                            #Note: No Thanks is Low Score -- must account for these
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
        print(f"-----------------------------------\n{game['name']} Totals\n---------------------------\nMatt Wins: {matt_wins} Matt High Score: {matt_high}"
              f"\nJill Wins: {jill_wins} Jill High Score {jill_high}\n")
