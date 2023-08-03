.. Keep title but hide it from the main page
.. title:: Welcome to SimComm

.. figure:: _static/logo.svg
   :align: center
   :class: dark-light
   :width: 530px

.. **SimComm** Documentation
.. =========================

**Release** |release|
|
**Date** |today|

Welcome to SimComm's documentation! SimComm is an optimized library for simulating wireless communication systems. It is purely written in Python and used NumPy and SciPy for numerical computation. It is designed to be easy to use and flexible to extend.
The library is actively developed and maintained by **Muhammad Umer** https://github.com/muhd-umer.

.. grid:: 3
   :gutter: 3

   .. grid-item-card:: :material-regular:`rocket_launch;3.5em`
      :class-card: api-reference
      :class-body: sd-text-white
      :link: quickstart
      :link-type: ref
      :text-align: center

      **Quickstart**

   .. grid-item-card:: :material-regular:`api;3.5em`
      :class-card: quickstart
      :class-body: sd-text-white
      :link: api
      :link-type: ref
      :text-align: center

      **API Reference**

   .. grid-item-card:: :material-regular:`science;3.5em`
      :class-card: research
      :class-body: sd-text-white
      :link: research
      :link-type: ref
      :text-align: center

      **Research**

.. toctree::
   :hidden:
   :maxdepth: 1

   Installation <installation>
   Quickstart <quickstart>
   API Reference <api>
   Research <research>
   Changelog <https://github.com/muhd-umer/simcomm/releases>