from cafe.drivers.unittest.decorators import tags
from containersroast.fixtures import ContainerHostFixture, NonContainerFixture


class TestProcessMgmt(NonContainerFixture):

    @tags(type='process')
    def test_fork_bomb(self):
        """ Test process limitation enforcement """
        max_procs = self.container_test_config.max_fork_bomb_processes
        max_plus_one = max_procs + 1
        log = self.fixture_log.info

        temp_script = '/tmp/forkabuse.py'
        script_complete_phrase = 'process complete'

        code = """#!/usr/bin/env python
import os, sys, time
num_procs = int(sys.argv[1])
for _ in xrange(num_procs):
    try:
        pid = os.fork()
    except OSError as e:
        if e.errno == 11:
            raise e
    if pid == 0:
        continue
    break
time.sleep(3)
print "{terminate}"
""".format(terminate=script_complete_phrase)

        # Verify Python is installed
        log('Checking if python is installed.')
        response = self._is_python_installed()
        if str(response.stdout) == str(self.ERROR_CODE):
            self.fail('Python is not installed on the host machine')
        binary = response.stdout
        log('Python found: {location}'.format(location=binary))

        # Create and validate remote test script
        log('Create the remote test script')
        self.client.execute("echo '{code}' > {filename}".format(
            filename=temp_script, code=code))

        log('Verifying temp test script was created.')
        cmd = 'dir -alF {filename}'.format(filename=temp_script)
        response = self.get_cmd_single_line_output(cmd=cmd)
        if ('no such file' in response.stdout.lower() or
                temp_script not in response.stdout):
            self.fail('Unable to find {filename}'.format(filename=temp_script))
        log('Test script exists: {location}'.format(location=response.stdout))

        # Execute the remote script and process the response
        response = self.client.execute('{binary} {script} {num_procs}'.format(
            script=temp_script, num_procs=max_plus_one, binary=binary),
            prompt=self._get_prompt())
        processes=response.stdout.count(script_complete_phrase)
        log('Number of processes executed: {num}'.format(num=processes))

        # Validate response
        msg = ("Successfully executed N={num_forks} forks.\n"
               "Actual:\t\tForked ({num_forks}) != lxc_max_procs ({max_procs})"
               "\nExpected:\tForked ({max_procs}) == lxc_max_procs "
               "({max_procs})\n")
        msg = msg.format(num_forks=max_plus_one + 1, max_procs=max_procs + 1)
        self.assertNotEqual(processes, max_plus_one + 1, msg)
        log("Successfully executed N={max_procs} forks.\n"
            "Expected:\tN ({max_procs}) == lxc_max_procs ({max_procs})"
            "\n".format(max_procs=processes))

        # Remove the script
        self.client.execute('rm {script}'.format(script=temp_script))

    def _is_python_installed(self):
        cmd = 'which python'
        return self.get_cmd_single_line_output(cmd=cmd)

    def _get_prompt(self):
        cmd = "echo 1"
        self.fixture_log.info('Determining command line prompt...')
        response = self.client.execute(cmd)
        prompt_line = response.stdout.split('\n')[-1].strip()
        prompt = prompt_line[-1:]
        self.fixture_log.info("Prompt: '{prompt}'".format(prompt=prompt))
        return prompt
