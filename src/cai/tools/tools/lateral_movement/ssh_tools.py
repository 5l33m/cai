"""
Lateral movement tools
======================

These helpers facilitate lateral movement within a network by
executing commands on remote hosts or testing connectivity.  They
are thin wrappers around standard UNIX utilities such as ``ssh``
and ``ping``.  An AI agent can call these functions to pivot from
one machine to another or to probe network reachability.
"""

from cai.tools.common import run_command  # pylint: disable=import-error
from cai.sdk.agents import function_tool  # pylint: disable=import-error


@function_tool
def ssh_exec(user: str, host: str, command: str, port: str = "22", identity_file: str = "", ctf=None) -> str:
    """Execute a command on a remote host via SSH.

    This function constructs and runs an SSH command to execute
    ``command`` on ``host`` as ``user``.  You can optionally specify
    a non‑default port or an identity file (private key).  The SSH
    client will inherit your current SSH configuration for other
    settings such as known_hosts and host verification.

    Args:
        user: Username on the remote host.
        host: Hostname or IP address of the remote machine.
        command: The shell command to run remotely (quotes are added
                 automatically).
        port: SSH port number as a string (default ``22``).
        identity_file: Path to an SSH private key for authentication
            (optional).
        ctf: Optional CTF sandbox context.

    Returns:
        Output from the remote command or any SSH error messages.
    """
    ssh_parts = ["ssh", "-p", port]
    if identity_file:
        ssh_parts += ["-i", identity_file]
    ssh_parts.append(f"{user}@{host}")
    # Wrap the remote command in single quotes to preserve quoting
    ssh_parts.append(f'"{command}"')
    full_cmd = " ".join(ssh_parts)
    return run_command(full_cmd, ctf=ctf)


@function_tool
def ping_host(host: str, count: int = 4, ctf=None) -> str:
    """Send ICMP echo requests to a host to test reachability.

    This function wraps the standard ``ping`` command.  It sends a
    specified number of echo requests to the destination and returns
    the collected statistics.  If ``ping`` is not installed or ICMP
    is blocked, the output will reflect that.

    Args:
        host: Hostname or IP address to ping.
        count: Number of ICMP requests to send (default 4).
        ctf: Optional CTF sandbox context.

    Returns:
        The ping output.
    """
    return run_command(f"ping -c {count} {host}", ctf=ctf)


# ---------------------------------------------------------------------------
# Extended functionality
# ---------------------------------------------------------------------------


@function_tool
def ssh_tunnel(local_port: int, remote_host: str, remote_port: int, user: str, host: str, direction: str = "L", identity_file: str = "", ctf=None) -> str:
    """Establish an SSH port forwarding tunnel.

    Port forwarding can be used to pivot through intermediate hosts or
    expose internal services.  This helper wraps ``ssh`` with the
    appropriate ``-L`` (local) or ``-R`` (remote) option and runs it
    in the background (``-f -N``) so that it doesn't block.

    Args:
        local_port: Port on the local machine (for ``-L``) or remote
            machine (for ``-R``) to bind.
        remote_host: Destination host on the other side of the tunnel.
        remote_port: Destination port on the other side of the tunnel.
        user: Username on the SSH gateway machine.
        host: Address of the SSH gateway.
        direction: Either ``"L"`` for local port forwarding or ``"R"``
            for remote port forwarding (default ``"L"``).
        identity_file: Path to an SSH private key (optional).
        ctf: Optional CTF sandbox context.

    Returns:
        Output from the SSH command.  If successful, the tunnel will
        remain open in the background until manually closed.
    """
    direction = direction.upper()
    if direction not in {"L", "R"}:
        return "Direction must be 'L' or 'R'."
    ssh_parts = ["ssh", "-f", "-N"]  # Run in background, no command execution
    if identity_file:
        ssh_parts += ["-i", identity_file]
    ssh_parts += [f"-{direction}", f"{local_port}:{remote_host}:{remote_port}"]
    ssh_parts += [f"{user}@{host}"]
    cmd = " ".join(ssh_parts)
    return run_command(cmd, ctf=ctf)


@function_tool
def smb_list_shares(host: str, user: str = "", password: str = "", domain: str = "", ctf=None) -> str:
    """List SMB shares on a remote host using ``smbclient``.

    This function queries a Windows or Samba server for available SMB
    shares.  It requires the ``smbclient`` utility from the Samba
    suite.  When no username or password is provided, the function
    attempts an anonymous login.

    Args:
        host: Target host (hostname or IP address).
        user: Username for authentication (optional).
        password: Password for authentication (optional).  Avoid
            including sensitive credentials in logs; consider
            environment variables or interactive input where possible.
        domain: Optional domain or workgroup.
        ctf: Optional CTF sandbox context.

    Returns:
        The share listing returned by ``smbclient``.
    """
    # Build the authentication string
    if user:
        # Escape percent signs in password to avoid shell interpolation
        pw = password.replace('%', '%%') if password else ""
        auth = f"-U {domain + '\\' if domain else ''}{user}%{pw}"
    else:
        auth = "-N"
    cmd = f"smbclient -L //{host} {auth} -g"
    return run_command(cmd, ctf=ctf)


@function_tool
def rsync_transfer(local_path: str, remote_path: str, user: str, host: str, port: str = "22", identity_file: str = "", direction: str = "upload", ctf=None) -> str:
    """Synchronise files or directories using ``rsync`` over SSH.

    ``rsync`` is a fast and flexible file transfer tool that can
    efficiently copy files either to or from a remote host.  This
    function supports both upload (default) and download directions.

    Args:
        local_path: Path to the source file/directory on the local
            system for uploads, or the destination path for downloads.
        remote_path: Destination path on the remote host for uploads,
            or the source path for downloads.
        user: Username on the remote host.
        host: Hostname or IP address of the remote machine.
        port: SSH port (default ``22``).
        identity_file: Path to an SSH private key (optional).
        direction: ``"upload"`` to copy from local to remote (default),
            or ``"download"`` to copy from remote to local.
        ctf: Optional CTF sandbox context.

    Returns:
        Output from the ``rsync`` command.
    """
    direction = direction.lower()
    ssh_opts = ["ssh", "-p", port]
    if identity_file:
        ssh_opts += ["-i", identity_file]
    remote = f"{user}@{host}:{remote_path}"
    # Assemble rsync command.  Wrap ssh options in quotes to ensure they are
    # passed as a single argument to rsync's -e option.
    ssh_cmd = " ".join(ssh_opts)
    base_cmd = ["rsync", "-avz", "-e", f'"{ssh_cmd}"']
    if direction == "upload":
        base_cmd += [local_path, remote]
    elif direction == "download":
        base_cmd += [remote, local_path]
    else:
        return "Direction must be 'upload' or 'download'."
    cmd = " ".join(base_cmd)
    return run_command(cmd, ctf=ctf)