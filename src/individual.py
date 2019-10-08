from random import randint

class Individual:
    def __init__(self, genes, network):
        '''
        Individuals get a gene distribution and a network to assert its fitness
        '''
        self.genes   = genes
        self.fitness = self.__fitness(network)

    def __fitness(self, network):
        '''
        This is just a test, only driving networks where enabled when this was written
        '''

        res = 0
        for i in range(0, len(self.genes)-1, 2):
            node_from = network.get_decoded_node_with_encoded_name(self.genes[i][0])
            node_to   = network.get_decoded_node_with_encoded_name(self.genes[i+2][0])

            res += network.shortest_path_cost(node_from, node_to)
        
        return 1.0/res #1/res since we a minimizing

    def mcrossover(self, other, network):
        '''
        Modified crossover 5.2.1 Potvin
        '''
        assert len(self.genes) == len(other.genes) #sanity check

        crossover_point = randint(0, len(self.genes)-1)

        offspring = self.genes[:crossover_point]
        p1_set    = set([x[0] for x in offspring]) #Just a bit of optimization

        for gene in other.genes:
            if gene[0] not in p1_set:
                offspring.append(gene)

        assert len(self.genes) == len(offspring) #sanity check

        return Individual(offspring, network)



    def breed(self, other, network):
        '''
        Breeds two individuals to create two offsprings. Look at crossover functions in Potvin paper
        Each offspring should be processed with mutation operator
        '''

        offspring1 = self.mcrossover(other, network)
        offspring2 =  self.mcrossover(other, network)
        offspring1.mutate()
        offspring2.mutate()
        return [offspring1, offspring2] #For now produce two offsprings (could have the same crossover point)

    def mutate(self):
        '''
        Mutate offspring
        The offspring only gets mutated with a certain probability
        '''
        if randint(0, 1000) < 50: #~5% chance of mutation this should be changed
            i, j = randint(0, len(self.genes)-1), randint(0, len(self.genes)-1)
            self.genes[i], self.genes[j] = self.genes[j], self.genes[i] #For now only swap order of two genes