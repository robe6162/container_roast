from cafe.drivers.unittest.decorators import tags
from cafe.engine.ssh.models.ssh_response import ExecResponse
from containersroast.fixtures import ContainerHostFixture, NonContainerFixture


@tags(type='filesys')
class TestFileSystem(NonContainerFixture):
    EXISTS = 'exists'

    def test_file_system_directory_depth(self):
        """Verify the configured directory depth is maintained. """

        test_test_debug = 1

        max_nodes = self.container_test_config.mkdir_depth
        temp_dir = self.container_test_config.temp_mkdir_dir
        log = self.fixture_log

        # Create the directories on the target system
        self._create_dirs(test_dir=temp_dir, max_nodes=max_nodes)
        self._goto_dir('{directory}..'.format(directory=temp_dir))

        # Check output to verify cmd worked correctly
        output_1 = self._get_slabinfo()
        try:
            if output_1.stdout == self.ERROR_CODE + test_test_debug:
                self.fail('No response from slabinfo cmd: {cmd}'.format(
                    cmd=output_1.stdin))
        except ValueError:
            self.fail('Unexpected type of response from slabinfo cmd: '
                      '{cmd}'.format(cmd=output_1.stdin))

        # Create N+1 directories on the target system
        max_nodes_plus_one = max_nodes + 1
        self._create_dirs(test_dir=temp_dir, max_nodes=max_nodes_plus_one)
        self._goto_dir('{directory}..'.format(directory=temp_dir))

        # Check output to verify cmd worked correctly
        output_2 = self._get_slabinfo()
        try:
            if output_2.stdout == self.ERROR_CODE + test_test_debug:
                self.fail('No response from slabinfo cmd: {cmd}'.format(
                    cmd=output_2.stdin))
        except ValueError:
            self.fail('Unexpected type of response from slabinfo cmd: '
                      '{cmd}'.format(cmd=output_2.stdin))

        try:
            log.debug('Apportioned some of the {index} inodes'.format(
                index=int(output_2.stdout) - int(output_1.stdout)))
        except ValueError:
            log.debug('Unable to determine change in apportioned inodes.')
            log.debug('OUTPUT 1: {output}'.format(output=output_1.stdout))
            log.debug('OUTPUT 2: {output}'.format(output=output_2.stdout))
            self.fail('Unable to determine change in apportioned inodes.')

        msg = 'Successfully created path with N={count} children.\n'.format(
            count=max_nodes_plus_one)

        msg = ('{msg}Actual:\t\thost_max_nodes ({host_nodes}) == '
               'lxc_max_nodes ({lxc_nodes})\n'.format(
               msg=msg, host_nodes=max_nodes, lxc_nodes=max_nodes_plus_one))

        msg = ('{msg}Expected:\thost_max_nodes ({max_nodes}) == '
               'lxc_max_nodes ({max_nodes})'.format(max_nodes=max_nodes,
                                                    msg=msg))
        self.assertEqual(int(output_1.stdout), int(output_2.stdout), msg)

    def tearDown(self):
        temp_dir = self.container_test_config.temp_mkdir_dir
        response = self.client.execute(
            '[ -d "{directory}" ] && echo "{found}"'.format(directory=temp_dir,
                                                            found=self.EXISTS))
        if self.EXISTS in response.stdout:
            self.client.execute('rm -rf {temp_dir}'.format(temp_dir=temp_dir))

    def _goto_dir(self, temp_dir):
        return self.client.execute('cd {directory}'.format(directory=temp_dir))

    def _create_dirs(self, test_dir, max_nodes, client=None):
        client = client or self.client

        setup_cmd = 'mkdir -p {directory}; cd {directory}'.format(
            directory=test_dir)

        overall_response = ExecResponse(
            stdin='', stdout='', stderr='', exit_status=-1)

        client.execute(setup_cmd)
        for iter_num in xrange(1, max_nodes):

            # Consider additional (more aggressive) approach for the cmd:
            # d=`printf "x/"%.0s {1..10}`; mkdir -p $d; cd $d

            cmd = 'mkdir {iter_num}; cd {iter_num}'.format(iter_num=iter_num)
            if self.DEBUG:
                self.fixture_log.debug('Issuing cmd: {cmd}'.format(cmd=cmd))

            cmd_response = self.client.execute(cmd)
            if cmd_response.stdout is not None:
                overall_response.stdout += cmd_response.stdout
            if cmd_response.stderr is not None:
                overall_response.stderr += cmd_response.stderr
            if (cmd_response.exit_status is not None and
                    int(cmd_response.exit_status) >
                    overall_response.exit_status):
                overall_response.exit_status = cmd_response.exit_status

        return overall_response

    def _get_slabinfo(self, client=None):
        slab_info_cmd = ("cat /proc/slabinfo | grep ext4_inode_cache | "
                         "cut -d' ' -f 6 ")
        return self.get_cmd_single_line_output(cmd=slab_info_cmd,
                                               client=client)
