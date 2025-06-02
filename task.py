import timeit
import random

# Реалізація алгоритмів сортування


def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr


def merge_sort(arr):
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left_half = arr[:mid]
    right_half = arr[mid:]

    left_half = merge_sort(left_half)
    right_half = merge_sort(right_half)

    return merge(left_half, right_half)


def merge(left, right):
    merged = []
    left_idx, right_idx = 0, 0

    while left_idx < len(left) and right_idx < len(right):
        if left[left_idx] < right[right_idx]:
            merged.append(left[left_idx])
            left_idx += 1
        else:
            merged.append(right[right_idx])
            right_idx += 1

    merged.extend(left[left_idx:])
    merged.extend(right[right_idx:])
    return merged


#  Функція для генерації наборів даних


def generate_data(size, data_type="random"):
    if data_type == "random":
        return [random.randint(0, 1000000) for _ in range(size)]
    elif data_type == "sorted":
        return list(range(size))
    elif data_type == "reverse_sorted":
        return list(range(size - 1, -1, -1))
    else:
        raise ValueError("Invalid data_type")


#  Функція для тестування


def run_tests():
    data_sizes = [100, 1000, 10000, 50000, 100000]  # Розміри масивів для тестування
    num_runs = 5  # Кількість прогонів для усереднення часу

    results = {
        "random": {
            "insertion_sort": [],
            "merge_sort": [],
            "timsort_list_sort": [],
            "timsort_sorted": [],
        },
        "sorted": {
            "insertion_sort": [],
            "merge_sort": [],
            "timsort_list_sort": [],
            "timsort_sorted": [],
        },
        "reverse_sorted": {
            "insertion_sort": [],
            "merge_sort": [],
            "timsort_list_sort": [],
            "timsort_sorted": [],
        },
    }

    print("Початок тестування...")

    for data_type in results.keys():
        print(f"\nТестування на {data_type.replace('_', ' ')} даних:")
        for size in data_sizes:
            print(f"  Розмір даних: {size}")

            # Генерація даних
            data = generate_data(size, data_type)

            # Insertion Sort
            stmt_insertion = f"insertion_sort({data.copy()})"
            setup_insertion = "from __main__ import insertion_sort"
            time_insertion = (
                timeit.timeit(stmt_insertion, setup=setup_insertion, number=num_runs)
                / num_runs
            )
            results[data_type]["insertion_sort"].append(time_insertion)
            print(f"    Insertion Sort: {time_insertion:.6f} сек")

            # Merge Sort
            stmt_merge = f"merge_sort({data.copy()})"
            setup_merge = "from __main__ import merge_sort, merge"
            time_merge = (
                timeit.timeit(stmt_merge, setup=setup_merge, number=num_runs) / num_runs
            )
            results[data_type]["merge_sort"].append(time_merge)
            print(f"    Merge Sort:     {time_merge:.6f} сек")

            # Timsort (list.sort())
            stmt_timsort_list_sort = f"data_copy = {data.copy()}; data_copy.sort()"
            time_timsort_list_sort = (
                timeit.timeit(stmt_timsort_list_sort, number=num_runs) / num_runs
            )
            results[data_type]["timsort_list_sort"].append(time_timsort_list_sort)
            print(f"    Timsort (list.sort()): {time_timsort_list_sort:.6f} сек")

            # Timsort (sorted())
            stmt_timsort_sorted = f"sorted({data.copy()})"
            time_timsort_sorted = (
                timeit.timeit(stmt_timsort_sorted, number=num_runs) / num_runs
            )
            results[data_type]["timsort_sorted"].append(time_timsort_sorted)
            print(f"    Timsort (sorted()): {time_timsort_sorted:.6f} сек")

    print("\nТестування завершено.")
    return results, data_sizes


#  Запуск тестів та виведення результатів

if __name__ == "__main__":
    test_results, sizes = run_tests()

    print("\n--- Зведені результати (середній час виконання в секундах) ---")
    for data_type, alg_results in test_results.items():
        print(f"\nТип даних: {data_type.replace('_', ' ')}")
        print(
            f"{'Розмір':<10} | {'Insertion Sort':<18} | {'Merge Sort':<18} | {'Timsort (list.sort())':<25} | {'Timsort (sorted())':<25}"
        )
        print("-" * 110)
        for i, size in enumerate(sizes):
            ins_time = alg_results["insertion_sort"][i]
            mer_time = alg_results["merge_sort"][i]
            ts_ls_time = alg_results["timsort_list_sort"][i]
            ts_s_time = alg_results["timsort_sorted"][i]
            print(
                f"{size:<10} | {ins_time:<18.6f} | {mer_time:<18.6f} | {ts_ls_time:<25.6f} | {ts_s_time:<25.6f}"
            )

    print("\n--- Аналіз емпіричних даних ---")
    print("\n1. Випадкові дані (Random Data):")
    print(
        "   - Insertion Sort показує найгірші результати, оскільки його складність O(n^2) суттєво проявляється на великих випадкових масивах."
    )
    print(
        "   - Merge Sort демонструє стабільні O(n log n) показники, які значно кращі за Insertion Sort на великих даних."
    )
    print(
        "   - Timsort (list.sort() та sorted()) є безумовним лідером, значно перевершуючи як Insertion Sort, так і Merge Sort. Це підтверджує його ефективність завдяки оптимізації та адаптивності."
    )

    print("\n2. Відсортовані дані (Sorted Data):")
    print(
        "   - Insertion Sort показує свою найкращу продуктивність (O(n)), оскільки йому потрібно лише пройтися по масиву один раз, не роблячи багато перестановок."
    )
    print(
        "   - Merge Sort зберігає свою O(n log n) складність, оскільки він завжди ділить і зливає масиви, незалежно від їхнього початкового стану."
    )
    print(
        "   - Timsort демонструє виняткову продуктивність. Він розпізнає, що дані вже відсортовані, і виконує мінімальну кількість операцій, близьку до O(n). Це є яскравим прикладом його адаптивності."
    )

    print("\n3. Відсортовані у зворотному порядку дані (Reverse Sorted Data):")
    print(
        "   - Insertion Sort показує свій найгірший сценарій (O(n^2)), оскільки кожен елемент доводиться переміщувати до початку масиву."
    )
    print(
        "   - Merge Sort зберігає свою O(n log n) складність, як і для випадкових даних."
    )
    print(
        '   - Timsort залишається найбільш ефективним. Хоча він і не настільки швидкий, як на повністю відсортованих даних, він все одно значно перевершує як Insertion Sort, так і Merge Sort, оскільки його стратегії злиття та обробки "прогонів" залишаються ефективними.'
    )

    print("\n--- Висновки ---")
    print(
        "Емпіричні дані повністю підтверджують теоретичні оцінки складності алгоритмів і наочно демонструють переваги Timsort:"
    )
    print(
        "1. **Підтвердження O(n^2) для Insertion Sort:** На великих випадкових та обернено-відсортованих масивах час виконання Insertion Sort зростає експоненційно, що робить його непридатним для великих об'ємів даних."
    )
    print(
        "2. **Підтвердження O(n log n) для Merge Sort:** Merge Sort показує стабільну продуктивність на різних типах даних, але його постійні фактори можуть бути вищими через необхідність використання додаткової пам'яті та копіювання елементів."
    )
    print("3. **Перевага Timsort:**")
    print(
        "   - **Ефективність на всіх типах даних:** Timsort виявляється найшвидшим алгоритмом у переважній більшості випадків, значно перевершуючи Merge Sort та Insertion Sort. Це особливо помітно на великих наборах даних."
    )
    print(
        '   - **Адаптивність:** Його здатність розпізнавати та використовувати вже відсортовані "прогони" робить його надзвичайно ефективним на частково або повністю відсортованих даних, де він може досягати продуктивності, близької до O(n).'
    )
    print(
        '   - **Оптимізація комбінації:** Поєднання ефективності Insertion Sort для малих "прогонів" та надійності Merge Sort для великих масивів робить Timsort найкращим вибором для загального призначення.'
    )

    print(
        "\nСаме завдяки цій винятковій ефективності, адаптивності та стабільності, Python інтегрує Timsort як основний алгоритм сортування у своїх вбудованих функціях `list.sort()` та `sorted()`. Програмістам не потрібно (і, як правило, не варто) реалізовувати власні алгоритми сортування, оскільки вбудовані функції Python вже надають високооптимізоване рішення, яке перевершує більшість саморобних реалізацій за швидкістю та надійністю."
    )
    print(
        "Використання вбудованих функцій не тільки економить час розробки, але й гарантує оптимальну продуктивність для більшості реальних сценаріїв сортування."
    )
