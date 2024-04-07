# pylint: disable=no-member, no-self-use
from typing import Set
import abc
from barky.domain import model
from djbarky.barkyapi import models as django_models


class AbstractRepository(abc.ABC):
    """
    Because it is based on an ABC, this abstract class repository can be used with
    any data storage strategy.
    """

    def __init__(self):
        self.bookmarks_set = set()  # type: Set[model.Bookmark]

    def add(self, bookmark: model.Bookmark):
        self.bookmarks_set.add(bookmark)

    def get(self, ref) -> model.Bookmark:
        bookmark = self._get(ref)
        if bookmark:
            self.bookmarks_set.add(bookmark)
        return bookmark

    @abc.abstractmethod
    def _get(self, reference):
        raise NotImplementedError


class DjangoRepository(AbstractRepository):
    """
    This concrete instance of the repository uses the Django ORM as the data storage strategy.
    """

    def add(self, bookmark):
        super().add(bookmark)
        self.update(bookmark)

    def update(self, batch):
        django_models.Bookmark.update_from_domain(batch)

    def _get(self, ref):
        return django_models.Bookmark.objects.filter(reference=ref).first().to_domain()

    def list(self):
        return [b.to_domain() for b in django_models.Bookmark.objects.all()]


class DjangoApiRepository(AbstractRepository):
    """
    This concrete instance of the repository uses the DRF, which abstracts its own data storage
    strategy.
    """

    def add(self, bookmark):
        # super().add(bookmark)
        # self.update(bookmark)
        pass

    def update(self, batch):
        # django_models.Bookmark.update_from_domain(batch)
        pass

    def _get(self, ref):
        # return (
        #     django_models.Bookmark.objects.filter(reference=ref)
        #     .first()
        #     .to_domain()
        # )
        pass

    def list(self):
        # return [b.to_domain() for b in django_models.Bookmark.objects.all()]
        pass
