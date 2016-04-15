from djapian import space, Indexer, CompositeIndexer

from store.models import Store

class StoreIndexer(Indexer):
    fields=['name']

space.add_index(Store,StoreIndexer,attach_as='indexer')
store_indexers=CompositeIndexer(Store.indexer)
