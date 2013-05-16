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

class InventoryItem(object):
    def __init__(self, id, name):
        self.__applyChanges(InventoryItemCreated(id, name))

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

        def it_can_be_renamed():
            _.item.rename(OTHER_NAME)
            expect(_.item.name).to.be.equal(OTHER_NAME)
