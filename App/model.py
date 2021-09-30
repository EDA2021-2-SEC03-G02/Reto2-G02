"""
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
def newCatalog():
    """
    Inicializa el catálogo de libros. Crea una lista vacia para guardar
    todos los libros, adicionalmente, crea una lista vacia para los autores,
    una lista vacia para los generos y una lista vacia para la asociación
    generos y libros. Retorna el catalogo inicializado.
    """
    catalog = {'artworks': None, "Medium" : None}
    
    catalog['artworks'] = lt.newList('SINGLE_LINKED', cmpfunction=compareartworks)
    #Paso 1: Modifique su catálogo para que al cargar las obras en una lista cree un índice por medio utilizando la librería Maps.py de DISClib.
    catalog['Medium'] = mp.newMap(10000,
                                   maptype='CHAINING',
                                   loadfactor=4.0,
                                   comparefunction=compareartworksmediumMAP)
    return catalog



def addArtwork(catalog, artwork):
    # Se adiciona el libro a la lista de libros
    lt.addLast(catalog['artworks'], artwork)
    #Se añade al mapa las obras con los medios como llaves
    if artwork["Medium"] != "":
        #print(artwork["Medium"])
        mp.put(catalog["Medium"], artwork["Medium"], artwork)
    addArtworkMedium(catalog, artwork)
    



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

def addArtworkMedium(catalog, artwork):
    try:
        mediums = catalog["Medium"]
        if (artwork["Medium"]!=""):
            medioArtwork = artwork["Medium"]
        existmedio = mp.contains(mediums, medioArtwork)
        if existmedio:
            entry = mp.get(mediums, medioArtwork)
            medium = me.getValue(entry)
        else:
            medium = newMedium(medioArtwork)
            mp.put(mediums, medioArtwork, medium)
    except Exception:
        return None

def newMedium(medioArtwork):
    entry = {"Medium": "", "artworks": None}
    entry["Medium"] = medioArtwork
    entry["artworks"] = lt.newList("SINGLE-LINKED", compareartworksmedium)
    return entry
        

def TopViejosPorMedium(catalog, medium):
    mapa = catalog["Medium"]
    #print(mp.get(mapa, medium))
    pareja = mp.get(mapa, medium)
    lista = me.getValue(pareja)
    print(lista)

    """if llave == medium:
        addLast(lista, obra)
        ms.fecha(lista)
        top(n)"""


# Construccion de modelos

# Funciones para agregar informacion al catalogo

# Funciones para creacion de datos

# Funciones de consulta

# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento
