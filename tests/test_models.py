from isic4kit.models import Image, Metadata, Segmentation, Study, Task
from datetime import datetime


def test_image_creation():
    image = Image(
        id="ISIC_0000123",
        name="ISIC_0000123.jpg",
        md5hash="abc123hash",
        created="2023-01-01T00:00:00",
        updated="2023-01-02T00:00:00",
    )

    assert image.id == "ISIC_0000123"
    assert image.name == "ISIC_0000123.jpg"
    assert image.md5hash == "abc123hash"
    assert isinstance(image.created, datetime)
    assert isinstance(image.updated, datetime)


def test_metadata_creation():
    metadata = Metadata(
        image_id="ISIC_0000123",
        clinical={"age": 50, "sex": "male", "diagnosis": "melanoma"},
        acquisition={"camera": "digital", "resolution": "1024x768"},
    )

    assert metadata.image_id == "ISIC_0000123"
    assert metadata.clinical["age"] == 50
    assert metadata.acquisition["camera"] == "digital"


def test_segmentation_creation():
    segmentation = Segmentation(
        id="seg_123",
        image_id="ISIC_0000123",
        created="2023-01-01T00:00:00",
        approved=True,
    )

    assert segmentation.id == "seg_123"
    assert segmentation.image_id == "ISIC_0000123"
    assert segmentation.approved is True


def test_study_creation():
    study = Study(
        id="study_123",
        name="Melanoma Study",
        description="A study about melanoma",
        created="2023-01-01T00:00:00",
        updated="2023-01-02T00:00:00",
    )

    assert study.id == "study_123"
    assert study.name == "Melanoma Study"
    assert study.description == "A study about melanoma"


def test_task_creation():
    task = Task(
        id="task_123",
        study_id="study_123",
        image_id="ISIC_0000123",
        annotation_type="diagnosis",
        created="2023-01-01T00:00:00",
        completed=False,
    )

    assert task.id == "task_123"
    assert task.study_id == "study_123"
    assert task.image_id == "ISIC_0000123"
    assert task.annotation_type == "diagnosis"
    assert task.completed is False
