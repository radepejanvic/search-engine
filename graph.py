class Graph:
    """ Reprezentacija jednostavnog grafa"""

    # ------------------------- Ugnjezdena klasa Vertex -------------------------
    class Vertex:
        __slots__ = '_element'

        def __init__(self, x):
            self._element = x

        def element(self):
            return self._element

        def __str__(self):
            return str(self._element)

    # ------------------------- Ugnjezdena klasa Edge -------------------------
    class Edge:
        __slots__ = '_origin', '_destination', '_element'

        def __init__(self, origin, destination, element=None):
            self._origin = origin
            self._destination = destination
            self._element = element

        def element(self):
            return self._element

        def __str__(self):
            return '({0},{1},{2})'.format(self._origin, self._destination, self._element)

    # ------------------------- Metode klase Graph -------------------------
    def __init__(self):
        self._outgoing = {}
        self._incoming = {}

    def get_inc_vertex(self, v):
        """Vraca sve cvorove koji ukazuju na odabrani"""
        return self._incoming[v].keys()

    def _validate_vertex(self, v):
        if not isinstance(v, self.Vertex):
            raise TypeError('Očekivan je objekat klase Vertex')
        if v not in self._outgoing:
            raise ValueError('Vertex ne pripada ovom grafu.')

    def vertex_count(self):
        return len(self._outgoing)

    def vertices(self):
        return self._outgoing.keys()

    def edge_count(self):
        total = sum(len(self._outgoing[v]) for v in self._outgoing)
        return total

    def edges(self):
        result = set()
        for secondary_map in self._outgoing.values():
            result.update(secondary_map.values())
        return result

    def get_edge(self, u, v):
        self._validate_vertex(u)
        self._validate_vertex(v)
        return self._outgoing[u].get(v)

    def degree(self, v, outgoing=True):
        self._validate_vertex(v)
        adj = self._outgoing if outgoing else self._incoming
        return len(adj[v])

    def incident_edges(self, v, outgoing=True):
        self._validate_vertex(v)
        adj = self._outgoing if outgoing else self._incoming
        for edge in adj[v].values():
            yield edge

    def insert_vertex(self, x=None):
        v = self.Vertex(x)
        self._outgoing[v] = {}
        self._incoming[v] = {}
        return v

    def insert_edge(self, u, v, x=None):
        if self.get_edge(u, v) is not None:
            raise ValueError('u and v are already adjacent')
        e = self.Edge(u, v, x)
        self._outgoing[u][v] = e
        self._incoming[v][u] = e
