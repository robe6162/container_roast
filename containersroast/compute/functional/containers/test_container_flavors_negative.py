"""
Copyright 2014 Rackspace

"""

from cafe.drivers.unittest.decorators import tags

from cloudcafe.common.tools.datagen import rand_name
from cloudcafe.compute.common.exceptions import BadRequest
from cloudcafe.compute.common.types import NovaServerStatusTypes
from cloudroast.compute.fixtures import ComputeFixture

from containerscafe.compute.config import ContainersConfig


class ContainerFlavorsNegativeTest(ComputeFixture):

    @classmethod
    def setUpClass(cls):
        super(ContainerFlavorsNegativeTest, cls).setUpClass()

        container_flavor_config = ContainersConfig()
        cls.container_flavor_id = container_flavor_config.primary_flavor

        # Create a server with a normal flavor
        cls.name = rand_name("server")
        cls.create_resp = cls.servers_client.create_server(
            cls.name, cls.image_ref, cls.flavor_ref)
        cls.server = cls.create_resp.entity
        cls.resources.add(cls.server.id,
                          cls.servers_client.delete_server)

        # Create a container from the container flavor class
        cls.name = rand_name("container")
        cls.create_resp = cls.servers_client.create_server(
            cls.name, cls.image_ref, cls.container_flavor_id)
        cls.container = cls.create_resp.entity
        cls.resources.add(cls.container.id,
                          cls.servers_client.delete_server)

        # Wait for both instances to become active
        cls.server_behaviors.wait_for_server_status(
            cls.server.id, NovaServerStatusTypes.ACTIVE)
        cls.server_behaviors.wait_for_server_status(
            cls.container.id, NovaServerStatusTypes.ACTIVE)

    @tags(type='smoke')
    def test_cannot_resize_container_to_server_flavor(self):
        """Verify that a container flavor cannot be resized to
        a server flavor.
        """
        with self.assertRaises(BadRequest):
            self.servers_client.resize(
                self.container.id, self.flavor_ref)

    @tags(type='smoke')
    def test_cannot_resize_server_to_container_flavor(self):
        """Verify that a server flavor cannot resize to a container flavor.
        """
        with self.assertRaises(BadRequest):
            self.servers_client.resize(
                self.server.id, self.performance_flavor_id)
