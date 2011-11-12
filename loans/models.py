from django.db import models

# Create your models here.

class Customers(models.Model):
  accountNumber = models.IntegerField()
  name = models.CharField(max_length=50)
  customerType = models.CharField(max_length=20)
  creditRating = models.IntegerField()

class Loans(models.Model):
  interestCategory = models.CharField(max_length=10)
  principal = models.DecimalField(max_digits=15, decimal_places=2)
  originalMonths = models.IntegerField()
  elapsedMonths = models.IntegerField()
  monthlyInstalment = models.DecimalField(max_digits=15, decimal_places=2)
  interestRate = models.DecimalField(max_digits=6, decimal_places=2) # This is annual interest rate in percentage.
  prepaymentPenaltyRate = models.DecimalField(max_digits=6, decimal_places=2)
  outstandingLoanBalance = models.DecimalField(max_digits=15, decimal_places=2)
  dateTaken = models.DateTimeField(auto_now_add=True)
  isSecured = models.BooleanField()
  security = models.CharField(max_length=100)
  customer = models.ForeignKey(Customers)
  
  def computeMonthlyInstalment(self):
    monthlyInterestRate = self.interestRate/(100*12)
    return (self.principal * monthlyInterestRate * (1 + monthlyInterestRate)**(self.originalMonths))/((1 + monthlyInterestRate)**(self.originalMonths) - 1)

  def computeOutstandingLoanBalance(self):
    monthlyInterestRate = self.interestRate/(100*12)
    return self.principal * ((1+monthlyInterestRate)**(self.originalMonths) - (1 + monthlyInterestRate)**(self.elapsedMonths))/((1 + monthlyInterestRate)**(self.originalMonths) - 1)

  def save(self, *args, **kwargs):
    self.monthlyInstalment = self.computeMonthlyInstalment()
    self.outstandingLoanBalance = self.computeOutstandingLoanBalance()
    super(Loans, self).save(*args, **kwargs)


class PaidInstallments(models.Model):
  amount = models.DecimalField(max_digits=15, decimal_places=2)
  loan = models.ForeignKey(Loans)
  datePaid = models.DateTimeField()
  merchantUsed = models.CharField(max_length=20)

class Applications(models.Model):
  customer = models.ForeignKey(Customers)
  loan = models.ForeignKey(Loans)
  dateApplied = models.DateTimeField(auto_now_add=True)
  details = models.TextField()
  status = models.CharField(max_length=20)
  remark = models.TextField()

class SupportTickets(models.Model):
  loan = models.ForeignKey(Loans)
  complaintType = models.CharField(max_length=20)
  complaintMessage = models.TextField()

#class Merchants(models.Model):


#class IdentityModule(models.Model):


#class AccountsModule(models.Model):


#class TransactionsModule(models.Model):

