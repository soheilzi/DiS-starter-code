import random
import sys

from world import log, world, HELLO_MSG

got_hello_from = []
got_echo_reply_from = []


def send_to_all_but_one(msg, but):
    for neighbor in world.neighbors:
        if neighbor == but or str(neighbor) == world.current_node:
            continue
        world.send_message(to=neighbor, msg=msg)


def process_msg_echo(src, msg):
    msgdata = msg.split(' ')[1].split(',')
    if world.parent is None and msgdata[0] == "initiate":
        world.parent = src
        send_to_all_but_one(msg=msg, but=src)

    if src != world.parent and msgdata[0] == "initiate":
        return

    if src != world.parent and msgdata[0] == "reply":
        got_echo_reply_from.append(src)
        world.subtree_size += int(msgdata[1]) + 1

    if world.parent is None and set(got_echo_reply_from + [world.current_node]) == set(world.neighbors):
        log("I am the initiator and this was deep.")
        log(f"network size is : {world.subtree_size + 1} and actual size is : {world.network_size}")
        sys.exit()

    if set(got_echo_reply_from + [world.parent, world.current_node]) == set(world.neighbors):
        world.send_message(to=world.parent, msg="echo reply," + str(world.subtree_size))
        log("its been a pleasure being part of this wave")
        sys.exit()


def process_msg_leader(src, msg):
    msgdata = msg.split(' ')[1].split(',')
    _round = int(msgdata[0])
    leaderID = int(msgdata[1])
    subtree_size = int(msgdata[2])
    msgtype = msgdata[3]

    if _round < world.round or (_round == world.round and leaderID < world.leaderID):
        return

    if src != world.parent and msgtype == "reply":
        got_echo_reply_from.append(src)
        world.subtree_size += subtree_size + 1

    if msgtype == "initiate" and _round > world.round or (_round == world.round and leaderID > world.leaderID):
        world.active = False
        world.leaderID = leaderID
        world.round = _round
        got_echo_reply_from.clear()
        world.subtree_size = 0
        world.parent = src
        log(f"I accept {leaderID} as my leader")
        send_to_all_but_one(msg=msg, but=src)

    if set(got_echo_reply_from + [world.parent, world.current_node]) == set(world.neighbors):
        world.send_message(to=world.parent, msg=f"election {world.round},{world.leaderID},{world.subtree_size},reply")
        log(f"its been a pleasure being part of wave {world.round}")

    if world.parent is None and world.active and set(got_echo_reply_from + [world.current_node]) == set(world.neighbors):
        log(f"My wave finished. Actual network size is {world.network_size}, I got {world.subtree_size + 1}")
        if world.network_size == world.subtree_size + 1:
            log(f"I am the leader with ID = {world.ID}")
        else:
            world.ID = random.choices(range(1, world.network_size + 1))[0]
            world.round += 1
            world.leaderID = world.ID
            log(f"I will try again with ID = {world.ID}")
            send_to_all_but_one(f"election {world.round},{world.leaderID},{0},initiate", but=-1)

def process_msg(src, msg):
    log(f"message from {src}: {msg}")
    msgtype = msg.split(' ')[0]

    if msgtype == "echo":
        process_msg_echo(src, msg)

    if msgtype == "election":
        process_msg_leader(src, msg)
