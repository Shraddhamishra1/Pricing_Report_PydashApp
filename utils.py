import os


def get_link(link: str) -> str:
    """
    Adds Dash App Name before the URL in deployed version and does nothing.

    Parameters
    ----------
    link : str
        URL to be modified

    Returns
    -------
    str
        Modified URL

    Examples
    --------
    >>> get_link("/assets/shell-logo.png") # for any images or static files
    "/assets/shell-logo.png" # in local development
    "/<dash-app-name>/assets/shell-logo.png" # in deployed version
    >>> get_link("/") # for home page
    "/" # in local development
    "/<dash-app-name>/" # in deployed version
    >>> get_link("/uploads") # for the Uploads page
    "/uploads" # in local development
    "/<dash-app-name>/uploads" # in deployed version
    """
    return f"{os.environ.get('SCRIPT_NAME', '')}{link}"
