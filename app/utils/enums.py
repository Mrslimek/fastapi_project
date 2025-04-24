from enum import Enum


class CompletionStatus(Enum):
    COMPLETED = "Completed"
    NOT_COMPLETED = "Not completed"
    ABANDONED = "Abandoned"