import threading
import random
import os
import time

total_objetos=1000000
total_pasos=1000
num_hilos=4
archivo="posiciones.txt"
objetos_por_hilo=total_objetos//num_hilos
bloqueo=threading.Lock()
objetos=[]
for _ in range(total_objetos):
    objetos.append({"x":random.uniform(0,100),"y":random.uniform(0,100),"vx":random.uniform(-1,1),"vy":random.uniform(-1,1)})
def mover_objetos(desde,hasta,numero_hilo):
    for paso in range(1,total_pasos+1):
        lineas=[]
        for i in range(desde,hasta):
            objetos[i]["x"]+=objetos[i]["vx"]
            objetos[i]["y"]+=objetos[i]["vy"]
            x=objetos[i]["x"]
            y=objetos[i]["y"]
            texto=f"{x:.4f} {y:.4f}\n"
            lineas.append(texto)
        with bloqueo:
            with open(archivo,"a",encoding="utf-8") as f:
                f.write(f"Paso {paso} - Hilo {numero_hilo}\n")
                f.writelines(lineas)
def main():
    if os.path.exists(archivo): os.remove(archivo)
    hilos=[]
    for i in range(num_hilos):
        inicio=i*objetos_por_hilo
        fin=total_objetos if i==num_hilos-1 else (i+1)*objetos_por_hilo
        hilo=threading.Thread(target=mover_objetos,args=(inicio,fin,i))
        hilos.append(hilo)
        hilo.start()
    for hilo in hilos: hilo.join()
    print("Terminado")
if __name__=="__main__":
    inicio=time.time()
    main()
    fin=time.time()
    print(f"Tiempo total: {fin-inicio:.2f} segundos")
