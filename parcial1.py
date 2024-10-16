#DEFINICION DE CLASES

#Defino la clase Process con sus respectivos atributos
class Process:
    def __init__(self, label, burst_time, arrival_time, queue, priority):
        #Atributos de que se definirian segun el archivo de entrada
        self.label = label
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.arrival_time = arrival_time
        self.queue = queue
        self.priority = priority
        #Atributos con valores inicializados
        self.wait_time = 0
        self.completion_time = 0
        self.response_time = None
        self.turnaround_time = 0

    #constructor de la clase
    def __repr__(self):
        return (f"Process({self.label}, BT={self.burst_time}, AT={self.arrival_time}, "f"Q={self.queue}, Pr={self.priority})")

#Definicio de la clase Queue
class Queue:
    def __init__(self, algorithm, quantum=None):
        #Atributos de la Queue
        self.algorithm = algorithm
        self.processes = []
        self.quantum = quantum

    #Metodo para añadir un proceso a la Queue
    def add_process(self, process):
        self.processes.append(process)

    #Metodo para definir que algoritmo se ejecutara en los procesos de la Queue
    def execute(self, current_time):
        #Ejecutar RR con el tiempo actual como argumento
        if self.algorithm == 'RR':
            return self.rr(current_time)
        #Ejecutar FCFs con el tiempo actual como argumento
        elif self.algorithm == 'FCFS':
            return self.fcfs(current_time)

    #Algoritmo para FCFS
    def fcfs(self, current_time):
        #Si no hay process se devuelve el mismo valor de current time sin alterar
        if not self.processes:
            return current_time
        #Por cada process en la Queue
        for process in self.processes:
            #Si response_time es nulo
            if process.response_time is None:
                #response_time sera 0 o el valor del tiempo actual menos el tiempo de llegada
                process.response_time = max(0, current_time - process.arrival_time)
            #Se incrementa curren_time el valor de burst
            current_time += process.burst_time 
            #Set completion time
            process.completion_time = current_time 
            #Set turnaround_time como la resta del tiempo de completado con el tiempo de llegada
            process.turnaround_time = process.completion_time - process.arrival_time
            #set wait_time como la resta del tiempo de regreso con el tiempo de ejecucion
            process.wait_time = process.turnaround_time - process.burst_time
        self.processes.clear() #limpiar
        return current_time
    
    #Algoritmo para RR
    def rr(self, current_time):
        #Retornar valor si no hay Process
        if not self.processes:
            return current_time
        #Mientras halla procesos
        while self.processes:
            #Eliminar Process de la Queue y retornarlo
            process = self.processes.pop(0) 
            #Setear response time
            if process.response_time is None:
                process.response_time = max(0, current_time - process.arrival_time)
            #Si el tiempo restante es mayor que el quantum
            if process.remaining_time > self.quantum:
                #Tiempo restante se le resta el quantum
                process.remaining_time -= self.quantum
                #Tiempo actual Suma el quantum
                current_time += self.quantum
                #Volver a agregar el proceso a la Cola
                self.processes.append(process)
            else:
                #Setear atributos
                current_time += process.remaining_time
                process.remaining_time = 0
                process.completion_time = current_time
                process.turnaround_time = process.completion_time - process.arrival_time
                process.wait_time = process.turnaround_time - process.burst_time
        return current_time

    

#Definir la clase Scheduler MLQ
class MLQScheduler:
    def __init__(self):
        self.queues = []

    #Añadir Queue
    def add_queue(self, queue):
        self.queues.append(queue)

    #Organizador
    def schedule(self):
        current_time = 0
        for queue in self.queues:
            current_time = queue.execute(current_time)

#Funcion para recibir y procesar archivo de entrada
def read_input_file(file_name):
    processes = []
    with open(file_name, 'r') as file:
        for line in file:
            if line.startswith("#") or not line.strip():
                continue
            data = line.split(";")
            label, bt, at, q, pr = data[0], int(data[1]), int(data[2]), int(data[3]), int(data[4])
            processes.append(Process(label, bt, at, q, pr))
    return processes

#Funcion para generar el archivo de salida
def out_file(processes, output_name):
    with open(output_name, 'w') as file:
        file.write("# label; BT; AT; Q; Pr; WT; CT; RT; TAT\n")
        
        totals = {'wait_time': 0, 'completion_time': 0, 'response_time': 0, 'turnaround_time': 0}
        num_processes = len(processes)

        for process in processes:
            file.write(f"{process.label};{process.burst_time};{process.arrival_time};"
                       f"{process.queue};{process.priority};{process.wait_time};"
                       f"{process.completion_time};{process.response_time};{process.turnaround_time}\n")
            totals['wait_time'] += process.wait_time
            totals['completion_time'] += process.completion_time
            totals['response_time'] += process.response_time
            totals['turnaround_time'] += process.turnaround_time

        averages = {key: total / num_processes for key, total in totals.items()}
        file.write(f"\nWT={averages['wait_time']:.1f}; CT={averages['completion_time']:.1f}; "
                   f"RT={averages['response_time']:.1f}; TAT={averages['turnaround_time']:.1f};\n")


#Funcion para recibir el nombre del archivo de texto
def get_input_file():
    return input("Ingrese el archivo de texto: ")

#Definicion del Main
if __name__ == "__main__":
    mlq_scheduler = MLQScheduler() #Creo un objeto MLQ_scheduler
    # Creo y añado las Queue con sus atributos
    mlq_scheduler.add_queue(Queue('RR', quantum=3)) 
    mlq_scheduler.add_queue(Queue('RR', quantum=5))
    mlq_scheduler.add_queue(Queue('FCFS'))

    input_file= get_input_file()
    processes = read_input_file(input_file)

    #Se añaden los process a las Queues
    for process in processes:
        if process.queue == 1:
            mlq_scheduler.queues[0].add_process(process)
        elif process.queue == 2:
            mlq_scheduler.queues[1].add_process(process)
        elif process.queue == 3:
            mlq_scheduler.queues[2].add_process(process)

   
    mlq_scheduler.schedule() #Ejecuto al organizador
    out_file(processes, 'salida.txt') #Se genera el archivo de salida
