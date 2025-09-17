"""Lateral movement package.

Exports lateral movement helper functions from
:mod:`cai.tools.lateral_movement.ssh_tools`.
"""

from .ssh_tools import (
    ssh_exec,
    ping_host,
    ssh_tunnel,
    smb_list_shares,
    rsync_transfer,
)  # noqa: F401