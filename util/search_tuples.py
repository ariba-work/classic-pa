from __future__ import annotations

from pm4py.objects.petri_net.obj import Marking, PetriNet


class HashableDict(dict):
    def __hash__(self):
        return hash(tuple(sorted(self.items())))

    def copy(self) -> HashableDict:
        return HashableDict(self)

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()


class StateSpaceItem:
    def __init__(self, marking: frozenset[str], parikh_vector: HashableDict):
        self.marking = marking
        self.parikh_vector = parikh_vector

    def __hash__(self):
        return hash((self.marking, self.parikh_vector))

    def __eq__(self, other: StateSpaceItem):
        return (self.marking, self.parikh_vector) == (other.marking, other.parikh_vector)

    def __ne__(self, other):
        # Not strictly necessary, but to avoid having both x==y and x!=y
        # True at the same time
        return not(self == other)


class DijkstraSearchTuple:
    """This class defines a search tuple as required for Dijkstra's algorithm.

    Attributes:
        g (int): Cost so far component
        m (Marking): Marking of the search state
        p (DijkstraSearchTuple | None): Predecessor state
        t (Transition | None): Transition that led to this state
        l (int): Length of the trace so far
        unique_transition_id (str): Unique transition identifier for the process net
    """
    def __init__(self,
                 cost: int,
                 marking: Marking,
                 parent: DijkstraSearchTuple | None,
                 transition: PetriNet.Transition | None):
        self.g = cost
        self.m = marking
        self.p = parent
        self.t = transition
        self.l = self.p.l + 1 if self.p else 0
        self.unique_transition_id = f't{self.l}'

    def get_firing_sequence(self):
        ret = []
        if self.p is not None:
            ret = ret + self.p.get_firing_sequence()
        if self.t is not None:
            ret.append(self.t)
        return ret

    def __lt__(self, other):
        if self.g < other.g:
            return True
        elif other.g < self.g:
            return False
        else:
            return other.l < self.l

    def __repr__(self):
        string_build = ["\nm=" + str(self.m), " g=" + str(self.g),
                        " path=" + str(self.get_firing_sequence()) + "\n\n"]
        return " ".join(string_build)


class SearchTuple(DijkstraSearchTuple):
    """This class defines a search tuple as required for A* algorithm.

    Attributes:
        g (int): Cost so far component
        h (int): Heuristic value
        x (list[float]): Solution vector of the marking equation
        feasible (bool): Defines whether a solution is feasible or not
        m (Marking): Marking of the search state
        p (DijkstraSearchTuple | None): Predecessor state
        t (Transition | None): Transition that led to this state
        l (int): Length of the trace so far
        unique_transition_id (str): Unique transition identifier for the process net
    """
    def __init__(self,
                 g: int,
                 h: int,
                 m: Marking,
                 p: SearchTuple | None,
                 t: PetriNet.Transition | None,
                 x: list[float],
                 feasible: bool):
        super().__init__(g, m, p, t)
        self.h = h
        self.x = x
        self.feasible = feasible

    @property
    def f(self):
        return self.g + self.h

    def __lt__(self, other: SearchTuple):
        if self.f < other.f:
            return True
        if other.f < self.f:
            return False
        if self.feasible and not other.feasible:
            return True
        if not self.feasible and other.feasible:
            return False
        if self.g < other.g:
            return True
        if other.g < self.g:
            return False
        return self.h < other.h

    def __repr__(self):
        string_build = ["\nm=" + str(self.m), " f=" + str(self.f), ' g=' + str(self.g), " h=" + str(self.h),
                        " path=" + str(self.get_firing_sequence()) + "\n\n"]
        return " ".join(string_build)
