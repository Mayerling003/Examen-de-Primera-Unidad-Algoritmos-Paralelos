import threading,multiprocessing
from collections import Counter
import time
contador_sec=Counter()
lock=threading.Lock()
resultados_sec=[]
lineas_totales=100000
def busqueda_paralela(coordenada,inicio,fin,resultados_compartidos):
    with open("posiciones.txt","r") as f:
        for idx,linea in enumerate(f):
            if idx<inicio:continue
            if idx>=fin:break
            puntos=linea.strip().split(' ')
            for punto in puntos:
                coords=punto.strip().split(',')
                try:
                    x=round(float(coords[0]),2)
                    y=round(float(coords[1]),2)
                    x_buscar=round(float(coordenada[0]),2)
                    y_buscar=round(float(coordenada[1]),2)
                    if x==x_buscar and y==y_buscar:
                        with lock:
                            resultados_compartidos.append({"linea":idx,"x":coords[0],"y":coords[1]})
                except (ValueError,IndexError):continue
def contar_frecuencias_paralelo(inicio,fin,frecuencias_compartidas):
    with open("posiciones.txt","r") as f:
        for idx,linea in enumerate(f):
            if idx<inicio:continue
            if idx>=fin:break
            puntos=linea.strip().split(' ')
            for punto in puntos:
                coords=punto.strip().split(',')
                try:
                    x=round(float(coords[0]),2)
                    y=round(float(coords[1]),2)
                    with lock:
                        frecuencias_compartidas[(x,y)]=frecuencias_compartidas.get((x,y),0)+1
                except (ValueError,IndexError):continue
def busqueda_secuencial(coordenada):
    with open("posiciones.txt","r") as f:
        for idx,linea in enumerate(f):
            puntos=linea.strip().split(' ')
            for punto in puntos:
                coords=punto.strip().split(',')
                try:
                    x=round(float(coords[0]),2)
                    y=round(float(coords[1]),2)
                    x_buscar=round(float(coordenada[0]),2)
                    y_buscar=round(float(coordenada[1]),2)
                    if x==x_buscar and y==y_buscar:
                        resultados_sec.append({"linea":idx,"x":coords[0],"y":coords[1]})
                except (ValueError,IndexError):continue
def contar_frecuencias_secuencial():
    with open("posiciones.txt","r") as f:
        for linea in f:
            puntos=linea.strip().split(' ')
            for punto in puntos:
                coords=punto.strip().split(',')
                try:
                    x=round(float(coords[0]),2)
                    y=round(float(coords[1]),2)
                    contador_sec[(x,y)]+=1
                except (ValueError,IndexError):continue
def ejecutar():
    coordenada_objetivo=[]
    coordenada_objetivo.append(float(input("Introduce la posición X: ")))
    coordenada_objetivo.append(float(input("Introduce la posición Y: ")))
    num_procesos=4
    rango_por_proceso=lineas_totales//num_procesos
    procesos=[]
    manager=multiprocessing.Manager()
    frecuencias_paralelas=manager.dict()
    resultados_paralelos=manager.list()
    tiempo_inicio_paralelo=time.time()
    for i in range(num_procesos):
        inicio=i*rango_por_proceso
        fin=(i+1)*rango_por_proceso
        p_busqueda=multiprocessing.Process(target=busqueda_paralela,args=(coordenada_objetivo,inicio,fin,resultados_paralelos))
        p_frecuencias=multiprocessing.Process(target=contar_frecuencias_paralelo,args=(inicio,fin,frecuencias_paralelas))
        procesos.extend([p_busqueda,p_frecuencias])
        p_busqueda.start()
        p_frecuencias.start()
    for p in procesos:p.join()
    tiempo_fin_paralelo=time.time()
    tiempo_inicio_secuencial=time.time()
    busqueda_secuencial(coordenada_objetivo)
    contar_frecuencias_secuencial()
    tiempo_fin_secuencial=time.time()
    return (tiempo_fin_paralelo-tiempo_inicio_paralelo),(tiempo_fin_secuencial-tiempo_inicio_secuencial),resultados_paralelos,frecuencias_paralelas
if __name__=="__main__":
    tiempo_paralelo,tiempo_secuencial,resultados_paralelos,frecuencias_paralelas=ejecutar()
    print(f"Tiempo ejecución paralelo: {tiempo_paralelo:.4f} segundos")
    print("Resultados búsqueda paralela:")
    for r in list(resultados_paralelos):print(r)
    print("Top 10 coordenadas más frecuentes (paralelo):")
    for coord,cant in Counter(frecuencias_paralelas).most_common(10):print(f"Coordenada {coord} aparece {cant} veces.")
    print("="*30)
    print(f"Tiempo ejecución secuencial: {tiempo_secuencial:.4f} segundos")
    print("Resultados búsqueda secuencial:")
    for r in resultados_sec:print(r)
    print("Top 10 coordenadas más frecuentes (secuencial):")
    for coord,cant in contador_sec.most_common(10):print(f"Coordenada {coord} aparece {cant} veces.")
    print("="*30)

