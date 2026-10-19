from django.shortcuts import render,get_object_or_404,redirect
from .models import Event,TicketTypes,Cartitems,OrderItem,Orders
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db import transaction
from decimal import Decimal

def events(request):
    try:
     events=Event.objects.all()
    

     return render(
        request,
        "dashboard.html",
        {"events":events}
     )
    except Exception as e:
       messages.error(request,e)

def eventdetails(request, event_id):
   
      event=get_object_or_404(Event,id=event_id)
      
      return render(
         request,
         "eventdetails.html",
         {"event":event}
      )
   
@login_required
@require_POST
def addtocart(request):
   try:
      tickettypeid=int(request.POST.get("tickettype"))
      quantity=int(request.POST.get("quantity",1))
   except(TypeError,ValueError):
      messages.error(request,"Enter a valid quantity and tickettype")
      return redirect("events")
   if quantity < 1 :
      messages.error(request,"Quantity should be atleast 1")
      return redirect("events")
   if not tickettypeid:
      messages.error(request,"please select one tickettype")
      return redirect("events")
      
   with transaction.atomic():
      ticketype=get_object_or_404(TicketTypes.objects.select_for_update(),id=tickettypeid)
      cartitem=Cartitems.objects.filter(user=request.user,ticketype=ticketype).first()
      already_in_cart=(cartitem.quantity if cartitem else 0)

      if already_in_cart + quantity > ticketype.quantity:
         messages.error(request,"not enough tickets")
         return redirect("event_details",event_id=ticketype.event.id)

      if cartitem:
         cartitem.quantity += quantity
         cartitem.save(update_fields=["quantity"])
      else:
         Cartitems.objects.create(
            user=request.user,
            ticketype=ticketype,
            quantity=quantity
         )
   messages.success(request,"Tickets added to your cart")
   return redirect("cart")

@login_required
def Cart(request):
   cart_items=Cartitems.objects.filter(
      user=request.user ).select_related("ticketype")
   total=sum(item.totalprice() for item in cart_items)
   context={"cartitems":cart_items,"total":total,}

   return render(request,"cart.html",context)

@login_required
def Checkout(request):
  
 try:
   buyer=request.user
   with transaction.atomic():
      cart_items=Cartitems.objects.filter(user=buyer)
      if not cart_items:
         raise ValueError("Your cart is empty")
         
      total=sum(item.totalprice() for item in cart_items)
      order=Orders.objects.create(
       buyer=buyer,
       amount=total,
       status="pending" )

      for item in cart_items:
         if item.ticketype.quantity < item.quantity :
            raise ValueError(f"Not enough {item.ticketype.name} tickets available")
            
         OrderItem.objects.create(
            order_id=order.id,
            ticket_type=item.ticketype,
            quantity=item.quantity,
            price=item.ticketype.price


         )
         item.ticketype.quantity -= item.quantity
         item.ticketype.save(update_fields=["quantity"])
  
 except ValueError as error:
        messages.error(request, str(error))
        return redirect("cart")     
 Cartitems.objects.filter(user=buyer).delete()
 messages.success(request,"Purchase successful")
 return redirect("dashboard")


@login_required
def Addevent(request):
   if request.method =='POST':
      name=request.POST.get("name","").strip()
      description=request.POST.get("description","").strip()
      location=request.POST.get("location","").strip()
      date=request.POST.get("date","")
      start_time=request.POST.get("time","")
      created_by=request.user

      ticket_names=request.POST.getlist("ticket_name[]")
      prices=request.POST.getlist("price[]")
      quantities=request.POST.getlist("quantity[]")

      if not all([name,description,location,date,start_time]):
         messages.error(request,"fill in all event details")
         return render(request,"addevent.html")

      if not (len(ticket_names) == len(prices) == len (quantities)):
         messages.error(request,"fill in all the ticket details")
         return render (request,"addevent.html")

      validated_tickettyes=[]
      for ticket_name,price,quantity in zip(ticket_names,prices,quantities):
         ticket_name=ticket_name.strip()
         price=Decimal(price)
         quantity=int(quantity)

         if (price < 0 or quantity <0):
           messages.error(request,"enter valid prices and quantities for the tickets")
           return render(request,"addevent.html")
         validated_tickettyes.append({"name":ticket_name,"price":price,"quantity":quantity})
      try:
          with transaction.atomic():
            event=Event.objects.create(
               name=name,
               description=description,
               location=location,
               date=date,
               start_time=start_time,
               created_by=created_by
             )
            for tickettype in validated_tickettyes:
               TicketTypes.objects.create(
                  event=event,
                  name=tickettype["name"],
                  price=tickettype["price"],
                  quantity=tickettype["quantity"]
                    )

            messages.success(request,"Event and tickettypes created successfully")
            return redirect("dashboard")
      except:
            messages.error(request,"Failed to create the event and tickets")
            return render(request,"addevent.html")

   return render(request,"addevent.html")









   


   
       


# Create your views here.
