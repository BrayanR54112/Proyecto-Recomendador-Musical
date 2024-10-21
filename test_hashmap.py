import pytest
from Recomendador import HashMap, NM  

def test_poner_y_obtener():
    hm = HashMap()
    hm.poner("clave1", "valor1")
    nodo = hm.obtener("clave1")
    assert nodo.retornaValor() == "valor1"

def test_contar():
    hm = HashMap()
    hm.poner("clave1", "valor1")
    hm.poner("clave2", "valor2")
    assert hm.contar() == 2

def test_eliminar_clave():
    hm = HashMap()
    hm.poner("clave1", "valor1")
    hm.eliminar_clave("clave1")
    with pytest.raises(KeyError):
        hm.obtener("clave1")

def test_redimensionar():
    hm = HashMap()
    hm.poner("clave1", "valor1")
    hm.redimensionar(20)
    nodo = hm.obtener("clave1")
    assert nodo.retornaValor() == "valor1"
