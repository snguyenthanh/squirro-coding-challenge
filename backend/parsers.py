from collections import deque


ARRAY_TYPES = (list, set, tuple)


def flatten_dict(data: dict, separator=".") -> dict:
    """
    Iterate through the dict and push nested ones into a stack.
    From the stack, we append the key-value pairs to a flattened dict.

    Example:
        data: dict = {
            'a': '123',
            'b': {
                'c': {
                    'd': 1,
                },
            },
            'e': [
                {
                    'f': 2,
                    'g': 3,
                },
                {
                    'h': 4,
                    'i': 5,
                },
            ],
        }

        flatten_dict(data) == {
            'a': '123',
            'b.c.d': 1,
            'e.0.f': 2,
            'e.0.g': 3,
            'e.1.h': 4,
            'e.1.i': 5,
        }
    """

    stack = deque()
    stack.append((data, ""))
    flattened_dict = {}

    def _iterate_and_flatten_dict(cur_dict: dict, cur_prefix: str = "") -> None:
        """
        Update the `flattened_dict` argument based on the keys and values found, on iteration.
        """
        for key, val in cur_dict.items():
            new_key = f"{cur_prefix}{separator}{key}" if cur_prefix else key
            if isinstance(val, dict):
                stack.append((val, new_key))
            elif isinstance(val, ARRAY_TYPES):
                stack.append(
                    [
                        (
                            item,
                            f"{cur_prefix}{separator}{key}{separator}{dict_index}"
                            if cur_prefix
                            else f"{key}{separator}{dict_index}",
                        )
                        for dict_index, item in enumerate(val)
                    ]
                )
            else:
                flattened_dict[new_key] = val

    while stack:
        stack_item = stack.pop()
        if isinstance(stack_item, tuple):
            cur_dict, cur_prefix = stack_item
            _iterate_and_flatten_dict(cur_dict=cur_dict, cur_prefix=cur_prefix)
        else:
            for dict_prefix in stack_item:
                cur_dict, cur_prefix = dict_prefix
                _iterate_and_flatten_dict(cur_dict=cur_dict, cur_prefix=cur_prefix)

    return flattened_dict