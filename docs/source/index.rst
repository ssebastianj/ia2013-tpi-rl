.. Inteligencia Artificial 2013: Aprendizaje por Refuerzo documentation master file, created by
   sphinx-quickstart on Mon Apr 08 10:45:06 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Inteligencia Artificial 2013: Aprendizaje por Refuerzo
======================================================

*Grupo Nº 1*
------------

* **Levin, Fabián Andrés** <*fabianlevin60@gmail.com*>

  * *Bitbucket*: https://bitbucket.org/fabitolevin88
  
* **Seba, Sebastián José** <*ssebastianj@gmail.com*> 
  
  * *Github*: https://github.com/ssebastianj
  * *Bitbucket*: https://bitbucket.org/ssebastianj
  
* **Vallejos, Lucía Belén** <*luvallejos89@gmail.com*>
  
  * *Bitbucket*: https://bitbucket.org/luvallejos

Dependencias
------------
* `Python <http://www.python.org/>`_ 2.7+ (Python 3 no soportado)
* `PyQt4 <http://www.riverbankcomputing.co.uk/software/pyqt/intro>`_ 4.10+
* `Qt4 <http://qt-project.org/>`_ 4.8.4+
* `NumPy <http://www.numpy.org/>`_ 1.7+
* `Matplotlib <matplotlib.org>`_ 1.2+
* `cDecimal <https://pypi.python.org/pypi/cdecimal/>`_ 2.3+
* `Sphinx <http://sphinx-doc.org/>`_ 1.2+

Contenido
---------

Contents:

.. toctree::
   :maxdepth: 2
   
.. automodule:: core.gridworld.gridworld
.. autoclass:: GridWorld
   :members:
   :private-members:
   :special-members:

.. automodule:: core.estado.estado
.. autoclass:: Estado
   :members:
   :private-members:
   :special-members:
        
.. autoclass:: TipoEstado
   :members:
   :private-members:
   :special-members:

.. automodule:: core.tecnicas.tecnica
.. autoclass:: QLTecnica
   :members:
   :private-members:
   :special-members:     

.. automodule:: core.tecnicas.egreedy
.. autoclass: EGreedy
   :members:
   :private-members:
   :special-members:
   
.. autoclass: Greedy
   :members:
   :private-members:
   :special-members: 

.. automodule:: core.tecnicas.softmax
.. autoclass:: Softmax
   :members:
   :private-members:
   :special-members:

.. automodule:: core.tecnicas.aleatorio
.. autoclass:: Aleatorio
   :members:
   :private-members:
   :special-members:

.. automodule:: core.qlearning.qlearning
.. autoclass:: QLearning
   :members:
   :private-members:
   :special-members:
   
.. automodule:: core.qlearning.workers
.. autoclass:: QLearningEntrenarWorker
   :members:
   :private-members:
   :special-members:

.. autoclass:: QLearningRecorrerWorker
   :members:
   :private-members:
   :special-members:

.. automodule:: gui.mainwindow
.. autoclass:: MainWindow
   :members:
   :private-members:
   
.. automodule:: gui.aboutdialog
.. autoclass:: AboutDialog
   :members:
   :private-members:
   
.. automodule:: gui.gwgenrndestadosdialog
.. autoclass:: GWGenRndEstadosDialog
   :members:
   :private-members:

.. automodule:: gui.gwopcionesdialog
.. autoclass:: GWOpcionesDialog
   :members:
   :private-members:

.. automodule:: tools.enum

.. automodule:: tools.listacircular
.. autoclass:: ListaCircular
   :members:
   :private-members:
   :special-members:
   
.. automodule:: core.qlearning.matrixinits
.. autoclass:: QLMatrixInicializador
   :members:
   :private-members:
   :special-members:

.. autoclass:: QLMatrixInitEnCero
   :members:
   :private-members:
   :special-members:
   
.. autoclass:: QLMatrixInitRandom
   :members:
   :private-members:
   :special-members:
   
.. autoclass:: QLMatrixInitEnRecompensa
   :members:
   :private-members:
   :special-members:
   
.. automodule:: graphs.avgrwds.worker
.. autoclass:: GraphRecompensasPromedioWorker
   :members:
   :private-members:
   :special-members:
   
.. automodule:: graphs.itersep.worker
.. autoclass:: GraphIteracionesXEpisodioWorker
   :members:
   :private-members:
   :special-members:
   
.. automodule:: graphs.matdiffs.worker
.. autoclass:: GraphMatrizDiffsWorker
   :members:
   :private-members:
   :special-members:
   
.. automodule:: graphs.sucessfuleps.worker
.. autoclass:: GraphSucessfulEpisodesWorker
   :members:
   :private-members:
   :special-members:

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
