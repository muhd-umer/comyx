:py:mod:`simcomm.metrics.common`
================================

.. py:module:: simcomm.metrics.common


Module Contents
---------------


Functions
~~~~~~~~~

.. autoapisummary::

   simcomm.metrics.common.get_outage
   simcomm.metrics.common.get_snr



.. py:function:: get_outage(instantaneous_rate, target_rate)

   
   Compute the outage probability.

   :param instantaneous_rate: The instantaneous rate(s) of the link(s).
   :type instantaneous_rate: float or list
   :param target_rate: The target rate of the link.
   :type target_rate: float

   :returns: The outage probability of the link(s).
   :rtype: outage (int or list)















   ..
       !! processed by numpydoc !!

.. py:function:: get_snr(signal_power, noise_power)

   
   Calculate the signal-to-noise ratio (SNR) in decibels.

   :param signal_power: Signal power in watts.
   :type signal_power: float or ndarray
   :param noise_power: Noise power in watts.
   :type noise_power: float

   :returns: The signal-to-noise ratio (SNR) in decibels.
   :rtype: snr (float or ndarray)















   ..
       !! processed by numpydoc !!

