﻿"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

import datetime
import time
import config as cf
import operator
import math
from DISClib.ADT import list as lt
from DISClib.Algorithms.Sorting import insertionsort as inser
from DISClib.Algorithms.Sorting import mergesort as ms
from DISClib.Algorithms.Sorting import quicksort as qs
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos
def newCatalog():
    """
    Inicializa el catálogo de libros. Crea una lista vacia para guardar
    todos los libros, adicionalmente, crea una lista vacia para los autores,
    una lista vacia para los generos y una lista vacia para la asociación
    generos y libros. Retorna el catalogo inicializado.
    """
    catalog = {'artists': None,
               'artworks': None,
               'nacionalidades': None,
              "Medium": None,
              "ConstituentID": None, 
              "artistMAP": None, 
              "DisplayName": None, 
              "Dates": None,
              "BeginDate": None, 
              "NationalityArtist": None, 
              "NationalityArtworks": None, 
              "Department": None}

    TipoDeLista= input('¿Cómo desea guardar el catálogo del museo?(ll = Linked_list, al = Array_List))  ')
    if TipoDeLista == 'll':
        catalog['artists'] = lt.newList('SINGLE_LINKED', cmpfunction=compareartist)
        catalog['artworks'] = lt.newList('SINGLE_LINKED', cmpfunction=compareartworks)
    elif TipoDeLista == 'al':
        catalog['artists'] = lt.newList('ARRAY_LIST', cmpfunction=compareartist)
        catalog['artworks'] = lt.newList('ARRAY_LIST', cmpfunction=compareartworks)
    catalog['nacionalidades']=lt.newList('ARRAY_LIST')
    catalog['Medium'] = mp.newMap(10000,
                                   maptype='PROBING',
                                   loadfactor=0.5,
                                   comparefunction=compareartworksmediumMAP)
    catalog["ConstituentID"] = mp.newMap(10000,
                                   maptype='PROBING',
                                   loadfactor=0.5,
                                   comparefunction=compareartworksConstituentIDMAP)
    catalog["DisplayName"] = mp.newMap(10000,
                                   maptype='PROBING',
                                   loadfactor=0.5,
                                   comparefunction=compareartistMAP)
    catalog["BeginDate"] = mp.newMap(10000,
                                   maptype='PROBING',
                                   loadfactor=0.5,
                                   comparefunction=compareartistMAP)
    catalog["NationalityArtist"] = mp.newMap(10000,
                                   maptype='PROBING',
                                   loadfactor=0.5,
                                   comparefunction=compareartistMAP)
    catalog["Dates"] = mp.newMap(5000,
                                   maptype='PROBING',
                                   loadfactor=0.5,
                                   comparefunction=compareartistMAP)
    catalog["NationalityArtworks"] = mp.newMap(10000,
                                   maptype='PROBING',
                                   loadfactor=0.5,
                                   comparefunction=compareartworksConstituentIDMAP)
    catalog["Department"] = mp.newMap(10000,
                                   maptype='CHAINING',
                                   loadfactor=4.0,
                                   comparefunction=compareartworksConstituentIDMAP)
    
    return catalog


def addArtwork(catalog, artwork):
    # Se adiciona el libro a la lista de libros
    lt.addLast(catalog['artworks'], artwork)
    AddNacionalidadesObras(catalog, artwork)
    addArtworkMedium(catalog, artwork)
    addArtworkConstituentID(catalog, artwork)
    addArtworkNationality(catalog, artwork)
    addArtworkDepartment(catalog, artwork)
    addArtworkDates(catalog, artwork)
    #Prueba de que guarda


def addArtist(catalog, artist):
    lt.addLast(catalog['artists'], artist)
    mp.put(catalog["DisplayName"], artist["DisplayName"], artist["ConstituentID"])
    if artist["Nationality"] != "" and artist["Nationality"] != " ":
        mp.put(catalog["NationalityArtist"], artist["ConstituentID"], artist["Nationality"])
    addArtistBeginDate(catalog, artist)

def getLast3Artists(catalog):
    artists = catalog['artists']
    sublista = lt.subList(artists, (len(artists))-3, 3)
    return sublista


def lastThreeArtworks(catalog):
    artworks = catalog['artworks']
    sublista = lt.subList(artworks, (len(artworks))-3, 3)
    return sublista

def addArtworkDepartment(catalog, artwork):
    try:
        deptos = catalog["Department"]
        depto = artwork["Department"]
        existDepto = mp.contains(deptos, depto)
        if existDepto:
            entry = mp.get(deptos, depto)
            dicc_depto = me.getValue(entry)
        else:
            dicc_depto = newDepto(depto)
            mp.put(deptos, depto, dicc_depto)
        lt.addLast(dicc_depto["obras"], artwork)
    except Exception:
        return None

def newDepto(depto):
    dicc = {"depto":"", "obras": None}
    dicc["depto"] = depto
    dicc["obras"] = lt.newList('ARRAY_LIST', cmpfunction=compareartist)
    return dicc


def addArtistBeginDate(catalog, artist):
    try:
        dates = catalog["BeginDate"]
        if artist["BeginDate"] != "" and artist["BeginDate"] != "":
            fecha = artist["BeginDate"]
            existFecha = mp.contains(dates, fecha)
            if existFecha:
                entry = mp.get(dates, fecha)
                dicc_fecha = me.getValue(entry)
            else:
                dicc_fecha = newFecha(fecha)
                mp.put(dates, fecha, dicc_fecha)
            lt.addLast(dicc_fecha["artistas"], artist)
    except Exception:
        return None

def newFecha(fecha):
    dicc = {"fecha":"", "artistas": None}
    dicc["fecha"] = fecha
    dicc["artistas"] = lt.newList('ARRAY_LIST', cmpfunction=compareartist)
    return dicc

def addArtworkConstituentID(catalog, artwork):
    try:
        ids = catalog["ConstituentID"]
        cadena = artwork["ConstituentID"]
        cadena = cadena.replace("[","")
        cadena = cadena.replace("]","") 
        lista = cadena.split(",")
        for id in lista:
            existID = mp.contains(ids, id)
            if existID:
                entry = mp.get(ids, id)
                dicc_ids = me.getValue(entry)
            else:
                dicc_ids = newID(id)
                mp.put(ids, id, dicc_ids)
            lt.addLast(dicc_ids["obras"], artwork)    
            
    except Exception:
        return None
def addArtworkDates(catalog,artwork):
    try:
        fechas=catalog["Dates"]
        if artwork["DateAcquired"] != "":
            fecha=artwork["DateAcquired"]
        else:
            fecha=""
        existe= mp.contains(fechas,fecha)
        if existe:
            entrada= mp.get(fechas, fecha)
            fecha_nueva= me.getValue(entrada)
        else:
            fecha_nueva=nuevaFecha(fecha)
            mp.put(fechas,fecha,fecha_nueva)
        lt.addLast(fecha_nueva["artworks"], artwork)
        medioDeAdq= artwork["CreditLine"].lower()
        if "purchase" in medioDeAdq:
            fecha_nueva["comprado"]+=1
    except Exception:
        return None


def nuevaFecha(fecha):
    entrada= {"fecha":'',"artworks":None,"comprado":0 }
    entrada["fecha"]=fecha
    entrada["artworks"]= lt.newList('ARRAY_LIST')
    return entrada



def newID(id):
    dicc = {"id": "", "obras": None}
    dicc["id"] = id
    dicc["obras"] = lt.newList(cmpfunction=compareartworks)
    return dicc

# Funciones para creacion de datos

# Funciones de consulta

# Funciones utilizadas para comparar elementos dentro de una lista
def cmpArtworkByDateAcquired(artwork1, artwork2):
    """
    Devuelve verdadero (True) si el 'DateAcquired' de artwork1 es menores que el de artwork2
    :
    artwork1: informacion de la primera obra que incluye su valor 'DateAcquired'
    artwork2: informacion de la segunda obra que incluye su valor 'DateAcquired'
    """

    try:
        fecha1 = artwork1['DateAcquired'].split('-')
    except:
        fecha1 = artwork1.split('-')

    fecha2 = artwork2['DateAcquired'].split('-')

    if fecha1 == [""]:
        fecha1=["3000","00","00"]
    if fecha2 == [""]:
        fecha2=["3000","00","00"]

    resultado = True

    if fecha1[0] > fecha2[0]:
        resultado = False
    elif fecha1[0] == fecha2[0]:
        if fecha1[1] > fecha2[1]:
            resultado = False
        elif fecha1[1] == fecha2[1]:
            if fecha1[2] > fecha2[2]:
                resultado = False
    
    return(resultado)
    
def cmpNacionalidadesPorRanking(pais1, pais2):

    result = pais1['numero_de_obras'] > pais2['numero_de_obras']
    return result


def compareartist(artistname1, artist):
    if artistname1['ConstituentID'] > artist['ConstituentID']:
        return 1
    elif artistname1['ConstituentID'] == artist['ConstituentID']:
        return 0
    else:
        return -1

def compareartworks(artworkname1,artwork):
    if artworkname1['ObjectID'] > artwork['ObjectID']:
        return 1
    elif artworkname1['ObjectID'] == artwork['ObjectID']:
        return 0
    else:
        return -1

def compareartworksmedium(artwork1,artwork2):
    if artwork1['Medium'] > artwork2['Medium']:
        return 1
    elif artwork1['Medium'] == artwork2['Medium']:
        return 0
    else:
        return -1

def compareartworksmediumMAP(medio, entry):
    medEntry = me.getKey(entry)
    if medio > medEntry:
        return 1
    elif medEntry == medio:
        return 0
    else:
        return -1

def compareartworksConstituentIDMAP(id, entry):
    idEntry = me.getKey(entry)
    if id > idEntry:
        return 1
    elif id == idEntry:
        return 0
    else:
        return -1
def compareartistMAP(keyname, artist):
    artistEntry = me.getKey(artist)
    if (keyname == artistEntry):
        return 0
    elif (keyname > artistEntry):
        return 1
    else:
        return -1

def compareartistBeginDateMAP(artista, entry):
    artistEntry = me.getKey(entry)
    if artista > artistEntry:
        return 1
    elif artistEntry == artista:
        return 0
    else:
        return -1
        
def compareartworkdepartment(artwork1,artwork2):
    if artwork1['Department'] > artwork2['Department']:
        return 1
    elif artwork1['Department'] == artwork2['Department']:
        return 0
    else:
        return -1

def compareArtistsYearBorn(artist1, artist2):
    a = int(artist1["BeginDate"])
    b = int(artist2["BeginDate"])
    if a < b:
        return 1
    else:
        return 0
def compareArtistsYearBornSimple(year1, year2):
    a = int(year1)
    b = int(year2)
    if a < b:
        return 1
    else:
        return 0

def compareCosto(artist1, artist2):
    a = int(artist1["costo"])
    b = int(artist2["costo"])
    if a > b:
        return 1
    else:
        return 0

def compareDate(artwork1, artwork2):
    if artwork1["Date"] == "":
        a = 0
    else:
        a = int(artwork1["Date"])
    if artwork2["Date"] == "":
        b = 0
    else: 
        b = int(artwork2["Date"])
    if a < b:
        return 1
    else:
        return 0
    """a = int(artist1["BeginDate"])
    b = int(artist2["BeginDate"])
    if a > b:
        return 1
    elif a == b:
        return 0
    else:
        return -1"""

# Funciones de ordenamiento

def sortArtworksDateAcquired(catalog, anio1, anio2, mes1, mes2, dia1, dia2):
    sublist  =  lt.newList(cmpfunction=compareartworks)
    strdateArt1=None
    obras =catalog["artworks"]
    dateArt1=datetime.datetime(int(anio1),int(mes1),int(dia1))
    dateArt2=datetime.datetime(int(anio2),int(mes2),int(dia2))
    for artwork in lt.iterator(obras):
        strdateArt1 = artwork['DateAcquired']
        if len(strdateArt1) == 0:
            year=1
            month=1
            day=1
        else:
            year=int(strdateArt1[0]+strdateArt1[1]+strdateArt1[2]+strdateArt1[3])
            month= int(strdateArt1[5]+strdateArt1[6])
            day= int(strdateArt1[8]+strdateArt1[9])
        dateArt3=datetime.datetime(year,month,day)
        if (dateArt3>= dateArt1) and (dateArt3<= dateArt2):
            lt.addLast(sublist, artwork)
                     
    sub_list = sublist.copy()
    start_time = time.process_time()
    sorted_list = ms.sort(sub_list, cmpArtworkByDateAcquired)
    stop_time = time.process_time()

    purchaseList = lt.newList(cmpfunction=compareartworks)
    for artwork in lt.iterator(sorted_list):
        if "Purchase" in artwork["CreditLine"]:
            lt.addLast(purchaseList, artwork)
    listFirst3 = sorted_list.copy()
    if len(listFirst3)>2:
        first3= lt.subList(listFirst3,0,3)
        last3 = lt.subList(listFirst3, len(listFirst3)-3, 3)
    else:
        first3= lt.subList(listFirst3)
        last3 = lt.subList(listFirst3)                  
                      
    numPurchase = len(purchaseList)
    num = len(sorted_list)
    elapsed_time_mseg = (stop_time - start_time)*1000
    return elapsed_time_mseg, num, numPurchase, first3, last3

#Funciones para requerimiento 2 reto 2
def getObrasEnRangoDeFechas(catalog, fecha1, fecha2):
    mapa_fechas= catalog['Dates']
    llaves_fechas= mp.keySet(mapa_fechas)
    compradas=0
    obras_en_rango=lt.newList(datastructure= "ARRAY_LIST")
    for fecha in lt.iterator(llaves_fechas):
        entrada = mp.get(mapa_fechas, fecha)
        pos_fecha= me.getValue(entrada)
        if pos_fecha != None:
            if (cmpArtworkByDateAcquired(pos_fecha['fecha'],fecha2)) and not (cmpArtworkByDateAcquired(pos_fecha['fecha'],fecha1)):
                compradas += pos_fecha['comprado']
                artistas_en_fecha= pos_fecha['artworks']
                for artwork in lt.iterator(artistas_en_fecha):
                    lt.addLast(obras_en_rango, artwork)   
    return obras_en_rango, compradas

def ordenarobras(obras_en_rango):
    sublista=lt.subList(obras_en_rango,1,lt.size(obras_en_rango))
    sublista=sublista.copy()
    start_time = time.process_time()
    sorted_list = ms.sort(sublista, cmpArtworkByDateAcquired)
    stop_time = time.process_time()
    time_ms=(stop_time - start_time)*1000
    return time_ms, sorted_list

#Funciones para requerimiento 3

def buscar_artista_constituentID(catalog, nombre):
    artistas = catalog["artists"]
    for artist in lt.iterator(artistas):
        if (str(nombre)) == (str(artist["DisplayName"])):
            return artist["ConstituentID"]
#LISTOOOOOO

def total_obras(catalog, nombre):
    id = buscar_artista_constituentID(catalog, nombre)
    obras = catalog["artworks"]
    contador = 0
    for obra in lt.iterator(obras):
        cadena = obra["ConstituentID"]
        cadena = cadena.replace("[","")
        cadena = cadena.replace("]","") 
        lista = cadena.split(",")
        for numero in lista:
            if str(id) == numero:
                contador += 1
    return contador
#LISTOOOOO

def lista_total_tecnicas(catalog, nombre):
    id = buscar_artista_constituentID(catalog, nombre)
    obras = catalog["artworks"]
    lista = lt.newList('ARRAY_LIST', cmpfunction=compareartworks)
    for obra in lt.iterator(obras):
        cadena = obra["ConstituentID"]
        cadena = cadena.replace("[","")
        cadena = cadena.replace("]","") 
        lista_nueva = cadena.split(",")
        for numero in lista_nueva:
            if str(id) == numero:
                lt.addLast(lista, obra)
    return lista, lt.size(lista)
#LISTOOOOOOO

def tecnica_mas_utilizada(lista):
    #ordenar por medio
    ms.sort(lista, compareartworksmedium)
    maxima = ""
    contadorM = -1
    actual = 0
    x = lt.getElement(lista, 1)
    actualO = x["Medium"]
    tecnicas = 1
    #revisar medio por medio con 4 variables: actual, contador actual, maximo, contador maximo
    for obra in lt.iterator(lista):
        if obra["Medium"] == actualO:
            actual += 1
            actualO = obra["Medium"]
        else:
            tecnicas += 1
            if actual>contadorM:
                maxima = actualO
                contadorM = actual
            actual = 1
            actualO = obra["Medium"]
    if actual>contadorM:
        maxima = actualO
        contadorM = actual
    return maxima, tecnicas
#LISTOOOOOO

def lista_tecnicas_mas_usadas(lista, tecnica):
    x = lt.newList(cmpfunction=compareartworks)
    for obra in lt.iterator(lista):
        if obra["Medium"] == tecnica:
            lt.addLast(x, obra)
    return x
#LISTOOOOOO

#Req 3 RETO 2

def total_obrasMAP(catalog, nombre):
    pareja = mp.get(catalog["DisplayName"], nombre)
    id = me.getValue(pareja)
    pareja_obras = mp.get(catalog["ConstituentID"], id)
    lista = me.getValue(pareja_obras)["obras"]
    return lista

def total_tecnicasMAP(lista):
    size = lt.size(lista)
    mapa = mp.newMap(comparefunction=compareartworksmediumMAP)
    for artwork in lt.iterator(lista):
        if artwork["Medium"] != "":
            medio = artwork["Medium"]
            existMedium = mp.contains(mapa, medio)
            if existMedium:
                entry = mp.get(mapa, medio)
                dicc_medio = me.getValue(entry)
            else:
                dicc_medio = newMedio(medio)
                mp.put(mapa, medio, dicc_medio)
            lt.addLast(dicc_medio["obras"], artwork)
    llaves = mp.keySet(mapa)
    tamaño = lt.size(llaves)
    maximo = 0
    mayor = ""
    for key in lt.iterator(llaves):
        entry = mp.get(mapa, key)
        lista1 = me.getValue(entry)["obras"]
        tamano = lt.size(lista1)
        if tamano > maximo:
            maximo = tamano
            mayor = key
    lista_final = mp.get(mapa, mayor)
    lista_final1 = me.getValue(lista_final)["obras"]
    tamanio = lt.size(lista_final1)
    return tamaño, size, mayor, lista_final1, tamanio









# Funciones req4
def NacionalidadNueva(nacionalidad):
    pais={'Pais':'',
          'Obra':None ,
          'NumeroDeObras':0}
    pais['Pais']=nacionalidad
    pais['Obra']=lt.newList('ARRAY_LIST')
    return pais

def AddNacionalidadesObras(catalog, artwork):
    ArtistasDeObras= artwork['ConstituentID']

    ListaIDs=ArtistasDeObras.strip("[]").split(", ")
    numArtistasObra=len(ListaIDs)
    ListaArtistas= lt.newList('ARRAY_LIST')
    cuenta = 0
    artistas=catalog['artists']
    for artista in lt.iterator(artistas):
        if artista['ConstituentID'] in ListaIDs:
          lt.addLast(ListaArtistas,artista)  
          cuenta+=1
        if cuenta == numArtistasObra:
            break
    for artista in lt.iterator(ListaArtistas):
        AddNuevaNacionalidad(catalog,artwork,artista)




def AddNuevaNacionalidad(catalog, artwork, artist):
    nacionalidad = artist['Nationality']
    if nacionalidad=="" or nacionalidad=="Nationality unknown":
        nacionalidad="N/A"
    nacionalidades= catalog['nacionalidades']
    existe=False
    for pais in lt.iterator(nacionalidades):
        nombre=pais['Pais']
        if nombre == nacionalidad:
            lt.addLast(pais['Obra'],artwork)
            pais['NumeroDeObras']+=1
            existe=True
    if existe==False:
        nuevopais= NacionalidadNueva(nacionalidad)
        nuevaobra= nuevopais['Obra']
        lt.addLast(nuevaobra,artwork)
        nuevopais['NumeroDeObras']+=1
        existe=True
        lt.addLast(nacionalidades,nuevopais)

def ordenarpaises(nacionalidades):
    sublista=lt.subList(nacionalidades,1,lt.size(nacionalidades))
    sublista=sublista.copy()
    start_time = time.process_time()
    sorted_list = ms.sort(sublista, cmpNacionalidadesPorRanking)
    stop_time = time.process_time()
    time_ms=(stop_time - start_time)*1000
    Rankingtop10 = lt.subList(sorted_list, 1, 10)
    return time_ms, Rankingtop10

#Req 4 Reto 2
def addArtworkNationality(catalog, artwork):
    try:
        cadena = artwork["ConstituentID"]
        cadena = cadena.replace("[","")
        cadena = cadena.replace("]","") 
        lista = cadena.split(",")
        mapa = catalog["NationalityArtworks"]
        for numero in lista:
            entry = mp.get(catalog["NationalityArtist"], numero)
            nationality = me.getValue(entry)
            if (nationality == ''):
                nationality = 'Nationality unknown'
            existArtwork = mp.contains(mapa, nationality)
            if existArtwork:
                entry1 = mp.get(mapa, nationality)
                dicc_nacion = me.getValue(entry1)
            else:
                dicc_nacion = newNacion(nationality)
                mp.put(mapa, nationality, dicc_nacion)
            lt.addLast(dicc_nacion["obras"], artwork)
            dicc_nacion['numero_de_obras'] +=1
    except Exception:
        return None

def newNacion(nationality):
    dicc = {"nacionalidad": "", "obras": None, "numero_de_obras":0}
    dicc["nacionalidad"] = nationality
    dicc["obras"] = lt.newList('ARRAY_LIST', cmpfunction=compareartworks)
    return dicc

def ObrasPorNacionalidad(catalog, nacionalidad):
    nacion = mp.get(catalog["NationalityArtworks"], nacionalidad)
    if nacion:
        lista =  me.getValue(nacion)["obras"]
        size = lt.size(lista)
        return size
    return "La nacionalidad no existe"

#función principal req 4 reto 2 
def getObrasPorNacionalidad(catalog):
    mapa = catalog['NationalityArtworks']
    llaves = mp.keySet(mapa)
    lista= lt.newList("ARRAY_LIST")

    for nacionalidad in lt.iterator(llaves):
        entry = mp.get(mapa, nacionalidad)
        pos_nacionalidad = me.getValue(entry)
        if pos_nacionalidad != None:
            lt.addLast(lista, pos_nacionalidad)
    
    result = ordenarpaises(lista)
    return result
    
    

    


#Funciones para requerimiento 1
def sublistaRangoArtistas(catalog, year1, year2):
    artistas = catalog["artists"]
    artistas = ms.sort(artistas, compareArtistsYearBorn)
    sublist = lt.newList(cmpfunction=compareartist)
    for artist in lt.iterator(artistas):
        year = int(artist["BeginDate"])
        if year !=0:   
            if year >= year1 and year <= year2:
                lt.addLast(sublist, artist)
    return sublist, lt.size(sublist)


def ArtistasNacimientoPrimeros3(lista):
    sublista = lt.subList(lista, 1, 3)
    return sublista

def ArtistasNacimientoUltimos3(lista):
    sublista = lt.subList(lista, lt.size(lista)-2, 3)
    return sublista

#Req 1 Reto 2
def addArtistBeginDate(catalog, artist):
    try:
        dates = catalog["BeginDate"]
        if artist["BeginDate"] != "" and artist["BeginDate"] != "":
            fecha = artist["BeginDate"]
            existFecha = mp.contains(dates, fecha)
            if existFecha:
                entry = mp.get(dates, fecha)
                dicc_fecha = me.getValue(entry)
            else:
                dicc_fecha = newFecha(fecha)
                mp.put(dates, fecha, dicc_fecha)
            lt.addLast(dicc_fecha["artistas"], artist)
    except Exception:
        return None

def BeginDateInRange(catalog, year1, year2):
    lista_fechas = mp.keySet(catalog["BeginDate"])
    fechas_ordenadas = ms.sort(lista_fechas, compareArtistsYearBornSimple)
    sublist = lt.newList(cmpfunction=compareartist)
    for fecha in lt.iterator(fechas_ordenadas):
        if fecha != "0" and fecha != 0:
            if int(fecha)>=year1 and int(fecha)<=year2:
                entry = mp.get(catalog["BeginDate"], fecha)
                lista_artistas = me.getValue(entry)["artistas"] 
                for artista in lt.iterator(lista_artistas):
                    lt.addLast(sublist, artista)
    return sublist, lt.size(sublist)    
# Req 3 Reto 2

def sublistaRangoArtistasMAP(catalog, year1, year2):
    llaves = mp.keySet(catalog["BeginDate"])


#Funciones para requerimiento 5

def ListaPorDepto(catalog, depto):
    obras = catalog["artworks"]
    obras_ordenadas =ms.sort(obras, compareartworkdepartment)
    sublist = lt.newList(cmpfunction=compareartworks)
    for obra in lt.iterator(obras_ordenadas):
        if obra["Department"] == depto:
            lt.addLast(sublist, obra)
    #La siguiente parte fue usada para analizar los casos posibles al momento de calcular volumenes y areas. Ignorar :).
    """for x in lt.iterator(obras_ordenadas):
        if x["Depth (cm)"] == "":
            respuesta = "NO"
        else:
            respuesta = x["Depth (cm)"]
        if x["Diameter (cm)"] == "":
            y = "NO"
        else: 
            y = x["Diameter (cm)"]
        if x["Height (cm)"] == "":
            z = "NO"
        else: 
            z = x["Height (cm)"]
        if x["Length (cm)"] == "":
            a = "NO"
        else: 
            a = x["Length (cm)"]

        if x["Width (cm)"] == "":
            b = "NO"
        else: 
            b = x["Width (cm)"]
        print("Profundidad: " +respuesta + "---Diametro: "+ y + "---Height: " + z+ "---Length: "+a+"---Width (cm): "+b)"""

    return sublist, lt.size(sublist)

def CalcularCostoEnvioObra(obra):
    final = 0
    peso = 0
    if obra["Weight (kg)"] !="":
        peso = float(obra["Weight (kg)"])
    costo_k = peso*72.00
    costo = 48.00
    #Cuando se tiene diametro
    if obra["Diameter (cm)"] != "0" and obra["Diameter (cm)"] != "":
        diametro = float(obra["Diameter (cm)"])
        #Diametro con altura, como un cilindro
        if obra["Height (cm)"] != "0" and obra["Height (cm)"] != "": 
            altura = float(obra["Height (cm)"])
            volumen = (2*math.pi*((diametro/2)**2))*(altura)
            costo = (9/125000)*volumen
            #(72usd/m^3 es equivalente a (9/125000)/cm^3)
        #Diametro solo, entonces círculo
        else:
            area = (2*math.pi*((diametro/2)**2))
            costo = (9/1250)*area
            #(72usd/m^2 es equivalente a (9/1250)/cm^2)
    else:
        #Hay Profundidad, volumen
        if obra["Depth (cm)"] != "0" and obra["Depth (cm)"] != "":
            profundidad = float(obra["Depth (cm)"])
            if obra["Height (cm)"] != "0" and obra["Height (cm)"] != "":
                height = float(obra["Height (cm)"])
            if obra["Length (cm)"] != "0" and obra["Length (cm)"] != "":
                length = float(obra["Length (cm)"])
            if obra["Width (cm)"] != "0" and obra["Width (cm)"] != "":
                width = float(obra["Width (cm)"])
            #Caso 1: Se se tiene height y length, pero no width
            if (obra["Height (cm)"] != "0" and obra["Height (cm)"] != "") and (obra["Length (cm)"] != "0" and obra["Length (cm)"] != "") and (obra["Width (cm)"] == "0" or obra["Width (cm)"] == ""):
                volumen = profundidad*height*length
                costo = (9/125000)*volumen
            #Caso 2: Si se tiene height y width, pero no length
            elif (obra["Height (cm)"] != "0" and obra["Height (cm)"] != "") and (obra["Length (cm)"] == "0" or obra["Length (cm)"] == "") and (obra["Width (cm)"] != "0" and obra["Width (cm)"] != ""):
                volumen = profundidad*height*width
                costo = (9/125000)*volumen
            #Caso 3: Si se tiene length y width, pero no height
            elif (obra["Height (cm)"] == "0" or obra["Height (cm)"] == "") and (obra["Length (cm)"] != "0" and obra["Length (cm)"] != "") and (obra["Width (cm)"] != "0" and obra["Width (cm)"] != ""):
                volumen = profundidad*length*width
                costo = (9/125000)*volumen
        #No hay profundidad, solo área
        else:
            if obra["Height (cm)"] != "0" and obra["Height (cm)"] != "":
                height = float(obra["Height (cm)"])
            if obra["Length (cm)"] != "0" and obra["Length (cm)"] != "":
                length = float(obra["Length (cm)"])
            if obra["Width (cm)"] != "0" and obra["Width (cm)"] != "":
                width = float(obra["Width (cm)"])
            #Caso 1: Se se tiene height y length, pero no width
            if (obra["Height (cm)"] != "0" and obra["Height (cm)"] != "") and (obra["Length (cm)"] != "0" and obra["Length (cm)"] != "") and (obra["Width (cm)"] == "0" or obra["Width (cm)"] == ""):
                area = height*length
                costo = (9/1250)*area
            #Caso 2: Si se tiene height y width, pero no length
            elif (obra["Height (cm)"] != "0" and obra["Height (cm)"] != "") and (obra["Length (cm)"] == "0" or obra["Length (cm)"] == "") and (obra["Width (cm)"] != "0" and obra["Width (cm)"] != ""):
                area = height*width
                costo = (9/1250)*area
            #Caso 3: Si se tiene length y width, pero no height
            elif (obra["Height (cm)"] == "0" or obra["Height (cm)"] == "") and (obra["Length (cm)"] != "0" and obra["Length (cm)"] != "") and (obra["Width (cm)"] != "0" and obra["Width (cm)"] != ""):
                area = length*width
                costo = (9/1250)*area
    if costo > costo_k:
        final = costo
    else:
        final = costo_k
    return final, peso
    
def CostoTodasObras(lista):
    costo = 0
    costo_total = 0
    peso_total = 0
    for obra in lt.iterator(lista):
       resultado = CalcularCostoEnvioObra(obra)
       costo = resultado[0]
       peso = resultado[1]
       peso_total += peso
       costo_total += costo
       obra["costo"] = costo
    lista_costo = lista.copy()
    return costo_total, peso_total, lista_costo

def ObrasMasAntiguas(lista):
    SinVacio = lt.newList(cmpfunction=compareartworks)
    lista_ord = ms.sort(lista, compareDate)
    for obra in lt.iterator(lista_ord):
        if obra["Date"] != "":
            lt.addLast(SinVacio, obra)
    top_5_antiguas = lt.subList(SinVacio, 1, 5)
    return(top_5_antiguas)

def ObrasMasCaras(lista):
    lista_ord = ms.sort(lista, compareCosto)
    top_5_caras = lt.subList(lista_ord, 1, 5)
    return top_5_caras

def ArtistaEnObra(catalog, obra):
    nombres = ""
    artistas = catalog["artists"]
    cadena = obra["ConstituentID"]
    cadena = cadena.replace("[","")
    cadena = cadena.replace("]","") 
    lista_nueva = cadena.split(",")
    for id in lista_nueva:
        for artista in lt.iterator(artistas):
            if artista["ConstituentID"] == str(id):
                nombre = artista["DisplayName"]
                nombres += "(" + nombre +")"
    return nombres

#Req 5 Reto2
def ListaDelDeptoMAP(catalog, depto):
    entry = mp.get(catalog["Department"], depto)
    lista = me.getValue(entry)["obras"]
    return lista, lt.size(lista)

#Lab 5

def addArtworkMedium(catalog, artwork):
    try:
        mediums = catalog["Medium"]
        if artwork["Medium"] != "":
            medio = artwork["Medium"]
            existMedium = mp.contains(mediums, medio)
            if existMedium:
                entry = mp.get(mediums, medio)
                dicc_medio = me.getValue(entry)
            else:
                dicc_medio = newMedio(medio)
                mp.put(mediums, medio, dicc_medio)
            lt.addLast(dicc_medio["obras"], artwork)

    except Exception:   
        return None

def newMedio(medio):
    dicc = {"medio": "", "obras": None}
    dicc["medio"] = medio
    dicc["obras"] = lt.newList('ARRAY_LIST', cmpfunction=compareartworks)
    return dicc

"""def addArtworkMedium(catalog, artwork):
    try:
        mediums = catalog["Medium"]
        if (artwork["Medium"]!=""):
            medioArtwork = artwork["Medium"]
        else:
            pass
        existmedio = mp.contains(mediums, medioArtwork)
        if existmedio:
            entry = mp.get(mediums, medioArtwork)
            medium = me.getValue(entry)
            lt.addLast(medium, artwork)
        else:
            medium = lt.newList(datastructure="ARRAY_LIST")
            lt.addLast(medium, artwork)
            mp.put(mediums, medioArtwork, medium)
            #medium = newMedium(medioArtwork)
            #mp.put(mediums, medioArtwork, medium)
        
        #lt.addLast(medium["artworks"], artwork)
        #print(medium["artworks"])
    except Exception:
        return None"""

"""def newMedium(medioArtwork):
    entry = {"Medium": "", "artworks": None}
    entry["Medium"] = medioArtwork
    entry["artworks"] = lt.newList("SINGLE_LINKED", compareartworksmedium)
    return entry"""
        

def ObrasPorMedium(catalog, medium):
    medium = mp.get(catalog["Medium"], medium)
    if medium:
        return me.getValue(medium)["obras"]
    return None

def nObrasMasAntiguas(lista, n):
    SinVacio = lt.newList(datastructure="ARRAY_LIST", cmpfunction=compareartworks)
    lista_ord = ms.sort(lista, compareDate)
    for obra in lt.iterator(lista_ord):
        if obra["Date"] != "":
            lt.addLast(SinVacio, obra)
    top_n_antiguas = lt.subList(SinVacio, 1, n)
    return top_n_antiguas



# Construccion de modelos

# Funciones para agregar informacion al catalogo

# Funciones para creacion de datos

# Funciones de consulta

# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento
