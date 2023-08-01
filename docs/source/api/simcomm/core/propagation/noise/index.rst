:py:mod:`simcomm.core.propagation.noise`
========================================

.. py:module:: simcomm.core.propagation.noise


Module Contents
---------------


Functions
~~~~~~~~~

.. autoapisummary::

   simcomm.core.propagation.noise.get_noise_power
   simcomm.core.propagation.noise.thermal_noise



.. py:function:: get_noise_power(bandwidth, temperature = 300, noise_figure = 0)

   
   Compute the noise power in dBm.

   :param bandwidth: Bandwidth in Hz.
   :param temperature: Temperature in Kelvin.
   :param noise_figure: Noise figure in dB.

   :returns: Noise power in dBm.















   ..
       !! processed by numpydoc !!

.. py:function:: thermal_noise(temperature = 300)

   
   Compute the thermal noise.

   :param bandwidth: Bandwidth in Hz.
   :param temperature: Temperature in Kelvin.

   :returns: Thermal noise.















   ..
       !! processed by numpydoc !!

