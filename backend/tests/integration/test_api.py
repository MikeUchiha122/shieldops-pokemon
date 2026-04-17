"""
Tests de integración — API completa (FastAPI TestClient).
Verifica que los 3 routers respondan correctamente y estén aislados.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


class TestHealthEndpoints:
    def test_health_global(self):
        r = client.get("/api/v1/health")
        assert r.status_code == 200
        data = r.json()
        assert "cerebros" in data
        assert "eyp"       in data["cerebros"]
        assert "lza"       in data["cerebros"]
        assert "go"        in data["cerebros"]
        assert "champions" in data["cerebros"]

    def test_health_eyp(self):
        r = client.get("/api/v1/eyp/health")
        assert r.status_code == 200
        body = r.json()
        assert body["cerebro"] == "eyp"
        assert body["ok"] is True

    def test_health_lza(self):
        r = client.get("/api/v1/lza/health")
        assert r.status_code == 200
        body = r.json()
        assert body["cerebro"] == "lza"
        assert body["ok"] is True

    def test_health_go(self):
        r = client.get("/api/v1/go/health")
        assert r.status_code == 200
        body = r.json()
        assert body["cerebro"] == "go"
        assert body["ok"] is True

    def test_health_champions(self):
        r = client.get("/api/v1/champions/health")
        assert r.status_code == 200
        body = r.json()
        assert body["cerebro"] == "champions"
        assert body["ok"] is True


class TestEyPAPI:
    def _payload_dano(self) -> dict:
        return {
            "atacante": {
                "nombre": "Miraidon",
                "tipos": ["electrico", "dragon"],
                "habilidad": "Motor Hadron",
                "item": "Choice Specs",
                "naturaleza": "timido",
                "nivel": 50,
                "stats_base": {"hp":100,"atq_fis":85,"def_fis":100,
                                "atq_esp":135,"def_esp":115,"vel":135},
                "evs": {"hp":4,"atq_fis":0,"def_fis":0,"atq_esp":252,"def_esp":0,"vel":252},
                "ivs": {"hp":31,"atq_fis":31,"def_fis":31,"atq_esp":31,"def_esp":31,"vel":31},
                "movimientos": [{"nombre":"Electro Drift","tipo":"electrico",
                                  "categoria":"especial","potencia":100,
                                  "precision":100,"pp":5,"prioridad":0}],
                "teratipo": None, "teraactivada": False,
            },
            "defensor": {
                "nombre": "Rillaboom",
                "tipos": ["planta"],
                "habilidad": "Bateria Hierba",
                "item": None,
                "naturaleza": "osado",
                "nivel": 50,
                "stats_base": {"hp":100,"atq_fis":125,"def_fis":90,
                                "atq_esp":60,"def_esp":70,"vel":85},
                "evs": {"hp":252,"atq_fis":252,"def_fis":6,"atq_esp":0,"def_esp":0,"vel":0},
                "ivs": {"hp":31,"atq_fis":31,"def_fis":31,"atq_esp":31,"def_esp":31,"vel":31},
                "movimientos": [{"nombre":"Grassy Glide","tipo":"planta",
                                  "categoria":"fisico","potencia":70,
                                  "precision":100,"pp":10,"prioridad":1}],
                "teratipo": None, "teraactivada": False,
            },
            "movimiento": {"nombre":"Electro Drift","tipo":"electrico",
                           "categoria":"especial","potencia":100,
                           "precision":100,"pp":5,"prioridad":0},
            "boost_atq": 0, "boost_def": 0, "boost_vel": 0,
            "pantallas": False, "critico": False, "n_rolls": 16,
        }

    def test_calculo_dano_ok(self):
        r = client.post("/api/v1/eyp/dano", json=self._payload_dano())
        assert r.status_code == 200
        body = r.json()
        assert body["cerebro"] == "eyp"
        assert body["ok"] is True
        assert body["data"]["dano_maximo"] >= body["data"]["dano_minimo"]
        assert len(body["data"]["rolls"]) == 16

    def test_invalid_evs_422(self):
        payload = self._payload_dano()
        payload["atacante"]["evs"]["hp"] = 300  # > 252
        r = client.post("/api/v1/eyp/dano", json=payload)
        assert r.status_code == 422

    def test_cerebros_aislados_eyp_no_acepta_payload_go(self):
        # Payload de GO no tiene los campos de EyP
        r = client.post("/api/v1/eyp/dano", json={"liga": "great", "pokemon": "Swampert"})
        assert r.status_code == 422


class TestLZAAPI:
    def _payload_dano(self) -> dict:
        return {
            "atacante": {
                "nombre": "Garchomp",
                "tipos": ["dragon", "tierra"],
                "stats": {"hp":170, "ataque":130, "defensa":95, "vel":102},
                "movimientos": [{
                    "nombre": "Garra Dragon",
                    "tipo": "dragon",
                    "categoria": "rapido",
                    "potencia": 80,
                    "startup_frames": 8,
                    "cooldown_ms": 600,
                    "alcance": "cuerpo_a_cuerpo",
                    "prioridad_accion": 0,
                }],
                "estado": "ninguno",
                "puede_mega": False, "mega_activa": False,
            },
            "defensor": {
                "nombre": "Togekiss",
                "tipos": ["hada", "volador"],
                "stats": {"hp":160, "ataque":75, "defensa":115, "vel":80},
                "movimientos": [{
                    "nombre": "Brillo Magico",
                    "tipo": "hada",
                    "categoria": "cargado",
                    "potencia": 80,
                    "startup_frames": 18,
                    "cooldown_ms": 1000,
                    "alcance": "cuerpo_a_cuerpo",
                    "prioridad_accion": 0,
                }],
                "estado": "ninguno",
                "puede_mega": False, "mega_activa": False,
            },
            "movimiento": {
                "nombre": "Garra Dragon",
                "tipo": "dragon",
                "categoria": "rapido",
                "potencia": 80,
                "startup_frames": 8,
                "cooldown_ms": 600,
                "alcance": "cuerpo_a_cuerpo",
                "prioridad_accion": 0,
            },
            "defensor_esquivando": False,
            "quemadura_activa": False,
        }

    def test_calculo_dano_lza(self):
        r = client.post("/api/v1/lza/dano", json=self._payload_dano())
        assert r.status_code == 200
        body = r.json()
        assert body["cerebro"] == "lza"
        assert body["ok"] is True
        assert body["data"]["cooldown_efectivo_ms"] == 600

    def test_cerebro_lza_aislado(self):
        r = client.post("/api/v1/lza/dano", json={"evs": {}, "ivs": {}})
        assert r.status_code == 422


class TestGOAPI:
    def _payload_cp(self) -> dict:
        # Nivel 18.5 es el optimo para Swampert IVs 0/15/14 en Great League (~1489 CP)
        return {
            "stats_base": {"ataque": 208, "defensa": 175, "hp": 225},
            "ivs": {"ataque": 0, "defensa": 15, "hp": 14},
            "nivel": 18.5,
            "liga": "great",
        }

    def _payload_dano(self) -> dict:
        pm_base = {
            "nombre": "Swampert",
            "tipos": ["agua", "tierra"],
            "stats_base": {"ataque": 208, "defensa": 175, "hp": 225},
            "ivs": {"ataque": 0, "defensa": 15, "hp": 14},
            "nivel": 27.5,
            "tipo_pokemon": "normal",
            "fast_move": {
                "nombre": "Pistola Agua", "tipo": "agua",
                "categoria": "rapido", "potencia": 5,
                "energia": 7, "duracion_turnos": 1,
            },
            "charged_moves": [{
                "nombre": "Hidrobomba", "tipo": "agua",
                "categoria": "cargado", "potencia": 130,
                "energia": -75, "duracion_turnos": 4,
            }],
            "energia_actual": 0,
        }
        return {
            "atacante": pm_base,
            "defensor": {**pm_base, "nombre": "Stunfisk-G",
                         "tipos": ["tierra","acero"],
                         "stats_base": {"ataque":166,"defensa":259,"hp":240}},
            "movimiento": {
                "nombre": "Hidrobomba", "tipo": "agua",
                "categoria": "cargado", "potencia": 130,
                "energia": -75, "duracion_turnos": 4,
            },
            "defensor_usa_escudo": False,
        }

    def test_calculo_cp_great_league(self):
        r = client.post("/api/v1/go/cp", json=self._payload_cp())
        assert r.status_code == 200
        body = r.json()
        assert body["cerebro"] == "go"
        assert body["ok"] is True
        assert body["data"]["cp"] >= 10
        assert body["data"]["dentro_del_cap"] is True

    def test_calculo_dano_go(self):
        r = client.post("/api/v1/go/dano", json=self._payload_dano())
        assert r.status_code == 200
        body = r.json()
        assert body["cerebro"] == "go"
        assert body["ok"] is True
        assert body["data"]["dano"] > 0

    def test_cerebro_go_aislado(self):
        r = client.post("/api/v1/go/cp", json={"naturaleza": "timido", "evs": {}})
        assert r.status_code == 422


class TestChampionsAPI:
    def _pokemon(self, nombre="Flutter Mane", tipos=None, hp=55, spa=135, spd=135):
        return {
            "nombre": nombre,
            "tipos": tipos or ["fantasma", "hada"],
            "stats_base": {
                "hp": hp, "ataque": 55, "defensa": 55,
                "ataque_especial": spa, "defensa_especial": spd, "velocidad": 135,
            },
            "evs": {"hp": 4, "ataque": 0, "defensa": 0,
                    "ataque_especial": 252, "defensa_especial": 0, "velocidad": 252},
            "ivs": {"hp": 31, "ataque": 31, "defensa": 31,
                    "ataque_especial": 31, "defensa_especial": 31, "velocidad": 31},
            "naturaleza": "modesto",
            "nivel": 50,
        }

    def test_dano_champions(self):
        payload = {
            "atacante": self._pokemon(),
            "defensor": self._pokemon("Garchomp", ["dragon", "tierra"], hp=50, spa=80, spd=50),
            "movimiento": "brillo_magico",
        }
        r = client.post("/api/v1/champions/dano", json=payload)
        assert r.status_code == 200
        body = r.json()
        assert body["cerebro"] == "champions"
        assert body["ok"] is True
        assert body["data"]["dano_maximo"] >= body["data"]["dano_minimo"]
        assert body["data"]["efectividad"] == 2.0   # hada vs dragon/tierra

    def test_dano_movimiento_invalido_422(self):
        payload = {
            "atacante": self._pokemon(),
            "defensor": self._pokemon(),
            "movimiento": "movimiento_que_no_existe_xyz",
        }
        r = client.post("/api/v1/champions/dano", json=payload)
        assert r.status_code == 422

    def test_catalogo_champions(self):
        r = client.get("/api/v1/champions/catalogo")
        assert r.status_code == 200
        body = r.json()
        assert body["cerebro"] == "champions"
        assert body["data"]["total"] > 0

    def test_catalogo_tier_s(self):
        r = client.get("/api/v1/champions/catalogo?tier=S")
        assert r.status_code == 200
        body = r.json()
        assert all(p["tier"] == "S" for p in body["data"]["pokemon"])

    def test_movimientos_champions(self):
        r = client.get("/api/v1/champions/movimientos")
        assert r.status_code == 200
        assert r.json()["data"]["total"] > 0

    def test_movimientos_por_tipo(self):
        r = client.get("/api/v1/champions/movimientos?tipo=dragon")
        assert r.status_code == 200
        movs = r.json()["data"]["movimientos"]
        assert all(m["tipo"] == "dragon" for m in movs)

    def test_cerebro_champions_aislado(self):
        # Payload de GO no puede ir a Champions
        r = client.post("/api/v1/champions/dano", json={"liga": "great", "pokemon": "Swampert"})
        assert r.status_code == 422


class TestAislamientoCerebros:
    """Verifica que los 4 cerebros no comparten estado ni se contaminan."""

    def test_endpoints_separados(self):
        r_eyp  = client.get("/api/v1/eyp/health")
        r_lza  = client.get("/api/v1/lza/health")
        r_go   = client.get("/api/v1/go/health")
        r_chmp = client.get("/api/v1/champions/health")
        assert r_eyp.json()["cerebro"]  == "eyp"
        assert r_lza.json()["cerebro"]  == "lza"
        assert r_go.json()["cerebro"]   == "go"
        assert r_chmp.json()["cerebro"] == "champions"

    def test_prefijos_no_se_mezclan(self):
        # /lza/validar-combate no existe en /eyp
        r = client.post("/api/v1/eyp/validar-combate", json={})
        assert r.status_code == 404 or r.status_code == 422

    def test_respuesta_incluye_cerebro_correcto(self):
        r = client.get("/api/v1/go/health")
        assert r.json()["cerebro"] == "go"
        assert r.json()["cerebro"] != "eyp"
        assert r.json()["cerebro"] != "champions"

    def test_champions_no_acepta_payload_eyp(self):
        # Payload EyP (con TipoElemental) no debe funcionar en Champions
        r = client.post("/api/v1/champions/dano", json={
            "atacante": {"tipos": ["electrico", "dragon"], "evs": {"atq_esp": 252}},
            "defensor": {},
            "movimiento": "brillo_magico",
        })
        assert r.status_code == 422
