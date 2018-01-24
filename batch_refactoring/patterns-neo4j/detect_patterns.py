import json
from collections import Counter
from json import JSONEncoder


class MyEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


class Refactoring:
    def __init__(self):
        self.type = None
        self.smells_before = None
        self.smells_after = None

    def __repr__(self):
        return "Refactoring(%s, %s, %s)" % (self.type, self.smells_before, self.smells_after)


class Interference:
    def __init__(self):
        self.introduced = 0
        self.removed = 0


class BatchSlice:
    def __init__(self, sequence):
        self.sequence = sequence  # tuple of ordered refactoring types
        self.occurrences = 0
        self.interferences = {}

    def introduction(self, smell):
        interference = self.interferences.get(smell, Interference())
        interference.introduced += 1
        self.interferences[smell] = interference

    def removal(self, smell):
        interference = self.interferences.get(smell, Interference())
        interference.removed += 1
        self.interferences[smell] = interference


def load_batches(filename):
    batches = {}
    with open(filename) as f:
        data = json.loads(f.read())
        for row in data:
            refactorings = batches.get(row["batch"]["hash_id"], [])
            ref = Refactoring()
            ref.type = row["refactoring"]["type"]
            ref.smells_before = row["smells_before"]
            ref.smells_after = row["smells_after"]
            refactorings.append(ref)
            batches[row["batch"]["hash_id"]] = refactorings
    return batches


def slices(refactorings):
    for i in range(2, len(refactorings) + 1):
        ref_slice = refactorings[:i]
        sequence = tuple(sorted([r.type for r in ref_slice]))
        yield sequence, ref_slice[0].smells_before, ref_slice[-1].smells_after


def slices_not_repeated(refactorings):
    sequence_set = set([r.type for r in refactorings])
    sequence = tuple(sorted(list(sequence_set)))
    yield sequence, refactorings[0].smells_before, refactorings[-1].smells_after


def changes(smells_before, smells_after):
    before = Counter(smells_before)
    after = Counter(smells_after)
    introductions = set()
    removals = set()

    for smell, count in before.iteritems():
        if after[smell] > count:
            introductions.add(smell)
        if after[smell] < count:
            removals.add(smell)

    for smell, count in after.iteritems():
        if before[smell] > count:
            removals.add(smell)
        if before[smell] < count:
            introductions.add(smell)

    return list(introductions), list(removals)


def print_impact(impact):
    for i in impact:
        print i
        print json.dumps(impact[i], indent=4, cls=MyEncoder, sort_keys=True)
        print ""


def interferences(batches):
    # key => tuple of ordered refactoring types
    # value => {occurrences: X,
    impact = {}
    total = len(batches)
    current = 0
    for hash_id, refactorings in batches.iteritems():
        current += 1
        print "Processing %s/%s" % (current, total)
        # if hash_id != 20143:
        #     continue
        for sequence, before, after in slices_not_repeated(refactorings):
            # computes the smell introductions and removals of the slice
            introductions, removals = changes(before, after)

            # print "Sequence:", sequence
            # print "Before:", before
            # print "After:", after
            # print "Introduces:", introductions
            # print "Removes:", removals
            # print ""

            batch_slice = impact.get(sequence, BatchSlice(sequence))

            batch_slice.occurrences += 1
            # register the introductions and removals
            for smell in introductions:
                batch_slice.introduction(smell)

            for smell in removals:
                batch_slice.removal(smell)

            impact[sequence] = batch_slice
        #     print "Impact State"
        #     print_impact(impact)
        # break
    cleanup(impact)
    return impact


# delete all sequences with less than 10 occurrences
def cleanup(impact):
    to_delete = []
    for k, v in impact.iteritems():
        if v.occurrences < 50:
            to_delete.append(k)
    for k in to_delete:
        del impact[k]


def detect(batches_filename, alias):
    bs = load_batches(batches_filename)
    ints = interferences(bs)
    with open("interferences/%s.json" % alias, "w") as out:
        data = json.dumps(ints.values(), indent=4, cls=MyEncoder, sort_keys=True)
        out.write(data)


detect("batches/batch_and_smells_scope_based.json", "scope_based")
detect("batches/batch_and_smells_element_based.json", "element_based")
detect("batches/batch_and_smells_version_based.json", "version_based")
