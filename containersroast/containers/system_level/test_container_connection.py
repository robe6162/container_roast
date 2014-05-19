from cafe.drivers.unittest.decorators import tags
from cafe.engine.ssh.models.ssh_response import ExecResponse
from containersroast.fixtures import ContainerFixture


@tags(type='rudimentary')
class TestContainerConnection(ContainerFixture):

    def test_container_connection(self):
        """Testing container connection."""

        log = self.fixture_log

        self.client.execute('ls')
