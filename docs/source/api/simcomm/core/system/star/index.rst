:py:mod:`simcomm.core.system.star`
==================================

.. py:module:: simcomm.core.system.star


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   simcomm.core.system.star.STAR




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


