from abc import ABCMeta, abstractmethod


class BaseOutput(metaclass=ABCMeta):
    """
    A class to hold tidy data representations of a data source.
    """

    @abstractmethod
    def __str__(self):
        """
        What happens when someone prints this object.
        """

    @abstractmethod
    def __repr__(self):
        """
        What happens when someone wants to view a representation
        of this object.
        """

    @abstractmethod
    def _transform(self):
        """
        The logic for resolving the relationships.
        """
