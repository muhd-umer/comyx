:py:mod:`simcomm.core.system.channel`
=====================================

.. py:module:: simcomm.core.system.channel


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   simcomm.core.system.channel.Channel




.. py:class:: Channel(transmitter, receiver, frequency, fading_args, pathloss_args, shape, no_link = False)


   
   A class representing a wireless channel. Used to generate channel coefficients. Also allows for the addition of external coefficients.

   :param transmitter: The transmitter object.
   :type transmitter: SystemObject
   :param receiver: The receiver object.
   :type receiver: SystemObject
   :param frequency: The frequency of the channel.
   :type frequency: float
   :param fading_args: The arguments for the fading model.
   :type fading_args: dict
   :param pathloss_args: The arguments for the pathloss model.
   :type pathloss_args: dict
   :param shape: The number of channel gains to generate.
   :type shape: tuple
   :param no_link: If True, the complex fading is zero.
   :type no_link: bool

   .. attribute:: transmitter

      Stores the transmitter object.

      :type: SystemObject

   .. attribute:: receiver

      Stores the receiver object.

      :type: SystemObject

   .. attribute:: frequency

      Stores the frequency of the channel.

      :type: float

   .. attribute:: fading_args

      Stores the arguments for the fading model.

      :type: dict

   .. attribute:: pathloss_args

      Stores the arguments for the pathloss model.

      :type: dict

   .. attribute:: shape

      Stores the shape of the channel coefficients.

      :type: tuple

   .. attribute:: distance

      Stores the distance between the transmitter and receiver.

      :type: float

   .. attribute:: pathloss

      Stores the pathloss between the transmitter and receiver.

      :type: float

   .. attribute:: ext_coefficients

      Stores the external coefficients of the channel.

      :type: array_like

   .. attribute:: coefficients

      Stores the channel coefficients.

      :type: array_like

   - Fading Args:
       - type (str): The type of fading model to use.
       - shape (int): The number of channel gains to generate.
       - ret (str): The return type, either "gains" or "coefficients".

       - Rayleigh Fading Args:
           - sigma (float): The scale factor of the Rayleigh distribution.

       - Rician Fading Args:
           - K (float): The K factor of the Rician distribution.
           - sigma (float): The scale factor of the Rician distribution.

   - Pathloss Args:
       - type (str): The type of pathloss model to use.

       - FSPL Args:
           - alpha (float): The pathloss exponent.
           - p0 (float): The reference pathloss at 1m.

       - Log Distance Args:
           - alpha (float): The pathloss exponent.
           - d0 (float): The breakpoint distance.
           - sigma (float): The standard deviation of the shadowing.















   ..
       !! processed by numpydoc !!
   .. py:method:: generate_channel()

      
      Generates the channel coefficients from the multipath fading and pathloss values.

      :returns: None















      ..
          !! processed by numpydoc !!

   .. py:method:: update_channel(value)

      
      Updates the channel coefficients from the multipath fading and pathloss values.

      :param value: The value to add to the channel coefficients.
      :type value: array_like

      :returns: None















      ..
          !! processed by numpydoc !!


