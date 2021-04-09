class bank :
  def __init__(self,name,bic,location,clients) :
    self.name=name
    self.bic=bic
    self.location=location
    self.clients=clients

class client :
  def __init__(self,first_name,last_name,date_of_birth,bank_account,password) :
    self.first_name=first_name
    self.last_name=last_name
    self.date_of_birth=date_of_birth
    self.bank_account=bank_account
    self.password=password

class bank_account :
  def __init__(self,account_number,amount,withdrawal_limit,withdrawal_limit_status) :
    self.account_number=account_number
    self.amount=amount
    self.withdrawal_limit=withdrawal_limit
    self.withdrawal_limit_status=withdrawal_limit_status

def transfer(account_number_giving,account_number_receiving,transfer_amount): 
  bank_account_giving= #Bank account with account_number_giving
  bank_account_receiving=#Bank account with account_number_receiving
  bank_account_giving.amount=bank_account_giving.amount-transfer_amount
  bank_account_receiving.amount=bank_account_giving.amount-transfer_amount

def withdrawal(account_number,withdrawal_amount):
  bank_account= #Bank account with this account_number
  if (bank_account.withdrawal_limit>bank_account.withdrawal_limit_status+withdrawal_amount) :
    bank_account.amount=bank_account.amount-withdrawal_amount


if __name__ = "__main__" :
  bank_account_1=bank_account(21,3000,400,20)
  bank_account_2=bank_account(26,100,30,0)
  transfer(21,26,500)
  withdrawal(21,100)





