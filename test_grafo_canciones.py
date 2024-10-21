from Recomendador import NodoCancion 
from Recomendador import GrafoCanciones 
import pytest
def test_grafo_canciones():
    # Crea una instancia del grafo
    grafo = GrafoCanciones()

    # Agrega canciones al grafo
    grafo.agregar_cancion("Song1", "Artist1")
    grafo.agregar_cancion("Song2", "Artist2")
    grafo.agregar_cancion("Song3", "Artist1")

    # Conecta las canciones entre sí
    grafo.conectar_canciones("Song1", "Song2")
    grafo.conectar_canciones("Song1", "Song3")

    # Verifica que se hayan agregado correctamente las canciones al grafo
    assert "Song1" in grafo.nodos
    assert "Song2" in grafo.nodos
    assert "Song3" in grafo.nodos

    # Verifica que las conexiones se hayan realizado correctamente
    assert grafo.nodos["Song1"] in grafo.nodos["Song2"].conexiones
    assert grafo.nodos["Song2"] in grafo.nodos["Song1"].conexiones
    assert grafo.nodos["Song1"] in grafo.nodos["Song3"].conexiones
    assert grafo.nodos["Song3"] in grafo.nodos["Song1"].conexiones

    # Verifica que las recomendaciones basadas en artista funcionen correctamente
    recomendaciones_artist1 = grafo.obtener_recomendaciones_por_artista("Artist1")
    assert "Song1" in recomendaciones_artist1
    assert "Song3" in recomendaciones_artist1
    assert "Song2" not in recomendaciones_artist1  # No debería estar ya que pertenece a "Artist2"
