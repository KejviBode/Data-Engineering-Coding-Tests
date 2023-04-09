# The below function doesn't work correctly. It should sum all the numbers at the
# current time. For example, 01:02:03 should return 6. Improve and fix the function,
# and write unit test(s) for it. Use any testing framework you're familiar with.


# [TODO]: fix the function
def sum_current_time(time_str: str) -> int:
    """Expects data in the format HH:MM:SS"""
    list_of_nums = time_str.split(":")
    if len(list_of_nums) != 3:
        raise ValueError("Date needs to be in format HH:MM:SS")
    for i in list_of_nums:
        if not i.isdigit():
            raise TypeError(
                "Input is not of type int and needs to be in format HH:MM:SS")
    list_of_ints = [int(time) for time in list_of_nums]
    if not 0 <= list_of_ints[0] < 24:
        raise ValueError("Hour must be between 00-23")
    if not 0 <= list_of_ints[1] < 59:
        raise ValueError("Minute must be between 00-59")
    if not 0 <= list_of_ints[2] < 59:
        raise ValueError("Second must be between 00-59")
    return sum(list_of_ints)
