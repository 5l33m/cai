"""Data exfiltration package.

Exports helper functions from
:mod:`cai.tools.data_exfiltration.exfiltration_tools`.
"""

from .exfiltration_tools import (
    compress_directory,
    scp_upload,
    scp_download,
    base64_encode_file,
    upload_http,
    split_file,
    compress_and_encrypt,
)  # noqa: F401