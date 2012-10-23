#!/usr/bin/python

from Game import Game

if __name__ == "__main__":
    g = Game(input_type='Console')
    print "Winner {0}".format(g.main_loop())

