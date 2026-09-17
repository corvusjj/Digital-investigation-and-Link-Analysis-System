from entities.base.entity import Entity

class BankAccount(Entity):
    def __init__(
            self,
            label,
            account_number,
            account_type,
            bank,
            account_holder,
            currency,
    ):
        super().__init__("BANK ACCOUNT", label)
        
        self.properties = {
            "account_number": account_number,
            "account_type": account_type,
            "bank": bank,
            "account_holder": account_holder,
            "currency": currency 
        }

class Transaction(Entity):
    def __init__(
            self,
            label,
            amount,
            currency,
            timestamp,
            transaction_type,
            sender_account,
            recipient_account,
            reference_number
    ):
        super().__init__("TRANSACTION", label)
        
        self.properties = {
            "amount": amount,
            "currency": currency,
            "timestamp": timestamp,
            "transaction_type": transaction_type,
            "sender_account": sender_account,
            "recipient_account": recipient_account,
            "reference_number": reference_number
        }

class Bank(Entity):
    def __init__(
            self,
            label,
            name,
            branch,
            address,
            swift_code,
            contact_number
    ):
        super().__init__("BANK", label)
        
        self.properties = {
            "name": name,
            "branch": branch,
            "address": address,
            "swift_code": swift_code,
            "contact_number": contact_number
        }
