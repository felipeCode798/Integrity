import os
import PyPDF2
from fastapi import FastAPI, File, UploadFile, Response, Form
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND, HTTP_200_OK
from model.user_connection import UserConnection
from schema.user_schema import UserSchema, InvestigatorSchema, DocumentsSchema, AnalisisSchema, ApocrifoSchema, InvestigatorsSchema,productservices
from utils import funciones
from datetime import datetime
from werkzeug.utils import secure_filename
from typing import Optional, Dict, Any
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
conn = UserConnection()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#---------------------------------------------------------------------------------#
#--------------- GET -------------------------------------------------------------#
#---------------------------------------------------------------------------------#

#---------------------------------------------------------------------------------#
#--------------- User ------------------------------------------------------------#
#---------------------------------------------------------------------------------#

"""
Keyword arguments: No recibe ningun
argument -- Consulta todos los usuarios registrados
Return: array -> items
"""
@app.get("/", status_code=HTTP_200_OK)
async def read_users():
    items = []
    data = conn.read_users()
    for i in data:
        dictionary = {}
        dictionary["user_id"] = i[0]
        dictionary["name"] = i[1]
        dictionary["dni"] = i[2]
        dictionary["id_ciudad"] = i[3]
        dictionary["phone"] = i[4]
        dictionary["email"] = i[5]
        dictionary["address"] = i[6]
        dictionary["photo"] = i[7]
        items.append(dictionary)
    return items


"""
Keyword arguments: user_id
argument -- Consulta usuarios registrados por id
Return: array -> dictionary
"""
@app.get("/api/user/{user_id}", status_code=HTTP_200_OK)
async def read_user(user_id: int):
    data = conn.read_user(user_id)
    if data:
        dictionary = {}
        dictionary["user_id"] = data[0]
        dictionary["name"] = data[1]
        dictionary["dni"] = data[2]
        dictionary["id_ciudad"] = data[3]
        dictionary["phone"] = data[4]
        dictionary["email"] = data[5]
        dictionary["address"] = data[6]
        dictionary["photo"] = data[7]
        return dictionary
    else:
        return Response(status_code=HTTP_404_NOT_FOUND)
    
#---------------------------------------------------------------------------------#
#--------------- City ------------------------------------------------------------#
#---------------------------------------------------------------------------------#
    

"""
Keyword arguments: No recibe ningun
argument -- Consulta todas las ciudades registradas
Return: array -> items
"""
@app.get("/api/city", status_code=HTTP_200_OK)
async def read_city():
    items = []
    data = conn.read_city()
    for i in data:
        dictionary = {}
        dictionary["ci_id"] = i[0]
        dictionary["name"] = i[1]
        items.append(dictionary)
    return items

#---------------------------------------------------------------------------------#
#--------------- Ivestigator -----l------------------------------------------------#
#---------------------------------------------------------------------------------#
"""
Keyword arguments: No recibe ningun
argument -- Consulta todos los investigadores registrados
Return: array -> items
"""
@app.get("/api/read_investigator", status_code=HTTP_200_OK)
async def read_investigator():
    items = []
    data = conn.read_investigator()
    for i in data:
        dictionary = {}
        dictionary["inv_id"] = i[0]
        dictionary["name"] = i[1]
        dictionary["dni"] = i[2]
        items.append(dictionary)
    return items

#---------------------------------------------------------------------------------#
#--------------- Documents CRUD --------------------------------------------------#
#---------------------------------------------------------------------------------#

"""
Keyword arguments: No recibe ningun
argument -- Consulta todos los docuemntos registrados sin el resultado del analisis del documento
Return: array -> items
"""
@app.get("/api/documents", status_code=HTTP_200_OK)
async def read_documents():
    items = []
    data = conn.read_documents()
    for i in data:
        dictionary = {}
        dictionary["id_document"] = i[0]
        dictionary["id_user"] = i[1]
        dictionary["product"] = i[2]
        dictionary["service"] = i[3]
        dictionary["id_city"] = i[4]
        dictionary["id_investigator"] = i[5]
        dictionary["value"] = i[6]
        dictionary["document"] = i[7]
        items.append(dictionary)
    return items

"""
Keyword arguments: id_document
argument -- Consulta los documentos registrados por id, sin el resultado del analisis del documento
Return: array -> dictionary
"""
@app.get("/api/document/{id_document}", status_code=HTTP_200_OK)
async def read_document_id(id_document: int):
    data = conn.read_document_id(id_document)
    if data:
        dictionary = {}
        dictionary["id_document"] = data[0]
        dictionary["id_user"] = data[1]
        dictionary["product"] = data[2]
        dictionary["service"] = data[3]
        dictionary["id_city"] = data[4]
        dictionary["id_investigator"] = data[5]
        dictionary["value"] = data[6]
        dictionary["document"] = data[7]
        return dictionary
    else:
        return Response(status_code=HTTP_404_NOT_FOUND)
    
"""
Keyword arguments: id_document
argument -- Trae el documento analizado por id
Return: data
"""

@app.get("/api/get_document/{id_document}", status_code=HTTP_200_OK)
async def get_document(id_document: int):
    data = conn.get_document(id_document)
    return data

#---------------------------------------------------------------------------------#
#--------------- Apocrifo CRUD ---------------------------------------------------#
#---------------------------------------------------------------------------------#

"""
Keyword arguments: No recibe ningun
argument -- Consulta todos los registros que han sido aporcrifos
Return: array -> items
"""
@app.get("/api/apocrifo", status_code=HTTP_200_OK)
async def read_apocrifo():
    items = []
    data = conn.read_apocrifo()
    for i in data:
        dictionary = {}
        dictionary["id_apocrifo"] = i[0]
        dictionary["creator"] = i[1]
        dictionary["autor"] = i[2]
        dictionary["producer"] = i[3]
        dictionary["name"] = i[4]
        dictionary["phone"] = i[5]
        dictionary["dni"] = i[6]
        items.append(dictionary)
    return items

"""
Keyword arguments: id_apocrifo
argument -- Consulta los registros que han sido apocrifos por id
Return: array -> dictionary
"""
@app.get("/api/apocrifo/{id_apocrifo}", status_code=HTTP_200_OK)
async def read_apocrifo_id(id_apocrifo: int):
    data = conn.read_apocrifo_id(id_apocrifo)
    if data:
        dictionary = {}
        dictionary["id_apocrifo"] = data[0]
        dictionary["creator"] = data[1]
        dictionary["autor"] = data[2]
        dictionary["producer"] = data[3]
        dictionary["name"] = data[4]
        dictionary["phone"] = data[5]
        dictionary["dni"] = data[6]
        return dictionary
    else:
        return Response(status_code=HTTP_404_NOT_FOUND)

#---------------------------------------------------------------------------------#
#--------------- Creator, Producer y Autor Consulta ------------------------------#
#---------------------------------------------------------------------------------#

"""
Keyword arguments: creator
argument -- Cuenta las couidencias de un creador en la blacklist
Return: array -> data
"""
@app.get("/api/consulta_creator", status_code=HTTP_200_OK)
async def consulta_creator(creator: str):
    data = conn.consulta_creator(creator)
    return data

"""
Keyword arguments: producer
argument -- Cuenta las couidencias de un productor en la blacklist
Return: array -> data
"""
@app.get("/api/consulta_producer", status_code=HTTP_200_OK)
async def consulta_producer(producer: str):
    data = conn.consulta_producer(producer)
    return data

"""
Keyword arguments: autor
argument -- Cuenta las couidencias de un autor en documentos apocrifos
Return: array -> data
"""
@app.get("/api/consulta_autor", status_code=HTTP_200_OK)
async def consulta_autor(autor: str):
    data = conn.consulta_autor(autor)
    return data

#---------------------------------------------------------------------------------#
#--------------- Producto o Servicio ---------------------------------------------#
#---------------------------------------------------------------------------------#

"""
Keyword arguments: No recibe ningun
argument -- Consulta todos los productos y servicios registrados
Return: array -> items
"""
@app.get("/api/read_productoservice", status_code=HTTP_200_OK)
async def read_productoservice():
    items = []
    data = conn.read_productoservice()
    for i in data:
        dictionary = {}
        dictionary["inv_id"] = i[0]
        dictionary["name"] = i[1]
        dictionary["dni"] = i[2]
        items.append(dictionary)
    return items

#---------------------------------------------------------------------------------#
#--------------- POST      -------------------------------------------------------#
#---------------------------------------------------------------------------------#

#---------------------------------------------------------------------------------#
#--------------- User CRUD -------------------------------------------------------#
#---------------------------------------------------------------------------------#

"""
Keyword arguments: user_data
argument -- Inserta un nuevo usuario
Return: Response 201
"""
@app.post("/api/info_user", status_code=HTTP_201_CREATED)
async def info_user(user_data: UserSchema):
    data = user_data.dict()
    conn.info_user(data)
    return Response(status_code=HTTP_201_CREATED)


#---------------------------------------------------------------------------------#
#--------------- Ivestigator CRUD ------------------------------------------------#
#---------------------------------------------------------------------------------#

"""
Keyword arguments: investigators_data
argument -- Inserta un nuevo investigador
Return: Response 201
"""
@app.post("/api/insert_investigator", status_code=HTTP_201_CREATED)
async def insert_investigator(investigators_data: InvestigatorsSchema):
    data = investigators_data.dict()
    conn.insert_investigator(data)
    return Response(status_code=HTTP_201_CREATED)

#---------------------------------------------------------------------------------#
#--------------- Documents CRUD --------------------------------------------------#
#---------------------------------------------------------------------------------#

"""
Keyword arguments: documents_data
argument -- Inserta datos de informacion de un nuevo documento
Return: Response 201
"""
@app.post("/api/info_documents", status_code=HTTP_201_CREATED)
async def info_documents(documents_data: InvestigatorSchema):
    data = documents_data.dict()
    now = datetime.now()
    time = now.strftime("%Y%H%M%S")
    data["document"] = f"{time}{data['document']}{'.pdf'}"
    conn.info_documents(data)
    return Response(status_code=HTTP_201_CREATED)

#---------------------------------------------------------------------------------#
#--------------- Apocrifo CRUD ---------------------------------------------------#
#---------------------------------------------------------------------------------#

"""
Keyword arguments: list
argument -- Inserta regitro de un documento apocrifo
Return: Response 201
"""
@app.post("/api/info_apocrifo", status_code=HTTP_201_CREATED)
async def info_apocrifo(list):
    data = list
    conn.info_apocrifo(data)
    return Response(status_code=HTTP_201_CREATED)

#---------------------------------------------------------------------------------#
#--------------- Analisis  -------------------------------------------------------#
#---------------------------------------------------------------------------------#

"""
Keyword arguments: list
argument -- Realiza el analisis de un documento cuando es pdf
Return: resultado
"""
@app.post("/analisis/")
async def analisis_endpoint(list):
    tipo = list[0]
    creacion_fecha = list[1]
    creacion_fecha_hora = list[2]
    modifica_fecha = list[3]
    modifica_fecha_hora = list[4]
    fecha = list[5]
    hora = list[6]
    creatorCont = list[7]
    authorCont = list[8]
    producerCont = list[9]
    creatorName = list[10]
    autorName = list[11]
    producerName = list[12]
    name = list[13]
    phone = list[14]
    dni = list[15]
    id_apocrifo = list[16]
    id_document = list[17]

    data = {
        "creator": creatorName,
        "autor": autorName,
        "producer": producerName,
        "name": name,
        "phone": phone,
        "dni": dni,
        'id_apocrifo': id_apocrifo
    }

    apocrifo = {
        'status': 'APOCRIFO',
        'id_document': id_document
    }

    autentico = {
        'status': 'AUTENTICO',
        'id_document': id_document
    }
    

    tipo = 'pdf'
    date = creacion_fecha + 9305
    hour = 144500

    if creatorCont >= 1:
        conn.status(apocrifo)
        conn.info_apocrifo(data)
        resultado = "Este documento posiblemente es apocrifo"
    elif authorCont >= 1:
        conn.status(apocrifo)
        conn.info_apocrifo(data)
        resultado = "Este documento posiblemente es apocrifo o el autor de este documento ha intentado subir documentos posiblemente apocrifos anteriormente"
    elif producerCont >= 1:
        conn.status(apocrifo)
        conn.info_apocrifo(data)
        resultado = "Este documento posiblemente es apocrifo"
    elif creacion_fecha != modifica_fecha:
        conn.status(apocrifo)
        conn.info_apocrifo(data)
        resultado = "Este documento posiblemente es apocrifo"
    elif creacion_fecha_hora != modifica_fecha_hora:
        conn.status(apocrifo)
        conn.info_apocrifo(data)
        resultado = "Este documento posiblemente es apocrifo"
    elif creacion_fecha == 0:
        conn.status(apocrifo)
        conn.info_apocrifo(data)
        resultado = "Este documento posiblemente es apocrifo"
    elif date > fecha:
        conn.status(apocrifo)
        conn.info_apocrifo(data)
        resultado = "Este documento posiblemente es apocrifo"
    elif hour > hora:
        conn.status(apocrifo)
        conn.info_apocrifo(data)
        resultado = "Este documento posiblemente es apocrifo"
    else:
        conn.status(autentico)
        resultado = "Este docuemto es autentico"

    return resultado

"""
Keyword arguments: name, phone, dni, file
argument -- devuelve el resultado del analisis de un documento
Return: resultado
"""
@app.post("/uploadfile/")
async def create_upload_file(name: str, phone: int, dni: int, file: UploadFile = File(...)):
    
    now = datetime.now()
    time = now.strftime("%Y%H%M%S")

    document = file

    if document != '':
        newName = time + document.filename
        with open("./uploads/"+newName, "wb") as f:
            f.write(file.file.read())

    if not os.path.exists("uploads"):
        os.mkdir("uploads")

    ruta = 'uploads/' + newName

    filename = secure_filename(document.filename)
    extension = filename.rsplit('.', 1)[1].lower()

    if extension != 'pdf':
        tipo = 'img'

        # Analizar la imagen utilizando diferentes técnicas.
        results = {}
        results['tipo'] = tipo
        results['manipulation'] = funciones.detect_manipulation(ruta)
        results['manipulation_pattern'] = funciones.detect_manipulation_pattern(ruta)
        results['noise'] = funciones.detect_noise(ruta)
        results['metadata'] = funciones.detect_metadata(ruta)
        results['compression'] = funciones.detect_compression(ruta)
        results['brightness'] = funciones.analyze_brightness(ruta)
    else:
        pdfReader = PyPDF2.PdfReader(open(ruta, 'rb'))
        info = pdfReader.metadata
        creatorName = str(info.get('/Creator'))
        autorName = str(info.get('/Author'))
        creationdate = info.get('/CreationDate')
        moddate = info.get('/ModDate')
        producerName = str(info.get('/Producer'))
        title = str(info.get('/Title'))
        funciones.ultima_fecha(ruta)
        fecha = funciones.ultima_fecha(ruta)
        funciones.ultima_fecha_hora(ruta)
        hora = funciones.ultima_fecha_hora(ruta)

        funciones.creacion_fecha(creationdate, moddate)
        creation_date = funciones.creacion_fecha(creationdate, moddate)

        funciones.creacion_fecha_hora(creationdate, moddate)
        creacion_fecha_hora = funciones.creacion_fecha_hora(creationdate, moddate)

        funciones.modifica_fecha(moddate)
        modifica_fecha = funciones.modifica_fecha(moddate)

        funciones.modifica_fecha_hora(moddate, info)
        modifica_fecha_hora = funciones.modifica_fecha_hora(moddate, info)

        id = conn.consulta_id()

        data = {
            'creator': creatorName,
            'autor': autorName,
            'produccer': producerName,
            'title': title,
            'creation_date': creation_date,
            'last_date': fecha,
            'id_document': id
        }

        await update_documents(data, id)
        creatorCont = await consulta_creator(creatorName)
        authorCont = await consulta_autor(autorName)
        producerCont = await consulta_producer(producerName)
        tipo = 'pdf'
        id_apocrifo = conn.next_id_apocrifo()
        id_status = conn.consulta_id()

        data = {
            'tipo': tipo,
            'creation_date': creation_date,
            'creacion_fecha_hora': creacion_fecha_hora,
            'modifica_fecha': modifica_fecha,
            'modifica_fecha_hora': modifica_fecha_hora,
            'fecha': fecha,
            'hora': hora,
            'creatorCont': creatorCont,
            'authorCont': authorCont,
            'producerCont': producerCont,
            'creatorName': creatorName,
            'autorName': autorName,
            'producerName': producerName,
            'name': name,
            'phone': phone,
            'dni': dni,
            'id_apocrifo': id_apocrifo,
            'id_status': id_status,
        }

        data = list(data.values())

        resultado = await analisis_endpoint(data)

    return resultado

#---------------------------------------------------------------------------------#
#--------------- Produto o Servicio ----------------------------------------------#
#---------------------------------------------------------------------------------#

"""
Keyword arguments: producservice_data
argument -- Inserta la informacion de un producto o servicio
Return: Response 201
"""
@app.post("/api/info_productoservice", status_code=HTTP_201_CREATED)
async def info_productoservice(producservice_data: productservices):
    data = producservice_data.dict()
    conn.info_productoservice(data)
    return Response(status_code=HTTP_201_CREATED)

#---------------------------------------------------------------------------------#
#--------------- PUT       -------------------------------------------------------#
#---------------------------------------------------------------------------------#

#---------------------------------------------------------------------------------#
#--------------- Ivestigator CRUD ------------------------------------------------#
#---------------------------------------------------------------------------------#

"""
Keyword arguments: investigator_data, id
argument -- Actualiza la informacion de un investigador
Return: Response 204
"""
@app.put("/api/update_investigator/{id_document}", status_code=HTTP_204_NO_CONTENT)
async def update_documents_info(investigator_data: InvestigatorSchema, id: int):
    data = investigator_data.dict()
    data["id_document"] = id
    conn.update_documents_info(data)
    return Response(status_code=HTTP_204_NO_CONTENT)

#---------------------------------------------------------------------------------#
#--------------- Documents CRUD --------------------------------------------------#
#---------------------------------------------------------------------------------#

"""
Keyword arguments: document_data, id
argument -- Actualiza la informacion de un documento 
Return: Response 204
"""
@app.put("/api/update_documents/{id_document}", status_code=HTTP_204_NO_CONTENT)
async def update_documents(investigator_data: DocumentsSchema, id: int):
    data = investigator_data.dict()
    data["id_document"] = id
    conn.update_documents(data)
    return Response(status_code=HTTP_204_NO_CONTENT)


"""
Keyword arguments: list, id
argument -- Inserta el analisis final de un documento
Return: Response 204
"""
@app.put("/api/update_document/{id_document}", status_code=HTTP_204_NO_CONTENT)
async def update_documents(list, id: int):
    data = list
    conn.update_documents(data)
    return Response(status_code=HTTP_204_NO_CONTENT)


#---------------------------------------------------------------------------------#
#--------------- Analisis --------------------------------------------------------#
#---------------------------------------------------------------------------------#

"""
Keyword arguments: analisis_data, id
argument -- Inserta el analisis el cual define si es apocrifo o no
Return: return_description
"""
@app.put("/api/status/{id_document}", status_code=HTTP_204_NO_CONTENT)
async def status(analisis_data: AnalisisSchema, id: int):
    data = analisis_data.dict()
    data["id_document"] = id
    conn.status(data)
    return Response(status_code=HTTP_204_NO_CONTENT)