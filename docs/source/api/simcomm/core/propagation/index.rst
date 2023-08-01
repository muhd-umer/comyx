:py:mod:`simcomm.core.propagation`
==================================

.. py:module:: simcomm.core.propagation


Submodules
----------
.. toctree::
   :titlesonly:
   :maxdepth: 1

   noise/index.rst
   pathloss/index.rst


Package Contents
----------------


Functions
~~~~~~~~~

.. autoapisummary::

   simcomm.core.propagation.get_noise_power
   simcomm.core.propagation.get_pathloss



.. py:function:: get_noise_power(bandwidth, temperature = 300, noise_figure = 0)

   
   Compute the noise power in dBm.

   :param bandwidth: Bandwidth in Hz.
   :param temperature: Temperature in Kelvin.
   :param noise_figure: Noise figure in dB.

   :returns: Noise power in dBm.















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

