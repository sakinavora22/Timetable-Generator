# backtracking algorithm for timetable scheduling
# tries every possible slot assignment for each subject.
# if a placement leads to a dead end, it undoes the choice and tries
# the next option. this guarantees finding a valid schedule if one exists.
#
# time complexity:  o(s^n) — s = number of slots, n = subjects
# space complexity: o(n)   — recursion depth

from config import DAYS, TIME_SLOTS


def generate_backtracking(subjects):
    # build a flat list of all (day, time) slot pairs for the week
    all_slots = [
        (day, time) for day in DAYS for time in TIME_SLOTS
    ]

    result = []         # stores the final timetable entries
    used_slots = set()  # keeps track of which slots are already taken

    def backtrack(index):
        # base case: all subjects have been placed successfully
        if index == len(subjects):
            return True

        subject = subjects[index]
        hours_needed = subject.get("time", 1)

        # try each possible starting position for this subject's block of slots
        for start in range(len(all_slots) - hours_needed + 1):
            # check if we can fit hours_needed consecutive free slots starting here
            candidate = []
            for offset in range(hours_needed):
                slot = all_slots[start + offset]
                # if this slot is already used, this starting position won't work
                if slot in used_slots:
                    break
                candidate.append(slot)

            # skip if we couldn't find enough consecutive free slots
            if len(candidate) != hours_needed:
                continue

            # mark all candidate slots as used
            for slot in candidate:
                used_slots.add(slot)

            # add timetable entries for this subject
            for day, time in candidate:
                result.append({
                    "subject": subject["name"],
                    "day": day,
                    "time": time,
                    "priority": subject.get("priority", 1)
                })

            # try to place the next subject
            if backtrack(index + 1):
                return True

            # placing the next subject failed, so undo this assignment
            # and try a different starting position
            for _ in range(hours_needed):
                result.pop()
            for slot in candidate:
                used_slots.discard(slot)

        # no valid placement found for this subject at any position
        return False

    # start the backtracking from the first subject
    backtrack(0)
    return result
