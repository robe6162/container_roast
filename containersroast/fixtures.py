from cafe.drivers.unittest.fixtures import BaseTestFixture
from containerscafe.containers.config \
    import ContainersSetupConfig, ContainerTestParameters
from containerscafe.containers.container_factory import BuildContainerClient

class ContainerHostFixture(BaseTestFixture):
    """
    Used for connecting to the system that will be HOSTING the container.
     (For nested containers, this host could be a container).
    """

    REFERENCE_POINT = BuildContainerClient.HOST
    ERROR_CODE = -1

    @classmethod
    def setUpClass(cls):
        super(ContainerHostFixture, cls).setUpClass()
        cls.container_config = ContainersSetupConfig()
        cls.container_test_config = ContainerTestParameters()
        cls.DEBUG = cls.container_test_config.debug

        container_type = cls.container_config.container_type
        container_name = cls.container_config.default_container_name

        container_init = BuildContainerClient(
            container_type=container_type,
            test_ref_point=cls.REFERENCE_POINT,
            container_config=cls.container_config,
            test_config=cls.container_test_config,
            username=cls.container_config.host_username,
            password=cls.container_config.host_password,
            container_name=container_name)

        cls.client = container_init.get_client()
        if cls.client is None:
            cls.assertClassSetupFailure(
                'Unable to create connection to target:\n'
                'Container Type: {type_}\n'
                'Reference Point: {ref_pt}\n'
                'Container Name: {name}'.format(type_=container_type,
                                                ref_pt=cls.REFERENCE_POINT,
                                                name=container_name))

    def setUp(self):
        super(ContainerHostFixture, self).setUp()
        self.fixture_log.info("DEBUG enabled: {debug}".format(
            debug=self.DEBUG))

        print self.client.execute('ls')

    @classmethod
    def tearDownClass(cls):
        super(ContainerHostFixture, cls).tearDownClass()
        cls.client.clean()


class ContainerFixture(ContainerHostFixture):
    """
    Used for connecting to the container.
    """

    REFERENCE_POINT = BuildContainerClient.HOST

    @classmethod
    def setUpClass(cls):
        super(ContainerFixture, cls).setUpClass()

        container_type = cls.container_config.container_type
        container_name = cls.container_config.default_container_name

        # TODO (nelsnelson) Automate container setup through client to host.
        print cls.client.execute('ls')

        cls.client.clean()

        container_init = BuildContainerClient(
            container_type=container_type,
            test_ref_point=BuildContainerClient.CONTAINER,
            container_config=cls.container_config,
            test_config=cls.container_test_config,
            username=cls.container_config.container_username,
            password=cls.container_config.container_password,
            container_name=container_name)

        cls.client = container_init.get_client()
        if cls.client is None:
            cls.assertClassSetupFailure(
                'Unable to create connection to target:\n'
                'Container Type: {type_}\n'
                'Reference Point: {ref_pt}\n'
                'Container Name: {name}'.format(type_=container_type,
                                                ref_pt=cls.REFERENCE_POINT,
                                                name=container_name))

    def setUp(self):
        super(ContainerFixture, self).setUp()
        self.fixture_log.info("DEBUG enabled: {debug}".format(
            debug=self.DEBUG))
        self.fixture_log.info("TEST REFERENCE POINT: {reference}".format(
            reference=self.REFERENCE_POINT))

    @classmethod
    def tearDownClass(cls):
        super(ContainerFixture, cls).tearDownClass()
        #cls.client.clean()


class NonContainerFixture(BaseTestFixture):

    """
    Used for building tests without a container available. Eventually this
    fixture should be deleted.
    """

    REFERENCE_POINT = BuildContainerClient.CONTAINER
    # REFERENCE_POINT = BuildContainerClient.HOST
    # REFERENCE_POINT = BuildContainerClient.HOST_TO_CONTAINER
    ERROR_CODE = -1

    @classmethod
    def setUpClass(cls):
        super(NonContainerFixture, cls).setUpClass()
        cls.container_config = ContainersSetupConfig()
        cls.container_test_config = ContainerTestParameters()
        cls.DEBUG = cls.container_test_config.debug

        container_type = cls.container_config.container_type
        container_name = cls.container_config.default_container_name

        container_init = BuildContainerClient(
            container_type=container_type,
            container_config=cls.container_config,
            test_ref_point=cls.REFERENCE_POINT,
            test_config=cls.container_test_config,
            container_name=container_name)

        cls.client = container_init.get_client()
        if cls.client is None:
            cls.assertClassSetupFailure(
                'Unable to create connection to target:\n'
                'Container Type: {type_}\n'
                'Reference Point: {ref_pt}\n'
                'Container Name: {name}'.format(type_=container_type,
                                                ref_pt=cls.REFERENCE_POINT,
                                                name=container_name))

    def setUp(self):
        super(NonContainerFixture, self).setUp()
        self.fixture_log.info("DEBUG enabled: {debug}".format(
            debug=self.DEBUG))
        self.fixture_log.info("TEST REFERENCE POINT: {reference}".format(
            reference=self.REFERENCE_POINT))

    @classmethod
    def tearDownClass(cls):
        super(NonContainerFixture, cls).tearDownClass()
        cls.client.clean()

    def get_cmd_single_line_output(self, cmd, client=None, prompts=None):
        log = self.fixture_log
        prompts = prompts or ('#', '\$')
        client = client or self.client

        response = client.execute(cmd)

        log.info('STD_OUT:\n{stdout}'.format(stdout=response.stdout))
        log.info('STD_ERR:\n{stderr}'.format(stderr=response.stdout))

        output = str(response.stdout).split('\n')[1].strip()
        for prompt in prompts:
            if prompt in str(output):
                output = self.ERROR_CODE
        response.stdout = output
        response.stdin = cmd
        return response
