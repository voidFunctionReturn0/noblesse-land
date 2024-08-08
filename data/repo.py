import psycopg2

# PostgreSQL 연결 정보
# TODO: DB 연결 정보 숨기기
USERNAME = 'postgres'
PASSWORD = 'postgres'
HOSTNAME = 'localhost'
PORT = '5433'
DATABASE_NAME = 'noblesse_land'

class Repo:
    def __init__(self):
        self.conn =  psycopg2.connect(host=HOSTNAME, dbname=DATABASE_NAME, user=USERNAME, password=PASSWORD, port=PORT)
        self.cur = self.conn.cursor()


    def get_building_id(self, building):
        self.cur.execute("SELECT id FROM buildings WHERE details = %s;", [building.details,])
        result = self.cur.fetchone()
        if result:
            return result[0]
        else:
            None
        
    
    def get_owner_id(self, owner):
        self.cur.execute("SELECT id FROM owners WHERE name = %s and organization = %s and position = %s and relation = %s;", [owner.name, owner.organization, owner.position, owner.relation])
        result = self.cur.fetchone()
        if result:
            return result[0]
        else:
            None
    
    def is_existing_owner_building(self, owner_building):
        self.cur.execute("SELECT owner_id FROM owner_buildings WHERE owner_id = %s and building_id = %s;", [self.get_owner_id(owner_building.owner), self.get_building_id(owner_building.building)])
        result = self.cur.fetchone()
        if result:
            return True
        else:
            return False


    def insert_building(self, building):
        if self.get_building_id(building) is None:
            if building.coordinates is None:
                SQL_QUERY = "INSERT INTO buildings (type, details, price, note) VALUES (%s, %s, %s, %s);"
                self.cur.execute(SQL_QUERY, (building.type, building.details, building.price, building.note))
            else:
                SQL_QUERY = "INSERT INTO buildings (type, details, price, note, coordinates) VALUES (%s, %s, %s, %s, %s);"
                self.cur.execute(SQL_QUERY, (building.type, building.details, building.price, building.note, f'({building.coordinates.lat},{building.coordinates.lng})'))
            self.conn.commit()
    

    def insert_owner(self, owner):
        if self.get_owner_id(owner) is None:
            SQL_QUERY = "INSERT INTO owners (name, organization, position, relation, image_path) VALUES (%s, %s, %s, %s, %s);"
            self.cur.execute(SQL_QUERY, (owner.name, owner.organization, owner.position, owner.relation, owner.image_path))
            self.conn.commit()
    

    def insert_owner_building(self, owner_building):
        building_id = self.get_building_id(owner_building.building)
        owner_id = self.get_owner_id(owner_building.owner)

        if not self.is_existing_owner_building(owner_building):
            SQL_QUERY = "INSERT INTO owner_buildings (owner_id, building_id, created_at) VALUES (%s, %s, %s);"
            self.cur.execute(SQL_QUERY, (owner_id, building_id, owner_building.created_at))
            self.conn.commit()
