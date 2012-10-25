from Player import *
from Board import *

class CLIClient:

    @staticmethod
    def main_phase(id, game):
        player = game.players[id]

        print "=== Turn {0}: Player {1}".format(game.turn, id)
        print player
        print "Board: {0}".format(game.board)


        while (True):
            input = raw_input('\nChoose: 1) Play 2) Buy. Hit Enter if done\n')

            if input == '1':
                while (True):
                    print "Choose a card to play or Enter for Done:"
                    i = 0
                    available_cards = sorted(list(set(
                        [x.name for x in player.hand]
                    )))
                    for name in available_cards:
                        print "{0}) {1}".format(i, name)
                        i += 1

                    card_choice = raw_input()
                    if card_choice == '':
                        break
                    card_choice = int(card_choice)

                    if card_choice < 0 or card_choice >= i:
                        print "\nInvalid Choice {0}\n".format(card_choice)
                        continue

                    while (True):
                        # Pick which casting zone to play to
                        valid_zones = game.board.get_valid_casting_hexes(game.players[id])
                        zone = raw_input('zone to cast to (0 for first zone from bottom, etc): ')
                        # Pick coordinates to place.
                        # You get stuck if you don't have anywhere to place.
                        try:
                            zone = int(zone)
                        except ValueError as e:
                            print "\nInvalid Choice - input not an int\n"
                            break
                        try:
                            game.play_card(available_cards[card_choice], id, valid_zones[zone])
                        except:
                            print "\nInvalid Play \n"
                            continue
                        break
                break
            elif input == '2':
                while (True):
                    print "Choose a card to buy:"
                    i = 0
                    available_cards = player.grimoire.get_buyable_card_names()
                    for name in available_cards:
                        print "{0}) {1}".format(i, name)
                        i += 1
                    card_choice = raw_input()
                    if card_choice == '':
                        break
                    card_choice = int(card_choice)

                    if card_choice < 0 or card_choice >= i:
                        print "\nInvalid Choice {0}\n".format(card_choice)
                        continue
                    player.buy(available_cards[card_choice])
                break
            elif input == '':
                break
            else:
                print "Invalid Command"

        return
