.. Keep title but hide it from the main page
.. title:: Comyx

.. figure:: _static/logo_full.svg
   :align: center
   :class: dark-light
   :width: 580px

.. **Comyx** Documentation
.. =========================

**Release** |release|
|
**Date** |today|

Welcome to Comyx's documentation! Comyx is a Python library for simulating wireless communication systems. It uses NumPy and SciPy for numerical computation, and Numba for just-in-time (JIT) compilation. It is designed to be easy to use and flexible to extend.
The library is actively developed and maintained by **Muhammad Umer** https://github.com/muhd-umer.


.. grid:: 3
   :gutter: 3

   .. grid-item-card:: :material-regular:`rocket_launch;3.5em`
      :class-card: api-reference
      :class-body: sd-text-white
      :link: quickstart.html
      :text-align: center

      **Quickstart**

   .. grid-item-card:: :material-regular:`api;3.5em`
      :class-card: quickstart
      :class-body: sd-text-white
      :link: api/index.html
      :text-align: center

      **API Reference**

   .. grid-item-card:: :material-regular:`science;3.5em`
      :class-card: research
      :class-body: sd-text-white
      :link: research.html
      :text-align: center

      **Research**

.. toctree::
   :hidden:
   :maxdepth: 1

   Installation <installation>
   Quickstart <quickstart>
   API Reference <api/index>
   Research <research>
   Changelog <https://github.com/muhd-umer/comyx/releases>