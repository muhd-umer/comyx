:py:mod:`simcomm.core.fading`
=============================

.. py:module:: simcomm.core.fading


Submodules
----------
.. toctree::
   :titlesonly:
   :maxdepth: 1

   rayleigh/index.rst
   rician/index.rst


Package Contents
----------------


Functions
~~~~~~~~~

.. autoapisummary::

   simcomm.core.fading.get_rvs



.. py:function:: get_rvs(type, shape, *args, **kwargs)

   
   Generates random variables from a distribution.

   :param type: The type of the fading. ("rayleigh", "rician")
   :type type: str
   :param shape: The number of fading coefficients to generate.
   :type shape: int or tuple of ints

   Rayleigh Args:
       sigma (float): The scale parameter of the Rayleigh distribution.

   Rician Args:
       K (float): Rician K-factor in dB.
       sigma (float): The scale parameter of the Rician distribution.

   :returns: Channel gains.















   ..
       !! processed by numpydoc !!

