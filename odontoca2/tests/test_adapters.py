from types import SimpleNamespace

from odontoca2.adapters import UltralyticsDetectorAdapter


class Scalar:
    def __init__(self, value):
        self.value = value
    def item(self):
        return self.value


class Coords:
    def __init__(self, values):
        self.values = values
    def tolist(self):
        return self.values


class FakeModel:
    names = {0: "caries", 1: "restoration"}

    def predict(self, source, verbose=False, **kwargs):
        boxes = SimpleNamespace(
            xyxy=[Coords([10, 20, 30, 40]), Coords([50, 60, 80, 90])],
            conf=[Scalar(0.66), Scalar(0.91)],
            cls=[Scalar(0), Scalar(1)],
        )
        return [SimpleNamespace(boxes=boxes, names=self.names)]


def test_ultralytics_adapter_normalizes_boxes_without_clinical_interpretation():
    out = UltralyticsDetectorAdapter(FakeModel()).predict("image")
    assert len(out) == 2
    assert out[0].class_name == "caries"
    assert out[0].score == 0.66
    assert out[0].bbox.x1 == 10
    assert out[1].class_name == "restoration"
