import multiprocessing

from services.api.service import run_api_service
from services.filter.service import filter_service
from services.publish.service import publish_service
from services.screaming.service import scream_service


queue1 = multiprocessing.Queue()
queue2 = multiprocessing.Queue()
queue3 = multiprocessing.Queue()


def main():
    process1 = multiprocessing.Process(target=run_api_service, args=[queue1])
    process2 = multiprocessing.Process(target=filter_service, args=[queue1, queue2])
    process3 = multiprocessing.Process(target=scream_service, args=[queue2, queue3])
    process4 = multiprocessing.Process(target=publish_service, args=[queue3])

    process1.start()
    process2.start()
    process3.start()
    process4.start()

    process1.join()
    process2.join()
    process3.join()
    process4.join()

if __name__ == "__main__":
    main()
