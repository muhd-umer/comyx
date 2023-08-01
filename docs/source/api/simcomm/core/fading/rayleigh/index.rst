:py:mod:`simcomm.core.fading.rayleigh`
======================================

.. py:module:: simcomm.core.fading.rayleigh


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   simcomm.core.fading.rayleigh.Rayleigh




.. py:class:: Rayleigh(sigma = 1)


   
   The Rayleigh distribution is a continuous probability distribution that describes the magnitude of a random vector with two independent, identically distributed (i.i.d.) Gaussian components with zero mean and equal standard deviation.

   **Density function**
       .. math::
           f(x) = \frac{x}{\sigma^2} \cdot \exp\left(-\frac{x^2}{2\sigma^2}\right)

   **Expected value**
       .. math::
           \sigma \cdot \sqrt{\frac{\pi}{2}}

   **Variance**
       .. math::
           \left(2 - \frac{\pi}{2}\right) \cdot \sigma^2

   **RMS value**
       .. math::
           \sqrt{2} \cdot \sigma

   :returns: A NumPy array of complex numbers representing the fading coefficients.

   .. attribute:: sigma

      The scale parameter of the Rayleigh distribution.

      :type: float

   Reference:
       https://en.wikipedia.org/wiki/Rayleigh_distribution















   ..
       !! processed by numpydoc !!
   .. py:method:: cdf(x)

      
      Returns the cumulative distribution function of the Rayleigh distribution.

      :param x: The input value.
      :type x: float

      :returns: The cumulative distribution function value at x.
      :rtype: cdf (float)















      ..
          !! processed by numpydoc !!

   .. py:method:: expected_value()

      
      Calculates the expected value of the Rayleigh distribution.

      :returns: The expected value of the Rayleigh distribution.
      :rtype: expected_value (float)















      ..
          !! processed by numpydoc !!

   .. py:method:: get_coefficients(size)

      
      Generates complex channel coefficients from the Rayleigh distribution.

      :param size: The number of channel coefficients to generate.
      :type size: int or tuple of ints

      :returns: An array of size `size` containing complex channel coefficients from the Rayleigh distribution.
      :rtype: coefficients (array_like)















      ..
          !! processed by numpydoc !!

   .. py:method:: get_samples(size)

      
      Generates random variables from the Rayleigh distribution.

      :param size: The number of random variables to generate.
      :type size: int or tuple of ints

      :returns: An array of size `size` containing random variables from the Rayleigh distribution.
      :rtype: samples (array_like)















      ..
          !! processed by numpydoc !!

   .. py:method:: pdf(x)

      
      Returns the probability density function of the Rayleigh distribution.

      :param x: The input value.
      :type x: float

      :returns: The probability density function value at x.
      :rtype: pdf (float)















      ..
          !! processed by numpydoc !!

   .. py:method:: rms_value()

      
      Calculates the RMS value of the Rayleigh distribution.

      :returns: The RMS value of the Rayleigh distribution.
      :rtype: rms (float)















      ..
          !! processed by numpydoc !!

   .. py:method:: variance()

      
      Calculates the variance of the Rayleigh distribution.

      :returns: The variance of the Rayleigh distribution.
      :rtype: variance (float)















      ..
          !! processed by numpydoc !!


