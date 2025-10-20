from app.models import Course

class ScheduleGrid:
    def __init__(self, jours, heures):
        self.jours = jours
        self.heures = heures
        self.grid = {jour: {heure: "" for heure in heures} for jour in jours}

    def add_course(self, course: Course):
        from datetime import datetime, timedelta

        fmt = "%H:%M"
        start = datetime.strptime(course.start_time, fmt)
        end = datetime.strptime(course.end_time, fmt)
        current = start

        while current < end:
            heure_str = current.strftime(fmt)
            if course.day in self.grid and heure_str in self.grid[course.day]:
                self.grid[course.day][heure_str] = f"{course.subject}\n{course.teacher}\n{course.room}\n{course.classe}"
            current += timedelta(hours=1)
