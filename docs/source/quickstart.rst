.. _quickstart:

Quickstart
==========

Installation
------------

Refer to the `Installation <installation.html>`_ page for instructions on how to install SimComm.

Getting Started
---------------

This following example shows how to use SimComm to simulate a simple wireless network. Let us assume that we have a network with two base stations with two respective cell-center users and one cell-edge user, as shown in the following figure:

.. figure:: _static/system.png
    :class: dark-light
    :width: 550px
    :align: center

Firstly, we need to define the environment, which includes the positions of the base stations and users, the fading and pathloss models as well as their configurations. To learn more about what models are available, refer to the `API <api.html>`_. The following code snippet shows how to define the environment:

.. code-block:: python

    environment = {
        "positions": {
            "BS1": [-50, 0, 25],
            "BS2": [50, 0, 25],
            "RIS": [0, 25, 5],
            "Uf": [0, 35, 1],
            "U1c": [-40, 18, 1],
            "U2c": [30, 22, 1],
        },
        "fading": {
            "rayleigh": {"type": "rayleigh", "sigma": 1},
            "ricianE": {"type": "rician", "K": 5, "sigma": 1},
            "ricianC": {"type": "rician", "K": 3, "sigma": 1},
        },
        "pathloss": {
            "center": {"type": "free-space", "alpha": 3, "p0": 30},
            "ris": {"type": "free-space", "alpha": 3, "p0": 30},
            "risOC": {"type": "free-space", "alpha": 2.7, "p0": 30},
            "risOE": {"type": "free-space", "alpha": 2.3, "p0": 30},
            "edge": {"type": "free-space", "alpha": 3.5, "p0": 30},
            "inter": {"type": "free-space", "alpha": 4, "p0": 30},
        },
    }

Next, we need to define the system objects, which include the base stations, users, and the STAR-RIS. The following code snippet shows how to define the system objects:

.. code-block:: python

    import argparse
    import os

    from simcomm.core import STAR, LinkCollection, Receiver, Transmitter

    N = 10000  # Number of channel realizations
    FREQ = 2.4e9  # Frequency of carrier signal in Hz
    Pt = np.linspace(-50, 30, 161)  # Transmit power in dBm

    # Create the base stations
    BS1 = Transmitter("BS1", positions["BS1"], transmit_power=Pt_lin)
    BS2 = Transmitter("BS2", positions["BS2"], transmit_power=Pt_lin)

    # Create the users (identical)
    U1c = Receiver("U1c", positions["U1c"], sensitivity=-110)
    U2c = Receiver("U2c", positions["U2c"], sensitivity=-110)
    Uf = Receiver("Uf", positions["Uf"], sensitivity=-110)

    K = 70  # Number of RIS elements
    bs1_assignment = K // 2  # Number of RIS elements assigned to BS1
    bs2_assignment = K - bs1_assignment  # Number of RIS elements assigned to BS2

    # Create the STAR-RIS element
    RIS = STAR("RIS", positions["RIS"], elements=K)

Lastly, we need to define the links between the system objects. The following code snippet shows how to define the links:

.. code-block:: python

    # Initialize the link collection (containing channel information)
    links = LinkCollection(N, FREQ)

    # Add the center links to the collection
    links.add_link(BS1, U1c, fading_cfg["rayleigh"], pathloss_cfg["center"], "1,c")
    links.add_link(BS2, U2c, fading_cfg["rayleigh"], pathloss_cfg["center"], "2,c")

    # Add the edge links to the collection
    links.add_link(BS1, Uf, fading_cfg["rayleigh"], pathloss_cfg["edge"], bs1_uf_link)
    links.add_link(BS2, Uf, fading_cfg["rayleigh"], pathloss_cfg["edge"], bs2_uf_link)

    # Add the RIS links to the collection
    links.add_link(BS1, RIS, fading_cfg["ricianC"], pathloss_cfg["ris"], "ris", bs1_assignment)
    links.add_link(BS2, RIS, fading_cfg["ricianC"], pathloss_cfg["ris"], "ris", bs2_assignment)
    links.add_link(RIS, U1c, fading_cfg["ricianC"], pathloss_cfg["risOC"], "ris", bs1_assignment)
    links.add_link(RIS, U2c, fading_cfg["ricianC"], pathloss_cfg["risOC"], "ris", bs2_assignment)
    links.add_link(RIS, Uf, fading_cfg["ricianE"], pathloss_cfg["risOE"], "ris", K)

Now, we can run the simulation. We just need to pass the environment, system objects, and links to the simulator. The following code snippet shows how to run the simulation:

.. code-block:: python

    # Run the simulation
    simulator = Simulator(environment, [BS1, BS2, U1c, U2c, Uf, RIS], links)
    simulator.run()

    # Save the results
    simulator.save(os.path.join("results", "example"))

By default, the simulator will only save the :code:`rates`, :code:`sum_rate`, :code:`outage`, :code:`se`, and :code:`ee`, into a :code:`.mat` file. However, you can define your own metrics and save them as well by modifying the :code:`metrics` attribute of the simulator.