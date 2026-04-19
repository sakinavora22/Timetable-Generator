# shortest job first (sjf) scheduling algorithm
# ignores priority and sorts subjects entirely by the time (hours) they require.
# subjects that take the least amount of time are scheduled first.
#
# time complexity:  o(n log n) — due to sorting
# space complexity: o(n)

from config import DAYS, TIME_SLOTS


def generate_sjf(subjects):
    # sort subjects primarily by time required (ascending)
    # tie-breaker: priority (descending) just in case times are equal
    sorted_subjects = sorted(
        subjects,
        key=lambda x: (x.get("time", 1), -x.get("priority", 1))
    )

    timetable = []
    slot_index = 0
    total_slots = len(DAYS) * len(TIME_SLOTS)

    for subject in sorted_subjects:
        hours_needed = subject.get("time", 1)

        for _ in range(hours_needed):
            if slot_index >= total_slots:
                break

            day = DAYS[slot_index // len(TIME_SLOTS)]
            time_slot = TIME_SLOTS[slot_index % len(TIME_SLOTS)]

            timetable.append({
                "subject": subject["name"],
                "day": day,
                "time": time_slot,
                "priority": subject.get("priority", 1),
                "time_required": hours_needed
            })

            slot_index += 1

    return timetable
