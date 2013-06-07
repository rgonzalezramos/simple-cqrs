from mamba import describe, context, before
from sure import *
from doublex import *
from hamcrest import instance_of

from spec.constants import *

from simplecqrs.persistence import Repository
from simplecqrs.inventory import InventoryItem
from simplecqrs.commands import *


class InventoryCommandsHandler(object):
    def __init__(self, inventory_item_repository):
        self.inventory_item_repository = inventory_item_repository

    def handle(self, command):
        if command.__class__ == CreateInventoryItem:
            self.inventory_item_repository.save(InventoryItem(command.item_id, command.item_name))

        if command.__class__ == RenameInventoryItem:
            item = self.inventory_item_repository.find_by_id(command.item_id)
            item.rename(command.new_item_name)
            self.inventory_item_repository.save(item, command.original_version)

        if command.__class__ == DeactivateInventoryItem:
            item = self.inventory_item_repository.find_by_id(command.item_id)
            item.deactivate()
            self.inventory_item_repository.save(item, command.original_version)




with describe('InventoryCommandsHandler') as _:

    @before.each
    def create_handler():
        _.repository = Spy(Repository)
        _.handler = InventoryCommandsHandler(_.repository)

    def it_can_handle_a_create_inventory_item_command():
        _.handler.handle(CreateInventoryItem(IRRELEVANT_ID, IRRELEVANT_NAME))

        assert_that(_.repository.save, called().with_args(instance_of(InventoryItem)))

    def it_can_handle_rename_inventory_item_commands():
        item = Spy(InventoryItem)
        with _.repository as r: r.find_by_id(IRRELEVANT_ID).returns(item)

        _.handler.handle(RenameInventoryItem(IRRELEVANT_ID, IRRELEVANT_NAME, IRRELEVANT_VERSION))

        assert_that(item.rename, called().with_args(IRRELEVANT_NAME))
        assert_that(_.repository.save, called().with_args(item, IRRELEVANT_VERSION))

    def it_can_handle_deactivate_inventory_item_commands():
        item = Spy(InventoryItem)
        with _.repository as r: r.find_by_id(IRRELEVANT_ID).returns(item)

        _.handler.handle(DeactivateInventoryItem(IRRELEVANT_ID, IRRELEVANT_VERSION))

        assert_that(item.deactivate, called())
        assert_that(_.repository.save, called().with_args(item, IRRELEVANT_VERSION))

