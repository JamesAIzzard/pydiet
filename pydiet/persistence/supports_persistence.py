import abc
import copy
from typing import TypedDict, Union, Dict, Optional, Any

from pydiet import persistence


class PersistenceInfo(TypedDict):
    data: Dict[str, Any]
    datafile_name: Optional[str]


class DBInfo(TypedDict):
    unique_field_name: str
    path_into_db: str


class SupportsPersistence(abc.ABC):

    @property
    def has_unsaved_changes(self) -> bool:
        if not self.datafile_exists:
            return True
        saved_data = persistence.persistence_service.read_datafile(self.datafile_path, Dict)
        if self._persistence_info['data'] == saved_data:
            return False
        else:
            return True

    @staticmethod
    @abc.abstractmethod
    def get_db_info() -> 'DBInfo':
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def _persistence_info(self) -> PersistenceInfo:
        raise NotImplementedError

    @abc.abstractmethod
    def set_datafile_name(self, datafile_name: str) -> None:
        raise NotImplementedError

    @property
    def datafile_exists(self) -> bool:
        if self._persistence_info['datafile_name'] is None:
            return False
        else:
            return True

    @property
    def unique_field_defined(self) -> bool:
        if self.unique_field_value is None:
            return False
        else:
            return True

    @classmethod
    def get_unique_field_name(cls) -> str:
        return cls.get_db_info()['unique_field_name']

    @property
    def unique_field_value(self) -> Optional[str]:
        return self._persistence_info['data'][self.get_unique_field_name()]

    @classmethod
    def get_path_into_db(cls) -> str:
        return cls.get_db_info()['path_into_db']

    @classmethod
    def get_index_filepath(cls) -> str:
        return '{}{}.json'.format(cls.get_path_into_db(), persistence.configs.indexes_filename)

    @property
    def datafile_name(self) -> Optional[str]:
        return self._persistence_info['datafile_name']

    @property
    def datafile_path(self) -> str:
        if not self.datafile_exists:
            raise persistence.exceptions.NoDatafileError
        else:
            return '{path_to_db_dir}{datafile_name}.json'.format(
                path_to_db_dir=self.get_path_into_db(),
                datafile_name=self.datafile_name)

    @property
    def data_copy(self) -> Union[Dict, TypedDict]:
        return copy.deepcopy(self._persistence_info['data'])

    def set_unique_field(self, value: str) -> None:
        if persistence.persistence_service.check_unique_val_avail(self.__class__, self.datafile_name, value):
            self._persistence_info['data'][self.get_unique_field_name()] = value
