.. Keep title but hide it from the main page
.. title:: Welcome to SimComm

.. image:: _static/logo.svg
   :align: center
   :class: transparent-background
   :width: 510px

.. **SimComm** Documentation
.. =========================

**Release** |release|
|
**Date** |today|

Welcome to SimComm's documentation! SimComm is an optimized library for simulating wireless communication systems. It is purely written in Python and used NumPy and SciPy for numerical computation. It is designed to be easy to use and flexible to extend.
The library is actively developed and maintained by **Muhammad Umer** https://github.com/muhd-umer.

.. grid:: 2
   :gutter: 3

   .. grid-item-card:: :material-regular:`api;3.5em`
      :class-card: api-reference
      :class-body: sd-text-white
      :link: api
      :link-type: ref
      :text-align: center

      **API Reference**

      The reference guide provides detailed documentation of the SimComm API. It describes the various modules and functions of the library.

   .. grid-item-card:: :material-regular:`science;3.5em`
      :class-card: research
      :class-body: sd-text-white
      :link: research
      :link-type: ref
      :text-align: center

      **Research**

      The research section provides the details of the research work done using the library.

.. toctree::
   :hidden:
   :maxdepth: 1

   Installation <installation>
   API Reference <api>
   Research <research>