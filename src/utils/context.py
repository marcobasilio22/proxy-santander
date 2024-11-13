class Context:
    def __init__(self, global_trace_id) -> None:
        self.global_trace_id = global_trace_id
        self.operations = []
        self.db_session = None
        self.timing = None

        self.media = None
        self.binary_body = None

    def add_session(self, db_session):
        self.db_session = db_session

    def add_operation(self, operation_id):
        self.operations.append({"id": operation_id})

    def remove_operation(self, operation_id):
        remaining_operations = []
        for operation in self.operations:
            if operation_id == operation["id"]:
                break
            self.add_operation(operation["id"])

        self.operations = remaining_operations

    def clear_operations(self):
        self.operations = []
