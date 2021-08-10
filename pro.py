import os
os.system("cls")
#Proyecto: Juego de buscaminas
import random
import re

#Mensaje de Bienvenida
print("\n\n\t\t\tBuscaminas ¿Estás listo para jugar?\n\n\t\t\t")
print("\t\t\t\t\tBy Tania\n\n\t\t\t")

#Crear tablero para representar al juego
class Tablero:
    def __init__(self, dim_size, num_bombas):
        self.dim_size = dim_size
        self.num_bombas = num_bombas
        self.tablero = self.hacer_nuevo_tablero()
        self.asignar_valores_tablero()
        self.excavar = set()

    def hacer_nuevo_tablero(self):
        #Generar un nuevo tablero
        tablero = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]

        #Colocar las bombas
        bombas_colocadas = 0
        while bombas_colocadas < self.num_bombas:
            lugar = random.randint(0, self.dim_size**2 - 1)
            hilera = lugar // self.dim_size
            columna = lugar % self.dim_size

            if tablero[hilera][columna] == '*':
                continue

            tablero[hilera][columna] = '*'
            bombas_colocadas += 1

        return tablero

    def asignar_valores_tablero(self):
        for h in range(self.dim_size):
            for c in range(self.dim_size):
                if self.tablero[h][c] == '*':
                    continue
                self.tablero[h][c] = self.conseguir_num_bombas_vecinas(h, c)

    def conseguir_num_bombas_vecinas(self, hilera, columna):

        num_bombas_vecinas = 0
        for h in range(max(0, hilera-1), min(self.dim_size-1, hilera+1)+1):
            for c in range(max(0, columna-1), min(self.dim_size-1, columna+1)+1):
                if h == hilera and c == columna:
                    continue
                if self.tablero[h][c] == '*':
                    num_bombas_vecinas += 1

        return num_bombas_vecinas

    def dig(self, hilera, columna):

        self.excavar.add((hilera, columna))

        if self.tablero[hilera][columna] == '*':
            return False
        elif self.tablero[hilera][columna] > 0:
            return True

        for h in range(max(0, hilera-1), min(self.dim_size-1, hilera+1)+1):
            for c in range(max(0, columna-1), min(self.dim_size-1, columna+1)+1):
                if (h, c) in self.excavar:
                    continue
                self.dig(h, c)
        return True

    def __str__(self):
    
        tablero_visible = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]
        for hilera in range(self.dim_size):
            for columna in range(self.dim_size):
                if (hilera,columna) in self.excavar:
                    tablero_visible[hilera][columna] = str(self.tablero[hilera][columna])
                else:
                    tablero_visible[hilera][columna] = ' '
        
        string_rep = ''
        amplitud = []
        for idx in range(self.dim_size):
            columnas = map(lambda x: x[idx], tablero_visible)
            amplitud.append(
                len(
                    max(columnas, key = len)
                )
            )

        indices = [i for i in range(self.dim_size)]
        indices_hilera = '   '
        celdas = []
        for idx, columna in enumerate(indices):
            format = '%-' + str(amplitud[idx]) + "s"
            celdas.append(format % (columna))
        indices_hilera += '  '.join(celdas)
        indices_hilera += '  \n'
        
        for i in range(len(tablero_visible)):
            hilera = tablero_visible[i]
            string_rep += f'{i} |'
            celdas = []
            for idx, columna in enumerate(hilera):
                format = '%-' + str(amplitud[idx]) + "s"
                celdas.append(format % (columna))
            string_rep += ' |'.join(celdas)
            string_rep += ' |\n'

        str_len = int(len(string_rep) / self.dim_size)
        string_rep = indices_hilera + '-'*str_len + '\n' + string_rep + '-'*str_len

        return string_rep

#Jugar
def play(dim_size=10, num_bombas=10):
    #Paso 1: Crear el tablero
    tablero = Tablero(dim_size, num_bombas)
    #Paso 2: Mostrar el tablero y preguntar dónde quiere excavar
    #Paso 3: Si la ubicación es una bomba, mostrar el mensaje de "Game Over"
    #Paso 4: Si la ubicación no es una bomba, volver a excavar
    #Paso 5: Repetir el paso 2 y 3 hasta que no haya más lugares
    safe = True 

    while len(tablero.excavar) < tablero.dim_size ** 2 - num_bombas:
        print(tablero)
        user_input = re.split(',(\\s)*', input("\n\n\t\t¿Dónde te gustaría excavar? Fila, columna: "))  # '0, 3'
        hilera, columna = int(user_input[0]), int(user_input[-1])
        if hilera < 0 or hilera >= tablero.dim_size or columna < 0 or columna >= dim_size:
            print("Invalid location. Try again.")
            continue

        safe = tablero.dig(hilera, columna)
        if not safe:
            break

    if safe:
        print("\n\n\t\t\t\t¡¡¡¡FELICIDADES!!!! ¡GANASTE!\n\n\t\t")
    else:
        print("\n\n\t\t\t\tGAME OVER :(\n\n\t\t")
        tablero.excavar = [(h,c) for h in range(tablero.dim_size) for c in range(tablero.dim_size)]
        print(tablero)

if __name__ == '__main__':
    play()