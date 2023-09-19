import random
import copy

class Individuo:
    def __init__(self, cromosoma=None):
        """
        Inicializa un objeto Individuo con un cromosoma aleatorio o el proporcionado.
        
        Args:
            cromosoma (list): Una lista de 8 números que representan el cromosoma.
        """
        if cromosoma is None:
            self.cromosoma = [random.randint(1, 8) for _ in range(8)]
        else:
            self.cromosoma = cromosoma
        self.fitness = 0
        self.conflictos = self.calcularConflictos()

    def mutacion(self):
        """
        Realiza una mutación en el cromosoma del individuo con una probabilidad del 20% en cada gen.
        Actualiza el número de conflictos después de la mutación.
        """
        for i in range(0, 8):
            mutacion = random.random()
            if mutacion <= 0.2:
                self.cromosoma[i] = random.randint(1, 8)
        self.conflictos = self.calcularConflictos()

    def calcularConflictos(self):
        """
        Calcula y devuelve el número de conflictos en el cromosoma del individuo.
        Los conflictos se refieren a la colocación de reinas en el mismo rango vertical o diagonal.
        """
        conflictos = 0

        verticales = [False] * 8 #arreglo auxiliar para no contar duplicados en vertical
        for i in range(0, 7): #para cada entrada i verificamos si hay un valor igual en el rango (i + 1, 8)
            for j in range(i + 1, 8):
                if self.cromosoma[i] == self.cromosoma[j] and verticales[i] == False:
                    verticales[i] = True
                    break
        conflictos += sum(verticales)

        diagonales = [False] * 8 #arreglo auxiliar para no contar duplicados en diagonal
        diagonales_invertidas = [False] * 8 #arreglo auxiliar para no contar duplicados en diagonal invertida
        for i in range(0, 8):
            valor = self.cromosoma[i]
            for j in range(1, 8 - i):
                if diagonales[i] and diagonales_invertidas[i]: #en este caso ya se contó un conflicto en diagonal y uno en diagonal invertida para cromosoma[i], por lo que pasamos a cromosoma[i+1]
                    break
                if self.cromosoma[i+j] == valor + j and diagonales[i] == False: #en este caso hay un conflicto en diagonal no contado anteriormente
                    diagonales[i] = True
                if self.cromosoma[i+j] == valor - j and diagonales_invertidas[i] == False: #en este caso hay un conflicto en diagonal invertida no contado anteriormente
                    diagonales_invertidas[i] = True
        conflictos += sum(diagonales)
        conflictos += sum(diagonales_invertidas)
        
        return conflictos

    def calcularFitness(self, mayor_numero_conflictos):
        """
        Calcula el fitness del individuo basado en el mayor número de conflictos y el mayor número posible de conflictos.
        
        Args:
            mayor_numero_conflictos (int): El máximo número de conflictos entre los individuos de la población actual.
        """
        self.fitness = mayor_numero_conflictos - self.conflictos

    def __str__(self):
        """
        Devuelve una representación legible en forma de cadena del individuo.
        """
        return f'{self.cromosoma} con fitness {self.fitness}'

    def __repr__(self):
        """
        Devuelve una representación oficial del individuo que puede usarse para recrear el objeto.
        """
        return f'Individuo({self.cromosoma})'
    
class Poblacion:
    def __init__(self):
        """
        Inicializa un objeto Poblacion con una población inicial vacía y mayor número de conflictos en 0.
        """
        self.poblacion = []
        self.mayor_numero_conflictos = 0

    def crearPoblacion(self):
        """
        Crea una población de 50 individuos aleatorios.
        """
        self.poblacion = [Individuo() for i in range(50)]

    def mejorIndividuo(self):
        """
        Encuentra el mejor individuo en la población basado en el fitness y devuelve una copia profunda de él.

        Returns:
            Individuo: El mejor individuo encontrado en la población.
        """
        mejor = max(self.poblacion, key=lambda x: x.fitness)
        mejorIndividuo = copy.deepcopy(mejor)
        return mejorIndividuo

    def mayorNumeroConflictos(self):
        """
        Calcula y almacena el máximo número de conflictos entre los individuos en la población.
        """
        mayor = max(self.poblacion, key=lambda x: x.conflictos).conflictos
        self.mayor_numero_conflictos = mayor

    def asignarFitness(self):
        """
        Asigna el valor de fitness a cada individuo en la población utilizando el mayor número de conflictos entre los individuos de la población.
        """
        for individuo in self.poblacion:
            individuo.calcularFitness(self.mayor_numero_conflictos)

    def haySolucion(self):
        """
        Verifica si al menos un individuo en la población tiene 0 conflictos, lo que indica una solución al problema.

        Returns:
            bool: True si hay al menos un individuo sin conflictos, False en caso contrario.
        """
        for individuo in self.poblacion:
            if individuo.conflictos == 0:
                return True
        return False

    def seleccionRuleta(self):
        """
        Realiza la selección de un individuo de la población utilizando el método de selección de ruleta.

        Returns:
            Individuo: El individuo seleccionado.
        """
        total_fitness = sum(individuo.fitness for individuo in self.poblacion)
        probabilidades = [individuo.fitness / total_fitness for individuo in self.poblacion]
        return random.choices(self.poblacion, probabilidades)[0]

if __name__ == "__main__":
    def recombinacion(individuo1, individuo2):
        """
        Función para recombinar dos individuos.
        
        Args:
            individuo1 (Individuo): Primer individuo para hacer la recombinación.
            individuo2 (Individuo): Segundo individuo para hacer la recombinación.
        
        Returns:
            Individuo: El hijo resultante de combinar individuo1 con individuo 2.
            
        """
        num = random.randint(1,6)
        cromosoma = individuo1.cromosoma[0:num]
        for i in range(num,8):
            cromosoma.append(individuo2.cromosoma[i])
        return Individuo(cromosoma = cromosoma)
        
    limite_generaciones = 1000
    generacion = 1
    
    poblacion = Poblacion()
    poblacion.crearPoblacion()
    poblacion.mayorNumeroConflictos()
    poblacion.asignarFitness()
    mejor_individuo = poblacion.mejorIndividuo()
    mejor_fitness = mejor_individuo.fitness
    
    while generacion <= limite_generaciones and (not poblacion.haySolucion()):
        nueva_poblacion = []
        nueva_poblacion.append(poblacion.mejorIndividuo())
        while len(nueva_poblacion) < 50:
            individuo1 = poblacion.seleccionRuleta()
            individuo2 = poblacion.seleccionRuleta()
            hijo = recombinacion(individuo1, individuo2)
            hijo.mutacion()
            nueva_poblacion.append(hijo)
        poblacion.poblacion = nueva_poblacion
        poblacion.mayorNumeroConflictos()
        poblacion.asignarFitness()
        mejor_individuo_actual = poblacion.mejorIndividuo()
        if mejor_individuo_actual.fitness > mejor_fitness:
            mejor_individuo = mejor_individuo_actual
            mejor_fitness = mejor_individuo_actual.fitness
        if generacion % 50 == 0:
            print(f'Generacion {generacion}: El mejor individuo encontrado hasta ahora es {mejor_individuo}.')
        generacion += 1
    
    if poblacion.haySolucion():
        print(f'Se encontro el optimo en la generacion {generacion}: {poblacion.mejorIndividuo()}.')
    else:
        print(f'El mejor individuo en 1000 generaciones fue {mejor_individuo}.')