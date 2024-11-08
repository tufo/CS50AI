import csv
import sys

from util import Node, StackFrontier, QueueFrontier

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}


def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass


def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    source = person_id_for_name(input("Name: "))
    if source is None:
        sys.exit("Person not found.")
    target = person_id_for_name(input("Name: "))
    if target is None:
        sys.exit("Person not found.")

    path = shortest_path(source, target)
    
    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        path = [(None, source)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")


def shortest_path(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    """

    # TO DO
    # raise NotImplementedError

    #self.source = source
    #self.goal = goal
    
    # initialize variable to keep track of number of states explored.
    #self.states_explored = 0
    states_explored = 0

    # create node that represents the start state (position, source).
    origin = Node(state=source, parent=None, action=None)

    # create a frontier (choose stack or queue)
    frontier1 = QueueFrontier() # notice there is no need to enter anything within parentheses.

    # add start state to frontier.
    frontier1.add(origin)

    # initialize explored set within self, which is empty
    # remember that sets are unordered and all elements are intended to be interpreted together as a unit, not individually/separately.
    #self.explored_set = set()
    explored_set = set()

    # implement loop.
    while True:

        # check whether the entire frontier is empty; call the .empty function.
        if frontier1.empty() == True:
            return "There is no solution."

        # call the .remove function, which removes node from frontier, and also assigns that selected node to be the active node.
        current_node = frontier1.remove()

        # update the number of states explored.
        states_explored += 1

        # check if state of node is the goal; if yes, then...
        if current_node.state == target:
            # initialize backtrack arrays (list variables).
            print("*************** PROBLEM HAS BEEN SOLVED ***************")
            path = []

            # target (goal), self, parents are states.
            # STATE: current person
            # PARENT: previous person
            # ACTION: a connector line, coordinates: movie_id

            # WHILE there are still parents to look for...
            while current_node.parent != None:
            
                # keep following up the parent nodes to find solution.
                # 42:18 in lecture
                
                # append (action, state) 2-tuple to path
                entry = (current_node.action, current_node.state)
                path.append(entry)

                # reassign the current_node to be its parent for next iteration.
                current_node = current_node.parent

            path.reverse()

            """
            print("Actions:")
            print(actions)
            print("States:")
            print(states)               
            print("Path: ")
            print(path)
            """

            return path
            
        # if goal has not yet been found, then...
        # add the state to the explored_set
        explored_set.add(current_node.state)

        # Add neighbors to the frontier using neighbors_for_person()
        # print(neighbors) will return: [('movie_id', 'person_id'), ...]
        # 43:18

        neighbors = neighbors_for_person(current_node.state) # this is a list of 2-tuples.

        """
        # Kevin Bacon: 102
        # Demi Moore: 193
        # A Few Good Men: 104257

        print("person_id: ")
        print(current_node.state)
        print("Neighbors: ")
        print(neighbors)
        """

        # self.neighbors will return a 2-tuple of (action, state)
        # for loop: (action, state) is a 2-tuple corresponding to 
        # for (action, state) in [(action1, state1), (action2, state2), ...]
        for (action, state) in (neighbors):
            # the state element has been extracted via the for loop.

            # exclude 'current_node by checking that it's not in the frontier' & 'already-explored states'
            if not frontier1.contains_state(state) and state not in explored_set:
                # create a child node; assign values of action and state to the object attributes.
                child = Node(state=state, parent=current_node, action=action)
                # add that new child node to the frontier.
                frontier1.add(child)



def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors


if __name__ == "__main__":
    main()
