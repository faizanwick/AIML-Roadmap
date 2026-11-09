from sqlalchemy import text
from app.db.session import engine

try:
    with engine.connect() as conn:
        result = conn.execute(text("select current_database()"))
        print(result.scalar())

except Exception as e:
    print(e)

finally:
    engine.dispose()