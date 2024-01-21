import subprocess
import json
import os
import clipboard as pc

SO = input("Windows(w) / Linux(l) --> ")

def borrar_pantalla():
    os.system("cls" if SO == "w" else "clear")

url = "https://fastapitest-mjo6.onrender.com/todolist"

delete_command = f"curl -s -X DELETE \
  {url}/borrar/all \
  -H accept:application/json"

get_command = f"curl -s {url}"

salir = False
while not salir:
    borrar_pantalla()
    print("##CLIENTE TODO##")
    i = 0
    for opcion in ["obtener", "crear", "eliminarall", "eliminar item","copiar"]:
        print(f"{i} - {opcion}")
        i += 1
    print()
    op = input("elija una operacion: ")
    try:
        if op not in "01234":
            raise ValueError("opcion invalida")
        operation = { "0" : get_command, "2" : delete_command}
        if op == "1":
            print()
            print("## CREAR ITEM ##")
            mensaje = input("mensaje: ")
            json_data = json.dumps({"mensaje": mensaje}).replace('"', '\\"')
            post_command = f'curl -s -X POST {url} -H "accept:application/json" -H "Content-Type:application/json" -d "{json_data}"'
            operation["1"] = post_command
            r = subprocess.check_output(post_command, shell=True, text=True)
            result = json.loads(r)
            print(result["status"])
        elif op == "0":
            r = subprocess.check_output(operation["0"], shell=True, text=True)
            result = json.loads(r)
            i = 0
            print()
            print("## ITEMS ##")
            for item in result["data"][0]["data"]:
                print(f"{item}")
                i+=1
            print()
        elif op == "3":
            print()
            print("## ELIMINAR UN ITEM ##") 
            r = subprocess.check_output(operation["0"], shell=True, text=True)
            result = json.loads(r)
            i = 0
            for item in result["data"][0]["data"]:
                print(f"{i} - {item}")
                i+=1
            print()
            borrar = input("elija opcion para borrar: ")
            print(f"la opcion que eligio fue {result['data'][0]['data'][int(borrar)]}")
            target = result['data'][0]['data'][int(borrar)].replace(" ","%20")
            delete_item_command = f'curl -s -X DELETE {url}/{target} -H "accept:application/json"'
            r = subprocess.check_output(delete_item_command, shell=True, text=True)
            result = json.loads(r)
        elif op == "4":
            r = subprocess.check_output(operation["0"], shell=True, text=True)
            result = json.loads(r)
            i = 0
            print()
            print("## QUE ITEM QUIERE COPIAR ##")
            print()
            for item in result["data"][0]["data"]:
                print(f"{i} - {item}")
                i+=1
            print()
            copiar = input("opcion -> ")
            pc.copy( result['data'][0]['data'][int(copiar)])
            print(f"Se ha copiado [ {result['data'][0]['data'][int(copiar)]} ] al portapapeles")
            print()
        elif op == "2":
            r = subprocess.check_output(delete_command, shell=True, text=True)
            result = json.loads(r)
            print(result)
        else:
            pass
        
        print()
        salir = input("###### SALIR(1) ######" ) == "1"
        print()
    except subprocess.CalledProcessError as e:
        print("Error al ejecutar curl:", e)
    except IndexError as e:
        print("error", e)
        salir = True
    except ValueError as e:
        print("error",e)
        salir = True
