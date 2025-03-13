import json
import time

from datasketch import HyperLogLog

def load_data(log_file_path: str):
    hll = HyperLogLog(p=14)
    log_remote_addrs = []
    with open(log_file_path, "r", encoding="utf-8") as file:
        for line in file:
            entry = json.loads(line.strip())
            if "remote_addr" in entry:
                log_remote_addrs.append(entry["remote_addr"])
                hll.update(entry["remote_addr"].encode("utf-8"))
            else:
                print("There is no valid remote_addr in entry:", entry)
    return hll, log_remote_addrs

def exact_count(log_remote_addrs: list[str]) -> int:
    return len(set(log_remote_addrs))

def hyperloglog_count(hll: HyperLogLog) -> float:
    return hll.count()

def display_comparison(exact_count, hyperloglog_count, exact_time, hll_time):
    print("Результати порівняння:")
    print(f"{"":<25}{"Точний підрахунок":>20}{"HyperLogLog":>15}")
    print(f"{"Унікальні елементи":<25}{exact_count:>20,.5f}{hyperloglog_count:>15,.5f}")
    print(f"{"Час виконання (сек.)":<25}{exact_time:>20.10f}{hll_time:>15.10f}")

if __name__ == "__main__":
    log_file_path = "lms-stage-access.log"

    hll, log_remote_addrs = load_data(log_file_path)

    start_time = time.perf_counter()
    exact = exact_count(log_remote_addrs)
    exact_count_time = time.perf_counter() - start_time

    start_time = time.perf_counter()
    hyperloglog = hyperloglog_count(hll)
    hyperloglog_count_time = time.perf_counter() - start_time

    display_comparison(exact, hyperloglog, exact_count_time, hyperloglog_count_time)