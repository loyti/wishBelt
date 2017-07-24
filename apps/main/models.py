from __future__ import unicode_literals

from django.db import models

from django.utils.timezone import utc

from datetime import datetime, timedelta

import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
noNumberPls = re.compile(r'^[a-zA-Z]+$')

class UserManager(models.Manager):
    def user_validator(self, postData):
        errors = []

        if 'email' in postData:
            if len(postData['email']) == 0:
                errors.append('Please enter your email address.')
            elif not EMAIL_REGEX.match(postData['email']):
                errors.append('Please enter a valid email address.')

        if 'user_name' in postData:
            if len(postData['user_name']) == 0:
                errors.append('Please enter your name.')
            elif len(postData['user_name']) < 3:
                errors.append('User name should be no fewer than 3 letters')
            elif not noNumberPls.match(postData['user_name']):
                errors.append('User name should have no numbers or special characters in it.')

        if 'alias' in postData:
            if len(postData['alias']) == 0:
                errors.append('Please enter your alias.')
            elif len(postData['alias']) < 3:
                errors.append('Alias should be no fewer than 3 letters')
            elif not noNumberPls.match(postData['alias']):
                errors.append('Alias should have no numbers or special characters in it.')

        if 'password' in postData:
            if len(postData['password']) == 0:
                errors.append('Please enter your password.')
            elif len(postData['password']) < 8:
                errors.append('Password should be no fewer than 8 characters')
            elif postData['password'] != postData['conf_pass']:
                errors.append('Password Confirmation do not match. Please try again.')

        if 'hireDate' in postData:
            if len(postData['hireDate']) == 0:
                errors.append('Please enter your birth date')
            else:
                hireDate = postData['hireDate']
                date_format = "%Y-%m-%d"
                hireDate = datetime.strptime(hireDate, date_format).date()
                now = datetime.now().date()

                if hireDate > now:
                    errors.append('Only hired professionals may register!')
                elif hireDate == now:
                    errors.append('Join tomorrow for today is your last day of freedom')

        return errors

class ItemManager(models.Manager):
    def item_validator(self, postData):
        errors = []

        if 'content' in postData:
            if len(postData['content']) < 5:
                errors.append('Please provide more details')

        return errors

class User(models.Model):
    user_name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    hireDate = models.DateField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Item(models.Model):
    content = models.CharField(max_length=255)
    user = models.ForeignKey(User, related_name="items")
    wishItems = models.ManyToManyField(User, related_name="user_items", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ItemManager()
