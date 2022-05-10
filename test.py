from myParser import Parser
from graph import Graph
from trie import Trie
import os
import time
import tabulate
from copy import deepcopy


def partition(array, low, high):
    pivot = array[high]
    i = low - 1
    for j in range(low, high):
        if array[j] <= pivot:
            i = i + 1
            (array[i], array[j]) = (array[j], array[i])
    (array[i + 1], array[high]) = (array[high], array[i + 1])
    return i + 1


def quickSort(array, low, high):
    if low < high:
        pi = partition(array, low, high)
        quickSort(array, low, pi - 1)
        quickSort(array, pi + 1, high)


class SearchEngine(object):
    def __init__(self, root):
        self.root = root
        self.files = []
        self.subs = []
        self.existing_vertexes = {}
        self.vert = {}
        self.p = Parser()
        self.g = Graph()
        self.t = Trie()

    def load(self):
        """
        Ucitavanje svih podataka u predvidjene strukture
        NEOPHODNO ZA POCETAK PROGRAMA
        """
        for (dir_path, dir_name, file_name) in os.walk(self.root):
            for file in file_name:  # prolazak kroz sve fajlove
                if file.endswith(".html"):

                    file_abs = os.path.abspath(os.path.join(dir_path, file))
                    # mozda nepotrebno (samo ovaj prvi red ispod)
                    self.files.append(file_abs)
                    if file_abs not in self.existing_vertexes:
                        self.existing_vertexes[file_abs] = self.g.insert_vertex(file_abs)
                    origin = self.existing_vertexes[file_abs]

                    """generisanje izlaznih grana iz svakog fajla u onaj koga linkuje"""
                    links, words = self.p.parse(file_abs)
                    for link in links:
                        if link not in self.existing_vertexes:
                            self.existing_vertexes[link] = self.g.insert_vertex(link)
                        destination = self.existing_vertexes[link]
                        self.g.insert_edge(origin, destination)

                    """generisane trie stabla"""
                    for i in range(len(words)):
                        word = words[i].lower()
                        self.t.insert(word, origin, i)

            # mozda nepotrebno
            for direct in dir_name:
                self.subs.append(os.path.abspath(os.path.join(dir_path, direct)))

    def find(self, word, number_of_results=10):
        """
        Vraca sortiran recnik:
        {stranica: rank}
        """
        ranking = {}
        occurances = self.t.word_count(word)
        if occurances is not None:
            for file in occurances.keys():
                link_word_count = 0
                try:
                    for link in self.g.get_inc_vertex(file):
                        link_word_count += len(occurances[link])
                except KeyError:
                    link_word_count = 0
                rank = round(len(occurances[file]) + self.g.degree(file, False) + 0.5 * link_word_count)
                if rank not in ranking:
                    ranking[rank] = []
                ranking[rank].append(file)

            sorted_ranks = list(ranking.keys())
            quickSort(sorted_ranks, 0, len(sorted_ranks) - 1)
            sorted_ranks.reverse()
            # results = []
            # result_ranks = []
            results_dict = {}
            for i in range(number_of_results):
                if i in range(len(sorted_ranks)):
                    for f in ranking[sorted_ranks[i]]:
                        results_dict[f] = sorted_ranks[i]
                    # results.extend(ranking[sorted_ranks[i]])
                    # result_ranks.append(sorted_ranks[i])
                else:
                    break
            # print(results)
            # print(result_ranks)
            # print(results_dict)
            return results_dict  # results, result_ranks
        else:
            return {}

    def logical(self, query, number_of_results=10):
        query1 = self.find(query[0], 1000)
        query2 = self.find(query[2], 1000)
        results = {}
        if query[1] == "&&":
            for key in query1.keys():
                if key in query2:
                    rank = query1[key] + query2[key]
                    results[rank] = key
        elif query[1] == "||":
            for key in query1.keys():
                if key in query2:
                    rank = query1[key] + query2[key]
                    results[rank] = key
                else:
                    rank = query1[key]
                    results[rank] = key
            for key in query2.keys():
                if key not in query2.values():
                    rank = query2[key]
                    results[rank] = key
        elif query[1] == "!":
            results = {}
            for key in query2.keys():
                if key in query1:
                    query1.pop(key)
            for i in range(number_of_results):
                if i in range(len(query1.keys())):
                    new_key = list(query1.keys())[i]
                    results[new_key] = query1[new_key]
            return results
            # return query1
        else:
            return results
        sorteds = list(results.keys())
        quickSort(sorteds, 0, len(sorteds) - 1)
        sorteds.reverse()
        sorted_dict = {}
        for i in range(number_of_results):
            if i in range(len(sorteds)):
                sorted_dict[results[sorteds[i]]] = sorteds[i]
                # for f in sorteds:
                #     sorted_dict[results[f]] = f
            else:
                break
        return sorted_dict

    def multy(self, query, number_of_results=10):
        results = {}
        packed = {}
        ranks = []
        files = []
        for word in query:
            occurances = self.find(word, 1000)
            for o in occurances.keys():
                if o in files:
                    ranks[files.index(o)] += occurances[o] * 2
                else:
                    files.append(o)
                    ranks.append(occurances[o])
        # ranks -> lista rankova
        # files -> lista fajlova
        for i in range(len(ranks)):
            if ranks[i] not in results:
                results[ranks[i]] = []
            results[ranks[i]].append(files[i])
        # resuls -> recnik vrednost:[file1, file2]

        quickSort(ranks, 0, len(ranks) - 1)
        ranks.reverse()
        for rank in ranks:
            for file in results[rank]:
                packed[file] = round(rank)

        keys = list(packed.keys())
        packed2 = {}
        for i in range(number_of_results):
            if i in range(len(keys)):
                packed2[keys[i]] = packed[keys[i]]
        return packed2

    def specific(self, query, number_of_results=10):

        occurances = self.t.word_count(query[0])
        # sorted_results = {}
        if occurances is None:
            return {}
        self.vert = {}
        for key in occurances.keys():
            self.vert[key] = []
        c = 0
        for word in query[1:]:
            c += 1
            next_word = self.t.word_count(word)
            if next_word is None:
                return {}
            for o in occurances.keys():
                if o not in next_word.keys():
                    try:
                        self.vert.pop(o)
                    except KeyError:
                        continue
                else:
                    if c == 1:
                        for i in occurances[o]:
                            if i+1 in next_word[o]:
                                self.vert[o].append(i+1)
                        if len(self.vert[o]) == 0:
                            try:
                                self.vert.pop(o)
                            except KeyError:
                                continue
                    else:
                        try:
                            for i in range(len(self.vert[o])):
                                if self.vert[o][i]+1 in next_word[o]:
                                    self.vert[o][i] += 1
                                if len(self.vert[o]) == 0:
                                    self.vert.pop(o)
                        except KeyError:
                            continue
        results = {}
        sorted_results = {}
        values = []
        for key in self.vert.keys():
            rank = len(self.vert[key]) + self.g.degree(key, False)
            values.append(rank)
            results[key] = rank
        values.sort(reverse=True)
        quickSort(values, 0, len(values) - 1)
        values.reverse()
        for i in range(number_of_results):
            if i in range(len(values)):
                for key in results.keys():
                    if results[key] == values[i]:
                        sorted_results[key] = values[i]
            else:
                break
        # for v in values:
        #     for key in results.keys():
        #         if results[key] == v:
        #             sorted_results[key] = v
        return sorted_results

    def print_dict(self, dictioanary, word="UPIT"):
        print()
        counter = 0
        for (r, a) in dictioanary.items():
            print(r, a)
            if counter == 0:
                words = self.p.parse(str(r))[1]
                if word == 0:
                    indexes = self.vert[r]
                    word_ind = indexes[0]
                else:
                    word_dict = self.t.word_count(word)
                    word_ind = word_dict[r][0]
                string = ""
                for i in range(word_ind - 10, word_ind):
                    try:
                        string += words[i] + " "
                    except IndexError:
                        continue
                for i in range(word_ind, word_ind + 11):
                    try:
                        string += words[i] + " "
                    except IndexError:
                        break
                counter += 1
                print("   kratak isecak:   " + string)
        if counter == 0:
            print("--- nema rezultata pretrage ---")
        print()

# p = Parser()
# reci = p.parse("python-2.7.7-docs-html/howto/argparse.html")
# print(reci[1].index("help"))
# print(reci[1])
# s = SearchEngine("python-2.7.7-docs-html/whatsnew")
# start = time.time()
# s.load()
# print("language")
# recnik1 = s.t.word_count("language")
# for (r, a) in recnik1.items():
#     print(r, a)
# print(len(recnik1.keys()))
# k = [4, 10, 1, 0, 12, 140, 23]
# quickSort(k, 0, len(k)-1)
# k.reverse()
# print(k)


