import os
import pickle
import os.path

class PersistentCache:
    def __init__(self, cache_dir):
        self.cache_dir = cache_dir

    def get(self, key):
        self.__check_folder()
        path = self._get_cache_path(key)
        if os.path.exists(path):
            with open(path, 'rb') as f:
                return pickle.load(f)

    def set(self, key, value):
        self.__check_folder()
        path = self._get_cache_path(key)
        with open(path, 'wb') as f:
            pickle.dump(value, f)

    def delete(self, key):
        self.__check_folder()
        path = self._get_cache_path(key)
        if os.path.exists(path):
            os.remove(path)

    def _get_cache_path(self, key):
        filename = f'{key}.pkl'
        return os.path.join(self.cache_dir, filename)

    def __check_folder(self):
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)

