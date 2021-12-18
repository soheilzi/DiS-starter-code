import random
# for number_of_nodes in range(5, 50, 5):
#     input_file = open(f'./inputs/complete_{number_of_nodes}.in', 'w')
#     print(f'{number_of_nodes}', file=input_file)
#     for i in range(1, number_of_nodes + 1):
#         for j in range(i + 1, number_of_nodes + 1):
#             print(f'{i} {j} {1}', file=input_file)
#
# # Undirected Ring
# for number_of_nodes in range(5, 50, 5):
#     input_file = open(f'./inputs/ring_{number_of_nodes}.in', 'w')
#     print(f'{number_of_nodes}', file=input_file)
#     for i in range(1, number_of_nodes + 1, 2):
#         if i != number_of_nodes:
#             print(f'{i} {i+1} {1}', file=input_file)
#         else:
#             print(f'{i} {1} {1}', file=input_file)
#
#         if i != 1:
#             print(f'{i} {i-1} {1}', file=input_file)
#         else:
#             print(f'{i} {number_of_nodes} {1}', file=input_file)
#
# # Star graph
# for number_of_nodes in range(5, 50, 5):
#     input_file = open(f'./inputs/star_{number_of_nodes}.in', 'w')
#     print(f'{number_of_nodes}', file=input_file)
#     for i in range(2, number_of_nodes + 1):
#         print(f'{1} {i} {1}', file=input_file)

# tree graph
edges = set()
for number_of_nodes in range(10, 40, 10):
    input_file = open(f'./tree{number_of_nodes}.in', 'w')
    print(f'{number_of_nodes}', file=input_file)

    while len(edges) < 2 * number_of_nodes - 2:
        n1 = random.choices(range(1, number_of_nodes + 1))[0]
        n2 = random.choices(range(1, number_of_nodes + 1))[0]
        if n1 == n2:
            continue
        currentlen = len(edges)
        edges.add(f'{n1} {n2} {1}')
        edges.add(f'{n2} {n1} {1}')
        if len(edges) != currentlen:
            print(f'{n1} {n2} {1}', file=input_file)


    # for i in range(1, number_of_nodes + 1):
    #     if i != number_of_nodes:
    #         print(f'{i} {i+1} {1}', file=input_file)