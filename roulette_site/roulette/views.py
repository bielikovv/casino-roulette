from Tools.scripts.win_add2path import modify
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.views.generic import View
from .models import *
from .forms import *
import random
from django.http import JsonResponse
from .utils import *


class ShowMainPage(View):
    color = ''
    amount_value = 0
    def get(self, request):
        global color
        global amount_value
        num = random.randint(1, 100)
        if request.user.is_authenticated:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                if 0 < num <= 2:
                    if color == 'GOLD':
                        multiply_win_value(request, amount_value, 50)
                        amount_value = save_win_bet(request, amount_value, 50, color)
                        return JsonResponse({'result': 'GOLD', 'after_bet_balance': get_balance(request)}, status=200)
                    amount_value = save_loss_bet(request, amount_value, color)
                    return JsonResponse({'result': 'GOLD', 'after_bet_balance': get_balance(request)}, status=200)
                elif 2 < num <= 21:
                    if color == 'BLUE':
                        multiply_win_value(request, amount_value, 5)
                        amount_value = save_win_bet(request, amount_value, 5, color)
                        return JsonResponse({'result': 'BLUE', 'after_bet_balance': get_balance(request)}, status=200)
                    amount_value = save_loss_bet(request, amount_value, color)
                    return JsonResponse({'result': 'BLUE', 'after_bet_balance': get_balance(request)}, status=200)
                elif 21 < num <= 52:
                    if color == 'RED':
                        multiply_win_value(request, amount_value, 3)
                        amount_value = save_win_bet(request, amount_value, 3, color)
                        return JsonResponse({'result': 'RED', 'after_bet_balance': get_balance(request)}, status=200)
                    amount_value = save_loss_bet(request, amount_value, color)
                    return JsonResponse({'result': 'RED', 'after_bet_balance': get_balance(request)}, status=200)
                elif 52 < num <= 100:
                    if color == 'BLACK':
                        multiply_win_value(request, amount_value, 2)
                        amount_value = save_win_bet(request, amount_value, 2, color)
                        return JsonResponse({'result': 'BLACK', 'after_bet_balance': get_balance(request)}, status=200)
                    amount_value = save_loss_bet(request, amount_value, color)
                    return JsonResponse({'result': 'BLACK', 'after_bet_balance': get_balance(request)}, status=200)
        return render(request, 'roulette/main_page.html')



    def post(self, request):
        global amount_value
        amount_value = request.POST.get('amount_value')
        global color
        color = request.POST.get('color')
        balance_control_after_bet(request, amount_value)
        return JsonResponse({"new_balance": get_balance(request), "amount_value":amount_value}, status=200)
    modify()



def show_user_profile(request):
    last_bets = StatisticRouletteUser.objects.filter(user=request.user).order_by("-time")[:10]
    token_recipient = request.POST.get('token')
    value_recipient = request.POST.get('value')
    if token_recipient:
        send_to_other_user(request, token_recipient, value_recipient)
        return JsonResponse({"new_balance": get_balance(request), "value_recipient":value_recipient, "recipient_name":get_recipient_nickname(token_recipient),})

    generate_and_save_token(request)
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
    return render(request, 'roulette/user_profile.html', {'form1': form1, 'form2': form2, 'all_bets_value': get_all_bets(request), 'all_wins_value': get_all_wins(request), 'last_bets': last_bets})



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

