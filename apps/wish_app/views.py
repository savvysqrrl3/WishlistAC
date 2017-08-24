from django.shortcuts import render, redirect, HttpResponse
from models import Item
from ..login_app.models import User
from django.contrib import messages

def dashboard(request):
	if not request.session['userid']:
		return redirect('/')
	thisUser = User.objects.get(id = request.session['userid'])
	context = {
	"my_items": Item.objects.filter(created_by = thisUser),
	"all_others": Item.objects.exclude(added_by = thisUser).exclude(created_by = thisUser),
	"added_items": Item.objects.filter(added_by = thisUser),
	}
	return render(request, "wish_app/index.html", context)

def wish_items(request):
	if not request.session['userid']:
		return redirect('/main')
	return render(request, "wish_app/create.html")

def createItem(request):
	results = Item.objects.itemVal(request.POST)
	if results ['status'] == False:
		for error in results['errors']:
			messages.error(request, error)
			return redirect('/wish_items')
	else:
		newItem = Item.objects.makeItem(request.POST)

	return redirect('/dashboard')

def deleteItem(request, id):
	Item.objects.get(id = id).delete()
	return redirect('/dashboard')

def show(request, id):
	if not request.session['userid']:
		return redirect('/main')
	context = {
	"thisItem": Item.objects.get(id=id),
	}
	return render(request, "wish_app/show.html", context)

def addItem(request, id):
	thisItem = Item.objects.get(id = id)
	thisUser = User.objects.get(id = request.session['userid'])
	thisItem.added_by.add(thisUser)
	thisItem.save()
	print thisItem.added_by.all()	
	return redirect('/dashboard')

def removeItem(request, id):
	thisItem = Item.objects.get(id = id)
	thisUser = User.objects.get(id = request.session['userid'])
	added_item = thisUser.our_items.filter(id = thisItem.id)
	if added_item[0]:
		print "Item found"
		thisUser.our_items.remove(thisItem)
	else:
		print "Item not found"
	return redirect('/dashboard')

