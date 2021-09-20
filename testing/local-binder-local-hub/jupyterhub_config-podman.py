######################################################################
## A development config to test BinderHub locally with podman.
#
# Additional dependencies:
# pip install podmanclispawner repo2podman
#
# Run `jupyterhub --config=jupyterhub_config-podman.py`

# Read in the Docker config, then override for Podman
with open('jupyterhub_config.py') as f:
    exec(f.read())

from binderhub.binderspawner_mixin import BinderSpawnerMixin
from podmanclispawner import PodmanCLISpawner

# image & token are set via spawn options
class LocalContainerSpawner(BinderSpawnerMixin, PodmanCLISpawner):
    pass


c.JupyterHub.spawner_class = LocalContainerSpawner
c.LocalContainerSpawner.remove = True

# c.JupyterHub.authenticator_class = 'dummy'

binderhub_config = os.path.join(os.path.dirname(__file__), 'binderhub_config-podman.py')
c.JupyterHub.services = [{
    "name": binderhub_service_name,
    "admin": True,
    "command": ["python", "-mbinderhub", f"--config={binderhub_config}"],
    "url": f"http://localhost:8585",
}]

# c.BinderHub.auth_enabled = True
# c.BinderHub.cors_allow_origin = "*"
# c.LocalContainerSpawner.auth_enabled = True
# c.LocalContainerSpawner.cors_allow_origin = "*"
# c.HubOAuth.hub_host = f'http://{hostip}:8000'
# c.HubOAuth.api_token = api_token
# c.HubOAuth.api_url = f'http://{hostip}:8000/hub/api/'
# c.HubOAuth.base_url = f'http://{hostip}:8585/'
# c.HubOAuth.hub_prefix = f'http://{hostip}:8585/hub/'
# c.HubOAuth.oauth_redirect_uri = f'http://{hostip}:8585/oauth_callback'
# c.HubOAuth.oauth_client_id = 'binder-oauth-client-test'
