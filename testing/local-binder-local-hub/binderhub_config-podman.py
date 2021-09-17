######################################################################
## A development config to test BinderHub locally with podman
#
# If you are running BinderHub manually (not via JupyterHub) run
# `python -m binderhub -f binderhub_config-podman.py`

# Read in the Docker config, then override for Podman

with open('binderhub_config.py') as f:
    exec(f.read())

from binderhub.registry import FakeRegistry
from binderhub.build_local import LocalRepo2dockerBuild
import subprocess

class LocalPodmanRegistry(FakeRegistry):
    async def get_image_manifest(self, image, tag):
        cmd = ['podman', 'image', 'exists', f'{image}:{tag}']
        print(' '.join(cmd))
        r = subprocess.call(cmd)
        if r == 0:
            return {"image": image, "tag": tag}
        return None

c.BinderHub.use_registry = True
c.BinderHub.registry_class = LocalPodmanRegistry
c.BinderHub.image_prefix = 'localhost/'

class LocalRepo2dockerPodmanBuild(LocalRepo2dockerBuild):
    def get_r2d_cmd_options(self):
        return super().get_r2d_cmd_options() + [
            '--engine', 'podman',
        ]

c.BinderHub.build_class = LocalRepo2dockerPodmanBuild
