.. _quickstart:

Quickstart
==========

Installation
------------

Refer to the `Installation <installation.html>`_ page for instructions on how to install Comyx.

Getting Started
---------------

This following example shows how to use Comyx to simulate a simple wireless network. Let us assume that we have a network with two base stations with two respective cell-center users and one cell-edge user, as shown in the following figure:

.. figure:: _static/system.png
    :class: dark-light
    :width: 550px
    :align: center

Firstly, we need to define the environment, which includes the positions of the base stations and users, the fading and pathloss models as well as their configurations. To learn more about what models are available, refer to the `API <api.html>`_. The following code snippet shows how to define the environment:

.. code-block:: python

    environment = {
        "positions": {
            "BS1": [-50, 0, 25],  # BS1 position
            "BS2": [50, 0, 25],  # BS2 position
            "RIS": [0, 25, 5],  # RIS position
            "Uf": [0, 35, 1],  # Uf position
            "U1c": [-40, 18, 1],  # U1c position
            "U2c": [30, 22, 1],  # U2c position
        },
        "fading": {
            "rayleigh": {"type": "rayleigh", "sigma": 1},  # Rayleigh fading
            "ricianE": {
                "type": "rician",
                "K": 5,
                "sigma": 1,
            },  # Rician fading for edge users
            "ricianC": {
                "type": "rician",
                "K": 3,
                "sigma": 1,
            },  # Rician fading for center users
        },
        "pathloss": {
            "center": {"type": "free-space", "alpha": 3, "p0": 30},  # Center users
            "ris": {"type": "free-space", "alpha": 3, "p0": 30},  # BS to RIS
            "risC": {"type": "free-space", "alpha": 2.7, "p0": 30},  # RIS to center users
            "risE": {"type": "free-space", "alpha": 2.3, "p0": 30},  # RIS to edge user
            "edge": {"type": "free-space", "alpha": 3.5, "p0": 30},  # Edge users
            "inter": {"type": "free-space", "alpha": 4, "p0": 30},  # Interference links
        },
    }

Next, we need to define the system objects, which include the base stations, users, and the STAR-RIS. The following code snippet shows how to define the system objects:

.. code-block:: python

    import argparse
    import os

    import numpy as np
    from config import constants, environment, setting

    import comyx.core.propagation as prop
    from comyx.core import STAR, LinkCollection, Receiver, Simulator, Transmitter
    from comyx.utils import dbm2pow

    Pt = np.linspace(-50, 30, 161)  # Transmit power in dBm
    Pt_lin = dbm2pow(Pt)  # Transmit power in linear scale
    N0 = prop.get_noise_power(BANDWIDTH, TEMP, 12)  # Noise power in dBm
    P_circuit = 10 ** (-3)  # Circuit power in watts

    params = setting[link_option]
    ris_enhanced = params["ris_enhanced"]  # Whether to use RIS-enhanced transmission

    # Create the base stations
    BS1 = Transmitter("BS1", positions["BS1"], Pt_lin, {"U1c": 0.3, "Uf": 0.7})
    BS2 = Transmitter("BS2", positions["BS2"], Pt_lin, {"U2c": 0.3, "Uf": 0.7})

    # Create the users (identical)
    U1c = Receiver("U1c", positions["U1c"], sensitivity=-110)
    U2c = Receiver("U2c", positions["U2c"], sensitivity=-110)
    Uf = Receiver("Uf", positions["Uf"], sensitivity=-110)

Lastly, we need to define the links between the system objects. The following code snippet shows how to define the links:

.. code-block:: python

    # Initialize the link collection (containing channel information)
    links = LinkCollection(N, FREQ)

    # Add the center links to the collection
    links.add_link(BS1, U1c, fading_cfg["rayleigh"], pathloss_cfg["center"], "1,c")
    links.add_link(BS2, U2c, fading_cfg["rayleigh"], pathloss_cfg["center"], "2,c")

    # Add the edge links to the collection
    links.add_link(BS1, Uf, fading_cfg["rayleigh"], pathloss_cfg["edge"], "f")
    links.add_link(BS2, Uf, fading_cfg["rayleigh"], pathloss_cfg["edge"], "f")

    # Add interference links to the collection
    links.add_link(BS1, U2c, fading_cfg["rayleigh"], pathloss_cfg["inter"], "i,c")
    links.add_link(BS2, U1c, fading_cfg["rayleigh"], pathloss_cfg["inter"], "i,c")

    # Update the link collection
    if ris_enhanced:
        K = params["ris_elements"]  # Number of RIS elements

        # Create the STAR-RIS element
        RIS = STAR("RIS", positions["RIS"], elements=K)

        # Add the RIS links to the collection
        links.add_link(BS1, RIS, fading_cfg["ricianC"], pathloss_cfg["ris"], "ris,b1")
        links.add_link(BS2, RIS, fading_cfg["ricianC"], pathloss_cfg["ris"], "ris,b2")
        links.add_link(RIS, U1c, fading_cfg["ricianC"], pathloss_cfg["risC"], "ris,b1")
        links.add_link(RIS, U2c, fading_cfg["ricianC"], pathloss_cfg["risC"], "ris,b2")
        links.add_link(RIS, Uf, fading_cfg["ricianE"], pathloss_cfg["risE"], "ris,f")
    else:
        RIS = None

Now, we can run the simulation. We just need to pass the environment, system objects, and links to the simulator. The following code snippet shows how to run the simulation:

.. code-block:: python

    # Simulate the system
    simulator = Simulator(
        [BS1, BS2], [U1c, U2c, Uf], link_option, RIS, custom_run, save_path
    )
    simulator.run(N, Pt, N0, links, SIGMA, P_circuit, comp=True)

By default, the simulator will only save the :code:`rates`, :code:`sum_rate`, :code:`outage`, :code:`se`, and :code:`ee`, into a :code:`.mat` file. However, you can define your own metrics and save them as well by modifying the :code:`metrics` attribute of the simulator.