from Tools.scripts.win_add2path import modify
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.views.generic import View
from .models import *
from .forms import *
import random
from django.http import JsonResponse


class ShowMainPage(View):
    color = ''
    amount_value = 0
    def get(self, request):
        global color
        global amount_value
        num = random.randint(1, 100)
        if request.user.is_authenticated:
            current_balance = Profile.objects.get(user=request.user)
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                if 0 < num <= 2:
                    if color == 'GOLD':
                        current_balance.balance += int(amount_value) * 50
                        current_balance.save()
                        StatisticRouletteUser.objects.create(user=request.user, bet_value=amount_value, win_value=int(amount_value)*50, color=color)
                        amount_value = 0
                        return JsonResponse({'result': 'GOLD', 'after_bet_balance': current_balance.balance}, status=200)
                    StatisticRouletteUser.objects.create(user=request.user, bet_value=amount_value, color=color)
                    amount_value = 0
                    return JsonResponse({'result': 'GOLD', 'after_bet_balance': current_balance.balance}, status=200)
                elif 2 < num <= 21:
                    if color == 'BLUE':
                        current_balance.balance += int(amount_value) * 5
                        current_balance.save()
                        StatisticRouletteUser.objects.create(user=request.user, bet_value=amount_value, win_value=int(amount_value)*5, color=color)
                        amount_value = 0
                        return JsonResponse({'result': 'BLUE', 'after_bet_balance': current_balance.balance}, status=200)
                    StatisticRouletteUser.objects.create(user=request.user, bet_value=amount_value, color=color)
                    amount_value = 0
                    return JsonResponse({'result': 'BLUE', 'after_bet_balance': current_balance.balance}, status=200)
                elif 21 < num <= 52:
                    if color == 'RED':
                        current_balance.balance += int(amount_value) * 3
                        current_balance.save()
                        StatisticRouletteUser.objects.create(user=request.user, bet_value=amount_value, win_value=int(amount_value)*3, color=color)
                        amount_value = 0
                        return JsonResponse({'result': 'RED', 'after_bet_balance': current_balance.balance}, status=200)
                    StatisticRouletteUser.objects.create(user=request.user, bet_value=amount_value, color=color)
                    amount_value = 0
                    return JsonResponse({'result': 'RED', 'after_bet_balance': current_balance.balance}, status=200)
                elif 52 < num <= 100:
                    if color == 'BLACK':
                        current_balance.balance += int(amount_value) * 2
                        current_balance.save()
                        StatisticRouletteUser.objects.create(user=request.user, bet_value=amount_value, win_value=int(amount_value)*2, color=color)
                        amount_value = 0
                        return JsonResponse({'result': 'BLACK', 'after_bet_balance': current_balance.balance}, status=200)
                    StatisticRouletteUser.objects.create(user=request.user, bet_value=amount_value, color=color)
                    amount_value = 0
                    return JsonResponse({'result': 'BLACK', 'after_bet_balance': current_balance.balance}, status=200)

        return render(request, 'roulette/main_page.html')



    def post(self, request):
        global amount_value
        amount_value = request.POST.get('amount_value')
        global color
        color = request.POST.get('color')

        current_balance = Profile.objects.get(user=request.user)
        current_balance.balance -= int(amount_value)
        current_balance.save()

        return JsonResponse({"new_balance": current_balance.balance, "amount_value":amount_value}, status=200)
    modify()



def show_user_profile(request):
    statistic = StatisticRouletteUser.objects.filter(user=request.user)
    all_bets_value = 0
    all_wins_value = 0
    for item in statistic:
        all_bets_value += item.bet_value
        if item.win_value != None:
            all_wins_value += int(item.win_value)
    if request.method == 'POST':
        form1 = RedactInfoUserForm(request.POST, instance=request.user)
        form2 = RedactInfoProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form1.is_valid() and form2.is_valid():
            form1.save()
            form2.save()
            return redirect('profile')
    else:
        form1 = RedactInfoUserForm(instance=request.user)
        form2 = RedactInfoProfileForm(instance=request.user.profile)
    return render(request, 'roulette/user_profile.html', {'form1': form1, 'form2': form2, 'all_bets_value':all_bets_value, 'all_wins_value': all_wins_value})



def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'roulette/register.html', {'form':form})



def login_user(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('roulette_main_page')
    else:
        form = LoginForm()
    return render(request, 'roulette/login.html', {'form':form})



def logout_user(request):
    logout(request)
    return redirect('roulette_main_page')

