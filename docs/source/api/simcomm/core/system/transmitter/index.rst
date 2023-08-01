:py:mod:`simcomm.core.system.transmitter`
=========================================

.. py:module:: simcomm.core.system.transmitter


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   simcomm.core.system.transmitter.Transmitter




.. py:class:: Transmitter(name, position, transmit_power)


   Bases: :py:obj:`simcomm.core.system.system.SystemObject`

   
   A class representing a transmitter. Inherits from SystemObject. Transmitters contain an empty attribute for power allocation factors to be assigned to the cellular users.

   :param name: The name of the transmitter.
   :type name: str
   :param position: The position of the transmitter in 2D or 3D space.
   :param transmit_power: The transmit power of the transmitter.

   .. attribute:: name

      Stores the name of the transmitter.

      :type: str

   .. attribute:: position

      Stores the position of the transmitter in 2D or 3D space.

      :type: list

   .. attribute:: antenna_gain

      Stores the gain of the transmitter's antenna.

      :type: float

   .. attribute:: losses

      Stores the losses of the transmitter.

      :type: float

   .. attribute:: transmit_power

      Stores the transmit power of the transmitter.

      :type: array_like

   .. attribute:: allocations

      Stores the power allocation factors assigned to the cellular users.

      :type: dict















   ..
       !! processed by numpydoc !!
   .. py:method:: bpsk_modulation(data)

      
      Performs BPSK modulation on the input data.
















      ..
          !! processed by numpydoc !!

   .. py:method:: get_allocation(receiver)

      
      Gets the power allocation for a given receiver.
















      ..
          !! processed by numpydoc !!

   .. py:method:: modulate(modulation_type, data, *args, **kwargs)

      
      Modulates the input data with the given modulation type.
















      ..
          !! processed by numpydoc !!

   .. py:method:: nqam_modulation(data, n)

      
      Performs N-QAM modulation on the input data with the specified value of n.
















      ..
          !! processed by numpydoc !!

   .. py:method:: qpsk_modulation(data)

      
      Performs QPSK modulation on the input data.
















      ..
          !! processed by numpydoc !!

   .. py:method:: set_allocation(receiver, allocation)

      
      Sets the power allocation for a given receiver.
















      ..
          !! processed by numpydoc !!


