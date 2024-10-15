from hivision.creator.face_detector import detect_face_retinaface
from hivision.creator.human_matting import extract_human_rmbg


def choose_handler(creator):
    creator.matting_handler = extract_human_rmbg
    creator.detection_handler = detect_face_retinaface
