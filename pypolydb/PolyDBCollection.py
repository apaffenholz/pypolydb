from .utilities import *
from .PolyDBCursor import PolyDBCursor

class PolyDBCollection():
    """
    A wrapper for a collection in PolyDB

    :param collectioname: name of the collection
    :result: an instance of PolyDBCollection
    """

    def __init__(self, db, collectionname=None):
        if collectionname:
            self._collection = db[collectionname]
            self._db = db
            self._name = collectionname
        else:
            self._collection = None

    def info(self) -> dict:
        """
        Returns information about a collection

        :param collection: the name of the collection
        :return: list
        """

        collection_coll = self._db['_collectionInfo.'+self._name]
        data  = { '_id' : self._name + '.2.1' }
        collection_info = collection_coll.find_one(data)

        if collection_info is None:
            print("No collection with this name found")
            return None

        info = {
            'author' : collection_info['author'],
            'contributor' : collection_info['contributor'],
            'maintainer' : collection_info['maintainer'],
            'references' : collection_info['references'],
            'description' : collection_info['description'],
        }
        return info

    def find_one(self, \
                 filter : list|None = None, \
                 sort : list|None = None, \
                 projection : list|None = None, \
                 skip : int = 0, \
                **kwargs) -> list|None:
        """
        Find one element in the collection

        :param filter: a filter document for the query
        :param sort: fix a specific sort order
        :param projection: a projection document for the query
        :param skip: specifies how many documents should be skipped at the beggining of the result set
        :return: a document from the database, or None if no document is found
        """

        if not kwargs:
            kwargs = dict()

        if filter is not None:
            kwargs['filter'] = filter

        if sort is not None:
            kwargs['sort'] = sort
        
        if projection is not None:
            kwargs['projection'] = projection

        if skip != 0:
            kwargs['skip'] = skip

        return _sanitize_result(self._collection.find_one(filter=filter))
    
    def name(self) -> str:
        return self._collection.name

    def find(self, \
             filter : list|None = None, \
             sort : list|None = None, \
             projection : list|None = None, \
             skip : int = 0, \
             limit : int = 0, \
             batch_size : int = 0, \
             **kwargs) -> PolyDBCursor|None:
        """
        Return a curser over all elements in the collection matching the given conditions

        :param filter: a filter document for the query
        :param sort: fix a specific sort order
        :param projection: a projection document for the query
        :param skip: specifies how many documents should be skipped at the beggining of the result set
        :param limit: limits the number of documents returned by the query
        :param batch_size: specifies how many documents should be obtained in each call to the database
        :return: a PolyDBCursor, or None if no document is found
        """

        if not kwargs:
            kwargs = dict()

        if filter is not None:
            kwargs['filter'] = filter

        if sort is not None:
            kwargs['sort'] = sort
        
        if projection is not None:
            kwargs['projection'] = projection

        if skip != 0:
            kwargs['skip'] = skip

        if limit != 0:
            kwargs['limit'] = limit

        if batch_size != 0:
            kwargs['batch_size'] = batch_size

        cur = self._collection.find(**kwargs)
        return PolyDBCursor(cur)
    
    def ids(self, \
            filter : list|None = None, \
            sort : list|None = None, \
            skip : int = 0, \
            limit : int = 0, \
            batch_size : int = 0, \
            **kwargs) -> list:
        """
        Return an array of all ids of all elements matching the given conditions


        :param filter: a filter document for the query
        :param sort: fix a specific sort order
        :param projection: a projection document for the query
        :param skip: specifies how many documents should be skipped at the beggining of the result set
        :param limit: limits the number of documents returned by the query
        :param batch_size: specifies how many documents should be obtained in each call to the database
        :return: a list of all ids whose documents satisfy the query
        """

        if not kwargs:
            kwargs = dict()

        if filter is not None:
            kwargs['filter'] = filter

        if sort is not None:
            kwargs['sort'] = sort

        if skip != 0:
            kwargs['skip'] = skip

        if limit != 0:
            kwargs['limit'] = limit

        if batch_size != 0:
            kwargs['batch_size'] = batch_size

        kwargs['projection'] = { '_id': 1 }

        cur = self._collection.find(**kwargs)

        ids = list()
        for i in cur:
            ids.append(i['_id'])

        return ids

    def distinct(self, property : str = None, filter : dict|None = None) -> dict:
        """
        Returns a list of distinct values for the property among all documents satisfying the filter

        :param property: the property for which the distinct values should be returned
        :param filter: a dictionary that specifies the documents that should be considered
        :return: a list of distinct values for the property among all documents satisfying the filter
        """
        if property is None:
            return dict()
        
        return self._collection.distinct(property, filter=filter)
    
    def count(self, filter : str|None = None) -> int:
        """
        Returns the number of documents in the collection satisfying the filter

        :param filter: a dictionary that specifies the documents that should be counted
        :return: the number of documents in the collection satisfying the filter
        """

        return self._collection.count_documents(filter=filter)
    
    def id(self, id : str|None = None) -> dict :
        """
        Return the element with the given id

        :param id: the id
        :return: the element with the given id
        """

        return _sanitize_result(self._collection.find_one(filter={'_id': id}))
