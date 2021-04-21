from dataclasses import dataclass
import logging as logging 
import time as time

logging.basicConfig(level=logging.INFO, format='%(message)s')

def is_positive(value) :
        if value>=0 :
            return 1
        else  :
            raise ValueError("Amount need to be a positive value")

class Bank :
    def __init__(self, name, bic, country_code, credit_interest) :
        self.name=name
        self.bic=bic
        self.country_code=country_code
        self.customers=[]
        self.account_created=0
        self.credit_interest=credit_interest
        
    def __str__(self):
        return "\n{}\n | BIC : {}\n | Country code : {}\n | Credit interest : {}%".format(self.name, self.bic, self.country_code, self.credit_interest)
     
    def account_number_generator(self) :
        account_number="{}{}{}".format(self.country_code, self.bic, self.account_created)
        self.account_created=self.account_created+1
        return account_number
        
    def add_customer(self, name) :
        account_number=self.account_number_generator()
        new_customer=Customer(name, account_number)
        self.customers.append(new_customer)
        return new_customer
        
    def search_customer(self, account_number) :
        for customer in self.customers:
            if customer.account_number == account_number:
                return customer
        raise ValueError("Customer doesn't exist in this bank.")
              
    def delete_account(self, account_number):
        customer=self.search_customer(account_number)
        if customer.amount==0 :
            self.customers.remove(customer)
        elif customer.amount>0 :
                raise ValueError("There is still money in your account.") 
        else :
            raise ValueError("You can't delete an account that has a credit.")
    
    def deposit(self, account_number, deposit_amount) :
        if is_positive(deposit_amount):
            customer=self.search_customer(account_number)
            customer.amount_update('+', deposit_amount)
        
    def withdrawal(self, account_number, amount):
        if is_positive(amount) :
            customer=self.search_customer(account_number)
            customer.amount_update('-', amount)
            self.overdraft_check(account_number)
            
    def remove_money(self, account_number, amount):
        if is_positive(amount) :
            customer=self.search_customer(account_number)
            customer.amount_update('-', amount)  
            self.overdraft_check(account_number)
          
    def get_amount(self, account_number) :
        customer=self.search_customer(account_number)
        return customer.amount
    
    @staticmethod
    def credit_calcul(amount, lenght, interest) :
        days_in_year=365
        credit=(-amount*lenght*interest)/days_in_year
        return credit
    
    def overdraft_check(self, account_number) :
        customer=self.search_customer(account_number)
        if customer.amount<0 :
            credit=self.credit_calcul(customer.amount, customer.authorized_overdraft_lenght, self.credit_interest)
            customer.amount_update('-', credit)
    
class Customer :
    def __init__(self, name, account_number) :
        self.name=name
        self.account_number=account_number
        self.__amount=0
        self.withdrawal_limit=600
        self.withdrawal_limit_status=0
        self.authorized_overdraft=True
        self.authorized_overdraft_lenght=10
       
    def __str__(self):
        return "\n{}\n | Account number : {}\n | Amount : {}\n".format(self.name, self.account_number, self.amount)
    
    def __repr__(self):
        return self.__str__()

    @property
    def amount(self) :
        return self.__amount
    
    @amount.setter
    def amount(self, new_value) :
        if new_value>=0 or (new_value<0 and self.authorized_overdraft) :
            self.__amount=new_value
        else :
            raise ValueError("Not enough money")
        
    def withdrawal_authorized(self, amount) :
        if self.withdrawal_limit>=self.withdrawal_limit_status+amount :
            return 1
        else :
            raise ValueError("The amount is too high for your withdrawal limit")
            
    def amount_update(self, transaction, value) :
        if transaction=='-' :
            new_amount=self.amount-value
            self.amount=new_amount
        elif transaction=='+' :
            new_amount=self.amount+value
            self.amount=new_amount
    
transfer_history=[]

@dataclass(frozen=True, eq=False)
class Transfer:
    title: str
    source: str
    destination: str
    amount: int
    
    def __str__(self):
        return "\nTitle : {}\n | Source : {}\n | Destination : {}\n | Amount : {}".format(self.title, self.source, self.destination, self.amount)
        
    def __repr__(self) :
        return self.__str__()
    
    @classmethod
    def add_to_history(Transfer, name, source, destination, amount) :
        transfer_history.append(Transfer(name, source, destination, amount))
    
def transfer(title, source_bank, source_account, destination_bank, destination_account, amount):
    source_bank.remove_money(source_account, amount)
    destination_bank.deposit(destination_account, amount)
    Transfer.add_to_history(title, source_account, destination_account, amount)
    
def account_transfer(old_bank, account_number, new_bank) :
    old_account=old_bank.search_customer(account_number)
    new_account=new_bank.add_customer(old_account.name)
    return new_account  
    
def change_bank(old_bank, old_account_number, new_bank):
    if old_bank.get_amount(old_account_number)>=0 :
        new_account=account_transfer(old_bank, old_account_number, new_bank)
        title="Bank change of {}".format(new_account.name)
        amount=old_bank.get_amount(old_account_number)
        transfer(title, old_bank, old_account_number, new_bank, new_account.account_number, amount)
        old_bank.delete_account(old_account_number)   
    else :
        raise ValueError("You can't leave your bank without paying your credit.")

if __name__ == "__main__" :
    
    logging.info("\n--------Creating banks--------")
    
    time.sleep(1)
    
    boursorama=Bank("Boursorama", 1, "FR", 15)
    revolut=Bank("Revolut", 2, "GB", 8)
    citibank=Bank("Citibank", 3, "US", 25)
    
    logging.info(boursorama)
    logging.info(revolut) 
    logging.info(citibank) 
    
    time.sleep(4)
    
    logging.info("\n--------Adding customers--------")
    
    time.sleep(1)
    
    boursorama.add_customer("Jean Renault")
    boursorama.add_customer("Marie Delacourt")
    boursorama.add_customer("Camille Leoret")
    revolut.add_customer("William Parker")
    revolut.add_customer("Tony Stark")
    revolut.add_customer("Harry Potter")
    citibank.add_customer("Will Smith")
    citibank.add_customer("Angelina Jolie")
    citibank.add_customer("John Shawn")
    
    logging.info("\n--------Banks customers lists--------")
    
    logging.info("Boursorama :\n{}".format(boursorama.customers))
    logging.info("Revolut :\n{}".format(revolut.customers))
    logging.info("Citibank :\n{}".format(citibank.customers))
    
    time.sleep(4)
        
    logging.info("\n--------Deposits--------")
    
    time.sleep(1)
    
    boursorama.deposit("FR10", 1000)
    boursorama.deposit("FR12", 500)
    revolut.deposit("GB22", 2000)
    citibank.deposit("US30", 2000)
    citibank.deposit("US31", 5000)
    citibank.deposit("US32", 600)
    
    logging.info("\n--------Accounts new status--------")
    
    logging.info("Boursorama :\n{}".format(boursorama.customers))
    logging.info("Revolut :\n{}".format(revolut.customers))
    logging.info("Citibank :\n{}".format(citibank.customers))
    
    time.sleep(4)
    
    logging.info("\n--------Withdrawals--------")
    
    time.sleep(1)
    
    boursorama.withdrawal("FR11", 10)
    boursorama.withdrawal("FR10", 10)
    revolut.withdrawal("GB20", 20)
    citibank.withdrawal("US30", 20)
    citibank.withdrawal("US32", 60)
    
    logging.info("\n--------Accounts new status--------")
    
    logging.info("Boursorama :\n{}".format(boursorama.customers))
    logging.info("Revolut :\n{}".format(revolut.customers))
    logging.info("Citibank :\n{}".format(citibank.customers))
    
    time.sleep(4)
    
    logging.info("\n--------Transfers--------")
    
    time.sleep(1)
    
    transfer("Rent", boursorama, "FR11", boursorama, "FR10", 200)
    transfer("Holidays", boursorama, "FR12", revolut, "GB20", 100)
    transfer("New car", revolut, "GB22", revolut, "GB21", 600)
    transfer("Doctor", citibank, "US31", citibank, "US30", 50)
    transfer("Refund", citibank, "US30", citibank, "US30", 20)
    
    logging.info("\n--------Transfer history--------")
    
    logging.info(transfer_history)
    
    time.sleep(2)
    
    logging.info("\n--------Accounts new status--------")
    
    logging.info("Boursorama :\n{}".format(boursorama.customers))
    logging.info("Revolut :\n{}".format(revolut.customers))
    logging.info("Citibank :\n{}".format(citibank.customers))
    
    time.sleep(4)
    
    logging.info("\n--------Bank change--------")
    
    time.sleep(1)
    
    change_bank(boursorama, "FR12", revolut)
    
    logging.info("\n--------Updated banks customers lists--------")
    
    logging.info("Boursorama :\n{}".format(boursorama.customers))
    logging.info("Revolut :\n{}".format(revolut.customers))
    logging.info("Citibank :\n{}".format(citibank.customers))
    
    
    
    
    
    
    
