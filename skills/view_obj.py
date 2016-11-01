

class CapabilityBreakdown(object):
    """ A view object that makes the rendering of the average skills easier """

    def __init__(self, distribution):
        assert len(distribution) == 5
        self._distribution = distribution

    @staticmethod
    def from_queryset(qs):
        pass

    @property
    def sum(self):
        return float(sum(self._distribution))

    def retrieve(self, idx):
        if self.sum:
            rel_val = int(100 * (self._distribution[idx] / self.sum))
        else:
            rel_val = 0

        return {
            'val': self._distribution[idx],
            'rel_val': rel_val
        }

    @property
    def one(self):
        return self.retrieve(0)

    @property
    def two(self):
        return self.retrieve(1)

    @property
    def three(self):
        return self.retrieve(2)

    @property
    def four(self):
        return self.retrieve(3)

    @property
    def five(self):
        return self.retrieve(4)

    @property
    def avg(self):
        if self.sum:
            weighted = sum([e[0]*e[1] for e in zip(range(1, 6), self._distribution)])
            average = weighted / self.sum

            rel_val = sum([int(100 * (e / self.sum)) for e in self._distribution]) / 5.0
        else:
            average = 0
            rel_val = 0

        return {
            'val': "{0:.2f}".format(average),
            'rel_val': rel_val
        }

