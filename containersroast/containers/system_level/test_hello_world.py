from cafe.drivers.unittest.decorators import tags
from cafe.engine.ssh.models.ssh_response import ExecResponse
from containersroast.fixtures import ContainerHostFixture


@tags(type='rudimentary')
class TestHelloWorld(ContainerHostFixture):

    def test_hello_world(self):
        """ Testing hello world """

        max_nodes = self.container_test_config.mkdir_depth
        log = self.fixture_log

        log.info('Hello, world!')

        print 'Hello, world!'

    def test_command_execution(self):
        """ Testing command execution on host """

        self.client.execute('ls')
