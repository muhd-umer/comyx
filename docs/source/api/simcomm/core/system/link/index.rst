:py:mod:`simcomm.core.system.link`
==================================

.. py:module:: simcomm.core.system.link


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   simcomm.core.system.link.LinkCollection




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


