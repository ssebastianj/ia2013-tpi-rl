#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import Queue
import multiprocessing
import numpy
import time
import sys
import random

from core.estado.estado import TIPOESTADO


# ============================================================================
#                         QLearningEntrenarWorker
# ============================================================================
class QLearningEntrenarWorker(multiprocessing.Process):
    u"""
    Worker encargado de realizar el aprendizaje de Q-Learning.
    """
    def __init__(self, inp_queue, out_queue, error_q):
        """
        Inicializador del worker.

        :param inp_queue: Cola de entrada.
        :param out_queue: Cola de salida de datos.
        :param error_q: Cola de salida de errores.
        """
        super(QLearningEntrenarWorker, self).__init__()
        self._inp_queue = inp_queue
        self._out_queue = out_queue
        self._error_queue = error_q
        self._stoprequest = multiprocessing.Event()
        self._pauserequest = multiprocessing.Event()
        self.name = "QLearningEntrenarWorker"
        self.input_data = None
        self._visitados_1 = None
        self._visitados_2 = None
        self._contador_ref = None
        self.matriz_r = None
        self.matriz_q = None
        self.estados = None
        self.tipos_vec_excluidos = None

    def _do_on_start(self):
        u"""
        Ejecuta tareas al comenzar el thread.
        """
        pass

    def _on_end(self):
        u"""
        Ejecuta tareas al finalizar el thread.
        """
        # Cerrar Queues
        self._inp_queue.close()
        self._inp_queue.join_thread()

        self._error_queue.close()
        self._error_queue.join_thread()

        self._out_queue.close()
        self._out_queue.join_thread()

    def run(self):
        u"""
        Método sobrecargado de clase padre Thread. Ejecuta el algoritmo de
        aprendizaje de Q-Learning.
        """
        # En Windows se obtiene mayor precisión al utilizar clock()
        # En UNIX conviene utilizar time()
        if sys.platform == 'win32':
            wtimer = time.clock
        else:
            wtimer = time.time

        # Registrar tiempo de comienzo
        running_start_time = wtimer()

        # Realizar tareas al comienzo
        self._do_on_start()

        # Procesar datos de entrada
        self.procesar_entrada()

        # Cachear acceso a funciones y atributos de instancia
        encolar_salida = self.encolar_salida
        generar_estado_aleatorio = self.generar_estado_aleatorio
        matriz_r = self.matriz_r
        matriz_q = self.matriz_q
        matriz_est_acc = self.matriz_est_acc
        tipos_vec_excluidos = self.tipos_vec_excluidos
        detectar_bloqueo = self.detector_bloqueo
        contar_ref = self._contar_ref
        gamma = self.gamma
        limitar_iteraciones = self.limitar_iteraciones
        cant_max_iteraciones = self.cant_max_iter
        stoprequest_isset = self._stoprequest.is_set
        pauserequest_isset = self._pauserequest.is_set
        obtener_accion = self.tecnica.obtener_accion
        tecnica = self.tecnica
        intervalo_diff_calc = self.interv_diff_calc
        ancho = self.ancho
        alto = self.alto
        inp_queue = self._inp_queue
        out_queue = self._out_queue
        # --------------------------------------------------------------------

        # Cantidad máxima de iteraciones antes de emitir un aviso
        cant_max_iter_general, stop_action = (self.cant_max_iter_gral_pack[0],
                                              self.cant_max_iter_gral_pack[1])

        # FIXME: Detector de bloqueos
        if detectar_bloqueo:
            self._contador_ref = self._crear_cont_ref(tipos_vec_excluidos)
            self._cant_estados_libres = len(self._contador_ref)
            self._visitados_1 = []
            self._visitados_2 = []

        # Variable utilizada para saber cuando decrementar el parámetro de la técnica
        decrementar_step = 0

        # Descontador utilizado para saber en que momento calcular la diferencia
        # entre dos matrices Q
        calc_mat_diff_cont = intervalo_diff_calc - 1

        # Bandera que determina si se calcula la diferencia de matrices
        matdiff_active = self.matdiff_status

        # Inicializar variable auxiliar de cálculo de diferencia
        tmp_diff_mat = 0

        # Matriz Q temporal
        matriz_anterior = None

        min_diff_mat = self.min_diff_mat  # Diferencia mínima entre matrices
        # Diferencia mínima temporal entre matrices (calculada)
        # Se le suma 1 para que la condición para entrar en el bucle 'while'
        # se cumpla al comenzar
        cantidad_episodios = self.cant_episodios  # Cantidad de episodios a ejecutar
        epnum = 1  # Inicializadoralizar número de episodio
        cant_cortes_iteraciones = 0

        # --- Estadísticas para gráficos -------------------------------------
        # --------------------------------------------------------------------
        # Contador de accesos a acción
        rp_cont_acc_accion = numpy.zeros((self.ancho, self.alto), numpy.int)
        # Sumatoria de recompensas inmediatas
        rp_sum_recomp_accion = numpy.zeros((self.ancho, self.alto), numpy.float)
        # Resultado de recompensas promedio de los estados elegidos
        rp_res_promedio = numpy.empty((cantidad_episodios, 1), numpy.float)
        # --------------------------------------------------------------------

        # --------------------------------------------------------------------
        # Cantidad de veces que se llegó al Estado Final
        cant_lleg_final = 0
        # Cantidad de episodios entre muestreo
        inter_muestreo = int(cantidad_episodios / (cantidad_episodios ** 0.5))
        # Contador para determinar cuando hacer el muestreo
        cont_interv_muestreo = 0
        # Contador para indexar el arreglo de Numpy
        contador_idx_arr = 0
        # Lista con episodios finalizados
        episodios_finalizados = numpy.empty((inter_muestreo + 1, 1), object)

        # --------------------------------------------------------------------
        # Cantidad de iteraciones por episodio
        # iters_por_episodio = numpy.empty((cantidad_episodios, 1), numpy.int)

        # Evolución de la diferencia entre matrices Q
        mat_diff_array = [intervalo_diff_calc, []]
        # ---------------------------------

        # Registrar tiempo de comienzo de los episodios
        ep_start_time = wtimer()

        # Ejecutar una cantidad dada de episodios o detener antes si se considera necesario
        while (not stoprequest_isset()) and (epnum <= cantidad_episodios):

            # Obtener coordenadas aleatorias y obtener Estado asociado
            x_act, y_act = generar_estado_aleatorio()

            # Normalizar coordenadas para uso interno
            # x_act -= 1
            # y_act -= 1

            # Generar estados aleatorios hasta que las coordenadas no
            # coincidan con las de un tipo excluido
            estado_actual = matriz_est_acc[x_act][y_act]

            # Obtener tipo de estado
            try:
                tipo_estado = estado_actual[0]
            except (TypeError, IndexError):
                tipo_estado = estado_actual

            # Generar nuevo número aleatorio si el actual se encuentra dentro
            # de la lista de tipos excluidos
            while (not stoprequest_isset()) and (tipo_estado in tipos_vec_excluidos):
                x_act, y_act = generar_estado_aleatorio()
                estado_actual = matriz_est_acc[x_act][y_act]

                # Obtener tipo de estado
                try:
                    tipo_estado = estado_actual[0]
                except (TypeError, IndexError):
                    tipo_estado = estado_actual

            # Recorrer hasta encontrar el estado final
            cant_iteraciones = 1
            while (not stoprequest_isset()) and (tipo_estado != TIPOESTADO.FINAL):
                # Registrar tiempo de comienzo de las iteraciones
                iter_start_time = wtimer()

                # TODO: Utilizar detector de bloqueos
                if detectar_bloqueo:
                    contar_ref((x_act, y_act))

                # Coordenada Y de la matriz (fila)
                # Para acceder a un elemento de la matriz Q o R se utiliza un esquema
                # de acceso del tipo "Base + Desplazamiento" donde las filas
                # representan los estados del GridWorld y las columnas representan
                # las acciones posibles apartir de dichos estados.
                fila_idx = (x_act * alto) + y_act

                # Obtener acciones posibles para el estado actual
                acciones = matriz_q[fila_idx]

                # Invocar a la técnica para que seleccione uno de las acciones
                accion_elegida = obtener_accion(acciones)

                # Coordenada X de la matriz (columna)
                columna_idx = accion_elegida

                # Obtener recompensa inmediata de la acción actual
                recompensa_accion = matriz_r[fila_idx][columna_idx]

                # Obtener vecinos del estado elegido por la acción
                acciones_est_elegido = matriz_q[accion_elegida]

                # Calcular el máximo valor Q de todos los vecinos
                max_q = numpy.nanmax(acciones_est_elegido)

                # =============================================================
                # Función de valor de Q-Learning
                # =============================================================
                nuevo_q = recompensa_accion + (gamma * max_q)

                # Actualizar valor de Q en matriz Q
                matriz_q[fila_idx][columna_idx] = nuevo_q
                # =============================================================

                encolar_salida({'EstadoActual': (x_act + 1, y_act + 1),
                                'NroEpisodio': epnum,
                                'NroIteracion': cant_iteraciones,
                                'ValorParametro': tecnica.valor_param_parcial,
                                'ProcesoJoined': False,
                                'ProcesoPaused': False
                                })

                # ------------ Recompensas promedio ---------------------------
                # Incrementar acceso y guardar recompensa inmediata para estadística
                rp_cont_acc_accion[x_act][y_act] += 1
                rp_sum_recomp_accion[x_act][y_act] += recompensa_accion
                # ------------------------------------------------------------

                # Calcular coordenadas y actualizar estado actual
                new_x = int(columna_idx / alto)
                new_y = columna_idx - (new_x * ancho)
                estado_actual = matriz_est_acc[new_x][new_y]

                # Obtener tipo de estado
                try:
                    tipo_estado = estado_actual[0]
                except (TypeError, IndexError):
                    tipo_estado = estado_actual

                # Nuevo estado = Acción elegida
                x_act, y_act = new_x, new_y

                # Comprobar si se alcanzó el número máximo de iteraciones
                # FIXME
                if limitar_iteraciones and (cant_max_iteraciones == cant_iteraciones):
                    # self.encolar_salida({'CorteIteracion': True})
                    cant_cortes_iteraciones += 1
                    cant_lleg_final -= 1
                    # Terminar y comenzar en un episodio nuevo
                    break

                # Comprobar si se alcanzó el número máximo de iteraciones general
                if cant_max_iter_general == cant_iteraciones:
                    if stop_action == 0:
                        # Finalizar ejecución de proceso
                        encolar_salida({'LoopAlarm': (True, 0)})
                        self._stoprequest.set()
                    elif stop_action == 1:
                        encolar_salida({'LoopAlarm': (True, 1)})
                        # Continuar con el siguiente episodio
                        break

                # Incrementar cantidad de iteraciones realizadas
                cant_iteraciones += 1

                # FIXME
                # iters_por_episodio[epnum - 1] = cant_iteraciones

                # ---------------------- Pausa --------------------------
                # ------------ Primer verificación ----------------------
                # Comprobar si se solicitó pausar el procesamiento
                if pauserequest_isset():
                    # Encolar datos de salida (Dump del contexto actual)
                    encolar_salida({'EstadoActual': (x_act + 1, y_act + 1),
                                    'NroEpisodio': epnum - 1,
                                    'NroIteracion': cant_iteraciones,
                                    'MatrizQ': matriz_q,
                                    'ProcesoJoined': False,
                                    'ProcesoPaused': True,
                                    'ValorParametro': tecnica.valor_param_parcial,
                                    'MatDiff': tmp_diff_mat,
                                    })

                    # Esperar 1 segundo
                    time.sleep(1)
                # ==================== Fin de iteraciones ====================

            iter_end_time = wtimer()

            try:
                # Calcular tiempo de ejecución de las iteraciones
                iter_exec_time = iter_end_time - iter_start_time
            except UnboundLocalError:
                iter_exec_time = 0

            decrementar_step += 1
            # Comprobar si es necesario decrementar el valor del parámetro
            if tecnica.intervalo_decremento == decrementar_step:
                # Decrementar valor del parámetro en 1 paso
                tecnica.decrementar_parametro()
                decrementar_step = 0

            # ------------------------------------------------------------------
            if matdiff_active:
                if calc_mat_diff_cont == 0:
                        # Realizar resta de ambas matrices Q
                        resta = numpy.subtract(matriz_q, matriz_anterior)
                        # Calcular potencia
                        potencia = numpy.power(resta, 2)
                        # Calcular error medio cuadrático
                        tmp_diff_mat = numpy.nansum(potencia) / numpy.sum(~numpy.isnan(potencia))

                        # Almacenar para estadística
                        mat_diff_array[1].append(tmp_diff_mat)

                        # Comprobar si la diferencia entre matrices supera la establecida
                        # por el usuario
                        if tmp_diff_mat < min_diff_mat:
                            self._stoprequest.set()

                        # Volver a cargar valor inicial a contador
                        calc_mat_diff_cont = intervalo_diff_calc
                elif calc_mat_diff_cont == 1:
                    # Resguardar Matriz Q creando una copia
                    matriz_anterior = numpy.copy(matriz_q)

                # Poner en la cola de salida los resultados
                encolar_salida({'EstadoActual': (x_act + 1, y_act + 1),
                                'NroEpisodio': epnum,
                                'NroIteracion': cant_iteraciones,
                                'IteracionesExecTime': iter_exec_time,
                                'ValorParametro': tecnica.valor_param_parcial,
                                'ProcesoJoined': False,
                                'ProcesoPaused': False,
                                'MatDiff': tmp_diff_mat,
                                })

                # Decrementar contador para saber si es necesario calcular
                # la diferencia entre las matrices Q
                calc_mat_diff_cont -= 1

            # Incrementar cantidad de accesos al Estado Final
            # FIXME
            cant_lleg_final += 1

            # Incrementar contador de muestreo
            # FIXME
            cont_interv_muestreo += 1

            # Registrar cuantas veces se llegó al Estado Final
            # FIXME: Estadística
            if cont_interv_muestreo == inter_muestreo:
                episodios_finalizados[contador_idx_arr][0] = (epnum, cant_lleg_final)
                contador_idx_arr += 1
                # Reiniciar contador
                cont_interv_muestreo = 0

            # Recompensas promedio -------------------------------------------
            rp_res_promedio[epnum - 1][0] = numpy.average(numpy.true_divide(rp_sum_recomp_accion,
                                                                            rp_cont_acc_accion))

            # Avanzar un episodio
            epnum += 1

            # ---------------------- Pausa --------------------------
            # ------------ Segunda verificación ---------------------
            # Comprobar si se solicitó pausar el procesamiento
            if pauserequest_isset():
                # Encolar datos de salida (Dump del contexto actual)
                encolar_salida({'EstadoActual': (x_act + 1, y_act + 1),
                                'NroEpisodio': epnum - 1,
                                'NroIteracion': cant_iteraciones,
                                'MatrizQ': matriz_q,
                                'ProcesoJoined': False,
                                'ProcesoPaused': True,
                                'ValorParametro': tecnica.valor_param_parcial,
                                'MatDiff': tmp_diff_mat,
                                })

                # Esperar 1 segundo
                time.sleep(1)
            # ======================= Fin de episodios =======================

        # FIXME: Estadística
        # Incluir estadísticas del último episodio
        try:
            episodios_finalizados[contador_idx_arr - 1][0] = (epnum - 1, cant_lleg_final)
        except IndexError:
            pass

        # Calcular tiempos de finalización
        running_end_time = ep_end_time = wtimer()

        # Calcular tiempos de procesamiento
        try:
            ep_exec_time = ep_end_time - ep_start_time
            running_exec_time = running_end_time - running_start_time
        except UnboundLocalError:
            ep_exec_time = 0
            running_exec_time = 0

        # Poner en la cola de salida los resultados
        encolar_salida({'EstadoActual': (x_act + 1, y_act + 1),
                        'NroEpisodio': epnum - 1,
                        'NroIteracion': cant_iteraciones,
                        'MatrizQ': matriz_q,
                        'EpisodiosExecTime': ep_exec_time,
                        'IteracionesExecTime': iter_exec_time,
                        'ProcesoJoined': True,
                        'ProcesoPaused': False,
                        'ValorParametro': tecnica.valor_param_parcial,
                        'RunningExecTime': running_exec_time,
                        'MatDiff': tmp_diff_mat,
                        'MatRecompProm': rp_res_promedio,
                        'EpFinalizados': episodios_finalizados,
                        # 'ItersXEpisodio': iters_por_episodio,
                        'MatDiffStat': mat_diff_array,
                        'MatEstAcc': matriz_est_acc
                        })

        # Realizar tareas al finalizar
        self._on_end()

    def encolar_salida(self, salida):
        u"""
        Colocar los resultandos del procesamiento en la cola de salida.

        :param salida: Información a colocar en la cola.
        """
        try:
            self._out_queue.put(salida)
        except Queue.Full:
            pass

    def encolar_errores(self, error):
        u"""
        Colocar los mensajes de errore en la cola de errores.

        :param error: Mensaje de error a colocar en la cola.
        """
        try:
            self._error_queue.put(error)
        except Queue.Full:
            pass

    def procesar_entrada(self):
        u"""
        Recibe e inicializa los datos de entradas que se utilizarán en el
        entrenamiento.
        """
        # Obtener matriz R y matriz Q
        try:
            self.input_data = self._inp_queue.get(True, 0.05)
        except Queue.Empty:
            return None

        # Obtener valores de entrada
        self.estados = self.input_data[0]
        self.coordenadas = self.input_data[1]
        self.gamma = self.input_data[2]
        self.cant_episodios = self.input_data[3]
        self.limitar_iteraciones, self.cant_max_iter = self.input_data[4]
        self.tecnica_pack = self.input_data[5]
        self.ancho, self.alto = self.input_data[6]
        self.detector_bloqueo = self.input_data[7]
        self.tipos_vec_excluidos = self.input_data[8]
        self.q_init_value_fn = self.input_data[9]
        self.matdiff_status, self.min_diff_mat, self.interv_diff_calc = self.input_data[10]
        self.cant_max_iter_gral_pack = self.input_data[11]
        self.tecnica = self.tecnica_pack[0](self.tecnica_pack[1],
                                            self.tecnica_pack[2],
                                            self.tecnica_pack[3])

        # Inicializar matrices de vecinos, Q y R
        self.matriz_est_acc, self.matriz_r, self.matriz_q = self.get_matrixes()

    def generar_estado_aleatorio(self):
        u"""
        Devuelve una tupla conteniendo las coordenadas X e Y aleatorias.
        """
        # Devolver un estado seleccionado aleatoriamente del conjunto de vecinos
        return (random.randint(0, self.ancho - 1), random.randint(0, self.alto - 1))

    def join(self, timeout=None):
        u"""
        Sobrecarga del método 'join'.

        :param timeout: Tiempo en milisegundos de espera.
        """
        # Activar flag indicando de que se solicitó detener el proceso
        self._stoprequest.set()
        # Notificar a proceso padre
        self.encolar_salida({'Joined': True})
        super(QLearningEntrenarWorker, self).join(timeout)

    def _crear_cont_ref(self, tipos_vec_exc):
        u"""
        Crea y configura un contador de referencias por cada estado accesible.

        :param tipos_vec_exc: Tipos de vecinos a excluir del contador.
        """
        matriz_q = self.matriz_q
        tipos_vec_exc.append(TIPOESTADO.FINAL)

        contador_ref = {}
        for i, fila in enumerate(matriz_q):
            for j, columna in enumerate(fila):
                if columna[0] not in tipos_vec_exc:
                    contador_ref[(i + 1, j + 1)] = 0

        return contador_ref

    def _contar_ref(self, estado):
        u"""
        Incrementa en 1 el contador de cada estado por cada acceso a sus coordenadas.

        :param estado: Estado al cual se ha accedido.
        """
        umbral_1 = 1
        umbral_2 = 2

        self._contador_ref[estado] += 1
        cont = self._contador_ref[estado]

        if cont == umbral_1:
            self._visitados_1.append(estado)
        elif cont == umbral_2:
            self._visitados_2.append(estado)

        self._comprobar_visitados()

    def _comprobar_visitados(self):
        u"""
        Verifica si el agente no puede acceder al estado final y finaliza la
        ejecución del algoritmo.
        """
        test_1 = len(self._visitados_1) == self._cant_estados_libres
        test_2 = len(self._visitados_1) == len(self._visitados_2)

        if test_1 or test_2:
            self._out_queue.put({'LoopAlarm': (True, 2)})

    def get_matrixes(self, include_vecinos=False):
        u"""
        Genera y devuelve la matriz de vecinos, matriz R y matriz Q.
        """
        # Verificar si hay tipos de vecinos a excluir de la matriz R
        if self.tipos_vec_excluidos is None:
            self.tipos_vec_excluidos = []

        # Cachear acceso a métodos y atributos
        get_vecinos_estado = self.get_vecinos_estado
        get_estado = self.get_estado
        tipos_vec_excluidos = self.tipos_vec_excluidos
        q_init_value_fn = self.q_init_value_fn
        ancho = self.ancho
        alto = self.alto
        dimension = ancho * alto

        # Matriz de vecinos
        matriz_estados = numpy.empty((alto, ancho), numpy.int)

        # Matriz Q
        matriz_q = numpy.empty((dimension, dimension), numpy.float)
        matriz_q.fill(numpy.nan)

        # Matriz R
        matriz_r = numpy.empty((dimension, dimension), numpy.float)
        matriz_r.fill(numpy.nan)

        for i in xrange(alto):
            fila = []
            fappend = fila.append

            for j in xrange(ancho):
                # Obtener estado actual y su ID de tipo
                estado = get_estado(i + 1, j + 1)
                estado_ide = estado.tipo.ide
                # Obtener los estados vecinos del estado actual (i, j)
                vecinos = get_vecinos_estado(i + 1, j + 1, True)

                # Calcular posición en eje Y
                y_coord = (i * alto) + j

                if include_vecinos:
                    evecinos = []
                    evappend = evecinos.append

                for x, y in vecinos:
                    est_vec = get_estado(x, y)

                    if est_vec.tipo.ide not in tipos_vec_excluidos:
                        # Calcular posición en eje X
                        x_coord = ((x - 1) * ancho) + (y - 1)

                        # Establecer valor Q inicial en matriz
                        matriz_q[y_coord][x_coord] = q_init_value_fn

                        # Establecer recompensa en matriz R
                        matriz_r[y_coord][x_coord] = est_vec.tipo.recompensa

                        if include_vecinos:
                            # Agregar coordenadas de vecino
                            evappend((y_coord, x_coord))

                if include_vecinos:
                    # Agregar columna a la fila
                    fappend((estado_ide, evecinos))
                else:
                    fappend(estado_ide)

            # Agregar fila a matriz de vecinos
            matriz_estados[i] = fila

        return (matriz_estados, matriz_r, matriz_q)

    def get_vecinos_estado(self, x, y, iterate=False):
        u"""
        Devuelve los estados adyacentes en función de un estado dado.
        Fuente: http://stackoverflow.com/questions/2373306/pythonic-and-efficient-way-of-finding-adjacent-cells-in-grid

        :param x: Fila del estado
        :param y: Columna del estado
        """
        coordenadas = self.coordenadas
        vecinos = []
        vappend = vecinos.append

        for fila, columna in ((x + i, y + j)
                              for i in (-1, 0, 1) for j in (-1, 0, 1)
                              if i != 0 or j != 0):
            if (fila, columna) in coordenadas:
                vappend((fila, columna))
        if iterate:
            return iter(vecinos)
        else:
            return vecinos

    def get_estado(self, x, y):
        u"""
        Devuelve un estado dadas sus coordenadas.

        :param x: Fila del estado
        :param y: Columna del estado
        """
        return self.estados[x - 1][y - 1]

    def pausar(self):
        u"""
        Solicitud de Pausa del procesamiento.
        """
        # Activar flag para pausar proceso
        self._pauserequest.set()

    def reanudar(self):
        u"""
        Solicitud de Reanudar el procesamiento.
        """
        # Desactivar flag para pausar proceso
        self._pauserequest.clear()


# ============================================================================
#                         QLearningRecorrerWorker
# ============================================================================
class QLearningRecorrerWorker(multiprocessing.Process):
    u"""
    Worker encargado de recorrer el GridWorld utilizando la matriz Q para seguir
    el mejor camino hasta el Estado Final.
    """
    def __init__(self, inp_queue, out_queue, error_queue):
        u"""
        Inicializador de QLearningRecorrerWorker.

        :param inp_queue: Cola de entrada.
        :param out_queue: Cola de salida de datos.
        :param error_queue: Cola de salida de errores.
        """
        super(QLearningRecorrerWorker, self).__init__()
        self._inp_queue = inp_queue
        self._out_queue = out_queue
        self._error_queue = error_queue
        self._stoprequest = multiprocessing.Event()
        self._pauserequest = multiprocessing.Event()
        self.name = "QLearningRecorrerWorker"
        self.input_data = None

    def _do_on_start(self):
        u"""
        Ejecuta tareas al comenzar el thread.
        """
        pass

    def _on_end(self):
        u"""
        Ejecuta tareas al finalizar el thread.
        """
        self._inp_queue.close()
        self._error_queue.close()
        self._out_queue.close()

    def run(self):
        u"""
        Método sobrecargado de clase padre Thread. Ejecuta el algoritmo de
        recorrido de Q-Learning.
        """
        if sys.platform == 'win32':
            wtimer = time.clock
        else:
            wtimer = time.time

        # Registrar tiempo de comienzo
        running_start_time = wtimer()

        # Realizar tareas al comienzo
        self._do_on_start()

        # Obtener la referencia a la instancia desde la cola de entrada
        try:
            self.input_data = self._inp_queue.get(True, 0.05)
        except Queue.Empty:
            return None

        matriz_q = self.input_data[0]
        matriz_est_acc = self.input_data[1]
        estado_inicial = self.input_data[2]

        ancho, alto = matriz_est_acc.shape

        # Lista que contiene la secuencia de estados comenzando por el
        # Estado Inicial
        camino_optimo = [estado_inicial]

        # Lista que contiene los máximos valores de Q pertenecientes al
        # camino óptimo
        q_values_co = []

        # Registrar tiempo de comienzo
        rec_start_time = wtimer()

        x_act, y_act = estado_inicial
        x_act -= 1
        y_act -= 1

        estado_actual = matriz_est_acc[x_act][y_act]
        try:
            tipo_estado = estado_actual[0]
        except TypeError:
            tipo_estado = estado_actual
        except IndexError:
            tipo_estado = estado_actual

        # Cachear acceso a funciones y atributos de instancia
        encolar_salida = self.encolar_salida
        pauserequest_isset = self._pauserequest.is_set
        stoprequest_isset = self._stoprequest.is_set
        inp_queue = self._inp_queue
        out_queue = self._out_queue
        co_append = camino_optimo.append
        qvals_append = q_values_co.append
        # --------------------------------------------------------------------

        # Inicializar contador de iteraciones
        cant_iteraciones = 1

        while (not stoprequest_isset()) and (tipo_estado != TIPOESTADO.FINAL):
            encolar_salida({'EstadoActual': (x_act + 1, y_act + 1),
                            'ProcesoJoined': False,
                            'ProcesoPaused': False,
                            'NroIteracion': cant_iteraciones})

            # Coordenada Y de la matriz (fila)
            # Para acceder a un elemento de la matriz Q o R se utiliza un esquema
            # de acceso del tipo "Base + Desplazamiento" donde las filas
            # representan los estados del GridWorld y las columnas representan
            # las acciones posibles apartir de dichos estados.
            fila_idx = (x_act * alto) + y_act

            # Obtener acciones a partir del estado actual
            acciones = matriz_q[fila_idx]
            # Buscar el estado que posea el mayor valor de Q
            maximo_q = numpy.nanmax(acciones)
            # Verificar si existen valores Q iguales al máximo
            maximos_q = numpy.where(acciones == maximo_q)[0]
            # Elegir una acción de manera aleatoria
            accion_elegida = numpy.random.choice(maximos_q)
            columna_idx = accion_elegida

            # Calcular coordenadas y actualizar estado actual
            new_x = int(columna_idx / alto)
            new_y = columna_idx - (new_x * ancho)

            estado_actual = matriz_est_acc[new_x][new_y]

            # Agregar estado al camino óptimo
            co_append((new_x + 1, new_y + 1))
            # Agregar Q máximo a lista
            qvals_append(maximo_q)

            # Obtener tipo de estado
            try:
                tipo_estado = estado_actual[0]
            except (TypeError, IndexError):
                tipo_estado = estado_actual

            # Nuevo estado = Acción elegida
            x_act = new_x
            y_act = new_y

            # Incrementar número de iteraciones
            cant_iteraciones += 1

            # ---------------------- Pausa --------------------------
            # ------------ Primer verificación ----------------------
            # Comprobar si se solicitó pausar el procesamiento
            if pauserequest_isset():
                # Encolar datos de salida (Dump del contexto actual)
                encolar_salida({'EstadoActual': (x_act + 1, y_act + 1),
                                'ProcesoJoined': False,
                                'ProcesoPaused': True,
                                'NroIteracion': cant_iteraciones})

                # Esperar 1 segundo
                time.sleep(1)
            # ==================== Fin iteraciones ============================

        # Registrar tiempo de finalización
        running_end_time = rec_end_time = wtimer()

        # Calcular tiempos de procesamiento
        try:
            rec_exec_time = rec_end_time - rec_start_time
            running_exec_time = running_end_time - running_start_time
        except UnboundLocalError:
            rec_exec_time = 0
            running_exec_time = 0

        # Poner en la cola de salida los resultados
        encolar_salida({'EstadoActual': (x_act + 1, y_act + 1),
                        'CaminoRecorrido': camino_optimo,
                        'ValoresQCR': q_values_co,
                        'RecorridoExecTime': rec_exec_time,
                        'ProcesoJoined': False,
                        'ProcesoPaused': False,
                        'RunningExecTime': running_exec_time
                        })

        # Realizar tareas al finalizar
        self._on_end()

    def join(self, timeout=None):
        u"""
        Sobrecarga del método 'join'.

        :param timeout: Tiempo en milisegundos de espera.
        """
        self._stoprequest.set()
        self.encolar_salida({'Joined': True})
        super(QLearningRecorrerWorker, self).join(timeout)

    def encolar_salida(self, salida):
        u"""
        Colocar los resultandos del procesamiento en la cola de salida.

        :param salida: Información a colocar en la cola.
        """
        try:
            self._out_queue.put(salida)
        except Queue.Full:
            pass

    def encolar_errores(self, error):
        u"""
        Colocar los mensajes de errore en la cola de errores.

        :param error: Mensaje de error a colocar en la cola.
        """
        try:
            self._error_queue.put(error)
        except Queue.Full:
            pass

    def pausar(self):
        u"""
        Solicitud de Pausa del procesamiento.
        """
        # Activar flag para pausar proceso
        self._pauserequest.set()

    def reanudar(self):
        u"""
        Solicitud de Reanudar el procesamiento.
        """
        # Desactivar flag para pausar proceso
        self._pauserequest.clear()
