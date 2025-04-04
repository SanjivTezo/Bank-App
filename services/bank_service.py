class BankService:
    def __init__(self, bank):
        self.bank = bank

    def add_currency(self, currency, exchange_rate):
        self.bank._accepted_currencies[currency] = exchange_rate
        self.bank.save_to_json()
        return f"{currency} added with exchange rate {exchange_rate}"

    def set_charges(self, rtgs_charge, imps_charge, same_bank=True):
        if same_bank:
            self.bank._same_bank_charges = {"RTGS": rtgs_charge, "IMPS": imps_charge}
            self.bank.save_to_json()
            return f"Same Bank Charges set to RTGS: {rtgs_charge}%, IMPS: {imps_charge}%"
        else:
            self.bank._other_bank_charges = {"RTGS": rtgs_charge, "IMPS": imps_charge}
            self.bank.save_to_json()
            return f"Other Bank Charges set to RTGS: {rtgs_charge}%, IMPS: {imps_charge}%"

    def see_service_charges(self):
        return {
            "same_bank": self.bank._same_bank_charges,
            "other_bank": self.bank._other_bank_charges
        }

    def display_currency_details(self):
        return self.bank._accepted_currencies