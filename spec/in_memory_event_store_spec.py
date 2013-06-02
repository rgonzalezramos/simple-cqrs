from mamba import describe, context, skip
from sure import expect

from spec.constants import *


class InMemoryEventStore(object):
    def __init__(self):
        self.events = {}

    def save(self, aggregate_id, events, version):
        self.events[aggregate_id] = events

    def get_events_for_aggregate(self, aggregate_id):
        return self.events[aggregate_id]

with describe(InMemoryEventStore) as _:

    with describe('getting events for an aggregate'):
        with context('when the aggregate is found'):
            def it_returns_the_aggregates_events():
                _.event_store = InMemoryEventStore()
                aggregate_id = IRRELEVANT_ID
                _.event_store.save(aggregate_id, IRRELEVANT_EVENT, IRRELEVANT_VERSION)
                expect(_.event_store.get_events_for_aggregate(aggregate_id)).to.be.equal(IRRELEVANT_EVENT)

        with context('when no aggregate with provided id is found'):
            @skip
            def it_raises_an_aggregate_not_found_exception():
                pass


