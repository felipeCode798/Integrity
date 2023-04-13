import os
import PyPDF2
from fastapi import FastAPI, File, UploadFile, Response, Form
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND, HTTP_200_OK
from model.user_connection import UserConnection
from schema.user_schema import UserSchema, InvestigatorSchema, DocumentsSchema, AnalisisSchema, ApocrifoSchema, Datos
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
#--------------- User CRUD -------------------------------------------------------#
#---------------------------------------------------------------------------------#

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

@app.post("/api/info_user", status_code=HTTP_201_CREATED)
async def info_user(user_data: UserSchema):
    data = user_data.dict()
    conn.info_user(data)
    return Response(status_code=HTTP_201_CREATED)


#---------------------------------------------------------------------------------#
#--------------- Ivestigator CRUD ------------------------------------------------#
#---------------------------------------------------------------------------------#

@app.get("/api/investigator", status_code=HTTP_200_OK)
async def read_investigator():
    items = []
    data = conn.read_investigator()
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

@app.get("/api/investigator/{id_document}", status_code=HTTP_200_OK)
async def read_investigator_id(id_document: int):
    data = conn.read_investigator_id(id_document)
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

@app.post("/api/info_investigator", status_code=HTTP_201_CREATED)
async def info_investigator(investigator_data: InvestigatorSchema):
    data = investigator_data.dict()
    conn.info_investigator(data)
    return Response(status_code=HTTP_201_CREATED)

@app.put("/api/update_investigator/{id_document}", status_code=HTTP_204_NO_CONTENT)
async def update_investigator(investigator_data: InvestigatorSchema, id: int):
    data = investigator_data.dict()
    data["id_document"] = id
    conn.update_investigator(data)
    return Response(status_code=HTTP_204_NO_CONTENT)

#---------------------------------------------------------------------------------#
#--------------- Documents CRUD --------------------------------------------------#
#---------------------------------------------------------------------------------#

@app.put("/api/update_document/{id_document}", status_code=HTTP_204_NO_CONTENT)
async def update_documents(list, id: int):
    data = list
    #data["id_document"] = id
    conn.update_documents(data)
    return Response(status_code=HTTP_204_NO_CONTENT)

#---------------------------------------------------------------------------------#
#--------------- Consulta Id -----------------------------------------------------#
#---------------------------------------------------------------------------------#

@app.put("/api/status/{id_document}", status_code=HTTP_204_NO_CONTENT)
async def status(analisis_data: AnalisisSchema, id: int):
    data = analisis_data.dict()
    data["id_document"] = id
    conn.status(data)
    return Response(status_code=HTTP_204_NO_CONTENT)

#---------------------------------------------------------------------------------#
#--------------- Apocrifo CRUD ---------------------------------------------------#
#---------------------------------------------------------------------------------#

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

@app.post("/api/info_apocrifo", status_code=HTTP_201_CREATED)
async def info_apocrifo(list):
    data = list
    conn.info_apocrifo(data)
    return Response(status_code=HTTP_201_CREATED)

@app.put("/api/update_apocrifo/{id_apocrifo}", status_code=HTTP_204_NO_CONTENT)
async def update_apocrifo(apocrifo_data: ApocrifoSchema, id: int):
    data = apocrifo_data.dict()
    data["id_apocrifo"] = id
    conn.update_apocrifo(data)
    return Response(status_code=HTTP_204_NO_CONTENT)

#---------------------------------------------------------------------------------#
#--------------- Creator y Producer Consulta -------------------------------------#
#---------------------------------------------------------------------------------#

@app.get("/api/consulta_creator", status_code=HTTP_200_OK)
async def consulta_creator(creator: str):
    data = conn.consulta_creator(creator)
    return data

@app.get("/api/consulta_producer", status_code=HTTP_200_OK)
async def consulta_producer(producer: str):
    data = conn.consulta_producer(producer)
    return data


#---------------------------------------------------------------------------------#
#--------------- Autor Consulta --------------------------------------------------#
#---------------------------------------------------------------------------------#

@app.get("/api/consulta_autor", status_code=HTTP_200_OK)
async def consulta_autor(autor: str):
    data = conn.consulta_autor(autor)
    return data


#---------------------------------------------------------------------------------#
#--------------- Pdf Analisis ----------------------------------------------------#
#---------------------------------------------------------------------------------#

@app.post("/analisis/")
async def analisis_endpoint(list):
    print('Esta es la data')
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
        print('caso 1')
        conn.status(apocrifo)
        conn.info_apocrifo(data)
        resultado = "Este documento posiblemente es apocrifo"
    elif authorCont >= 1:
        print('caso 2')
        conn.status(apocrifo)
        conn.info_apocrifo(data)
        resultado = "Este documento posiblemente es apocrifo o el autor de este documento ha intentado subir documentos posiblemente apocrifos anteriormente"
    elif producerCont >= 1:
        print('caso 3')
        conn.status(apocrifo)
        conn.info_apocrifo(data)
        resultado = "Este documento posiblemente es apocrifo"
    elif creacion_fecha != modifica_fecha:
        print('caso 4')
        conn.status(apocrifo)
        conn.info_apocrifo(data)
        resultado = "Este documento posiblemente es apocrifo"
    elif creacion_fecha_hora != modifica_fecha_hora:
        print('caso 5')
        conn.status(apocrifo)
        conn.info_apocrifo(data)
        resultado = "Este documento posiblemente es apocrifo"
    elif creacion_fecha == 0:
        print('caso 6')
        conn.status(apocrifo)
        conn.info_apocrifo(data)
        resultado = "Este documento posiblemente es apocrifo"
    elif date > fecha:
        print('caso 7')
        conn.status(apocrifo)
        conn.info_apocrifo(data)
        resultado = "Este documento posiblemente es apocrifo"
    elif hour > hora:
        print('caso 8')
        conn.status(apocrifo)
        conn.info_apocrifo(data)
        resultado = "Este documento posiblemente es apocrifo"
    else:
        print('caso 9')
        conn.status(autentico)
        resultado = "Este docuemto es autentico"

    return resultado

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