from __future__ import absolute_import, division, print_function
import copy, random
from game import Game

MOVES = {0: 'up', 1: 'left', 2: 'down', 3: 'right'}
MAX_PLAYER, CHANCE_PLAYER = 0, 1 

# Tree node. To be used to construct a game tree. 
class Node: 
    # Recommended: do not modify this __init__ function
    def __init__(self, state, player_type):
        self.state = (state[0], state[1])

        # to store a list of (direction, node) tuples
        self.children = []

        self.player_type = player_type

    # returns whether this is a terminal state (i.e., no children)
    def is_terminal(self):
        #TODO: complete this
        return len(self.children) == 0
    

# AI agent. Determine the next move.
class AI:
    # Recommended: do not modify this __init__ function
    def __init__(self, root_state, search_depth=3): 
        self.root = Node(root_state, MAX_PLAYER)
        self.search_depth = search_depth
        self.simulator = Game(*root_state)

    # (Hint) Useful functions: 
    # self.simulator.current_state, self.simulator.set_state, self.simulator.move

    # TODO: build a game tree from the current node up to the given depth
    def build_tree(self, node = None, depth = 0):
        
        if depth == 0:
            return
        
        elif node.player_type == MAX_PLAYER:
            for move in MOVES:
                self.simulator.set_state(*node.state)
                moved = self.simulator.move(move)
                if moved:
                    new_node = Node(self.simulator.current_state(), 1 - node.player_type)
                    node.children.append((move, new_node))
                    self.build_tree(new_node, depth - 1)
        
        elif node.player_type == CHANCE_PLAYER:
            open_tiles = self.simulator.get_open_tiles()
            for (i,j) in open_tiles:
                self.simulator.set_state(*node.state)
                self.simulator.tile_matrix[i][j] = 2
                new_node = Node(self.simulator.current_state(), 1 - node.player_type)
                node.children.append((None, new_node))
                self.build_tree(new_node, depth - 1)


    # TODO: expectimax calculation.
    # Return a (best direction, expectimax value) tuple if node is a MAX_PLAYER
    # Return a (None, expectimax value) tuple if node is a CHANCE_PLAYER
    def expectimax(self, node = None):
        # TODO: delete this random choice but make sure the return type of the function is the same
        if node is None:
            node = self.root

        if node.is_terminal():
            current_score = node.state[1]
            return None, current_score
 
        elif node.player_type == MAX_PLAYER:
            best_direction = None
            best_score = float('-inf')
            for direction, child in node.children:
                _, score = self.expectimax(child)
                if score > best_score:
                    best_score = score
                    best_direction = direction
            return best_direction, best_score

        elif node.player_type == CHANCE_PLAYER:
            total_score = 0
            for direction, child in node.children:
                _, score = self.expectimax(child)
                total_score += score/len(node.children)
            return None, total_score

    # Return decision at the root
    def compute_decision(self):
        self.build_tree(self.root, self.search_depth)
        direction, _ = self.expectimax(self.root)
        return direction

    # TODO (optional): implement method for extra credits
    def compute_decision_ec(self):
        return random.randint(0, 3)

