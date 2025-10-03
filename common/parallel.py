from tqdm.auto import tqdm
from concurrent.futures import ThreadPoolExecutor, Future
from typing import Callable, Iterable, List, Optional, TypeVar

T = TypeVar('T')
R = TypeVar('R')

class TqdmParallelProgress:
    """
    A helper class for parallel execution with progress tracking using tqdm.
    """

    def __init__(self, pool: Optional[ThreadPoolExecutor] = None, max_workers: int = 6) -> None:
        """
        Initialize the TqdmParallelProgress instance.

        Args:
            pool (Optional[ThreadPoolExecutor]): An optional ThreadPoolExecutor instance.
            max_workers (int): Maximum number of worker threads if pool is not provided.
        """
        if pool is None:
            self.pool = ThreadPoolExecutor(max_workers=max_workers)
        else:
            self.pool = pool

    def map_progress(self, sequence: Iterable[T], function: Callable[[T], R]) -> List[R]:
        """
        Apply a function to each item in the sequence in parallel, showing a tqdm progress bar.

        Args:
            sequence (Iterable[T]): The sequence of items to process.
            function (Callable[[T], R]): The function to apply to each item.

        Returns:
            List[R]: The list of results from applying the function.
        """
        results: List[R] = []

        with tqdm(total=len(sequence)) as progress:
            futures: List[Future] = []

            for el in sequence:
                future = self.pool.submit(function, el)
                future.add_done_callback(lambda p: progress.update())
                futures.append(future)

            for future in futures:
                result = future.result()
                results.append(result)

        return results

    def shutdown(self) -> None:
        """
        Shutdown the underlying ThreadPoolExecutor.
        """
        self.pool.shutdown()