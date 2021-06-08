from task2.user import NonNegativeFilter, RegexMatchFilter, User
import pytest


def test_non_negative_filter():

    filter_obj = NonNegativeFilter()

    with pytest.raises(ValueError):
        for num in range(-1, -50, -1):
            filter_obj.filter(num)

    for num in range(0, 50):
        filter_obj.filter(num)


def test_regex_match_filter():
    # Starts with
    filter_obj = RegexMatchFilter('^dog')
    with pytest.raises(ValueError):
        filter_obj.filter('cat')
    filter_obj.filter('dog')
    filter_obj.filter('dog and cat')

    # Only numbers
    filter_obj = RegexMatchFilter('^[0-9]+$')
    with pytest.raises(ValueError):
        filter_obj.filter('ffds875')
        filter_obj.filter('')
    filter_obj.filter('54578854')


@pytest.mark.parametrize('name, level, experience', [
    ('Nagibator xada', 0, 0),  # space in name
    ('Figaro3000', -1, 0),  # negative level value
    ('Kukumber21', 20, -400)  # negative exp value
])
def test_create_user_with_invalid_arguments_raise_exc(name, level, experience):

    with pytest.raises(ValueError):
        User(name=name,
             level=level,
             experience=experience)


def test_do_action_for_paid_user():
    '''If paid user does actions, the number of actions does not decrease.'''
    paid_user = User('paid_user')
    paid_user.prolong_paid_subscription(days=1)

    # keep count of remaning actions before do action
    user_actions_remaining = paid_user._actions_remaining

    paid_user.do_action()
    assert paid_user.actions_remaining == user_actions_remaining
    assert paid_user.experience == 240


def test_do_action_for_free_user():
    '''If free user does actions, the number of actions decrements.'''
    free_user = User('free_user')

    # keep count of remaning actions before do action
    user_actions_remaining = free_user.actions_remaining

    free_user.do_action()
    assert free_user.actions_remaining == user_actions_remaining - 1
    assert free_user.experience == 240


def test_finish_user_day():
    user = User('monicalind', level=5, experience=1600)
    user.do_action()  # decrements count of remaining actions and add 240exp
    user.finish_day()

    assert user.level == 8
    assert user.experience == 340
    assert user.actions_remaining == 3
