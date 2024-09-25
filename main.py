import dataclasses
import pprint
from enum import Enum
from typing import Union

requirement_number_of_classes = {
    '23MAT221': {
        'theory': 3,
        'lab': 1
    },
    '23CSE207': {
        'theory': 1,
        'lab': 1
    },
    '23MEE207': {
        'theory': 1,
        'lab': 1
    },
    '23MEE208': {
        'theory': 2,
        'lab': 1
    },
    '23MEE209': {
        'theory': 3,
        'lab': 1
    },
    '23EEE206': {
        'theory': 3,
        'lab': 0
    },
    '23ECE207': {
        'theory': 2,
        'lab': 1
    },
    '22ADM201': {
        'theory': 1,
        'lab': 0
    },
    '23LSE201': {
        'theory': 3,
        'lab': 0
    }
}


class ClassType(Enum):
    THEORY = 1
    LAB = 2


@dataclasses.dataclass
class Subject:
    code: str
    professor_code: str


@dataclasses.dataclass
class Slot:
    day: int
    slot: int
    class_type: ClassType

    def __init__(self, class_type, day, slot):
        self.class_type = class_type
        self.day = day
        self.slot = slot

        if self.class_type == ClassType.LAB and self.slot not in [0, 3, 5]:
            raise ValueError('Invalid slot for lab')

    def __repr__(self):
        return f'Day={self.day} Slot={self.slot}'

    def __eq__(self, other):
        return self.day == other.day and self.slot == other.slot


class TimeTable:

    def __init__(self):
        self.schedule: list[list[Union[Subject, None]]] = [[None for _ in range(7)] for _ in range(5)]

    def add_class(self, subject: Subject, slot: Slot):
        if self.schedule[slot.day][slot.slot] is not None:
            raise ValueError('Slot already occupied')

        self.schedule[slot.day][slot.slot] = subject

        if slot.class_type == ClassType.LAB:
            if slot.slot == 0:
                self.schedule[slot.day][slot.slot + 1] = subject
                self.schedule[slot.day][slot.slot + 2] = subject
            elif slot.slot in [3, 5]:
                self.schedule[slot.day][slot.slot + 1] = subject


class Constraint:
    ...


class Solver:
    def __init__(self, timetable, classes):
        self.timetable = timetable
        self.classes = classes
        self.constraints = []

    def add_constraint(self, constraint: Constraint):
        self.constraints.append(constraint)

    def solve(self):
        current_day = 0
        current_slot = 0
        for subject_code, number_of_classes in self.classes.items():
            theory = number_of_classes['theory']

            for _ in range(theory):
                s = Slot(ClassType.THEORY, current_day, current_slot)
                self.timetable.add_class(Subject(subject_code, 'professor_code'), s)

                current_slot += 1

                if current_slot == 7:
                    current_slot = 0
                    current_day += 1

        for subject_code, number_of_classes in self.classes.items():
            lab = number_of_classes['lab']

            for _ in range(lab):
                s = Slot(ClassType.LAB, current_day, current_slot)
                self.timetable.add_class(Subject(subject_code, 'professor_code'), s)

                if current_slot == 0:
                    current_slot = 3
                elif current_slot == 3:
                    current_slot = 5
                else:
                    current_slot = 0
                    current_day += 1


solver = Solver(TimeTable(), requirement_number_of_classes)
solver.solve()

pprint.pprint(solver.timetable.schedule)
