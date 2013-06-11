#!/usr/bin/env python
# ! -*- coding: utf-8 -*-

from __future__ import absolute_import

import datetime
import Queue
import logging
import multiprocessing
import numpy
import os
import sys
import time
import matplotlib.pyplot as plt

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


def ejecutar_prueba(estados, gamma, tecnica_idx, parametro, cant_episodios,
                    paso_decremento, intervalo_decremento, limitar_iteraciones,
                    cant_max_iteraciones, valor_inicial, detener_por_diff,
                    diff_minima, interv_calculo_diff, nro_prueba):

    # Logging Config
    logging.basicConfig(level=logging.DEBUG,
                        format="[%(levelname)s] – %(threadName)-10s : %(message)s")

    gamma = float(gamma)

    tecnica_idx = int(tecnica_idx)
    if tecnica_idx == 0:
        tecnica = Greedy
    elif tecnica_idx == 1:
        tecnica = EGreedy
    elif tecnica_idx == 2:
        tecnica = Softmax
    elif tecnica_idx == 3:
        tecnica = Aleatorio

    cant_episodios = int(cant_episodios)
    parametro = float(parametro)
    paso_decremento = float(paso_decremento)
    intervalo_decremento = int(intervalo_decremento)

    if isinstance(limitar_iteraciones, bool):
        limitar_nro_iteraciones = limitar_iteraciones
    else:
        if limitar_iteraciones.strip().lower() == 'false':
            limitar_nro_iteraciones = False
        elif limitar_iteraciones.strip().lower() == 'true':
            limitar_nro_iteraciones = True

    cant_max_iter = int(cant_max_iteraciones)

    estado_excelente = window_config["tipos_estados"][TIPOESTADO.EXCELENTE]

    #===========================================================================
    # if valor_inicial == 0:
    #     init_value_fn = 0
    # elif valor_inicial > 0:
    #     init_value_fn = estado_excelente.recompensa + valor_inicial
    # else:
    #     init_value_fn = 0
    #===========================================================================
    init_value_fn = valor_inicial

    if isinstance(detener_por_diff, bool):
        matdiff_status = detener_por_diff
    else:
        if detener_por_diff.strip().lower() == 'false':
            matdiff_status = False
        elif detener_por_diff.strip().lower() == 'true':
            matdiff_status = True

    matriz_min_diff = float(diff_minima)
    intervalo_diff_calc = int(interv_calculo_diff)

    estados_num = eval(estados)

    ancho, alto = len(estados_num), len(estados_num[0])

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

    # logging.debug(entrenar_worker)

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

                sys.stdout.write("Estado actual: {0}\n".format(estado_actual_ent))
                sys.stdout.write("Número episodio: {0}\n".format(nro_episodio))
                sys.stdout.write("Iteración: {0}\n".format(cant_iteraciones))
                #===============================================================
                # sys.stdout.write("Estado actual: {0}\n \
                #                   Número episodio: {1}\n \
                #                   Iteración: {2}\n \
                #                   Tiempo ejecución episodio: {3}\n \
                #                   Tiempo ejecución iteración: {4}\n \
                #                   Loop Alarm: {5}\n \
                #                   Parámetro: {6}\n \
                #                   Tiempo de ejecución entrenamiento: {7}\n \
                #                   Diferencia entre matrices: {8}\n \
                #                   Corte por iteraciones: {9}\n\r".format(estado_actual_ent,
                #                                                     nro_episodio,
                #                                                     cant_iteraciones,
                #                                                     episode_exec_time,
                #                                                     iter_exec_time,
                #                                                     loop_alarm,
                #                                                     valor_parametro,
                #                                                     running_exec_time_ent,
                #                                                     tmp_mat_diff,
                #                                                     corte_iteracion
                #                                                     )
                #                   )
                # sys.stdout.flush()
                #===============================================================

                time.sleep(0.01)
        except Queue.Empty:
            pass
        except AttributeError:
            pass

        active_children = multiprocessing.active_children()
        for proceso in active_children:
            if not proceso.is_alive():
                proceso.join(0.01)

        if not active_children:
            entrenar_worker.join(0.01)
            break

    # logging.debug(graph_episodios_finalizados)
    # logging.debug(graph_recompensas_promedio)
    # logging.debug(matriz_q_inp)

    parametros = (gamma,
                 (tecnica_idx, parametro, paso_decremento, intervalo_decremento),
                 cant_episodios,
                 (limitar_nro_iteraciones, cant_max_iter),
                 init_value_fn
                 )

    graficar_recompensas_promedio((nro_prueba, parametros, graph_recompensas_promedio))
    graficar_episodios_exitosos((nro_prueba, parametros, graph_episodios_finalizados))


def get_all_from_queue(cola):
    try:
        while 1:
            yield cola.get_nowait()
    except Queue.Empty:
        raise StopIteration


def graficar_episodios_exitosos(tupla):
    nro_prueba = tupla[0]
    run_values = tupla[1]
    gamma = run_values[0]
    id_tecnica, parametro, paso_decrem, interv_decrem = run_values[1]
    cant_episodios = run_values[2]
    limitar_nro_iter, cant_max_iter = run_values[3]
    init_value = run_values[4]

    xy_values = tupla[2]
    x_values = [pair[0][0] for pair in xy_values if not numpy.equal(pair, None)]
    y_values = [pair[0][1] for pair in xy_values if not numpy.equal(pair, None)]

    figure = plt.gcf()
    figure.canvas.set_window_title(u"Definir título de la ventana")

    plt.plot(x_values, y_values)
    plt.grid(True)
    plt.title(u"Definir título del gráfico")
    plt.xlabel(u"Episodios")
    plt.ylabel(u"%")

    str_gamma = r"$\gamma={0}$".format(gamma)

    if id_tecnica == 0:
        str_tecnica = "Greedy"
        str_parametro = ""
    elif id_tecnica == 1:
        str_tecnica = r"$\epsilon$-Greedy"
        str_parametro = r"$\epsilon={0}$".format(parametro)
    elif id_tecnica == 2:
        str_tecnica = "Softmax"
        str_parametro = r"$\tau={0}$".format(parametro)
    elif id_tecnica == 3:
        str_tecnica = "Aleatorio"
        str_parametro = ""
    else:
        pass

    if limitar_nro_iter:
        str_limit_iter = "Limitar a {0} iteraciones".format(cant_max_iter)
    else:
        str_limit_iter = ""

    # Mostrar parámetros de entrenamiento
    plt.text(plt.axis()[0] + 5,
             plt.axis()[1] - 10,
             "{0}\n{1} ({2})\n".format(str_gamma,
                                       str_tecnica,
                                       str_parametro
                                      ),
             fontdict={'fontsize': 12}
             )

    fecha = datetime.datetime.now()
    output_dir = os.path.abspath(os.path.join(TEST_PATH, fecha.strftime("%d-%m-%Y")))

    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    test_dir = os.path.abspath(os.path.join(output_dir, "Prueba {0}".format(nro_prueba)))

    if not os.path.exists(test_dir):
        os.mkdir(test_dir)

    plt.savefig(os.path.abspath(os.path.join(test_dir, 'episodios_exitosos.png')))
    plt.close()


def graficar_recompensas_promedio(tupla):
    nro_prueba = tupla[0]
    run_values = tupla[1]
    gamma = run_values[0]
    id_tecnica, parametro, paso_decrem, interv_decrem = run_values[1]
    cant_episodios = run_values[2]
    limitar_nro_iter, cant_max_iter = run_values[3]
    init_value = run_values[4]

    xy_values = tupla[2]
    x_values = [pair[0][0] for pair in xy_values if not numpy.equal(pair, None)]
    y_porc = [(val[0][0] * 100) / float(val[0][1]) for val in xy_values if not numpy.equal(pair, None)]

    figure = plt.gcf()
    figure.canvas.set_window_title(u"Definir título de la ventana")

    plt.plot(x_values, y_porc)
    plt.grid(True)
    plt.title(u"Definir título del gráfico")
    plt.xlabel(u"Episodios")
    plt.ylabel(u"%")

    str_gamma = r"$\gamma={0}$".format(gamma)

    if id_tecnica == 0:
        str_tecnica = "Greedy"
        str_parametro = ""
    elif id_tecnica == 1:
        str_tecnica = r"$\epsilon$-Greedy"
        str_parametro = r"$\epsilon={0}$".format(parametro)
    elif id_tecnica == 2:
        str_tecnica = "Softmax"
        str_parametro = r"$\tau={0}$".format(parametro)
    elif id_tecnica == 3:
        str_tecnica = "Aleatorio"
        str_parametro = ""
    else:
        pass

    if limitar_nro_iter:
        str_limit_iter = "Limitar a {0} iteraciones".format(cant_max_iter)
    else:
        str_limit_iter = ""

    # Mostrar parámetros de entrenamiento
    plt.text(plt.axis()[0] + 5,
             plt.axis()[1] - 10,
             "{0}\n{1} ({2})\n".format(str_gamma,
                                       str_tecnica,
                                       str_parametro
                                      ),
             fontdict={'fontsize': 12}
             )

    fecha = datetime.datetime.now()
    output_dir = os.path.abspath(os.path.join(TEST_PATH, fecha.strftime("%d-%m-%Y")))

    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    test_dir = os.path.abspath(os.path.join(output_dir, "Prueba {0}".format(nro_prueba)))

    if not os.path.exists(test_dir):
        os.mkdir(test_dir)

    plt.savefig(os.path.abspath(os.path.join(test_dir, 'recompensas_promedio.png')))
    plt.close()


if __name__ == '__main__':
    TEST_PATH = os.path.abspath(os.path.join(os.pardir, '..', 'pruebas'))

    archivo_pruebas = os.path.join(TEST_PATH, 'pruebas.csv')

    with open(archivo_pruebas, 'r') as apf:
        contador_pruebas = 1

        for linea_prueba in apf:
            if (linea_prueba.strip() != '') and (not linea_prueba.startswith('#')):
                items = linea_prueba.split(';')

                sys.stdout.write("Ejecutando prueba {0}\n".format(contador_pruebas))
                try:
                    ejecutar_prueba(items[0],
                                    items[1],
                                    items[2],
                                    items[3],
                                    items[4],
                                    items[5],
                                    items[6],
                                    items[7],
                                    items[8],
                                    items[9],
                                    items[10],
                                    items[11],
                                    items[12],
                                    contador_pruebas)
                    sys.stdout.write("Prueba {0} OK\n".format(contador_pruebas))
                except TypeError:
                    sys.stdout.write("Prueba {0} ERROR\n".format(contador_pruebas))
                    continue
                except ValueError:
                    sys.stdout.write("Prueba {0} ERROR\n".format(contador_pruebas))
                    continue
                except AttributeError:
                    sys.stdout.write("Prueba {0} ERROR".format(contador_pruebas))
                #===============================================================

                contador_pruebas += 1
        sys.stdout.write("Fin de pruebas")
