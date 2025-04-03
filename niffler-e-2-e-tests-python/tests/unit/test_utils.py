from hypothesis import given, strategies as st


def insertion_sort(arr):
    result = arr.copy()
    for i in range(1, len(result)):
        key = result[i]
        j = i - 1
        while j >= 0 and result[j] > key:
            result[j + 1] = result[j]
            j -= 1
        result[j + 1] = key
    return result


# @pytest.mark.parametrize(
#     "arr, expected",
#     [
#         ([4, 5], [4, 5]),
#     ],
# )
# def test_insertion_sort(arr, expected):
#     assert insertion_sort(arr) == expected


@given(st.lists(st.integers(), min_size=0, max_size=20))
def test_insertion_sort(fuzz_input):
    assert insertion_sort(fuzz_input) == sorted(fuzz_input), \
        f"Sorting failed for input: {fuzz_input}"
