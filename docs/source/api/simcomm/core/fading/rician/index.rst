:py:mod:`simcomm.core.fading.rician`
====================================

.. py:module:: simcomm.core.fading.rician


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   simcomm.core.fading.rician.Rician




.. py:class:: Rician(K, sigma = 1)


   
   The Rician distribution is a continuous probability distribution that describes the length of a two-dimensional vector with components that are independent Gaussian random variables.

   Density Function
       .. math::
           f(x) = \frac{x}{\sigma^2} \exp\left(-\frac{x^2 + \nu^2}{2\sigma^2}\right) I_0\left(\frac{x\nu}{\sigma^2}\right)

   , where :math:`I_0` is the modified Bessel function of the first kind.

   Expected value
       .. math::
           \sigma \sqrt{\frac{\pi}{2}} \exp\left(-\frac{\nu^2}{2\sigma^2}\right)

   Variance
       .. math::
           2\sigma^2 + \nu^2 - \frac{\pi\sigma^2}{2}

   RMS value
       .. math::
           \sigma \sqrt{2 + \frac{\pi}{2}}

   .. attribute:: K

      The Rician factor, which is the ratio between the power of the direct path and the power of the scattered paths.

      :type: float

   .. attribute:: omega

      The scale parameter, which is the total power from both the line-of-sight and scattered paths.

      :type: float

   .. attribute:: sigma

      The scale parameter, which is the standard deviation of the distribution.

      :type: float

   .. attribute:: nu

      The location parameter, which is the shift of the distribution.

      :type: float

   Reference:
       https://en.wikipedia.org/wiki/Rice_distribution















   ..
       !! processed by numpydoc !!
   .. py:method:: cdf(x)

      
      Return the cumulative distribution function of the Rician distribution.

      :param x: The value at which to evaluate the cumulative distribution
      :type x: float

      :returns: The cumulative distribution function evaluated at x.
      :rtype: cdf (ndarray)















      ..
          !! processed by numpydoc !!

   .. py:method:: expected_value()

      
      Return the expected value of the Rician distribution.

      :returns: The expected value of the Rician distribution.
      :rtype: expected_value (float)















      ..
          !! processed by numpydoc !!

   .. py:method:: get_coefficients(size)

      
      Generate complex fading coefficients from the Rician distribution.

      :param size: The number of channel coefficients to generate.
      :type size: int or tuple of ints

      :returns: An array of size `size` containing complex channel
                coefficients from the Rician distribution.
      :rtype: coefficients (array_like)















      ..
          !! processed by numpydoc !!

   .. py:method:: get_samples(size)

      
      Generate random variables from the Rician distribution.

      :param size: The number of random variables to generate.
      :type size: int or tuple of ints

      :returns: An array of size `size` containing random variables from
                the Rician distribution.
      :rtype: samples (array_like)















      ..
          !! processed by numpydoc !!

   .. py:method:: pdf(x)

      
      Return the probability density function of the Rician distribution.

      :param x: The value at which to evaluate the probability density function.
      :type x: float

      :returns: The probability density function evaluated at x.
      :rtype: pdf (float)















      ..
          !! processed by numpydoc !!

   .. py:method:: rms_value()

      
      Return the RMS value of the Rician distribution.

      :returns: The RMS value of the Rician distribution.
      :rtype: rms (float)















      ..
          !! processed by numpydoc !!

   .. py:method:: variance()

      
      Return the variance of the Rician distribution.

      :returns: The variance of the Rician distribution.
      :rtype: variance (float)















      ..
          !! processed by numpydoc !!


