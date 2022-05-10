class TrieNode:
    """Cvor trie strukture"""

    def __init__(self, char, documents=None):
        self.char = char
        self.is_end = False
        self.counter = 0
        self.children = {}
        self.documents = documents


class Trie(object):
    """Trie objekat"""

    def __init__(self):
        """
        Trie bavezno sadrzi jedan cvor, i on ne sadrzi slova
        """
        self.root = TrieNode("")

    def insert(self, word, file, index):
        """
        Dodaj rec u trie stablo
        Vezuje recnik formata {vertex(file):[indexes of words]}
        za svaku pojedinacnu rec
        """
        word = word.lower()
        node = self.root
        for char in word:
            if char in node.children:
                node = node.children[char]
            else:
                new_node = TrieNode(char)
                node.children[char] = new_node
                node = new_node

        node.is_end = True

        if node.documents is None:
            node.documents = {}

        if file not in node.documents.keys():
            node.documents[file] = []

        node.counter += 1
        node.documents[file].append(index)

    def word_count(self, word):
        """Vraca recnik formata {vertex(file):[indexes of words]...} ili
           None ukoliko rec ne postoji Trie-u"""
        node = self.root
        for char in word:
            if char in node.children:
                node = node.children[char]
            else:
                return None
        return node.documents
