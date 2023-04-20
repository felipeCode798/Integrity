import psycopg2


class UserConnection():
    def __init__(self):
        try:
            self.db = psycopg2.connect("dbname=INTEGRITY user=postgres password=12345678 host=localhost port=5433")
        except psycopg2.OperationalError as err:
            print("Error: ", err)
            self.conn.close()


    #---------------------------------------------------------------------------------#
    #--------------- User CRUD -------------------------------------------------------#
    #---------------------------------------------------------------------------------#


    def info_user(self, data):
        with self.db.cursor() as cur:
            cur.execute("INSERT INTO users (user_id,name,dni,id_ciudad,phone,email,address,photo) VALUES (%(user_id)s, %(name)s, %(dni)s, %(id_ciudad)s, %(phone)s, %(email)s, %(address)s, %(photo)s)", data)
            self.db.commit()

    def read_users(self):
        with self.db.cursor() as cur:
            cur.execute("SELECT * FROM users")
            data = cur.fetchall()
            return data
    
    def read_user(self, user_id):
        with self.db.cursor() as cur:
            cur.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
            data = cur.fetchone()
            return data
    
    def read_city(self):
        with self.db.cursor() as cur:
            cur.execute("SELECT * FROM cities")
            data = cur.fetchall()
            return data

    def read_investigators(self):
        with self.db.cursor() as cur:
            cur.execute("SELECT * FROM investigator")
            data = cur.fetchall()
            return data

    #---------------------------------------------------------------------------------#
    #--------------- Documents Ivestigator CRUD --------------------------------------#
    #---------------------------------------------------------------------------------#

    def insert_investigator(self, data):
        with self.db.cursor() as cur:
            cur.execute("INSERT INTO investigator (inv_id, name, dni) VALUES (%(inv_id)s,%(name)s, %(dni)s)", data)
            self.db.commit()

    def info_investigator(self, data):
        with self.db.cursor() as cur:
            cur.execute("INSERT INTO documents (id_document,id_user,product,service,id_city,id_investigator,value,document) VALUES (%(id_document)s,%(id_user)s, %(product)s, %(service)s, %(id_city)s, %(id_investigator)s, %(value)s, %(document)s)", data)
            self.db.commit()
    
    def read_investigator(self):
        with self.db.cursor() as cur:
            cur.execute("SELECT * FROM documents")
            data = cur.fetchall()
            return data
    
    def read_investigator_id(self, id_document):
        with self.db.cursor() as cur:
            cur.execute("SELECT * FROM documents WHERE id_document = %s", (id_document,))
            data = cur.fetchone()
            return data
    
    def update_investigator(self, data):
        with self.db.cursor() as cur:
            cur.execute("UPDATE documents SET id_user = %(id_user)s, product = %(product)s, service = %(service)s, id_city = %(id_city)s, id_investigator = %(id_investigator)s, value = %(value)s, document = %(document)s WHERE id_document = %(id_document)s", data)
            self.db.commit()

    def update_documents(self, data):
        with self.db.cursor() as cur:
            cur.execute("UPDATE documents SET creator = %(creator)s, autor = %(autor)s, producer = %(produccer)s, title = %(title)s, creationdate = %(creation_date)s, lastdate = %(last_date)s WHERE id_document = %(id_document)s", data)
            self.db.commit()

    
    def delete_documents(self, id_document):
        with self.db.cursor() as cur:
            cur.execute("DELETE FROM documents WHERE id_document = %s", (id_document,))
            self.db.commit()
    
    #---------------------------------------------------------------------------------#
    #--------------- Consulta Id -----------------------------------------------------#
    #---------------------------------------------------------------------------------#

    def consulta_id(self):
        with self.db.cursor() as cur:
            cur.execute("SELECT MAX(id_document) FROM public.documents")
            data = cur.fetchone()
            data = data[0]
            return data
    
    def netx_id(self):
        with self.db.cursor() as cur:
            cur.execute("SELECT MAX(id_document) FROM public.documents")
            data = cur.fetchone()
            data = data[0] + 1
            return data
        
    def status(self, data):
        with self.db.cursor() as cur:
            status =data['status']
            data['status'] = status
            cur.execute("UPDATE documents SET status = %(status)s WHERE id_document = %(id_document)s", data)
            self.db.commit()
    
    def consulta_id_apocrifo(self):
        with self.db.cursor() as cur:
            cur.execute("SELECT MAX(id_apocrifo) FROM public.apocrypha")
            data = cur.fetchone()
            data = data[0]
            return data

    def next_id_apocrifo(self):
        with self.db.cursor() as cur:
            cur.execute("SELECT MAX(id_apocrifo) FROM public.apocrypha")
            data = cur.fetchone()
            if data[0] is None:
                data = 1
            else:
                data = data[0] 
                data = data + 1
            return data

    #---------------------------------------------------------------------------------#
    #--------------- Autor Consulta --------------------------------------------------#
    #---------------------------------------------------------------------------------#

    def consulta_autor(self, autor):
        with self.db.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM apocrypha WHERE autor = %s", (autor,))
            data = cur.fetchone()
            data = data[0]
            return data

    #---------------------------------------------------------------------------------#
    #--------------- Apocrifo CRUD ---------------------------------------------------#
    #---------------------------------------------------------------------------------#

    def info_apocrifo(self, data):
        with self.db.cursor() as cur:
            cur.execute("INSERT INTO apocrypha (id_apocrifo,creator,autor,producer,name,phone,dni) VALUES (%(id_apocrifo)s,%(creator)s, %(autor)s, %(producer)s, %(name)s, %(phone)s, %(dni)s)", data)
            self.db.commit()

    def read_apocrifo(self):
        with self.db.cursor() as cur:
            cur.execute("SELECT * FROM apocrypha")
            data = cur.fetchall()
            return data
        
    def read_apocrifo_id(self, id_apocrifo):
        with self.db.cursor() as cur:
            cur.execute("SELECT * FROM apocrypha WHERE id_apocrifo = %s", (id_apocrifo,))
            data = cur.fetchone()
            return data
        
    def delete_apocrifo(self, id_apocrifo):
        with self.db.cursor() as cur:
            cur.execute("DELETE FROM apocrypha WHERE id_apocrifo = %s", (id_apocrifo,))
            self.db.commit()

    #---------------------------------------------------------------------------------#
    #--------------- Creator y Producer Consulta -------------------------------------#
    #---------------------------------------------------------------------------------#

    def consulta_creator(self, creator):
        with self.db.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM listblack WHERE creator = %s", (creator,))
            data = cur.fetchone()
            data = data[0]
            return data

    def consulta_producer(self, producer):
        with self.db.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM listblack WHERE producer = %s", (producer,))
            data = cur.fetchone()
            data = data[0]
            return data

    def __def__(self):
        self.db.close()