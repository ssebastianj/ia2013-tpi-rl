#!/usr/bin/env python
# ! -*- coding: utf-8 -*-

from __future__ import absolute_import

import csv
import decimal
import Queue
import logging
import multiprocessing
import numpy
import os
import sys
import time

sys.path.append(os.path.abspath(os.path.join(os.pardir)))

from core.qlearning.qlearning import QLearning
from core.gridworld.gridworld import GridWorld
from core.estado.estado import Estado, TipoEstado, TIPOESTADO
from core.tecnicas.aleatorio import Aleatorio
from core.tecnicas.egreedy import EGreedy, Greedy
from core.tecnicas.softmax import Softmax

from graphs.avgrwds.worker import GraphRecompensasPromedioWorker
from graphs.sucessfuleps.worker import GraphSucessfulEpisodesWorker
from graphs.matdiffs.worker import GraphMatrizDiffsWorker
from graphs.itersep.worker import GraphIteracionesXEpisodioWorker

TESTS_DIR = os.path.abspath(os.path.join(os.pardir, '..', 'pruebas'))

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
                    diff_minima, interv_calculo_diff, nro_prueba, output_dir):

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
    estado_final = window_config["tipos_estados"][TIPOESTADO.FINAL]

    if valor_inicial == 0:
        init_value_fn = 0
    elif valor_inicial > 0:
        init_value_fn = estado_final.recompensa + valor_inicial
    else:
        init_value_fn = 0

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

    # Crear GridWorld de estados
    estados = numpy.empty((alto, ancho), Estado)
    coordenadas = []

    tipos_estados = window_config["tipos_estados"]

    # Crear una lista de listas
    for i in xrange(1, alto + 1):
        fila = numpy.empty((1, ancho), Estado)
        for j in xrange(1, ancho + 1):
            fila[0][j - 1] = Estado(i, j, tipos_estados[estados_num[i - 1][j - 1]])
            coordenadas.append((i, j))
        estados[i - 1] = fila

    gridworld = GridWorld(ancho, alto, tipos_estados, estados, [TIPOESTADO.PARED])

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
    try:
        entrenar_worker = qlearning.entrenar(out_queue, error_queue)
    except TypeError:
        return
    except ValueError:
        return
    except AttributeError:
        return
    except decimal.Overflow:
        return

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
                matriz_q_inp = ql_ent_info.get('MatrizQ', None)
                valor_parametro = ql_ent_info.get('ValorParametro', None)
                running_exec_time_ent = ql_ent_info.get('RunningExecTime', 0.0)
                tmp_mat_diff = ql_ent_info.get('MatDiff', None)
                corte_iteracion = ql_ent_info.get('CorteIteracion', None)
                graph_recompensas_promedio = ql_ent_info.get('MatRecompProm', None)
                graph_episodios_finalizados = ql_ent_info.get('EpFinalizados', None)
                graph_mat_diff = ql_ent_info.get('MatDiffStat', None)
                graph_iters_por_episodio = ql_ent_info.get('ItersXEpisodio', None)

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

    test_dir = os.path.abspath(os.path.join(output_dir, "Prueba_{0}".format(nro_prueba)))
    if not os.path.exists(test_dir):
        os.mkdir(test_dir)
    csv_path = os.path.abspath(os.path.join(test_dir, 'info.csv'))

    with open(csv_path, 'wb') as csvf:
        csv_writer = csv.writer(csvf, dialect='excel', delimiter=';')
        csv_writer.writerow(['Gamma', gamma])
        csv_writer.writerow(['Tecnica', tecnicas[tecnica_idx]])
        csv_writer.writerow(['Parametro', parametro])
        csv_writer.writerow(['Paso decremento', paso_decremento])
        csv_writer.writerow(['Intervalo decremento', intervalo_decremento])
        csv_writer.writerow(['Episodios', cant_episodios])
        csv_writer.writerow(['Limitar iteraciones', limitar_iteraciones])
        csv_writer.writerow(['Cant. Max. Iteraciones', cant_max_iter])
        csv_writer.writerow(['Valor Inicial', init_value_fn])
        csv_writer.writerow([])

    graficar_recompensas_promedio((parametros, graph_recompensas_promedio), nro_prueba, output_dir)
    # graficar_episodios_exitosos((parametros, graph_episodios_finalizados), nro_prueba, output_dir)
    # graficar_iters_por_episodio((parametros, graph_iters_por_episodio), nro_prueba, output_dir)
    graficar_diferencias_matrizq((parametros, graph_mat_diff), nro_prueba, output_dir)


def get_all_from_queue(cola):
    try:
        while 1:
            yield cola.get_nowait()
    except Queue.Empty:
        raise StopIteration


def graficar_episodios_exitosos(tupla, nro_prueba, output_dir):
    worker = GraphSucessfulEpisodesWorker(tupla)

    test_dir = os.path.abspath(os.path.join(output_dir, "Prueba_{0}".format(nro_prueba)))

    if not os.path.exists(test_dir):
        os.mkdir(test_dir)

    image_path = os.path.abspath(os.path.join(test_dir, 'episodios_exitosos.png'))
    worker.guardar_dibujo(image_path)

    csv_path = os.path.abspath(os.path.join(test_dir, 'info.csv'))
    worker.exportar_info(csv_path, True)


def graficar_recompensas_promedio(tupla, nro_prueba, output_dir):
    worker = GraphRecompensasPromedioWorker(tupla)

    test_dir = os.path.abspath(os.path.join(output_dir, "Prueba_{0}".format(nro_prueba)))

    if not os.path.exists(test_dir):
        os.mkdir(test_dir)

    image_path = os.path.abspath(os.path.join(test_dir, 'recompensas_promedio.png'))
    worker.guardar_dibujo(image_path)

    csv_path = os.path.abspath(os.path.join(test_dir, 'info.csv'))
    worker.exportar_info(csv_path, True)


def graficar_iters_por_episodio(tupla, nro_prueba, output_dir):
    worker = GraphIteracionesXEpisodioWorker(tupla)

    test_dir = os.path.abspath(os.path.join(output_dir, "Prueba_{0}".format(nro_prueba)))

    if not os.path.exists(test_dir):
        os.mkdir(test_dir)

    image_path = os.path.abspath(os.path.join(test_dir, 'iters_por_ep.png'))
    worker.guardar_dibujo(image_path)

    csv_path = os.path.abspath(os.path.join(test_dir, 'info.csv'))
    worker.exportar_info(csv_path, True)


def graficar_diferencias_matrizq(tupla, nro_prueba, output_dir):
    worker = GraphMatrizDiffsWorker(tupla)

    test_dir = os.path.abspath(os.path.join(output_dir, "Prueba_{0}".format(nro_prueba)))

    if not os.path.exists(test_dir):
        os.mkdir(test_dir)

    image_path = os.path.abspath(os.path.join(test_dir, 'difs_mat_q.png'))
    worker.guardar_dibujo(image_path)

    csv_path = os.path.abspath(os.path.join(test_dir, 'info.csv'))
    worker.exportar_info(csv_path, True)


if __name__ == '__main__':
    lista_archivos_pruebas = []

    sys.stdout.write("Indexando archivos de pruebas...\n")
    for root, folder, archivos in os.walk(TESTS_DIR):
        for archivo in archivos:
            if archivo.endswith(".csv") and archivo != "info.csv":
                lista_archivos_pruebas.append(os.path.join(root, archivo))

    for archivo_pruebas in lista_archivos_pruebas:
        sys.stdout.write("Usando archivo '{0}'...\n".format(archivo_pruebas))

        nombre_archivo = os.path.splitext(os.path.basename(archivo_pruebas))[0]
        test1_dir = os.path.abspath(os.path.join(os.path.dirname(archivo_pruebas),
                                                'resultados'))

        if not os.path.exists(test1_dir):
            os.mkdir(test1_dir)

        test2_dir = os.path.abspath(os.path.join(test1_dir, nombre_archivo))

        if not os.path.exists(test2_dir):
            os.mkdir(test2_dir)

        with open(archivo_pruebas, 'rb') as apf:
            # dialecto = csv.Sniffer().sniff(apf.read(), delimiters=';')
            inp_csv = csv.reader(apf, dialect='excel', delimiter=';')

            contador_pruebas = 1

            for linea_prueba in inp_csv:
                sys.stdout.write("Ejecutando prueba {0}... ".format(contador_pruebas))

                try:
                    ejecutar_prueba(linea_prueba[0],
                                    linea_prueba[1],
                                    linea_prueba[2],
                                    linea_prueba[3],
                                    linea_prueba[4],
                                    linea_prueba[5],
                                    linea_prueba[6],
                                    linea_prueba[7],
                                    linea_prueba[8],
                                    linea_prueba[9],
                                    linea_prueba[10],
                                    linea_prueba[11],
                                    linea_prueba[12],
                                    contador_pruebas,
                                    test2_dir)

                    sys.stdout.write("Prueba {0} OK\n".format(contador_pruebas))
                    contador_pruebas += 1
                except decimal.Overflow:
                    sys.stdout.write("Prueba {0} ERROR\n".format(contador_pruebas))
                    contador_pruebas += 1
                    continue
                except TypeError:
                    sys.stdout.write("Prueba {0} ERROR\n".format(contador_pruebas))
                    contador_pruebas += 1
                    continue
                except ValueError:
                    sys.stdout.write("Prueba {0} ERROR\n".format(contador_pruebas))
                    contador_pruebas += 1
                    continue
                except AttributeError:
                    sys.stdout.write("Prueba {0} ERROR\n".format(contador_pruebas))
                    contador_pruebas += 1
                    continue
                except multiprocessing.ProcessError:
                    sys.stdout.write("Prueba {0} ERROR\n".format(contador_pruebas))
                    contador_pruebas += 1
                    continue

            sys.stdout.write("Fin de pruebas\n\n")
