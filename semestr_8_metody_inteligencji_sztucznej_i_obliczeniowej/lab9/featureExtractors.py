from misio.pacman.game import Directions, Actions
from misio.pacman.util import CustomCounter, manhattan_distance

def closestFood(pos, food, capsules, walls):
    """
    closestFood -- this is similar to the function that we have
    worked on in the search project; here its all in one place
    """
    fringe = [(pos[0], pos[1], 0)]
    expanded = set()
    while fringe:
        pos_x, pos_y, dist = fringe.pop(0)
        if (pos_x, pos_y) in expanded:
            continue
        expanded.add((pos_x, pos_y))
        # if we find a food at this location then exit
        if food[pos_x][pos_y] or (pos_x, pos_y) in capsules:
            return dist
        # otherwise spread out from the location to its neighbours
        nbrs = Actions.getLegalNeighbors((pos_x, pos_y), walls)
        for nbr_x, nbr_y in nbrs:
            fringe.append((nbr_x, nbr_y, dist + 1))
    # no food found
    return None


class SimpleExtractor():
    """
    Returns simple features for a basic reflex Pacman:
    - whether food will be eaten
    - how far away the next food is
    - whether a ghost collision is imminent
    - whether a ghost is one step away
    """

    def getFeatures(self, state, action):
        # extract the grid of food and wall locations and get the ghost locations
        food = state.getFood()
        capsules = state.getCapsules()
        walls = state.getWalls()
        ghosts = state.getGhostStates()
        ghosts_positions = state.getGhostPositions()
        map_size = walls.width * walls.height

        features = CustomCounter()

        features["bias"] = 1.0

        # compute the location of pacman after he takes the action
        x, y = state.getPacmanPosition()
        dx, dy = Actions.directionToVector(action)
        next_x, next_y = int(x + dx), int(y + dy)

        # count the number of ghosts 1-step away
        features["#-of-ghosts-1-step-away"] = sum(
            (next_x, next_y) in Actions.getLegalNeighbors(g.getPosition(), walls) and g.scaredTimer < 2 for g in ghosts)

        # if there is no danger of ghosts then add the food feature
        if not features["#-of-ghosts-1-step-away"] and (food[next_x][next_y] or (next_x, next_y) in capsules):
            features["eats-food"] = 1.0

        dist = closestFood((next_x, next_y), food, capsules, walls)
        if dist is not None:
            features["closest-food"] = float(dist) / map_size

        features["can-enter"] = 1.0
        if features["#-of-ghosts-1-step-away"] > 0 and state.getNumFood() > 1:
            food_amount = 0

            # Possible next positions
            next_possitions = Actions.getLegalNeighbors((next_x, next_y), walls)
            # if (x, y) in next_possitions:
            #     next_possitions.remove((x, y))
            # if (next_x, next_y) in next_possitions:
            #     next_possitions.remove((next_x, next_y))
            print(x, y, action, next_possitions)
            input()

        features.divideAll(10.0)
        return features
