import psycopg2
import random

conn = psycopg2.connect(
    host="localhost",
    database="biblioteca",
    user="postgres",
    password="123"
)
cur = conn.cursor()
cur.execute("DELETE FROM libros_calificacion;")
conn.commit()

cur.execute("SELECT id FROM libros_libro;")
libros = [row[0] for row in cur.fetchall()]

cur.execute("SELECT id FROM auth_user;")
usuarios = [row[0] for row in cur.fetchall()]

if len(usuarios) < 1:
    raise Exception("Debe haber al menos 1 usuario en la base de datos.")

for libro_id in libros:
    # 20% probabilidad de que el libro NO tenga calificaciones
    if random.random() < 0.2:
        continue

    cantidad_calificaciones = random.randint(1, min(7, len(usuarios)))
    usuarios_elegidos = random.sample(usuarios, cantidad_calificaciones)

    for user_id in usuarios_elegidos:
        # Usar una distribución normal centrada en 3.0 para simular puntajes realistas
        puntaje = min(5.0, max(0.5, round(random.gauss(3.0, 1.0), 1)))
        cur.execute("""
            INSERT INTO libros_calificacion (libro_id, usuario_id, calificacion)
            VALUES (%s, %s, %s)
        """, (libro_id, user_id, puntaje))

conn.commit()
cur.close()
conn.close()

print("✅ Calificaciones aleatorias insertadas correctamente.")
