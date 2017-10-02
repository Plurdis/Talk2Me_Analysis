# Format
#   CSV, Json으로 반환


class BaseCollector:
    def __init__(self):
        pass

    def get_csv(self):
        raise NotImplementedError

    def get_json(self):
        raise NotImplementedError