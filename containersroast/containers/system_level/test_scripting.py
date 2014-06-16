from cafe.drivers.unittest.decorators import tags
from cafe.engine.ssh.models.ssh_response import ExecResponse
from containersroast.fixtures import ContainerFixture


@tags(type='rudimentary')
class TestContainerScripting(ContainerFixture):

    def test_container_scripting(self):
        """ Testing container connection """

        log = self.fixture_log.info

        # Verify Python is installed
        log('Checking if python is installed.')
        response = self._is_python_installed()
        if str(response.stdout) == str(self.ERROR_CODE):
            self.fail('Python is not installed on the host machine')
        binary = response.stdout
        log('Python found: {location}'.format(location=binary))

        print self.execute(cmd='ls')

    def _is_python_installed(self):
        cmd = 'which python'
        return self.get_cmd_single_line_output(cmd=cmd)
