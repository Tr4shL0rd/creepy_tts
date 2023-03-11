import time
import os
import os.path
import pickle
import shutil

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

    def clean_up(self):
        """Cache clean up """
        self.__check_folder()
        # check cache folder creation date
        cache_creation_date = os.path.getmtime(self.cache_dir)
        max_age = 604800 # 7 days in seconds
        if (time.time() - cache_creation_date) >= 1:#max_age:
            # delete cache
            #os.rmdir(self.cache_dir)
            shutil.rmtree(self.cache_dir)


        return cache_creation_date
    def _get_cache_path(self, key):
        filename = f'{key}.pkl'
        return os.path.join(self.cache_dir, filename)

    def __check_folder(self):
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)

