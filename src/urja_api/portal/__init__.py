"""Portal Anti-Corruption Layer package.

Contains all communication, authentication, session lifecycle, and parsing
logic specific to the legacy Urja Meter Ops web portal.
"""

from urja_api.portal.client import PortalClient

__all__ = ["PortalClient"]
