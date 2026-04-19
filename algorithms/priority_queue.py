# priority queue (heap) based scheduling
# inserts all subjects into a max-priority heap and always extracts
# the highest-priority subject next. this ensures the most urgent
# tasks get scheduled into the earliest available slots.
#
# time complexity:  o(n log n) — heap push and pop operations
# space complexity: o(n)

import heapq
from utils.config import DAYS, TIME_SLOTS


def priority_queue_schedule(subjects):
    # build a max-heap using python's heapq (which is a min-heap)
    # we negate the priority so the highest priority comes out first
    # heap entries: (-priority, -time_required, index, subject_dict)
    heap = []
    for i, subj in enumerate(subjects):
        priority = subj.get("priority", 1)
        time_req = subj.get("time", 1)
        heapq.heappush(heap, (-priority, -time_req, i, subj))

    # create all available time slots for the week
    all_slots = [(day, time) for day in DAYS for time in TIME_SLOTS]
    slot_index = 0
    timetable = []

    # keep extracting the highest-priority subject and assigning slots
    while heap and slot_index < len(all_slots):
        # pop the subject with the highest priority from the heap
        neg_priority, neg_time, _, subject = heapq.heappop(heap)
        hours_needed = subject.get("time", 1)

        # assign consecutive slots for each hour this subject needs
        for _ in range(hours_needed):
            if slot_index >= len(all_slots):
                break
            day, time_slot = all_slots[slot_index]
            timetable.append({
                "subject": subject["name"],
                "day": day,
                "time": time_slot,
                "priority": subject.get("priority", 1),
                "heap_order": -neg_priority
            })
            slot_index += 1

    return timetable
