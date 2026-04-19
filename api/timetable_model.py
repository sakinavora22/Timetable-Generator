# timetable model
# handles validation and data normalization for subject entries
# makes sure incoming data is correct before passing it to the algorithms


def validate_subjects(subjects):
    # checks that the subjects list has the right structure
    # returns a tuple: (is_valid, error_message)
    # error_message is none if everything is valid

    if not isinstance(subjects, list):
        return False, "Subjects must be a list"

    # loop through each subject and check required fields
    for i, subj in enumerate(subjects):
        # every subject must have a name
        if "name" not in subj:
            return False, f"Subject at index {i} is missing 'name'"

        # priority must be a number if provided
        if not isinstance(subj.get("priority", 1), (int, float)):
            return False, f"Subject '{subj['name']}' has invalid priority"

        # time (hours needed) must be a number if provided
        if not isinstance(subj.get("time", 1), (int, float)):
            return False, f"Subject '{subj['name']}' has invalid time"

    # all checks passed
    return True, None


def normalize_subject(subj):
    # fills in default values for any optional fields that are missing
    # this ensures every subject has a consistent structure for the algorithms
    return {
        "name": subj["name"],
        "priority": subj.get("priority", 1),       # default priority is 1 (lowest)
        "time": subj.get("time", 1),                # default is 1 hour
        "deadline": subj.get("deadline", 99),        # default deadline is far in the future
        "conflicts": subj.get("conflicts", [])       # no conflicts by default
    }


def format_timetable(raw_entries):
    # groups timetable entries by day for easier display on the frontend
    # returns a dictionary like { "monday": [entry1, entry2], "tuesday": [...] }
    result = {}
    for entry in raw_entries:
        day = entry.get("day", "Unknown")
        if day not in result:
            result[day] = []
        result[day].append(entry)
    return result
