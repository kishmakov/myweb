class NoteRecord(object):
    def __init__(self, record_id, header, tags, summary):
        self.id = record_id
        self.header = header
        self.summary = summary
        self.tags = tags
