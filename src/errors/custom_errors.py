from errors import QIException

class NotFoundAccount(QIException):
    code = "SP000001"

    def __init__(self, account_key) -> None:
        title = "Account not Found"
        http_status = 404
        description = f"Account with key {account_key} was not found."
        translation = f"A conta com chave {account_key} não foi encontrada."
        super().__init__(title, self.code, http_status, description, translation)

class AlreadyExistsAccountWithThisNumberDigitBranch(QIException):
    code = "SP000002"

    def __init__(
        self,
        account_number: str,
        account_digit: str,
        account_branch: str,
    ) -> None:
        title = "Existing account number, digit and branch"
        http_status = 409
        description = f"An account with the number {account_number}, digit {account_digit} and branch {account_branch} already exists"
        translation = f"Uma conta com o número {account_number}, digito {account_digit} e agência {account_branch} já existe"
        super().__init__(title, self.code, http_status, description, translation)

class AlreadyExistsAccountKey(QIException):
    code = "SP000003"

    def __init__(self, account_key: str) -> None:
        title = "Already Exists Account Key"
        http_status = 409
        description = f"The Account with key: {account_key} already exists"
        translation = f"A Conta com esse key: {account_key} ja existe"
        super().__init__(title, self.code, http_status, description, translation)

class NotFoundTransaction(QIException):
    code = "SP000004"

    def __init__(self, account_transactions_key: str) -> None:
        title = "Not Found Transaction"
        http_status = 404
        description = f"No transaction found with the key: {account_transactions_key}"
        translation = f"Não existe transação com a chave: {account_transactions_key}"
        super().__init__(title, self.code, http_status, description, translation)

class NotFoundTransactions(QIException):
    code = "SP000005"

    def __init__(self, start_date: str, end_date: str) -> None:
        title = "Not Found Transaction"
        http_status = 404
        description = f"No transaction found between these dates: {start_date} and {end_date}"
        translation = f"Não existe transação entre essas datas: {start_date} e {end_date}"
        super().__init__(title, self.code, http_status, description, translation)

class NotFoundPendingTransaction(QIException):
    code = "SP000006"

    def __init__(self) -> None:
        title = "Not Found Pending Transaction"
        http_status = 404
        description = f"Not found Pending Transaction"
        translation = f"Não há transações pendentes"
        super().__init__(title, self.code, http_status, description, translation)

class InvalidTransactionStatus(QIException):
    code = "SP000007"

    def __init__(self,status,account_transaction_key) -> None:
        title = "Invalid Transaction Status"
        http_status = 400
        description = f"The account transaction with key ({account_transaction_key}) was in the invalid status ({status}) to send"
        translation = f"A transação de chave ({account_transaction_key}) com status imvalido ({status}) para reenvio"
        super().__init__(title, self.code, http_status, description, translation)
