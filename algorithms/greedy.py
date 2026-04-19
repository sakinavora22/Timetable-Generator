# greedy algorithm for timetable scheduling
# sorts subjects by priority (highest first) and assigns them to the
# earliest available time slots. this is a fast approach that makes
# the best local choice at each step.
#
# time complexity:  o(n log n) — dominated by sorting
# space complexity: o(n)

from utils.config import DAYS, TIME_SLOTS


def generate_greedy(subjects):
    # sort subjects by priority descending, with hours needed as a tiebreaker
    # this ensures the most important subjects get scheduled first
    sorted_subjects = sorted(
        subjects,
        key=lambda x: (x.get("priority", 1), x.get("time", 1)),
        reverse=True
    )

    timetable = []
    slot_index = 0  # tracks which slot we're filling next across the whole week

    # calculate total number of available slots in the week
    total_slots = len(DAYS) * len(TIME_SLOTS)

    # go through each subject and assign it to consecutive slots
    for subject in sorted_subjects:
        hours_needed = subject.get("time", 1)

        # assign one slot per hour the subject needs
        for _ in range(hours_needed):
            # stop if we've run out of slots
            if slot_index >= total_slots:
                break

            # figure out which day and time this slot falls on
            day = DAYS[slot_index // len(TIME_SLOTS)]
            time_slot = TIME_SLOTS[slot_index % len(TIME_SLOTS)]

            # add this slot assignment to the timetable
            timetable.append({
                "subject": subject["name"],
                "day": day,
                "time": time_slot,
                "priority": subject.get("priority", 1),
                "slot_index": slot_index
            })

            slot_index += 1

    return timetable
