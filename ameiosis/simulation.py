"""
"""
import math
from collections import defaultdict

from lanchester import LanchesterSquareAllies
from lanchester.side import Side, Battalion, AlliableMixin, RetreatingSideMixin, ReinforcableSideMixin


class Faction:
    """Members of the same faction become allies in
    """
    def __init__(self, name, *members):
        self.__name = name
        self.members = set(members) or set()
        for member in members:
            member.faction = self

    @property
    def name(self):
        return self.__name

    def __hash__(self):
        return hash(self.__name)

    def add_member(self, member):
        member.faction = self
        self.members.add(member)

    @property
    def depleted(self):
        return all([member.depleted for member in self.members])

    @property
    def not_depleted(self):
        return any([member.not_depleted for member in self.members])


# Maybe move to lanchester lib.
class EngageableMixin:
    def __init__(self, *engagements):
        self.__engagements = set(engagements)

    def _get_engagements(self):
        return self.__engagements

    def _set_engagements(self, val):
        self.__engagements.add(val)

    @property
    def engagements(self):
        return self._get_engagements()

    @engagements.setter
    def engagements(self, val):
        self._set_engagements(val)


class Blob(Side, EngageableMixin, AlliableMixin, RetreatingSideMixin,
           ReinforcableSideMixin):
    """
    """
    def __init__(self, size, strength, faction=Faction('default'),
                 engagements=()):
        Side.__init__(self, size, strength)
        AlliableMixin.__init__(self)
        EngageableMixin.__init__(self, *engagements)
        RetreatingSideMixin.__init__(self)
        ReinforcableSideMixin.__init__(self)
        faction.add_member(self)

    def _get_calc_units(self):
        return ReinforcableSideMixin._get_calc_units(self) + RetreatingSideMixin._get_calc_units(self) - Side._get_calc_units(self)

    def _get_allies(self):
        return {member for engagement in self._get_engagements()
                        for member in engagement.get_faction_members(
                                                                self.faction)}

class Engagement:
    def __init__(self, *blobs, alg=LanchesterSquareAllies()):
        self.blobs = blobs
        self.alg = alg
        self.__engaged_factions = defaultdict(list)

        for blob in self.blobs:
            blob.engagements = self
            self.__engaged_factions[blob.faction].append(blob)

    def get_faction_members(self, faction):
        return self.__engaged_factions[faction]

    def do_round(self):
        return self.alg.do_round(*self.blobs)

    @property
    def finished(self):
        def filter_factions(faction, engaged):
            if any([member.not_depleted for member in engaged]):
                return faction

        if len(list(
                filter(lambda v: v is not None, [filter_factions(faction,
                                                                    engaged)
                        for faction,engaged in self.__engaged_factions.items()])))\
                <= 1:
            return True

    def iterate_engagement(self, max):
        i = 0
        while not self.finished and i < max:
            self.do_round()
            yield [side.units for side in self.blobs]
        yield [side.units for side in self.blobs]