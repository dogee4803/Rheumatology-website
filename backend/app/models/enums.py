import enum

class UserRole(str, enum.Enum):
    patient = "patient"
    admin = "admin"
    medical_reviewer = "medical_reviewer"

class Sex(str, enum.Enum):
    male = "male"
    female = "female"
    undisclosed = "undisclosed"

class SessionStatus(str, enum.Enum):
    in_progress = "in_progress"
    completed = "completed"
    abandoned = "abandoned"

class ScreeningLevel(str, enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"
    red_flag = "red_flag"

class IntakeStatus(str, enum.Enum):
    taken = "taken"
    skipped = "skipped"
    delayed = "delayed"

class DataSource(str, enum.Enum):
    patient = "patient"
    doctor = "doctor"

class ReviewStatus(str, enum.Enum):
    draft = "draft"
    under_review = "under_review"
    approved = "approved"
    published = "published"

class ReminderType(str, enum.Enum):
    medication = "medication"
    visit = "visit"
    lab = "lab"

class AuditAction(str, enum.Enum):
    read = "read"
    create = "create"
    update = "update"
    delete = "delete"
    export = "export"