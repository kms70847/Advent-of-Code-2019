from collections import defaultdict

EMPTY = 0
BUG = 1

edge_indices = {
    "left": [(0, y) for y in range(5)],
    "right": [(4, y) for y in range(5)],
    "top": [(x,0) for x in range(5)],
    "bottom": [(x, 4) for x in range(5)]
}

#static collection of the locations of each neighbor of each cell.
#the values are (depth_delta, x, y) tuples.
p1_neighbor_locations = defaultdict(list)
for x in range(5):
    for y in range(5):
        for dx,dy in (0,1), (1,0), (0,-1), (-1,0):
            if 0 <= x+dx < 5 and 0 <= y+dy < 5:
                p1_neighbor_locations[x,y].append((0, x+dx, y+dy))

p2_neighbor_locations = defaultdict(list)
for x in range(5):
    for y in range(5):
        if x == 2 and y == 2:
            continue
        for dx,dy in (0,1), (1,0), (0,-1), (-1,0):
            if (
            0 <= x+dx < 5 and 
            0 <= y+dy < 5 and 
            (x+dx != 2 or y+dy !=2)
            ):
                p2_neighbor_locations[x,y].append((0, x+dx, y+dy))
interdepth_adjacencies = {"left": (1,2), "right": (3,2), "top": (2,1), "bottom": (2,3)}
for edge_name, cell in interdepth_adjacencies.items():
    for p in edge_indices[edge_name]:
        p2_neighbor_locations[p].append((-1, *cell))
        p2_neighbor_locations[cell].append((1, *p))

class State:
    def __init__(self, field=None, depth=0, quarantined=True):
        if field is None:
            self.field = [[EMPTY]*5 for y in range(5)]
        else:
            self.field = field

        self.depth = depth

        self.quarantined = quarantined
        self.neighbor_locations = p1_neighbor_locations if self.quarantined else p2_neighbor_locations

        self.parent = None
        self.child = None

    def root(self):
        """Returns the highest-depth state in the chain."""
        state = self
        while state.parent is not None:
            state = state.parent
        return state

    def tick(self):
        """
        Move the simulation forward by one step for `self` and all other states in the chain.
        Returns the chain's root.
        """
        assert self.parent is None
        root = self._create_new_states_if_needed()
        for state in root.iter_chain(): state._tick()
        for state in root.iter_chain(): state._update()
        return root

    def _create_new_states_if_needed(self):
        """
        Determine whether any new parents or children need to be created this tick in order to accommodate the spread of bugs.
        Returns the root of self.
        """
        assert self.parent is None
        for state in self.iter_chain():
            for x in range(5):
                for y in range(5):
                    c = state.field[y][x]
                    if c == BUG:
                        for depth_delta, n_x, n_y in state.neighbor_locations[x,y]:
                            if depth_delta == -1 and state.parent is None:
                                assert not state.quarantined
                                state.parent = State(field=None, depth=state.depth-1, quarantined=state.quarantined)
                                state.parent.child = state
                            if depth_delta == 1 and state.child is None:
                                assert not state.quarantined
                                state.child = State(field=None, depth=state.depth+1, quarantined=state.quarantined)
                                state.child.parent = state

        return self.parent if self.parent is not None else self

    def _tick(self):
        """
        Internal helper function for `tick`. Responsible for everything except actually updating the field.
        Assumes that all parent/child states that are infectable already exist. Call `_create_new_states_if_needed` prior to this to ensure this.
        """
        self.new_field = [[None]*5 for y in range(5)]

        for x in range(5):
            for y in range(5):
                c = self.field[y][x]
                neighbor_count = 0
                for depth_delta, n_x, n_y in self.neighbor_locations[x,y]:
                    state = None
                    if depth_delta == -1:
                        state = self.parent
                    elif depth_delta == 1:
                        state = self.child
                    else:
                        state = self
                    neighbor_count += 0 if state is None else state.field[n_y][n_x]
                if c == BUG and neighbor_count != 1:
                    self.new_field[y][x] = EMPTY
                elif c == EMPTY and neighbor_count in (1,2):
                    self.new_field[y][x] = BUG
                else:
                    self.new_field[y][x] = c

    def _update(self):
        """
        Internal helper function for `tick`.
        Update field data with the new field data calculated in `_tick`.
        """
        self.field = self.new_field
        del self.new_field #not strictly necessary, but useful for debugging

    def rating(self):
        """
        Returns the biodiversity rating of this state.
        Unlike most public methods, this only considers `self`, and not any of its descendants.
        """
        return sum((self.field[y][x]==BUG) * (2 ** (5*y+x)) for x in range(5) for y in range(5))
        
    def bug_count(self):
        """
        Returns the number of bugs in this state and its descendants.
        """
        total = 0
        for state in self.iter_chain():
            total += sum(state.field[y][x] for y in range(5) for x in range(5))
        return total

    def iter_chain(self):
        """
        Iterates over self and all its descendants.
        """
        state = self
        while state is not None:
            yield state
            state = state.child

    def __repr__(self):
        rows = []
        glyphs = {EMPTY: ".", BUG: "#"}
        state = self
        while state is not None:
            rows.append(f"Depth {state.depth}:")
            for y in range(5):
                rows.append("".join(glyphs[state.field[y][x]] for x in range(5)))
            state = state.child
        return "\n".join(rows)
        

starting_field = []
with open("input") as file:
    for line in file:
        starting_field.append([])
        for c in line.strip():
            starting_field[-1].append(BUG if c == "#" else EMPTY)

#part 1
state = State(starting_field, 0, True)
seen = {str(state)}
while True:
    state = state.tick()
    if str(state) in seen: 
        break
    seen.add(str(state))
print(state.rating())

#part 2
state = State(starting_field, 0, False)
for t in range(200):
    state = state.tick()
print(state.bug_count())