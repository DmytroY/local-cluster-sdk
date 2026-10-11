# local-cluster-sdk/src/local_cluster_sdk/exceptions.py

class ClusterSDKError(Exception):
    """Base exception for all SDK errors."""
    pass

class ClusterUnreachableError(ClusterSDKError):
    """Raised when the server is down or blocked by an iptables firewall."""
    pass

class ModelSwapTimeoutError(ClusterSDKError):
    """Raised when swapping models in limited RAM environments causes a timeout."""
    pass
