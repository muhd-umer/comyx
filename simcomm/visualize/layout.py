import os
from typing import List, Tuple

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.image import imread
from matplotlib.patches import Circle


def plot_network(
    area: float,
    radius: float,
    bs_pos: List[Tuple[float, float]],
    user_pos: List[Tuple[float, float]],
    ris_pos: List[Tuple[float, float]] = None,
    save: bool = False,
    save_path: str = None,
) -> None:
    """Plot the layout of the network.

    Args:
        area: The area of the network.
        radius: The radius of the base stations.
        bs_pos: The positions of the base stations.
        user_pos: The positions of the users.
        ris_pos: The positions of the RISs. Defaults to None.
        save: Whether to save the figure. Defaults to False.
        save_path: The path to save the figure. Required if save is True.

    Returns:
        None
    """
    _, ax = plt.subplots(figsize=(6, 4))
    plt.xlabel("x (m)")
    plt.ylabel("y (m)")
    plt.xlim([-area, area])
    plt.ylim([-area / 1.5, area / 1.5])
    plt.grid()

    for bs in bs_pos:
        circle = Circle(bs, radius=radius, fill=False, alpha=0.25)
        ax.add_patch(circle)
        bs_img = imread("../resources/bs.png")
        plt.imshow(
            bs_img, extent=[bs[0] - 30, bs[0] + 30, bs[1] - 40, bs[1] + 40], zorder=2
        )

    for i, bs in enumerate(bs_pos):
        if ris_pos is not None:
            for j, ris in enumerate(ris_pos):
                plt.plot([bs[0], ris[0]], [bs[1], ris[1]], "k-", zorder=1)

    for user in user_pos:
        for bs in bs_pos:
            if np.linalg.norm(user - bs) == np.min(
                np.linalg.norm(user_pos - bs, axis=1)
            ):
                plt.plot([bs[0], user[0]], [bs[1] + 25, user[1]], "g-", zorder=1)
            else:
                if (user == user_pos[1]).all():
                    plt.plot([bs[0], user[0]], [bs[1] + 25, user[1]], "b:", zorder=1)
                else:
                    # plt.plot([bs[0], user[0]], [bs[1] + 25, user[1]], "r--", zorder=1)
                    pass
        user_img = imread("../resources/user.png")
        plt.imshow(
            user_img,
            extent=[user[0] - 30, user[0] + 30, user[1] - 30, user[1] + 30],
            zorder=2,
        )

    if ris_pos is not None:
        for ris in ris_pos:
            ris_img = imread("../resources/starris.png")
            plt.imshow(
                ris_img,
                extent=[ris[0] - 35, ris[0] + 35, ris[1] - 50, ris[1] + 50],
                zorder=0,
            )

        for j, user in enumerate(user_pos):
            if j == 0 or j == 2:
                plt.plot([ris[0], user[0]], [ris[1], user[1]], "k--", zorder=1)
            else:
                plt.plot([ris[0], user[0]], [ris[1], user[1]], "m--", zorder=1)

        plt.plot([], [], "g-", label="Direct Link", zorder=1)
        # plt.plot([], [], "r--", label="Interference Link", zorder=1)
        plt.plot([], [], "b--", label="ICI Link", zorder=1)
        plt.plot([], [], "k--", label="Reflection Link", zorder=1)
        plt.plot([], [], "m--", label="Transmission Link", zorder=1)

    else:
        plt.plot([], [], "g-", label="Direct Link", zorder=1)
        # plt.plot([], [], "r--", label="Interference Link", zorder=1)
        plt.plot([], [], "b--", label="ICI Link", zorder=1)

    plt.title("Network Layout")
    plt.legend()
    if save:
        assert save_path is not None, "Please specify a path to save the figure."
        plt.savefig(os.path.join(save_path, "layout.pdf"), bbox_inches="tight")
    plt.show()
    plt.show()
