:py:mod:`simcomm.core.system.system`
====================================

.. py:module:: simcomm.core.system.system


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   simcomm.core.system.system.SystemObject




.. py:class:: SystemObject(name, position)


   
   Base class for all system objects in the network except for the channel, as it is not a physical object.

   :param name: The name of the system object.
   :type name: str
   :param position: The [x, y] or [x, y, z] coordinates of the system object.
   :type position: array_like

   .. attribute:: name

      Stores the name of the system object.

      :type: str

   .. attribute:: position

      Stores the [x, y] or [x, y, z] coordinates of the system object.

      :type: array_like















   ..
       !! processed by numpydoc !!
   .. py:method:: __str__()

      
      Return str(self).
















      ..
          !! processed by numpydoc !!


