import os
from test import SearchEngine


def is_valid_path(path):
    root = os.path.abspath("python-2.7.7-docs-html")
    if path == root:
        return True
    for (dir_path, dir_name, file_name) in os.walk(root):
        for d in dir_name:
            if path == os.path.abspath(os.path.join(dir_path, d)):
                return True
    return False


def input_type(string):
    query = string.lower().split()
    query_type = ""
    if string != "":
        if len(query) == 1:
            query_type = "single"
        elif "&&" in query or "||" in query or "!" in query and len(query) == 3:
            query_type = "logical"
        elif query[0].startswith('"') and query[-1].endswith('"'):
            query[0] = query[0].replace('"', '')
            query[-1] = query[-1].replace('"', '')
            query_type = "specific"
            pass
        else:
            query_type = "multy"
    return query_type, query


def main():
    num_results = 10
    while True:
        print("--- SEARCH ENGINE ---")
        print("1) Odaberite direktorijum")
        print("x) Ugasite program")
        choice = input(">> ").lower()
        while choice not in "1x":
            print("--- neispravan unos ---")
            choice = input(">> ").lower()
        if choice == "1":
            print("Unesite apsolutnu putanju direktorijuma")
            choice1 = input(">> ")
            while is_valid_path(choice1) is False:
                print("--- neispravan unos ---")
                choice1 = input(">> ")
            # inicijalizacija klase searchengine
            se = SearchEngine(choice1)
            se.load()
            root = choice1.split("\\")[-1]
            while True:
                print("--- DIREKTORIJUM: " + root + " ---")
                print("1) Pretraga")
                print("2) Podesi parametre")
                print("x) Nazad")
                choice2 = input(">> ").lower()
                while choice2 not in "12x":
                    print("--- neispravan unos ---")
                    choice2 = input(">> ")
                if choice2 == "1":
                    print("--- logicki operatori ---")
                    print("&& -> AND, || -> OR, ! -> NOT")
                    query = input(">> ")
                    while input_type(query)[0] == "":
                        print("--- neispravan unos ---")
                        query = input(">> ")
                    query_type = input_type(query)
                    if query_type[0] == "single":
                        se.print_dict(se.find(query_type[1][0], num_results), query_type[1][0])
                    elif query_type[0] == "logical":
                        se.print_dict(se.logical(query_type[1], num_results), query_type[1][0])
                    elif query_type[0] == "multy":
                        se.print_dict(se.multy(query_type[1], num_results), query_type[1][0])
                    elif query_type[0] == "specific":
                        se.print_dict(se.specific(query_type[1], num_results), 0)
                elif choice2 == "2":
                    while True:
                        print("--- IZMENA PARAMETARA ---")
                        print("1) Broj rezultata pretrage")
                        print("x) Nazad")
                        choice3 = input(">> ")
                        while choice3 not in "1x":
                            print("--- neispravan unos ---")
                            choice3 = input(">> ")
                        if choice3 == "1":
                            print("Unesite broj rezultata pretrage")
                            choice4 = input(">> ")
                            while not choice4.isdigit() or len(choice4) > 3:
                                print("--- neispravan unos ---")
                                choice4 = input(">> ")
                            num_results = int(choice4)
                        else:
                            break
                else:
                    break
        else:
            break


if __name__ == "__main__":
    main()
