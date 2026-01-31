from database.banco import SessaoLOCAL

def get_db():
    db = SessaoLOCAL()
    try:
        yield db
    finally:
        db.close()
