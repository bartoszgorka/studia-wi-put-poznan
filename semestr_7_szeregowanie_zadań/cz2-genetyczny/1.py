from random import randint
import math

class GeneticScheduler:
    def __init__(self, n, k, h, ot, tpt, dd, bs, gv, stl):
        self.best_scheduled = bs # TO PRZYCHODZI Z PIERWSZYCH ALGORYTMÓW
        self.gen_zero = []
        self.population = 100  # Must be x * 4
        self.mutation_rate = 0.1
        self.mutation_rate_percent = self.mutation_rate * 100
        self.mutation_flat = int(n * self.mutation_rate)
        self.generations = 500

    def create_gen_zero(self):
        pass
        # Tyle ile mam populacji - robię iteracje w pętli
        # W każdej iteracji robię tyle mutacji ile pozwolono
        # Zamieniam dwa taski ze sobą (losowo wybrane)
        # Nowe uszeregowanie dodaję do puli - czyli będę mieć na koniec w tym => populations + 1 (bazowe)

    def crossover(self, s1, s2):
        pass
        # Robimy 1-point crossover
        # Z range 0 - n losuję indeks miejsca w którym robię przecięcie
        # Tworzę dwa nowe uszeregowania - na początek każdego przed przecięciem wrzucam rodzica drugiego
        # Czyli jak mam [1, 2, 3 | 4, 5, 6] i [3, 4, 2 | 5, 6, 1] to jeden ma [1, 2, 3] a drugi [3, 4, 2]
        # Następnie z drugiego z rodziców wyrzucam już użyte zadania
        #   to co zostało (w tej kolejności) dorzucam na koniec uszeregowania

    def create_new_gen(self, prev, group_size):
        # Robimy nową iterację epoki
        # Odpalamy tyle mutacji ile zakładaliśmy - to nam generuje nowe populacje
        # W zależności czy trafiliśmy w szansę na mutację to dokładamy populację która ma zmienioną jedną cechę
        # TODO mutacja - podmiana dwóch zadań X z Y w ramach jednego uszeregowania, wynik jako nowa populacja
        # Wybieramy najlepsze `get_best`
        # Jeżeli mamy jeszcze czas i nie wykorzystano już wszystkich epok to robimy kolejną pętlę

    def get_best(self, population):
        # Co epokę robić wybranie X najlepszych uszeregowań np. 10
        # Może turniej? To powinno pozwolić na lepsze mutacje
        # Te uszeregowania przechodzą do kolejnej epoki

    def run(self):
        pass
        # Przygotowuję populację zerową z `populations + 1` uszeregowaniami
        # Robię X epok biorąc poprzednią jako bazową - kolejne populacje wyjdą
        # Wybieram najlepsze uszeregowanie (z całej grupy którą zebrałem)
        # Liczę i zwracam funkcję celu i moment startu
