from pymongo import MongoClient
from pymongo import errors
import re

from .PolyDBCollection import PolyDBCollection


class polyDB:
    """
    Wrapper for polyDB

    :param username: username
    :type username: string
    :param password: password
    :param host: host
    :param port: port
    :param use_ssl: use TLS
    :return: a polyDB instance
    """

    def __init__(self, username='polymake',
                 password='database',
                 host='db.polymake.org',
                 port=27017,
                 use_ssl=True,
                 directConnection=True,
                 **kwargs):

        self._client = MongoClient('mongodb://' + username + ':' + password + '@' + host + ':' + str(port),
                                   tls=use_ssl, directConnection=directConnection,
                                   **kwargs)
        try:
            self._client.admin.command('ping')
            print("connection to polydb established")
        except errors.ConnectionFailure:
            print("polydb server not available")
        self._db = self._client.polydb

    def _db(self):
        return self._db

    def _list_collection_names(self, filter: list | None = None) -> list:
        """
        wraps the list_collections_names command from mongo db

        :param filter: filter for collection names
        :return: list of collection names
        """
        query_filter = {}
        if filter is not None:
            query_filter = {"name": {"$regex": filter}}
        return self._db.list_collection_names(filter=query_filter,
                                              authorizedCollections=True)

    def subsections(self, section: str | None = None, recursive: bool = False) -> list:
        """
        Returns a list of all subsections of a given section (root if no section given).

        :param section: The name of the section
        :param recursive: default False, if true will recursively return the names of all subsections as well

        :return: list subsections of a section
        """
        filterstring = r"^_sectionInfo\."
        if section is not None and section != "":
            filterstring += section + r"\."
        sections = self._list_collection_names(filter=filterstring)
        sections.sort()
        if not recursive:
            sections = [re.match(filterstring + r"([\w] + )" + r".*", s).group(1) for s in sections]
        else:
            sections_array = [re.match(filterstring + r"(.*)", s).group(1) for s in sections]

            sections = {}
            for a in sections_array:
                sections_temp = sections
                s = a.split(".")
                for e in s:
                    if e not in sections_temp:
                        sections_temp[e] = {}
                    sections_temp = sections_temp[e]

        return sections

    def collections_list(self, section: str | None = None) -> list:
        """
        Obtain a list of collections in a section

        :param section: the name of the section
        :return: list of collections
        """
        filterstring_base = r"^_collectionInfo"
        if section is not None and section != "":
            filterstring_base += r"\." + section
        filterstring = filterstring_base + r"\.[\w.]+$"

        collections = self._list_collection_names(filter=filterstring)
        return [re.match(filterstring_base + r"\.([\w.]+)$", c).group(1)
                for c in collections]

    def get_collection(self, collectionname: str) -> PolyDBCollection:
        """
        Obtain a handle for a collection in polyDB

        :param collectionname: the name of the collection
        :return: an instance of PolyDBCollection
        """
        return PolyDBCollection(self._db, collectionname)

    def section_info(self, section: str = None) -> list:
        """
        Returns information about a section

        :param section: the name of the section
        :return: list
        """
        if section is None or section == "":
            return {}
        section_coll = self._db['_sectionInfo.' + section]
        data = {'_id': section + '.2.1'}
        section_info = section_coll.find_one(data)
        if section_info is None:
            print("No section with this name found")
            return None
        return {
            'maintainer': section_info['maintainer'],
            'description': section_info['description'],
            'sectionDepth': section_info['sectionDepth'],
            'sections': self.subsections(section=section, recursive=False),
            'collections': self.collections_list(section=section)
        }

    def collection(self, collection: str = None) -> list:
        """
        Returns information about a collection

        :param collection: the name of the collection
        :return: list
        """
        if collection is None or collection == "":
            return None

        collection_coll = self._db['_collectionInfo.' + collection]
        data = {'_id': collection + '.2.1'}
        collection_info = collection_coll.find_one(data)

        if collection_info is None:
            print("No collection with this name found")
            return None

        return {
            'author': collection_info['author'],
            'contributor': collection_info['contributor'],
            'maintainer': collection_info['maintainer'],
            'references': collection_info['references'],
            'description': collection_info['description'],
        }
