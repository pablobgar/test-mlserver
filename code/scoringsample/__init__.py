import asyncio
import logging
import os
import subprocess as sp
import tempfile
from typing import Union

from mlserver.cli.serve import load_settings
from mlserver.server import MLServer


def prometheus_configuration(directory: Union[str, None]) -> None:
    """
    Configures Prometheus multiprocess mode for exposing the metrics endpoint in FastAPI.
    More info in https://github.com/prometheus/client_python#multiprocess-mode-eg-gunicorn
    If the property in the configmap is not set (amiga.prometheus.multiproc_dir) or
    the environment variable PROMETHEUS_MULTIPROC_DIR has no value,
    sets a default one in a system teporary dir.
    """

    if directory:
        # Configure the the PROMETHEUS_MULTIPROC_DIR with the configmap property
        os.environ["PROMETHEUS_MULTIPROC_DIR"] = directory
    if not os.environ.get("PROMETHEUS_MULTIPROC_DIR"):
        with tempfile.TemporaryDirectory() as tmpdirname:
            os.environ["PROMETHEUS_MULTIPROC_DIR"] = tmpdirname
    path_metrics = os.environ["PROMETHEUS_MULTIPROC_DIR"]
    if not os.path.exists(path_metrics):
        os.makedirs(path_metrics)
    logging.debug(f"Defaulting PROMETHEUS_MULTIPROC_DIR to {path_metrics}")


async def start_mlserver_virgin(path: str):
    settings, models_settings = await load_settings(path)

    server = MLServer(settings)
    await server.start(models_settings)


def start() -> None:

    prometheus_configuration(None)
    ml_path = os.environ.get("ML_MODELS_PATH", "ml_models")

    os.chdir(ml_path)
    asyncio.run(start_mlserver_virgin("."))

    # Other way for start mlserver
    # sp.check_call("mlserver start .", shell=True)
