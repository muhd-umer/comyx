:py:mod:`simcomm.core.system.receiver`
======================================

.. py:module:: simcomm.core.system.receiver


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   simcomm.core.system.receiver.Receiver




.. py:class:: Receiver(name, position, sensitivity)


   Bases: :py:obj:`simcomm.core.system.system.SystemObject`

   
   A class representing a receiver. Inherits from SystemObject. Receivers contain empty attributes for rate, outage, and SNR.

   :param name: The name of the receiver.
   :type name: str
   :param position: [x, y] coordinates of the system object, [x, y, z] coordinates if 3D.
   :type position: list
   :param sensitivity: The sensitivity of the receiver in dBm.
   :type sensitivity: float

   .. attribute:: sensitivity

      Stores the sensitivity of the receiver in dBm.

      :type: float

   .. attribute:: rate

      Stores the rate of the receiver in bits per second.

      :type: array_like

   .. attribute:: outage

      Stores the outage of the receiver in dB.

      :type: array_like

   .. attribute:: snr

      Stores the SNR of the receiver in dB.

      :type: array_like















   ..
       !! processed by numpydoc !!
   .. py:method:: bpsk_demodulation(received_signal)

      
      Perform BPSK demodulation on the received signal
















      ..
          !! processed by numpydoc !!

   .. py:method:: demodulate(modulation_type, received_signal, *args, **kwargs)

      
      Demodulate the received signal using the specified modulation type
















      ..
          !! processed by numpydoc !!

   .. py:method:: nqam_demodulation(received_signal, n)

      
      Perform N-QAM demodulation on the received signal with the specified value of n
















      ..
          !! processed by numpydoc !!

   .. py:method:: qpsk_demodulation(received_signal)

      
      Perform QPSK demodulation on the received signal
















      ..
          !! processed by numpydoc !!


