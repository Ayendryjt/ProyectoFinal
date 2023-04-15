import threading
import time
import random

class Filosofo(threading.Thread):
    def __init__(self, nombre, tenedor_izquierdo, tenedor_derecho):
        threading.Thread.__init__(self)
        self.nombre = nombre
        self.tenedor_izquierdo = tenedor_izquierdo
        self.tenedor_derecho = tenedor_derecho

    def run(self):
        for i in range(5):
            print(f'{self.nombre} está pensando.')
            time.sleep(random.uniform(0, 1))
            self.tomar_tenedores()
            print(f'{self.nombre} está comiendo.')
            time.sleep(random.uniform(0, 1))
            self.soltar_tenedores()
        print(f'{self.nombre} ha terminado de comer.')

    def tomar_tenedores(self):
        tenedor1, tenedor2 = self.tenedor_izquierdo, self.tenedor_derecho
        while True:
            tenedor1.acquire() # Intentar tomar el tenedor izquierdo
            bloqueado = not tenedor2.acquire(False)
            if not bloqueado:
                break
            tenedor1.release() # Liberar el tenedor izquierdo
            print(f'{self.nombre} no pudo tomar ambos tenedores y está esperando.')
            time.sleep(random.uniform(0, 1))
        else:
            return
          
    def soltar_tenedores(self):
        self.tenedor_izquierdo.release()
        self.tenedor_derecho.release()
        print(f'{self.nombre} ha soltado los tenedores.')


if __name__ == '__main__':
    random.seed(100)
    n_filosofos = 5
    tenedores = [threading.Semaphore(1) for i in range(n_filosofos)]
    filosofos = [Filosofo(f'Filósofo {i}', tenedores[i], tenedores[(i+1)%n_filosofos]) for i in range(n_filosofos)]
    for f in filosofos:
        f.start()
    for f in filosofos:
        f.join()






