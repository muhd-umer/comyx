:py:mod:`simcomm.core`
======================

.. py:module:: simcomm.core


Subpackages
-----------
.. toctree::
   :titlesonly:
   :maxdepth: 3

   fading/index.rst
   propagation/index.rst
   system/index.rst


Package Contents
----------------

Classes
~~~~~~~

.. autoapisummary::

   simcomm.core.LinkCollection
   simcomm.core.Receiver
   simcomm.core.STAR
   simcomm.core.Transmitter



Functions
~~~~~~~~~

.. autoapisummary::

   simcomm.core.get_noise_power
   simcomm.core.get_pathloss
   simcomm.core.get_rvs



.. py:class:: LinkCollection(size, frequency)


   
   Contains a collection of links accessible by name. Used to store all the channel coefficients and their corresponding types for the system under test.

   :param size: The size of the links.
   :type size: int
   :param frequency: The frequency of the carrier signal in Hz.
   :type frequency: float

   .. attribute:: links

      A dictionary of links.

      :type: dict

   .. attribute:: link_types

      A dictionary of link types.

      :type: dict

   .. attribute:: size

      The size of the links.

      :type: int

   .. attribute:: frequency

      The frequency of the carrier signal in Hz.

      :type: float















   ..
       !! processed by numpydoc !!
   .. py:method:: __str__()

      
      Returns a string representation of the LinkCollection.

      :returns: A string representation of the LinkCollection. Displays links as "Transmitter
                -> Receiver" along with the type of link and shape of the channel.















      ..
          !! processed by numpydoc !!

   .. py:method:: add_link(transmitter, receiver, fading_args, pathloss_args, type, elements = None)

      
      Adds a link to the collection.

      :param transmitter: The transmitter object.
      :type transmitter: SystemObject
      :param receiver: The receiver object.
      :type receiver: SystemObject
      :param fading_args: The arguments for the fading model.
      :type fading_args: dict
      :param pathloss_args: The arguments for the pathloss model.
      :type pathloss_args: dict
      :param type: The type of link. Can be "1,c", "2,c", "f", "ris", or "dne".
      :type type: str
      :param elements: The number of elements in the RIS. Defaults to None.
      :type elements: int, optional















      ..
          !! processed by numpydoc !!

   .. py:method:: get_gain(transmitter, receiver)

      
      Gets the gain between a transmitter and receiver.

      :param transmitter: The transmitter object.
      :type transmitter: SystemObject
      :param receiver: The receiver object.
      :type receiver: SystemObject

      :returns: The gain between the transmitter and receiver.
      :rtype: gain (ndarray)















      ..
          !! processed by numpydoc !!

   .. py:method:: get_link(transmitter, receiver)

      
      Gets the channel between a transmitter and receiver.

      :param transmitter: The transmitter object.
      :type transmitter: SystemObject
      :param receiver: The receiver object.
      :type receiver: SystemObject

      :returns: The channel between the transmitter and receiver.
      :rtype: link (ndarray)















      ..
          !! processed by numpydoc !!

   .. py:method:: get_link_type(transmitter, receiver)

      
      Gets the type of link between a transmitter and receiver.

      :param transmitter: The transmitter object.
      :type transmitter: SystemObject
      :param receiver: The receiver object.
      :type receiver: SystemObject

      :returns: The type of link between the transmitter and receiver.
      :rtype: link_type (str)















      ..
          !! processed by numpydoc !!

   .. py:method:: update_link(transmitter, receiver, value)

      
      Combines a value with the channel between a transmitter and receiver.

      :param transmitter: The transmitter object.
      :type transmitter: SystemObject
      :param receiver: The receiver object.
      :type receiver: SystemObject
      :param value: The value to combine with the channel.
      :type value: ndarray

      :returns: None















      ..
          !! processed by numpydoc !!


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


.. py:class:: STAR(name, position, elements, beta_r = 0.5, beta_t = 0.5, custom_assignment = None)


   Bases: :py:obj:`simcomm.core.system.system.SystemObject`

   
   A class representing a STAR-RIS. Inherits from SystemObject. Passive in nature, can only reflect the incoming signal.

   :param name: The name of the STAR-RIS.
   :type name: str
   :param position: [x, y] coordinates of the STAR-RIS, [x, y, z] coordinates if 3D.
   :type position: List[float]
   :param elements: The number of elements in the RIS.
   :type elements: int
   :param beta_r: The reflection coefficients of the RIS. Defaults to 0.5.
   :type beta_r: float, optional
   :param beta_t: The transmission coefficients of the RIS. Defaults to 0.5.
   :type beta_t: float, optional
   :param custom_assignment: Custom  assignment, i.e., different number of elements assigned to BS1 and BS2 or beta_r and beta_t other than halved.
   :type custom_assignment: dict

   .. attribute:: name

      Stores the name of the system object.

      :type: str

   .. attribute:: position

      Stores the [x, y] coordinates of the system object, [x, y, z] coordinates if 3D.

      :type: List[float]

   .. attribute:: elements

      Stores the number of elements in the RIS.

      :type: int

   .. attribute:: beta_r

      Stores the reflection coefficients of the RIS.

      :type: ndarray

   .. attribute:: theta_r

      Stores the phase shifts of the RIS.

      :type: ndarray

   .. attribute:: beta_t

      Stores the transmission coefficients of the RIS.

      :type: ndarray

   .. attribute:: theta_t

      Stores the phase shifts of the RIS.

      :type: ndarray

   .. attribute:: custom_assignment

      Stores the custom assignment, i.e., different number of elements assigned to BS1 and BS2 or beta_r and beta_t other than halved.

      :type: dict

   .. attribute:: transmission_matrix

      Stores the transmission matrix of the RIS.

      :type: ndarray

   .. attribute:: reflection_matrix

      Stores the reflection matrix of the RIS.

      :type: ndarray















   ..
       !! processed by numpydoc !!
   .. py:method:: merge_link(links, transmitter, receiver)

      
      Updates the link between the SystemObject and SystemObject with combined channel. Expects the arguments to be in the order as link is defined.

      :param links: The collection of links in the system.
      :type links: link.LinkCollection
      :param transmitter: The transmitter(s) in the system. Pass a list of transmitters if link type between SystemObject and SystemObject is "E".
      :type transmitter: Union[SystemObject, List[SystemObject]]
      :param receiver: The receiver in the system.
      :type receiver: SystemObject

      :raises AssertionError: If there are not exactly 2 base stations or 3 receivers.















      ..
          !! processed by numpydoc !!

   .. py:method:: set_reflection_parameters(links, transmitters, receivers)

      
      Sets the reflection parameters of the RIS.

      :param links: The collection of links in the system.
      :type links: link.LinkCollection
      :param transmitters: The list of transmitters in the system.
      :type transmitters: List[SystemObject]
      :param receivers: The list of receivers in the system.
      :type receivers: List[SystemObject]

      :raises AssertionError: If there are not exactly 2 base stations or 2 cell-center receivers.















      ..
          !! processed by numpydoc !!

   .. py:method:: set_transmission_parameters(links, transmitters, receiver)

      
      Sets the transmission parameters of the RIS.

      :param links: The collection of links in the system.
      :type links: link.LinkCollection
      :param transmitters: The list of transmitters in the system.
      :type transmitters: List[SystemObject]
      :param receiver: The far receiver (UF) in the system.
      :type receiver: SystemObject

      :raises AssertionError: If there are not exactly 2 base stations.















      ..
          !! processed by numpydoc !!


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

