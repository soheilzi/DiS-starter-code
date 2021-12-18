#! /usr/bin/python3

import sys

from world import world, log
from algorithm import send_to_all_but_one

if __name__ == '__main__':
    log(f'Hello from node{world.current_node}')
    log(f'My ID is {world.ID}')
    log(f'I\'m connected to nodes {world.neighbors}')
    log(f'I have edges {world.edges}')

    # if world.current_node == "9":
    #     log("I initiated the echo")
    #     send_to_all_but_one(msg="echo 9,X", but=-1)
    #     world.flag = False
    send_to_all_but_one(f"election {world.round},{world.leaderID},X,initiate", but=-1)

    try:
        world.listen()
    except KeyboardInterrupt:
        log("received keyboard interrupt")
        sys.exit(0)
