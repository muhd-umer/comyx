:py:mod:`simcomm.utils`
=======================

.. py:module:: simcomm.utils


Submodules
----------
.. toctree::
   :titlesonly:
   :maxdepth: 1

   utils/index.rst


Package Contents
----------------


Functions
~~~~~~~~~

.. autoapisummary::

   simcomm.utils.db2pow
   simcomm.utils.dbm2pow
   simcomm.utils.get_distance
   simcomm.utils.inverse_qfunc
   simcomm.utils.laguerre
   simcomm.utils.pow2db
   simcomm.utils.pow2dbm
   simcomm.utils.qfunc
   simcomm.utils.randomize_user_pos
   simcomm.utils.rolling_mean
   simcomm.utils.wrapTo2Pi



.. py:function:: db2pow(db)

   
   Convert decibels to power.

   :param db: Power in decibels.
   :type db: float or ndarray

   :returns: Power.
   :rtype: pow (float or ndarray)















   ..
       !! processed by numpydoc !!

.. py:function:: dbm2pow(dbm)

   
   Convert decibels relative to 1 milliwatt to power.

   :param dbm: Power in decibels relative to 1 milliwatt.
   :type dbm: float or ndarray

   :returns: Power in watts.
   :rtype: pow (float or ndarray)















   ..
       !! processed by numpydoc !!

.. py:function:: get_distance(pt1, pt2, dim = 2)

   
   Calculate the Euclidean distance between two points.

   :param pt1: First point as a list of [x, y] or [x, y, z] coordinates.
   :type pt1: list
   :param pt2: Second point as a list of [x, y] or [x, y, z] coordinates.
   :type pt2: list
   :param dim: Dimension of the points. Default is 2.
   :type dim: int

   :returns: Euclidean distance between the two points.
   :rtype: distance (float)















   ..
       !! processed by numpydoc !!

.. py:function:: inverse_qfunc(x)

   
   Inverse Q function.

   :param x: Input to the inverse Q function.
   :type x: ndarray

   :returns: The inverse Q function.
   :rtype: inverse_qfunc (ndarray)















   ..
       !! processed by numpydoc !!

.. py:function:: laguerre(x, n)

   
   Compute the Laguerre polynomial.

   :param x: Input to the Laguerre polynomial.
   :type x: float or ndarray
   :param n: The order of the Laguerre polynomial.
   :type n: float

   :returns: The Laguerre polynomial.
   :rtype: laguerre (float or ndarray)















   ..
       !! processed by numpydoc !!

.. py:function:: pow2db(power)

   
   Convert power to decibels.

   :param power: Power in watts.
   :type power: float or ndarray

   :returns: Power in decibels.
   :rtype: db (float or ndarray)















   ..
       !! processed by numpydoc !!

.. py:function:: pow2dbm(power)

   
   Convert power to decibels relative to 1 milliwatt.

   :param pow: Power in watts.
   :type pow: float or ndarray

   :returns: Power in decibels relative to 1 milliwatt.
   :rtype: dbm (float or ndarray)















   ..
       !! processed by numpydoc !!

.. py:function:: qfunc(x)

   
   Compute the Q function.

   :param x: Input to the Q function.
   :type x: ndarray

   :returns: The Q function.
   :rtype: qfunc (ndarray)















   ..
       !! processed by numpydoc !!

.. py:function:: randomize_user_pos(bs_pos, user_pos, edge_idx, r_min = [30], r_max = [100])

   
   Randomize the positions of the users in the network, except for the edge user.

   :param bs_pos: A list of the positions of the base stations.
   :type bs_pos: list
   :param user_pos: A list of the positions of the users.
   :type user_pos: list
   :param edge_idx: The index of the edge user.
   :type edge_idx: int
   :param r_min: A list of minimum distances between the users and the base stations. Defaults to [30].
   :type r_min: list
   :param r_max: A list of maximum distances between the users and the base stations. Defaults to [100].
   :type r_max: list

   :returns: A list of the positions of the users.
   :rtype: list















   ..
       !! processed by numpydoc !!

.. py:function:: rolling_mean(data, window_size)

   
   Compute the rolling mean of a curve.

   :param data: The curve to filter.
   :type data: ndarray
   :param window_size: The size of the window.
   :type window_size: int

   :returns: The filtered curve.
   :rtype: list















   ..
       !! processed by numpydoc !!

.. py:function:: wrapTo2Pi(theta)

   
   Wrap an angle to the interval [0, 2 * pi].

   :param theta: The angle to wrap.
   :type theta: ndarray

   :returns: The wrapped angle.
   :rtype: wrapped_theta (ndarray)















   ..
       !! processed by numpydoc !!

