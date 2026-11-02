import sqlite3
from fastapi import Depends, FastAPI, HTTPException, status, Response
from pydantic import BaseModel, Field
from database import crear_tabla, get_db
from ai import generar_resumen

app = FastAPI(title="API de Reseñas", version="1.0")
crear_tabla()


class RegistroFeedback(BaseModel):
    cliente: str = Field(min_length=3, max_length=100)
    comentario: str | None = Field(default=None, max_length=300)
    calificacion: int = Field(ge = 1, le = 5)


class Feedback(RegistroFeedback):
    id: int
    sentimiento: str | None = Field(default=None)

class ResumenGeneral(BaseModel):
    total_resenas: int
    resumen: str = Field(max_length=100)


def fila_a_resenas(fila: sqlite3.Row) -> Feedback:
    return Feedback(
        id = fila["id"],
        cliente = fila["cliente"],
        comentario = fila["comentario"],
        calificacion = int(fila["calificacion"]),
        sentimiento = fila["sentimiento"]        
    )


def buscar_fila(db: sqlite3.Connection, id: int) -> sqlite3.Row:
    fila = db.execute("SELECT * FROM resenas WHERE id = ?", (id,)).fetchone()
    if fila is None:
        raise HTTPException(status_code=404, detail="Reseña no encontrada")
    return fila


@app.post("/resenas", response_model=Feedback, status_code=status.HTTP_201_CREATED)
def crear_resena(datos: RegistroFeedback, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.execute(
        " INSERT INTO resenas (cliente, comentario, calificacion) VALUES (?, ?, ?)",
        (datos.cliente, datos.comentario, datos.calificacion),
    )
    db.commit()
    nueva_fila = buscar_fila(db, cursor.lastrowid)
    return fila_a_resenas(nueva_fila)



@app.get("/resenas", response_model=list[Feedback])
def listar_resenas(
    calificacion: int | None = None,
    sentimiento: str | None = None,
    db: sqlite3.Connection = Depends(get_db),
):
    consulta = "SELECT * FROM resenas WHERE 1 = 1"
    parametros = []

    if calificacion is not None:
        if calificacion < 1 or calificacion > 5:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="La calificación debe estar entre 1 y 5",
            )

        consulta += " AND calificacion = ?"
        parametros.append(calificacion)

    if sentimiento is not None:
        sentimiento = sentimiento.lower()

        if sentimiento not in {"positivo", "neutral", "negativo"}:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=(
                    "El sentimiento debe ser positivo, neutral o negativo"
                ),
            )

        consulta += " AND sentimiento = ?"
        parametros.append(sentimiento)

    consulta += " ORDER BY id"

    filas = db.execute(consulta, parametros).fetchall()

    return [fila_a_resenas(fila) for fila in filas]


@app.get("/resenas/resumen", response_model=ResumenGeneral)
def obtener_resumen(
    db: sqlite3.Connection = Depends(get_db),
):
    filas = db.execute(
        "SELECT comentario FROM resenas ORDER BY id"
    ).fetchall()

    if not filas:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No existen reseñas para resumir",
        )

    comentarios = [fila["comentario"] for fila in filas]

    try:
        resumen = generar_resumen(comentarios)
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="No fue posible generar el resumen con IA",
        ) from error

    return ResumenGeneral(
        total_resenas=len(comentarios),
        resumen=resumen,
    )


@app.get("/resenas/{id}", response_model=Feedback)
def obtener_resena(
    id: int,
    db: sqlite3.Connection = Depends(get_db),
):
    fila = buscar_fila(db, id)
    return fila_a_resenas(fila)


@app.put("/resenas/{id}", response_model=Feedback)
def actualizar_resena(
    id: int,
    datos: RegistroFeedback,
    db: sqlite3.Connection = Depends(get_db),
):
    buscar_fila(db, id)

    db.execute(
        """
        UPDATE resenas
        SET cliente = ?,
            comentario = ?,
            calificacion = ?,
            sentimiento = NULL
        WHERE id = ?
        """,
        (
            datos.cliente,
            datos.comentario,
            datos.calificacion,
            id,
        ),
    )

    db.commit()

    fila_actualizada = buscar_fila(db, id)
    return fila_a_resenas(fila_actualizada)


@app.delete(
    "/resenas/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def eliminar_resena(
    id: int,
    db: sqlite3.Connection = Depends(get_db),
):
    buscar_fila(db, id)

    db.execute(
        "DELETE FROM resenas WHERE id = ?",
        (id,),
    )
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)





