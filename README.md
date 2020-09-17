# Board Game Geek XML Parser
## Description
<p>This program interacts with boardgamegeek.com's XML API.  By providing your username, this program will make call the API and building a list of dictionaries composed of your owned games, owned expansions, and wish list.  This program will also obtain pricing data and an Amazon link to your games.  Output can be in abbreviated or long form.</p>
## Usage
<pre>bggapi.py [user name] [-h]</pre>
## Commands
<ul>Options
  <li>g: output your owned games' names, MSRPs, prices and Amazon Links</li>
  <li>w: output your wish list, with name of game, msrp, price and Amazon link</li>
  <li>e: output your owned expansions' anmes, MSRPs, prices and Amazon Links</li>
  <li>-h: help</li>
  <li>q: quit</li>
</ul>
<ul>Flags
  <li>-f: output full information (see below)</li>
  <li>-s: sort your chosen list by any key</li>
</ul>
## Data
<p>This program obtains the following information from the BGG API:</p>
<ul>The following is always printed to screen:
  <li>Name of game</li>
  <li>MSRP</li>
  <li>Current Price</li>
  <li>Amazon Link</li>
</ul>
<ul>The following are printed to screen when using the -f flag
  <li>Board Game Geek Primary Key</li>
  <li>Year Game Was Published</li>
  <li>Minimum Players Count</li>
  <li>Maximum Player Count</li>
  <li>Minimum Estimated Play Time</li>
  <li>Maximum Estimated Play Time</li>
  <li>Total Number of BGG Users Who Own The Game</li>
  <li>Rating</li>
  <li>Total Number of Ratings</li>
  <li>Average Rating</li>
  <li>Bayes Average</li>
  <li>Standard Deviation</li>
  <li>A List Of Where The Game Ranks on BGG's Ranking Board
  <li>Overall Rank</li>
  <li>Subcategory Rank</li></li>
  <li>Owned? (Yes=1, No=0)</li>
  <li>On Your Wish List? (Yes=1, No=0)</li>
  <li>Number Of Times You Played The Game</li>
</ul>
## Sample Output
### Without -f flag
<pre>----------------------------------------
name: Sentient
msrp: None
price: $107.63
link: https://www.amazon.com/dp/B06Y414DPC?tag=itemtext-boardgamegeek-20&linkCode=ogi&th=1&psc=1
----------------------------------------
name: Sherlock Holmes Consulting Detective: The Thames Murders & Other Cases
msrp: $49.99
price: $43.40
link: https://www.amazon.com/dp/2370990074?tag=itemtext-boardgamegeek-20&linkCode=ogi&th=1&psc=1
----------------------------------------
.
.
----------------------------------------
Total:  31
----------------------------------------
Command:</pre>
### With -f flag
<pre>
----------------------------------------
name: Ticket to Ride: USA 1910
bgg_id: 24439
year_published: 2006
min_players: 1
max_players: 8
min_play_time: 120
max_play_time: 240
total_owned: 47614
rating: 6
total_ratings: 36174
average_rating: 7.26436
bayes_average:: 7.07662
std_dev: 1.69397
Board Game Rank: 314
Thematic Rank: 110
own: 1
wish_list: 0
num_plays: 0
msrp: $19.99
price: $15.99
amzlink: https://www.amazon.com/dp/B000K8FYAS?tag=itemtext-boardgamegeek-20&linkCode=ogi&th=1&psc=1
----------------------------------------
Total:  12
----------------------------------------
Command:</pre>
