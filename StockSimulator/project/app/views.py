import numpy as np
from json import loads as load_json
import datetime

from django.contrib.auth import authenticate, login, logout, decorators
from django.db import IntegrityError
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from .models import User, Stock, StockInPortfolio, Portfolio, Event
from .forms import NewStockForm, AddStockForm, NewEventForm, AddEventForm


# Default view
def index(request):
    return render(request, "app/index.html")


# Authentication
def login_view(request):
    if request.method == "POST":

        # Signs the user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "app/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "app/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "app/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "app/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "app/register.html")


# Stocks Management
@decorators.login_required
def stocks(request):
    data =  list(map(lambda stock: {'stock': stock, 'form': NewStockForm(initial={
        'price': stock.price,
        'volatility': stock.volatility,
        'annualchange': stock.annualchange
    })}, Stock.objects.filter(user=request.user)))

    return render(request, "app/stocks.html", {'data': data})


@decorators.login_required
def new_stock(request):
    if request.method == "POST":
        name = request.POST["name"]
        price = float(request.POST["price"])
        volatility = float(request.POST["volatility"])
        annualchange = float(request.POST["annualchange"])

        if name == "" or (price <= 0) or (not 0 <= volatility<= 1) or (not 0 <= annualchange <= 100):
            return render(request, "app/new_stock.html", {'new_stock_form': NewStockForm(), 'alert_message': 'There was an error creating the stock!', 'alert_message_type': 'danger'})
        else:
            new_stock = Stock(name=name, price=price, volatility=volatility, annualchange=annualchange, user=request.user)
            new_stock.save()
            return HttpResponseRedirect(reverse("stocks"))
    else:    
        return render(request, "app/new_stock.html", {'new_stock_form': NewStockForm()})
    

@decorators.login_required
def edit_stock(request):
    if request.method == "POST":
        id = int(request.POST["stock_id"])
        price = float(request.POST["price"])
        volatility = float(request.POST["volatility"])
        annualchange = float(request.POST["annualchange"])

        stocks = Stock.objects.filter(id=id, user=request.user)

        if len(stocks) != 1 or (price <= 0) or (not 0 <= volatility<= 1) or (not 0 <= annualchange <= 100):
            return render(request, "app/stocks.html", {'new_stock_form': NewStockForm(), 'alert_message': 'There was an error editing the stock!', 'alert_message_type': 'danger'})
        else:
            stock = stocks[0]
            stock.price = price
            stock.volatility = volatility
            stock.annualchange = annualchange
            stock.save()
            return HttpResponseRedirect(reverse("stocks"))
        

@decorators.login_required
def delete_stock(request):
    if request.method == "POST":
        id = int(request.POST["id"])
        if Stock.objects.filter(id=id, user=request.user).count() == 1:
            Stock.objects.get(id=id, user=request.user).delete()

    return HttpResponseRedirect(reverse("stocks"))


# Events Management
@decorators.login_required
def events(request):
    data =  list(map(lambda event: {'event': event, 'form': NewEventForm(initial={
        'strength': event.strength,
        'decay_rate': event.decay_rate,
    })}, Event.objects.filter(user=request.user)))

    return render(request, "app/events.html", {'data': data})


@decorators.login_required
def new_event(request):
    if request.method == "POST":
        name = request.POST["name"]
        strength = float(request.POST["strength"])
        decay_rate = float(request.POST["decay_rate"])

        if name == "" or not (0 <= decay_rate <= 1) or not (-1 <= strength <= 1):
            return render(request, "app/new_event.html", {'new_event_form': NewEventForm(), 'alert_message': 'There was an error creating the event!', 'alert_message_type': 'danger'})
        else:
            new_event = Event(name=name, strength=strength, decay_rate=decay_rate, user=request.user)
            new_event.save()
            return HttpResponseRedirect(reverse("events"))
    else:    
        return render(request, "app/new_event.html", {'new_event_form': NewEventForm()})
    

@decorators.login_required
def edit_event(request):
    if request.method == "POST":
        id = int(request.POST["event_id"])
        strength = float(request.POST["strength"])
        decay_rate = float(request.POST["decay_rate"])

        events = Event.objects.filter(id=id, user=request.user)

        if len(events) != 1 or not (0 <= decay_rate <= 1) or not (-1 <= strength <= 1):
            return render(request, "app/events.html", {'new_event_form': NewEventForm(), 'alert_message': 'There was an error editing the event!', 'alert_message_type': 'danger'})
        else:
            event = events[0]
            event.strength = strength
            event.decay_rate = decay_rate
            event.save()
            return HttpResponseRedirect(reverse("events"))
        

@decorators.login_required
def delete_event(request):
    if request.method == "POST":
        id = int(request.POST["id"])
        if Event.objects.filter(id=id, user=request.user).count() == 1:
            Event.objects.get(id=id, user=request.user).delete()

    return HttpResponseRedirect(reverse("events"))


# Portfolio Management
@decorators.login_required
def portfolio(request):

    if Portfolio.objects.filter(user=request.user).count() == 1:
        portfolio = Portfolio.objects.get(user=request.user)
        stocks_in_portfolio = StockInPortfolio.objects.filter(portfolio=portfolio)
        total_value = round(sum(record.amount * record.stock.price for record in stocks_in_portfolio), 2)
        doughnut_data = [{'value': round(record.amount * record.stock.price, 2), 'name': record.stock.name} for record in stocks_in_portfolio]

    else:
        doughnut_data = []
        stocks_in_portfolio = None
        total_value = 0

    has_stock = Stock.objects.filter(user=request.user).count() > 0

    return render(request, "app/portfolio.html", {'form': AddStockForm(user=request.user), 'doughnut_data': doughnut_data, 'stocks_in_portfolio': stocks_in_portfolio, 'total_value': total_value, 'has_stock': has_stock})
        

@decorators.login_required
def add_stock(request):
    if request.method == "POST":
        if Stock.objects.filter(id=int(request.POST["stock"]), user=request.user).count() == 1:
            stock = Stock.objects.get(id=int(request.POST["stock"]), user=request.user)
            amount = float(request.POST["amount"])

            if Portfolio.objects.filter(user=request.user).count() == 1:
                portfolio = Portfolio.objects.get(user=request.user)
            else:
                portfolio = Portfolio(user=request.user)
                portfolio.save()
        

            if StockInPortfolio.objects.filter(stock=stock, portfolio=portfolio).count() == 1:
                stock_in_portfolio = StockInPortfolio.objects.get(stock=stock, portfolio=portfolio)
                stock_in_portfolio.amount = amount
                stock_in_portfolio.save()
            else:
                stock_in_portfolio = StockInPortfolio(stock=stock, amount=amount, portfolio=portfolio)
                stock_in_portfolio.save()

    return HttpResponseRedirect(reverse("portfolio"))


@decorators.login_required
def remove_stock(request):
    if request.method == "POST":
        id = int(request.POST["id"])
        if StockInPortfolio.objects.filter(id=id).count() == 1:
            object = StockInPortfolio.objects.get(id=id)
            if object.portfolio.user == request.user:
                object.delete()

    return HttpResponseRedirect(reverse("portfolio"))


# Simulator
@decorators.login_required
def simulator(request):

    if Portfolio.objects.filter(user=request.user).count() == 1:
        portfolio = Portfolio.objects.get(user=request.user)
        stocks_in_portfolio = StockInPortfolio.objects.filter(portfolio=portfolio)
        total_value = round(sum(record.amount * record.stock.price for record in stocks_in_portfolio), 2)
        doughnut_data = [{'value': round(record.amount * record.stock.price, 2), 'name': record.stock.name} for record in stocks_in_portfolio]
    else:
        doughnut_data = []
        stocks_in_portfolio = None
        total_value = 0

    return render(request, "app/simulator.html", {
        'form': AddEventForm(user=request.user), 
        'doughnut_data': doughnut_data, 
        'stocks_in_portfolio': stocks_in_portfolio, 
        'total_value': total_value,
        'has_events': Event.objects.filter(user=request.user).count() != 0
    })


@decorators.login_required
def simulation(request):
    if request.method == "POST":
        request_body = load_json(request.body)

        if Portfolio.objects.filter(user=request.user).count() == 1:
            portfolio = Portfolio.objects.get(user=request.user)
            stocks_in_portfolio = StockInPortfolio.objects.filter(portfolio=portfolio)
            starting_date = datetime.datetime.combine(datetime.date.today(), datetime.time())

            # Get all the events
            events = []
            for event_id, date in request_body['events']:
                if Event.objects.filter(id=event_id, user=request.user).count() == 1:
                    event = Event.objects.get(id=event_id, user=request.user)
                    events.append((event, (datetime.datetime.strptime(date, '%Y-%m-%d') - starting_date).days))

            results = {}
            np.random.seed(0)

            for record in stocks_in_portfolio:
                stock = record.stock

                # Average daily return based on the annualchange
                daily_return = (1 + (float(stock.annualchange) / 100)) ** (1 / 365) - 1

                # Average daily volatility
                daily_volatility = float(stock.volatility) / np.sqrt(365)

                # Simulate random daily percentage changes based on the daily return and daily volatility
                daily_changes = np.random.normal(daily_return, daily_volatility, 365)

                # Calculates the daily prices
                prices_with_events = [float(stock.price)]
                prices_without_events = [float(stock.price)]
                event_effects = np.zeros(365)

                # Adds the event impact
                for event, day in events:
                    # Applies the impact for each day after the event start with a decaying strength
                    for i in range(day, 365):
                        event_effects[i] += float(event.strength) * ((1 - float(event.decay_rate)) ** (i - day))

                # Calculates the final prices with the event impact
                for day, change in enumerate(daily_changes):
                    prices_without_events.append(prices_without_events[-1] * (1 + change))
                    prices_with_events.append(prices_with_events[-1] * (1 + change + event_effects[day]))

                # Adds the prices to the results
                results[stock.id] = {
                    'name': stock.name,
                    'prices_without_events': prices_without_events,
                    'prices_with_events': prices_with_events,
                    'units_owned': float(record.amount)
                }

            return JsonResponse({'result': 'success', 'data': results})
        
        else:

            return JsonResponse({'result': 'failure', 'message': 'Portfolio is empty!'})


    