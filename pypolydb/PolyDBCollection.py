from .utilities import _sanitize_result
from .PolyDBCursor import PolyDBCursor
import json


class PolyDBCollection:
    """
    A wrapper for a collection in PolyDB

    :param collectioname: name of the collection
    :result: an instance of PolyDBCollection
    """

    def __init__(self, db, collectionname=None):
        if collectionname:
            info_collectionname = "_collectionInfo." + collectionname

            self._collection = db[collectionname]
            self._infoCollection = db[info_collectionname]
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

        collection_coll = self._db['_collectionInfo.' + self._name]
        data = {'_id': self._name + '.2.1'}
        collection_info = collection_coll.find_one(data)

        if collection_info is None:
            print("No collection with this name found")
            return None

        info = {
            'author': collection_info['author'],
            'contributor': collection_info['contributor'],
            'maintainer': collection_info['maintainer'],
            'references': collection_info['references'],
            'description': collection_info['description'],
        }
        return info

    def find_one(self,
                 filter: list | None = None,
                 sort: list | None = None,
                 projection: list | None = None,
                 skip: int = 0,
                 **kwargs) -> list | None:
        """
        Find one element in the collection

        :param filter: a filter document for the query
        :param sort: fix a specific sort order
        :param projection: a projection document for the query
        :param skip: specifies how many documents should be skipped at the beginning of the result set
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
            kwargs['skip'] = int(skip)

        return _sanitize_result(self._collection.find_one(**kwargs))

    def name(self) -> str:
        return self._collection.name

    def find(self,
             filter: list | None = None,
             sort: list | None = None,
             projection: list | None = None,
             skip=0,
             limit: int = 0,
             batch_size: int = 0,
             **kwargs) -> PolyDBCursor | None:
        """
        Return a curser over all elements in the collection matching the given conditions

        :param filter: a filter document for the query
        :param sort: fix a specific sort order
        :param projection: a projection document for the query
        :param skip: specifies how many documents should be skipped at the beginning of the result set
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

    def aggregate(self,
                  pipeline: list | None = None,
                  batch_size: int = 0,
                  **kwargs) -> PolyDBCursor | None:
        """
        Return a cursor over all elements in the collection matching the given conditions

        :param pipeline: an aggregation pipeline
        :param batch_size: specifies how many documents should be obtained in each call to the database
        :return: a PolyDBCursor, or None if no document is found
        """

        if not kwargs:
            kwargs = dict()

        if pipeline is not None:
            kwargs['pipeline'] = pipeline

        if batch_size != 0:
            kwargs['batch_size'] = batch_size

        cur = self._collection.aggregate(**kwargs)
        return PolyDBCursor(cur)

    def ids(self,
            filter: list | None = None,
            sort: list | None = None,
            skip: int = 0,
            limit: int = 0,
            batch_size: int = 0,
            **kwargs) -> list:
        """
        Return an array of all ids of all elements matching the given conditions


        :param filter: a filter document for the query
        :param sort: fix a specific sort order
        :param projection: a projection document for the query
        :param skip: specifies how many documents should be skipped at the beginning of the result set
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

        kwargs['projection'] = {'_id': 1}

        return [i['_id'] for i in self._collection.find(**kwargs)]

    def distinct(self, property: str = None, filter: dict | None = None) -> dict:
        """
        Returns a list of distinct values for the property among all documents satisfying the filter

        :param property: the property for which the distinct values should be returned
        :param filter: a dictionary that specifies the documents that should be considered
        :return: a list of distinct values for the property among all documents satisfying the filter
        """
        if property is None:
            return dict()

        return self._collection.distinct(property, filter=filter)

    def count(self, filter: str | None = None) -> int:
        """
        Returns the number of documents in the collection satisfying the filter

        :param filter: a dictionary that specifies the documents that should be counted
        :return: the number of documents in the collection satisfying the filter
        """

        return self._collection.count_documents(filter=filter)

    def id(self, id: str | None = None) -> dict:
        """
        Return the element with the given id

        :param id: the id
        :return: the element with the given id
        """

        return _sanitize_result(self._collection.find_one(filter={'_id': id}))

    def schema(self) -> dict:
        """
        Return the schema describing an object in the collection
        """

        id = "schema.2.1"
        filter = {"_id": id}
        schema_doc = self._infoCollection.find_one(filter=filter)

        schema_string = json.dumps(schema_doc["schema"]).replace("__", "$")
        return json.loads(schema_string)

    polymake_templated_types_one_argument = ["Array", "Vector",
                                             "Serialized",
                                             "IncidenceMatrix",
                                             "Set", "Graph",
                                             "SparseVector"]

    polymake_templated_types_two_arguments = ["Matrix", "Pair",
                                              "UniPolynomial",
                                              "HashMap", "Map",
                                              "Polynomial",
                                              "SparseMatrix"]

    def build_polymake_type(self, type: dict = None) -> str:
        item = type.pop(0)
        typedef = item
        if item in self.polymake_templated_types_one_argument:
            typedef += "<"
            typedef += self.build_polymake_type(type)
            typedef += ">"
        elif item in self.polymake_templated_types_two_arguments:
            typedef += "<"
            typedef += self.build_polymake_type(type)
            typedef += ","
            typedef += self.build_polymake_type(type)
            typedef += ">"

        return typedef

    def type_of(self, property: str = None) -> str:
        coll_schema = self.schema()
        ref = None
        if "allOf" in coll_schema:
            ref = coll_schema["allOf"][0]["properties"][property]["$ref"]
        else:
            ref = coll_schema["properties"][property]["$ref"]
        path = ref.split("/", 3)
        typedef = ""
        if "description" in coll_schema["definitions"][path[2]]:
            typedef = coll_schema["definitions"][path[2]]["description"]
        else:
            typedef = "polymake::"
            type = path[2].split("-")
            typedef += type.pop(0) + "::"
            typedef += self.build_polymake_type(type)
        return typedef
