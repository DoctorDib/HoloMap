# from multiprocessing import shared_memory
# import numpy as np

# import config 

# class SharedDataSingleton:
#     _instance = None
#     _shm = None
#     _array = None

#     def __new__(cls, size, dtype=np.float64):
#         if cls._instance is None:
#             cls._instance = super(SharedDataSingleton, cls).__new__(cls)
#             cls._dtype = dtype
#             cls._size = size
#             cls._shm = shared_memory.SharedMemory(create=True, size=size * np.dtype(dtype).itemsize)
#             cls._array = np.ndarray((size,), dtype=dtype, buffer=cls._shm.buf)
#         return cls._instance

#     def write_data(self, data):
#         if len(data) > self._size:
#             raise ValueError("Data size exceeds the allocated shared memory size.")
#         np.copyto(self._array, data)

#     def read_data(self):
#         return self._array[:]

#     def close(self):
#         self._shm.close()
#         self._shm.unlink()

# # # Usage
# # singleton_instance = SharedDataSingleton(10)  # Size of 10 elements
# # singleton_instance.write_data(np.arange(10))  # Writing data to the shared array
# # print(singleton_instance.read_data())  # Reading data from the shared array

# # # Properly closing the shared memory
# # singleton_instance.close()


