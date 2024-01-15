API Reference
=============

API reference for the ``comyx`` package.

.. toctree::
   :titlesonly:
   
{% for module in ['core', 'metrics', 'stats', 'utils', 'visualize'] %}
   comyx/{{ module }}/index
{% endfor %}