"""
Privilege escalation tools
==========================

This module provides helper functions for the privilege‑escalation
phase.  The functions wrap common enumeration commands used to
discover potential escalation vectors such as SUID binaries, sudo
permissions and kernel information.  They return the raw output
from the host so that an AI agent can interpret the results.
"""

from cai.tools.common import run_command  # pylint: disable=import-error
from cai.sdk.agents import function_tool  # pylint: disable=import-error


@function_tool
def list_suid_files(ctf=None) -> str:
    """List all SUID binaries on the system.

    The SUID (set‑user‑ID) bit allows executables to run with the
    privileges of their owner (often root).  Misconfigured SUID
    binaries are a common privilege escalation vector.

    Args:
        ctf: Optional CTF sandbox context.

    Returns:
        A newline‑separated list of SUID files found on the system.
    """
    cmd = "find / -perm -4000 -type f 2>/dev/null"
    return run_command(cmd, ctf=ctf)


@function_tool
def sudo_permissions(ctf=None) -> str:
    """Show the current user's sudo privileges.

    Running ``sudo -l`` prints the commands that the current user is
    allowed to execute via sudo without a password.  This information
    is useful for identifying potential escalation paths.

    Args:
        ctf: Optional CTF sandbox context.

    Returns:
        The output of ``sudo -l``.
    """
    return run_command("sudo -l", ctf=ctf)


@function_tool
def kernel_info(ctf=None) -> str:
    """Return kernel and operating system information.

    This function runs ``uname -a`` to display the kernel version,
    architecture and other platform details.  Knowing the kernel
    version can help determine whether known local privilege
    escalation exploits are applicable.

    Args:
        ctf: Optional CTF sandbox context.

    Returns:
        The output of ``uname -a``.
    """
    return run_command("uname -a", ctf=ctf)


# ---------------------------------------------------------------------------
# Extended functionality
# ---------------------------------------------------------------------------


@function_tool
def world_writable_dirs(ctf=None) -> str:
    """Enumerate world‑writable directories on the filesystem.

    World‑writable directories can sometimes be abused for privilege
    escalation, especially if they reside in privileged locations.  This
    function uses ``find`` to search for directories with the write bit
    set for all users.

    Args:
        ctf: Optional CTF sandbox context.

    Returns:
        A newline‑separated list of world‑writable directories.
    """
    cmd = "find / -perm -0002 -type d 2>/dev/null"
    return run_command(cmd, ctf=ctf)


@function_tool
def list_file_capabilities(ctf=None) -> str:
    """List file capabilities set on binaries.

    Linux file capabilities grant fine‑grained privileges to executables.
    Misconfigured capabilities can provide unintended access.  This
    function runs ``getcap -r /`` to recursively list capabilities on
    every file.  Note that ``getcap`` may not be installed on all
    systems.

    Args:
        ctf: Optional CTF sandbox context.

    Returns:
        The output of ``getcap -r /``.
    """
    return run_command("getcap -r / 2>/dev/null", ctf=ctf)


@function_tool
def list_cron_jobs(ctf=None) -> str:
    """Enumerate system and user cron jobs.

    Cron jobs executed with elevated privileges can be leveraged for
    privilege escalation if they run scripts from writable locations.
    This function gathers cron jobs from ``/etc/crontab``, ``/etc/cron*``
    directories and the current user's crontab.

    Args:
        ctf: Optional CTF sandbox context.

    Returns:
        Combined listings of system and user cron entries.
    """
    commands = [
        "echo '[System crontab]'",
        "cat /etc/crontab 2>/dev/null || true",
        "echo '\n[/etc/cron* directories]'",
        "ls -l /etc/cron* 2>/dev/null || true",
        "echo '\n[Current user crontab]'",
        "crontab -l 2>/dev/null || echo 'No user crontab'",
    ]
    cmd = " && ".join(commands)
    return run_command(cmd, ctf=ctf)