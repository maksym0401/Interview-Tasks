import re
from typing import Any, List, Union


class BaseFilter:
    '''Base filter class for using in descriptors'''

    def __call__(self, value: Any):
        self.filter(value)

    def filter(self, value: Any):
        '''Need to be implemented in sub classes.
        Raise ValueError if filter is not passed.'''
        raise NotImplementedError


class NonNegativeFilter(BaseFilter):

    def filter(self, value: int):
        if value < 0:
            raise ValueError('Cannot be negative.')


class RegexMatchFilter(BaseFilter):

    def __init__(self, pattern: str) -> None:
        self.pattern = re.compile(pattern)

    def filter(self, value: str):
        if not self.pattern.match(value):
            raise ValueError(f"String '{value}' doesn't match pattern.")


class Attribute:
    '''Attribute descriptor'''

    def __init__(
            self,
            set_filters: Union[BaseFilter, List[BaseFilter], None] = None):

        if isinstance(set_filters, list):
            self.set_filters = set_filters
        else:
            self.set_filters = [set_filters]

    def __set_name__(self, owner, name: str):
        self.public = name
        self.private = f'_{name}'

    def __get__(self, instance, owner=None) -> Any:
        return getattr(instance, self.private)

    def __set__(self, instance, value: Any):
        for filter in self.set_filters:
            filter(value)

        setattr(instance, self.private, value)


class User:

    name = Attribute(set_filters=RegexMatchFilter('^[a-zA-Z0-9-._]+$'))
    experience = Attribute(set_filters=NonNegativeFilter())
    level = Attribute(set_filters=[NonNegativeFilter()])

    paid_days_remaining = Attribute(set_filters=NonNegativeFilter())
    actions_remaining = Attribute(set_filters=NonNegativeFilter())

    free_users_action_limit = 3  # actions limit for free user

    def __init__(self, name: str, level: int = 0, experience: int = 0):

        self.name = name
        self.level = level
        self.experience = experience

        self.actions_remaining = 3
        self.paid_days_remaining = 0

    def do_action(self):
        '''Do action, get experience'''
        if self.is_free_user():
            if self.is_actions_remaining():
                self.actions_remaining -= 1
            else:
                return
        self.experience += 240  # give to user some expexperience

    def prolong_paid_subscription(self, days: int):
        self.paid_days_remaining += days

    def is_actions_remaining(self) -> bool:
        return self.actions_remaining != 0

    def is_free_user(self) -> bool:
        return self.paid_days_remaining == 0

    def is_paid_user(self) -> bool:
        return not self.is_free_user()

    def finish_day(self):
        '''Level up by every 500xp. Renew actions remaining.'''
        while self.experience >= 500:
            self.experience -= 500
            self.level += 1

        self.actions_remaining = User.free_users_action_limit
        if self.is_paid_user():
            self._paid_days_remaining -= 1
