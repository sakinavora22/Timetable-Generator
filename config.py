# configuration settings for the timetable scheduler
# defines the days of the week, available time slots, and server settings

# toggle debug mode for development
DEBUG = True

# port the flask server runs on
PORT = 5000

# maximum number of time slots available per day
MAX_SLOTS_PER_DAY = 8

# days of the week used in the timetable
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

# available time slots for scheduling, from morning to evening
TIME_SLOTS = [
    "8:00 AM", "9:00 AM", "10:00 AM", "11:00 AM",
    "12:00 PM", "1:00 PM", "2:00 PM", "3:00 PM",
    "4:00 PM", "5:00 PM"
]
