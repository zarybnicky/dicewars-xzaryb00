from dicewars.ai.utils import (
    attack_succcess_probability,
    probability_of_holding_area as probability_of_holding_area_client
)

def get_features(board, atk_name, def_name):
    attacker = board.get_area_by_name(atk_name)
    defender = board.get_area_by_name(def_name)
    atk_owner = attacker.owner_name
    atk_1_neighbors = k_neighbors(board, 1, atk_name)
    atk_2_neighbors = k_neighbors(board, 2, atk_name)
    def_1_neighbors = k_neighbors(board, 1, def_name)
    def_2_neighbors = k_neighbors(board, 2, def_name)
    return (
        (   # Inputs
            attacker.dice / 8,
            defender.dice / 8,
            attack_succcess_probability(attacker.dice, defender.dice),
            probability_of_holding_area(board, attacker.name, attacker.dice, atk_owner),
            probability_of_holding_area(board, attacker.name, 1, atk_owner),
            sum(area.dice for area in atk_1_neighbors if area.owner_name == atk_owner) / 100,
            sum(area.dice for area in atk_2_neighbors if area.owner_name == atk_owner) / 100,
            sum(area.dice for area in def_1_neighbors if area.owner_name != atk_owner) / 100,
            sum(area.dice for area in def_2_neighbors if area.owner_name != atk_owner) / 100,
        ),
        [   # Outputs
            1, # Holding atk after N turns
            1, # Holding def after N turns
        ],
        (   # Helper data
            atk_owner,
            attacker,
            defender,
        ),
    )


def k_neighbors(board, neighborhood_size, start):
    neighbors = set()
    current_areas = set([start])
    for i in range(neighborhood_size):
        new_areas = set()
        for a in current_areas:
            for an in board.get_area_by_name(a).adjacent_areas_names:
                if an not in neighbors:
                    neighbors.add(an)
                    new_areas.add(an)
        current_areas = new_areas
    if start in neighbors:
        neighbors.remove(start)
    return [board.get_area_by_name(i) for i in neighbors]


def probability_of_holding_area(board, area_name, area_dice, player_name):
    """Copied over from AI utils, adapted for the server"""
    area = board.get_area_by_name(area_name)
    probability = 1.0
    for adj in area.adjacent_areas_names:
        adjacent_area = board.get_area_by_name(adj)
        if adjacent_area.get_owner_name() != player_name:
            enemy_dice = adjacent_area.get_dice()
            if enemy_dice == 1:
                continue
            lose_prob = attack_succcess_probability(enemy_dice, area_dice)
            hold_prob = 1.0 - lose_prob
            probability *= hold_prob
    return probability


def get_features_client(board, atk_name, def_name):
    attacker = board.get_area(atk_name)
    defender = board.get_area(def_name)
    atk_owner = attacker.owner_name
    atk_1_neighbors = k_neighbors_client(board, 1, atk_name)
    atk_2_neighbors = k_neighbors_client(board, 2, atk_name)
    def_1_neighbors = k_neighbors_client(board, 1, def_name)
    def_2_neighbors = k_neighbors_client(board, 2, def_name)
    return (
        (   # Inputs
            attacker.dice / 8,
            defender.dice / 8,
            attack_succcess_probability(attacker.dice, defender.dice),
            probability_of_holding_area_client(board, attacker.name, attacker.dice, atk_owner),
            probability_of_holding_area_client(board, attacker.name, 1, atk_owner),
            sum(area.dice for area in atk_1_neighbors if area.owner_name == atk_owner) / 100,
            sum(area.dice for area in atk_2_neighbors if area.owner_name == atk_owner) / 100,
            sum(area.dice for area in def_1_neighbors if area.owner_name != atk_owner) / 100,
            sum(area.dice for area in def_2_neighbors if area.owner_name != atk_owner) / 100,
        ),
        [   # Outputs
            1, # Holding atk after N turns
            1, # Holding def after N turns
        ],
        (   # Helper data
            atk_owner,
            attacker,
            defender,
        ),
    )


def k_neighbors_client(board, neighborhood_size, start):
    neighbors = set()
    current_areas = set([start])
    for i in range(neighborhood_size):
        new_areas = set()
        for a in current_areas:
            for an in board.get_area(a).neighbours:
                if an not in neighbors:
                    neighbors.add(an)
                    new_areas.add(an)
        current_areas = new_areas
    if start in neighbors:
        neighbors.remove(start)
    return [board.get_area(i) for i in neighbors]
