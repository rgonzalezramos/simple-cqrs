from mamba import describe, before, context
from sure import expect

IRRELEVANT_ID = 'id'
IRRELEVANT_NAME = 'irrelevant name'
OTHER_NAME = 'other name'

class InventoryItemCreated(object):
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def apply(self, inventory_item):
        inventory_item.id = self.id
        inventory_item.name = self.name


class InventoryItemRenamed(object):
    def __init__(self, new_name):
        self.new_name = new_name

    def apply(self, inventory_item):
        inventory_item.name = self.new_name


class InventoryItem(object):
    def __init__(self, id, name):
        self.__applyChanges(InventoryItemCreated(id, name))

    def rename(self, new_name):
        self.__applyChanges(InventoryItemRenamed(new_name))

    def __applyChanges(self, event):
        event.apply(self)

with describe(InventoryItem) as _:

    @before.each
    def create_an_item():
        _.item = InventoryItem(IRRELEVANT_ID, IRRELEVANT_NAME)

    def it_has_an_id():
        expect(_.item.id).to.be.equal(IRRELEVANT_ID)

    def it_has_a_name():
        expect(_.item.name).to.be.equal(IRRELEVANT_NAME)

    with context('renaming'):

        def it_can_be_renamed_if_the_new_name_is_valid():
            _.item.rename(OTHER_NAME)
            expect(_.item.name).to.be.equal(OTHER_NAME)

        def it_cannot_be_renamed_if_the_new_name_is_invalid():
            expect(_.item.rename).when.called_with(None).to.throw(ValueError)
            expect(_.item.rename).when.called_with('').to.throw(ValueError)
