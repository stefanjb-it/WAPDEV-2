import traceback
import exercises as ex


def _evaluate(func, param, exp_outcome, check_exception=False):
    if check_exception:
        try:
            result = func(*param)
            return False, result
        except exp_outcome:
            return True, "Raised %s" % exp_outcome
    else:
        result = func(*param)
        return result == exp_outcome, result


def stringify_param(param):
    if len(param[0]) == 0:
        return "[]"
    return str(param).replace("[", "").replace("]", "")


def msg(is_ok, func, param, expected_outcome, real_outcome):
    if is_ok:
        status = "OK"
    else:
        status = "FAILED"
    return "%s:%s(%s) - Your result: %s / Expected result: %s" % (status,
                                                                  func.__name__,
                                                                  stringify_param(param),
                                                                  result,
                                                                  expected_outcome)


if __name__ == '__main__':
    movie_title = "Blade runner 2049"
    avg_temperatures = [
        (1, 12),
        (2, 10),
        (3, 14),
        (4, 16),
        (5, 17),
        (6, 20),
        (7, 29),
        (8, 30),
        (9, 22),
        (10, 18),
        (11, 14),
        (12, 10)
    ]
    wc_count = {'Los': 2, 'Angeles': 2, 'is': 2, 'bigger': 1, 'than': 2, 'Berlin': 2, 'but': 1, 'older': 1, '.': 1}
    most_common_words = ["Los","Angeles","is","than","Berlin"]

    score = 0
    evaluations = [
        (ex.count_characters, [movie_title], 17, False),
        (ex.first_three_letters, [movie_title], "Bla", False),
        (ex.last_three_letters, [movie_title], "049", False),
        (ex.split_words, [movie_title], ["Blade", "runner", "2049"], False),
        (ex.replace, [movie_title, "2049", "2051"], "Blade runner 2051", False),
        (ex.normalize, [movie_title, 1], "blade runner 2049", False),
        (ex.normalize, [movie_title, 2], "BLADE RUNNER 2049", False),
        (ex.normalize, [movie_title, 3], "Blade runner 2049", False),
        (ex.normalize, [movie_title, 4], ValueError, True),
        (ex.find_title, [["Blade runner", "Star trek", "staR wars"], "Star"], ["Star trek", "staR wars"], False),
        (ex.find_title, [["Blade runner", "Star trek", "staR wars"], "test"], [], False),
        (ex.calculate_mean, [[8, 4, 10, 2]], 6.0, False),
        (ex.min_mean_max, [[8, 4, 10, 2]], (2, 6.0, 10), False),
        (ex.calculate_mean, [[]], None, False),
        (ex.min_mean_max, [[]], None, False),
        (ex.mean_temperature, [avg_temperatures], 17.7, False),
        (ex.mean_temperature, [[]], None, False),
        (ex.word_count, ["Los Angeles is bigger than Berlin but Berlin is older than Los Angeles ."], wc_count, False),
        (ex.common_words, ["Los Angeles is bigger than Berlin but Berlin Berlin is older than Los Angeles ."], most_common_words, False),
    ]
    for func, param, exp_outcome, check_exception in evaluations:
        try:
            is_ok, result = _evaluate(func, param, exp_outcome, check_exception)
            if is_ok:
                score = score + 1
            print(msg(is_ok, func, param, exp_outcome, result))
        except NotImplementedError:
            print("FAILED - NOT IMPLEMENTED: %s(%s) - expected output:%s " % (func.__name__, stringify_param(param) ,
                                                                              exp_outcome))
        except Exception as details:
            print("Execution of function call %s(%s) FAILED with this error:" % (func.__name__, stringify_param(param)))
            print()
            print(traceback.format_exc())
            print()
    print("Score: %s/%s" % (score, len(evaluations)))
