import random
import sys

from world import log, world, HELLO_MSG

got_hello_from = []
got_echo_reply_from = []
got_waive_reply_from = []


def send_to_all_but_one(msg, but):
    for neighbor in world.neighbors:
        if neighbor == but or str(neighbor) == world.current_node:
            continue
        world.send_message(to=neighbor, msg=msg)


def process_msg_echo(src, msg):
    msgdata = msg.split(' ')[1].split(',')
    msg_wave_id = msgdata[0]
    if (world.parent is None or world.parent == src) and int(world.current_node) != int(msg_wave_id):
        world.parent = src
        send_to_all_but_one(msg=msg, but=src)

    if src != world.parent:
        got_echo_reply_from.append(src)
        if msgdata[1] != "X":
            world.subtree_size += int(msgdata[1]) + 1

    if int(world.current_node) == int(msg_wave_id) and set(got_echo_reply_from + [world.current_node]) == set(world.neighbors):
        log("I am the initiator and this was deep.")
        log(f"network size is : {world.subtree_size + 1} and actual size is : {world.network_size}")
        sys.exit()

    if set(got_echo_reply_from + [world.parent, world.current_node]) == set(world.neighbors):
        world.send_message(to=world.parent, msg=f"echo {msg_wave_id}," + str(world.subtree_size))
        log("its been a pleasure being part of this wave")
        sys.exit()


def process_msg_leader(src, msg):
    world.message_election_count += 1
    msgdata = msg.split(' ')[1].split(',')
    _round = int(msgdata[0])
    leaderID = int(msgdata[1])
    subtree_size = msgdata[2]

    if _round < world.round or (_round == world.round and leaderID < world.leaderID):
        return

    if src != world.parent:
        got_waive_reply_from.append(src)
        if subtree_size != "X":
            world.subtree_size += int(subtree_size) + 1

    if _round > world.round or (_round == world.round and leaderID > world.leaderID):
        world.active = False
        log("I am now passive so forget about me and my ID")
        world.leaderID = leaderID
        world.round = _round
        got_waive_reply_from.clear()
        world.subtree_size = 0
        world.parent = src
        log(f"I accept {leaderID} as my leader")
        send_to_all_but_one(msg=msg, but=src)

    if set(got_waive_reply_from + [world.parent, world.current_node]) == set(world.neighbors):
        world.send_message(to=world.parent, msg=f"election {world.round},{world.leaderID},{world.subtree_size}")
        log(f"its been a pleasure being part of wave {world.round}")

    if world.parent is None and world.active and set(got_waive_reply_from + [world.current_node]) == set(world.neighbors):
        log(f"My wave finished. Actual network size is {world.network_size}, I got {world.subtree_size + 1}")
        if world.network_size == world.subtree_size + 1:
            log(f"I am the leader with ID = {world.ID}")
            log("I will initiate a kill echo")
            world.subtree_size = 0
            send_to_all_but_one(msg=f"terminate {world.current_node},X", but=-1)
        else:
            world.ID = random.choices(range(1, world.network_size + 1))[0]
            world.round += 1
            world.leaderID = world.ID
            got_waive_reply_from.clear()
            world.subtree_size = 0
            log(f"I will try again with ID = {world.ID}")
            send_to_all_but_one(f"election {world.round},{world.leaderID},X", but=-1)


def process_msg_terminate(src, msg):
    msgdata = msg.split(' ')[1].split(',')
    msg_wave_id = msgdata[0]
    if world.parent == src and int(world.current_node) != int(msg_wave_id):
        send_to_all_but_one(msg=msg, but=src)
        got_echo_reply_from.append(src)
        world.subtree_size = 0

    if src != world.parent:
        got_echo_reply_from.append(src)
        if msgdata[1] != "X":
            world.subtree_size += int(msgdata[1]) + 1

    if int(world.current_node) == int(msg_wave_id) and set(got_echo_reply_from + [world.current_node]) == set(world.neighbors):
        log("I am the terminate initiator and the leader.")
        log(f"network size is : {world.network_size} and I got : {world.subtree_size + 1}")
        print(f"I am node {world.current_node} and I am the leader with ID {world.ID}")
        print(f"Message count : {world.message_election_count}")
        sys.exit()

    if int(world.current_node) != int(msg_wave_id) and set(got_echo_reply_from + [world.current_node]) == set(world.neighbors):
        world.send_message(to=world.parent, msg=f"terminate {msg_wave_id}," + str(world.subtree_size))
        log(f"my leader has ID {world.leaderID}(with node ID {msg_wave_id}) and my parent is node{world.parent}")
        log("its been a pleasure being part of this termination wave")
        print(f"I am node {world.current_node} and my leader is node {msg_wave_id} with ID {world.leaderID} my parent node is node{world.parent}")
        print(f"Message count : {world.message_election_count}")
        sys.exit()


def process_msg(src, msg):
    log(f"message from {src}: {msg}")
    msgtype = msg.split(' ')[0]

    if msgtype == "echo":
        process_msg_echo(src, msg)

    if msgtype == "election":
        process_msg_leader(src, msg)

    if msgtype == "terminate":
        process_msg_terminate(src, msg)
