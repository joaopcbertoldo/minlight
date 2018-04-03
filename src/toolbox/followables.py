from typing import Set, Iterable
from abc import ABC, abstractmethod
from datetime import datetime
from threading import Thread


# Followable
class Followable:

    def __init__(self):
        # followers (observers)
        self._followers: Set['AbsFollower'] = set()

    # notify
    def _notify_followers(self):
        """Call notify on all the followers."""
        for f in self._followers:
            f.notify(self)

    # subscribe
    def subscribe(self, follower: 'AbsFollower'):
        """Subscribe a new follower to the MobilePoint."""
        assert isinstance(follower, AbsFollower), f'Follower must be AbsFollower.'
        # update the set
        self._followers.update([follower])

    # subscribe_many
    def subscribe_many(self, followers: Iterable['AbsFollower']):
        """Subscribe all the followers."""
        for f in followers:
            self.subscribe(f)


# AbsFollower
class AbsFollower(ABC):
    """Abstract follower --> oberver in observer pattern for a folowable object."""

    # _on_notify
    @abstractmethod
    def _on_notify(self, f):
        """Abstract method that takes an action on notification. f is a Followable. TO BE OVERWRITTEN."""
        pass

    # init
    def __init__(self):
        """Capture the datetime of creation (used to uniquely identify a follower)."""
        # assign the creation moment
        self._dt = datetime.now()

    # hash
    def __hash__(self):
        """
        Followers are uniquely identified by the hash of their creation datetime.
        This is done because the followables use sets of followers.
        """
        return hash(self._dt)

    # notify
    def notify(self, f):
        """Start a new thread to execute the follower's action. Called by the followable."""
        p = Thread(target=self._on_notify, args=(f,))  # create a thread
        p.start()  # start it
        # TODO: remove the join, create a "follower set" --> //ize the followers, but wait until all are done
        p.join()
