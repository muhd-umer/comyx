:py:mod:`simcomm.core.propagation.pathloss`
===========================================

.. py:module:: simcomm.core.propagation.pathloss


Module Contents
---------------


Functions
~~~~~~~~~

.. autoapisummary::

   simcomm.core.propagation.pathloss.free_space
   simcomm.core.propagation.pathloss.friis
   simcomm.core.propagation.pathloss.get_pathloss
   simcomm.core.propagation.pathloss.log_distance



.. py:function:: free_space(distance, alpha, p0)

   
   Free space path loss model.

   :param distance: Distance between transmitter and receiver.
   :type distance: float
   :param alpha: Path loss exponent.
   :type alpha: float
   :param p0: Reference path loss at 1m.
   :type p0: float

   :returns: Path loss in dB.
   :rtype: loss (array_like)















   ..
       !! processed by numpydoc !!

.. py:function:: friis(distance, frequency)

   
   Friis path loss model.

   :param distance: Distance between transmitter and receiver.
   :type distance: float
   :param frequency: Frequency of the signal.
   :type frequency: float

   :returns: Path loss in dB.
   :rtype: loss (float)















   ..
       !! processed by numpydoc !!

.. py:function:: get_pathloss(type, distance, frequency, *args, **kwargs)

   
   Get path loss in dB.

   :param type: Path loss model type. ("free-space", "log-distance")
   :type type: str
   :param distance: Distance between transmitter and receiver.
   :type distance: float
   :param frequency: Frequency of the signal.
   :type frequency: float
   :param \*args: Positional arguments for the path loss model.
   :param \*\*kwargs: Keyword arguments for the path loss model.

   :returns: Path loss in dB.

   - FSPL Args:
       - alpha (float): Path loss exponent.
       - p0 (float): Reference path loss at 1m.

   - Log Distance Args:
       - d0 (float): The breakpoint distance.
       - alpha (float): The path loss exponent.
       - sigma (float): The shadow fading standard deviation.















   ..
       !! processed by numpydoc !!

.. py:function:: log_distance(distance, frequency, d0, alpha, sigma)

   
   Log distance path loss model.

   :param distance: Distance between transmitter and receiver.
   :type distance: float
   :param frequency: Frequency of the signal.
   :type frequency: float
   :param d0: Break distance.
   :type d0: float
   :param alpha: Path loss exponent.
   :type alpha: float
   :param sigma: Shadow fading standard deviation.
   :type sigma: float

   :returns: Path loss in dB.
   :rtype: loss (float)















   ..
       !! processed by numpydoc !!

