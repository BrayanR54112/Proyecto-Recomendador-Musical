import pytest
from avance1 import RecomendadorMusical 

def test_agregar_y_recomendar():
    recomendador = RecomendadorMusical()
    recomendador.agregar_cancion("feliz", "Canción Feliz")
    recomendaciones = recomendador.recomendar_canciones("feliz")
    assert "Canción Feliz" in recomendaciones

def test_vaciar_recomendaciones():
    recomendador = RecomendadorMusical()
    recomendador.agregar_cancion("triste", "Canción Triste")
    recomendador.vaciar_recomendaciones()
    recomendaciones = recomendador.recomendar_canciones("triste")
    assert len(recomendaciones) == 0
