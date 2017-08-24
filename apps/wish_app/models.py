from __future__ import unicode_literals

from django.db import models
from ..login_app.models import User

class ItemManager(models.Manager):
	def itemVal(self, postData):
		results = {'status': True, 'errors': []}
		if not postData ['item_name'] or len(postData ['item_name']) < 3:
			results['status'] = False
			results['errors'].append("Please re-enter item name. Item's name must be 3 or more characters long.")
		return results
			
	def makeItem(self, postData):
		thisUser = User.objects.get(id = postData['user_id'])
		thisItem = Item.objects.create(name = postData['item_name'], created_by = thisUser)
		print "*************", thisItem.name, "created by", thisItem.created_by.name, "************"
		return thisItem


class Item(models.Model):
	name = models.CharField(max_length = 55)
	created_at = models.DateTimeField(auto_now_add=True)
	created_by = models.ForeignKey(User, related_name = "my_items")
	added_by = models.ManyToManyField(User, related_name = "our_items")
	objects = ItemManager()

