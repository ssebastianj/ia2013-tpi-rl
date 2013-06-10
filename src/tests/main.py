#!/usr/bin/env python
# ! -*- coding: utf-8 -*-

from __future__ import absolute_import

import Queue
import logging
import multiprocessing
import numpy
import time

from core.qlearning.qlearning import QLearning
from core.gridworld.gridworld import GridWorld
from core.estado.estado import Estado, TipoEstado, TIPOESTADO
from core.tecnicas.aleatorio import Aleatorio
from core.tecnicas.egreedy import EGreedy, Greedy
from core.tecnicas.softmax import Softmax


tecnicas = {0: "Greedy",
            1: "ε-Greedy",
            2: "Softmax",
            3: "Aleatorio"
            }

gw_dimensiones = ["3 x 3", "4 x 4", "5 x 5",
                  "6 x 6", "7 x 7", "8 x 8", "9 x 9", "10 x 10"]

window_config = {"item":
                  {"show_tooltip": True,
                   "menu_estado":
                   {"ocultar_tipos":
                    [TIPOESTADO.AGENTE],
                    "enabled": True
                    },
                   "size": 40},
                  "gw":
                 {"entrenamiento": {"actual_state": {"show": True, "color": "#000000", "icono": None},
                                    "recompfinalauto": True},
                  "recorrido": {"actual_state": {"show": True, "color": "#000000", "icono": None}}
                  },
                  "tipos_estados":
                  {0: TipoEstado(0, None, "Inicial", "I", "#FF5500", None),
                   1: TipoEstado(1, 1000, "Final", "F", "#00AB00", None),
                   2: TipoEstado(2, None, "Agente", "A", "#474747", None),
                   3: TipoEstado(3, 0, "Neutro", "N", "#FFFFFF", None),
                   4: TipoEstado(4, 100, "Excelente", "E", "#BB0011", None),
                   5: TipoEstado(5, 50, "Bueno", "B", "#4F0ACC", None),
                   6: TipoEstado(6, -50, "Malo", "M", "#EB00A1", None),
                   7: TipoEstado(7, None, "Pared", "P", "#000000", None),
                   },
                  "opt_path":
                 {"color": "#55FF00",
                     "pintar_inicial": False,
                     "pintar_final": False,
                     "delay": 0,
                     "show_icon": False
                  },
                  "exponentes_final": {6: 12,
                                       7: 17,
                                       8: 19,
                                       9: 28,
                                       10: 31
                                       }
                  }


def test1():
    # Logging Config
    logging.basicConfig(level=logging.DEBUG,
                        format="[%(levelname)s] – %(threadName)-10s : %(message)s")

    gamma = 0.8
    tecnica = EGreedy
    cant_episodios = 10
    parametro = 0.1
    paso_decremento = 0.01
    intervalo_decremento = 1
    limitar_nro_iteraciones = False
    cant_max_iter = 200
    init_value_fn = 0
    matdiff_status = False
    matriz_min_diff = 0.0001
    intervalo_diff_calc = 10

    estados_num = [[3, 3, 3, 3, 3, 3],
                   [3, 3, 3, 3, 3, 3],
                   [3, 3, 3, 3, 3, 3],
                   [3, 3, 3, 3, 3, 3],
                   [3, 3, 3, 3, 3, 3],
                   [3, 3, 3, 3, 3, 1]]

    ancho, alto = len(estados_num), len(estados_num[0])

    estado_excelente = window_config["tipos_estados"][TIPOESTADO.EXCELENTE]
    recomp_excelente = estado_excelente.recompensa
    exponente = window_config["exponentes_final"][ancho]

    calc_recomp_final = int(recomp_excelente / (gamma ** exponente))

    estado_final_cfg = window_config["tipos_estados"][TIPOESTADO.FINAL]
    estado_final_cfg.recompensa = calc_recomp_final

    estados = numpy.empty((alto, ancho), Estado)
    coordenadas = []

    # Crear una lista de listas
    for i in xrange(1, alto + 1):
        fila = numpy.empty((1, ancho), Estado)
        for j in xrange(1, ancho + 1):
            fila[0][j - 1] = Estado(i, j, window_config["tipos_estados"][estados_num[i - 1][j - 1]])
            coordenadas.append((i, j))
        estados[i - 1] = fila

    gridworld = GridWorld(ancho, alto, window_config["tipos_estados"], estados, [TIPOESTADO.PARED])

    estado_final_gw = gridworld.tipos_estados[TIPOESTADO.FINAL]
    estado_final_gw.recompensa = calc_recomp_final

    # Crear una nueva instancia de Q-Learning
    qlearning = QLearning(gridworld,
                          gamma,
                          (tecnica, parametro, paso_decremento, intervalo_decremento),
                          cant_episodios,
                          (limitar_nro_iteraciones, cant_max_iter),
                          init_value_fn,
                          (matdiff_status, matriz_min_diff, intervalo_diff_calc),
                          None)

    out_queue = multiprocessing.Queue()
    error_queue = multiprocessing.Queue()
    entrenar_worker = qlearning.entrenar(out_queue, error_queue)

    logging.debug(entrenar_worker)

    matriz_q_inp = None
    graph_recompensas_promedio = None
    graph_episodios_finalizados = None

    while True:
        try:
            data_entrenar = get_all_from_queue(out_queue)

            for ql_ent_info in data_entrenar:
                estado_actual_ent = ql_ent_info.get('EstadoActual', None)
                nro_episodio = ql_ent_info.get('NroEpisodio', None)
                cant_iteraciones = ql_ent_info.get('NroIteracion', None)
                episode_exec_time = ql_ent_info.get('EpisodiosExecTime', 0.0)
                iter_exec_time = ql_ent_info.get('IteracionesExecTime', 0.0)
                worker_joined = ql_ent_info.get('ProcesoJoined', False)
                loop_alarm = ql_ent_info.get('LoopAlarm', False)
                matriz_q = ql_ent_info.get('MatrizQ', None)
                valor_parametro = ql_ent_info.get('ValorParametro', None)
                running_exec_time_ent = ql_ent_info.get('RunningExecTime', 0.0)
                tmp_mat_diff = ql_ent_info.get('MatDiff', None)
                corte_iteracion = ql_ent_info.get('CorteIteracion', None)
                recompensas_promedio = ql_ent_info.get('RecompProm', None)
                episodios_finalizados = ql_ent_info.get('EpFinalizados', None)

                matriz_q_inp = matriz_q
                graph_recompensas_promedio = recompensas_promedio
                graph_episodios_finalizados = episodios_finalizados

                logging.debug(estado_actual_ent)
                logging.debug(nro_episodio)
                logging.debug(cant_iteraciones)
                logging.debug(episode_exec_time)
                logging.debug(iter_exec_time)
                logging.debug(loop_alarm)
                logging.debug(valor_parametro)
                logging.debug(running_exec_time_ent)
                logging.debug(tmp_mat_diff)
                logging.debug(corte_iteracion)

                time.sleep(0.05)
        except Queue.Empty:
            pass
        except AttributeError:
            pass

        active_children = multiprocessing.active_children()
        for proceso in active_children:
            if not proceso.is_alive():
                proceso.join(0.01)

        if not active_children:
            break

    logging.debug(graph_episodios_finalizados)
    logging.debug(graph_recompensas_promedio)
    logging.debug(matriz_q_inp)


def get_all_from_queue(cola):
    try:
        while 1:
            yield cola.get_nowait()
    except Queue.Empty:
        raise StopIteration


if __name__ == '__main__':
    test1()
