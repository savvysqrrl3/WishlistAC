from __future__ import unicode_literals

from django.db import models
import re
import bcrypt

class UserManager(models.Manager):
	def regVal(self, postData):
		results = {'status': True, 'errors': []}
		if len(postData['name']) < 3:
			results['errors'].append("Name must be three characters or longer.")
		if len(postData['username']) < 3:
			results['errors'].append("Username must be three characters or longer.")
		if len(postData['password']) < 8:
			results['errors'].append("Password must have at least eight characters")
		if postData['password'] != postData['confirmpw']:
			results['errors'].append("Passwords do not match")
		if len(self.filter(username = postData['username'])) > 0:
			results['errors'].append("User already exists. Please log in or choose a different username.")
		if not postData['created_at']:
			results['errors'].append("Please enter today's date.")
		if len(results['errors']) > 0:
			results['status'] = False
		return results
		
	def createUser(self, postData):
		hashedpw = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
		user = User.objects.create(name = postData['name'], username = postData['username'], password = hashedpw, created_at = postData['created_at'])
		return user

	def loginVal(self, postData):
		results = {'status': True, 'errors': [], 'user': None} 
		users = self.filter(username = postData['username'])
		if len(users) < 1:
				results['errors'].append("No matching user found.")
				results['status'] = False
		else:
			if len(postData['username']) < 3:
				results['status'] = False
				results['errors'].append("Something went wrong! Please try again.")
			
			if bcrypt.checkpw(postData['password'].encode(), users[0].password.encode()) == False:
				results['errors'].append("Password does not match.")
			if len(results['errors']) > 0:
				results['status'] = False
			else:
				results['user'] = users[0]
		return results

class User(models.Model):
	name = models.CharField(max_length = 30)
	username = models.CharField(max_length = 25)
	created_at = models.DateTimeField(auto_now_add=True)
	password = models.CharField(max_length = 100)
	objects = UserManager()


