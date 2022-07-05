from codecs import StreamWriter
from django.db import models,transaction
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
class customerGroup(models.Model):
    customerGroupId = models.AutoField(primary_key=True)
    customerGroupName = models.CharField(('name'),max_length=200)
    isDefault = models.BooleanField(("Is Default"),default=False)
    createdAt = models.DateTimeField(("Created At"),auto_now_add=True)
    updatedAt = models.DateTimeField(("Updated At"),auto_now=True)

    def save(self, *args, **kwargs):
        if not self.isDefault:
            return super(customerGroup, self).save(*args, **kwargs)
        with transaction.atomic():
            customerGroup.objects.filter(
                isDefault=True).update(isDefault=False)
            return super(customerGroup, self).save(*args, **kwargs)

    def __str__(self):
        return self.customerGroupName

def default_customerGroup():
    return customerGroup.objects.get(isDefault=True)

class customer(models.Model):
    customerId = models.AutoField(primary_key=True)
    firstName = models.CharField(('First Name'), max_length=100)
    lastName = models.CharField(('Last Name'), max_length=100)
    mobileNumber = PhoneNumberField(('Mobile Number'), null=False, blank=False, unique=True)
    email = models.EmailField(('email Id'),null=False, blank=False, unique=True)
    profileImage = models.ImageField(('Profile Image'),upload_to='images/')
    password = models.CharField(("Password"),max_length=50)
    customerGroup = models.ForeignKey(customerGroup,on_delete=models.CASCADE,null=False,default=default_customerGroup)
    emailVarificationDate = models.DateTimeField(default=None,null=True,blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    code = models.CharField(max_length=8,default="00000000")
    emailSentOn = models.DateTimeField(null=True,blank=True,default=None)

    def __str__(self):
        return self.firstName

class state(models.Model):
    stateId = models.AutoField(primary_key=True)
    stateName = models.CharField(("State Name"),max_length=24,unique=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.stateName

class city(models.Model):
    cityId = models.AutoField(primary_key=True)
    stateName = models.ForeignKey('State',on_delete=models.CASCADE,null=True)
    cityName = models.CharField(("City Name"),max_length=24,unique=True)
    
    def __str__(self):
        return self.cityName

class customerAddress(models.Model):
    customerAddressId = models.AutoField(primary_key=True)
    addressName = models.CharField(('Name'),max_length=100)
    building = models.CharField(('Building / House No.'),max_length=200)
    street = models.CharField(('Street'),max_length=200)
    postalCode = models.IntegerField(('Postal Code'))
    landMark = models.CharField(('Landmark'),max_length=200)
    isDefault = models.BooleanField(("Is Default"),default=False)
    city = models.ForeignKey(city,on_delete=models.CASCADE,null=False)
    state = models.ForeignKey(state,on_delete=models.CASCADE,null=False)
    customer = models.ForeignKey(customer,on_delete=models.CASCADE,null=False)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.isDefault:
            return super(customerAddress, self).save(*args, **kwargs)
        with transaction.atomic():
            customerAddress.objects.filter(
                isDefault=True).filter(customer=self.customer).update(isDefault=False)
            return super(customerAddress, self).save(*args, **kwargs)

    def __str__(self):
        return self.addressName +str(self.customer)