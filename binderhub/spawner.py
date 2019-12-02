from tornado import web
from kubespawner import KubeSpawner
from traitlets import Unicode


# image set via user options
class AuthenticatedBinderSpawner(KubeSpawner):

    def start(self):
        if 'image' in self.user_options:
            self.image = self.user_options['image']
        return super().start()

    def get_env(self):
        env = super().get_env()
        if 'repo_url' in self.user_options:
            env['BINDER_REPO_URL'] = self.user_options['repo_url']
        for key in (
                'binder_ref_url',
                'binder_launch_host',
                'binder_persistent_request',
                'binder_request'):
            if key in self.user_options:
                env[key.upper()] = self.user_options[key]
        return env


# image & token are set via spawn options
class AnonymousBinderSpawner(AuthenticatedBinderSpawner):

    allow_origin = Unicode(
        '',
        config=True,
        help="""
        CORS: allowed origins
        """
    )

    def get_args(self):
        args = [
            '--ip=0.0.0.0',
            '--port=%i' % self.port,
            '--NotebookApp.base_url=%s' % self.server.base_url,
            '--NotebookApp.token=%s' % self.user_options['token'],
            '--NotebookApp.trust_xheaders=True',
        ]
        if self.allow_origin:
            args.append('--NotebookApp.allow_origin=' + self.allow_origin)
        return args + self.args

    def start(self):
        if 'token' not in self.user_options:
            raise web.HTTPError(400, "token required")
        if 'image' not in self.user_options:
            raise web.HTTPError(400, "image required")
        return super().start()
