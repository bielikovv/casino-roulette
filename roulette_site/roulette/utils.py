import random
from .models import *



def save_win_bet(request, amount_value, multiply_value, color):
    if amount_value != 0:
        StatisticRouletteUser.objects.create(user=request.user, bet_value=amount_value, win_value=int(amount_value) * multiply_value, color=color)
        amount_value = 0
        return amount_value



def save_loss_bet(request, amount_value, color):
    if amount_value != 0:
        StatisticRouletteUser.objects.create(user=request.user, bet_value=amount_value, color=color)
        amount_value = 0
        return amount_value



def multiply_win_value(request, amount_value, multiply_value):
    current_balance = Profile.objects.get(user=request.user)
    current_balance.balance += int(amount_value) * multiply_value
    current_balance.save()
    return current_balance.balance



def get_balance(request):
    current_balance = Profile.objects.get(user=request.user)
    return current_balance.balance


def balance_control_after_bet(request, amount_value):
    current_balance = Profile.objects.get(user=request.user)
    current_balance.balance -= int(amount_value)
    current_balance.save()


def generate_and_save_token(request):
    chars = 'abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    password = ''
    for i in range(31):
        password += random.choice(chars)
    token = Profile.objects.get(user=request.user)
    if token.token == None:
        token.token = password
        token.save()



def get_all_bets(request):
    statistic = StatisticRouletteUser.objects.filter(user=request.user)
    all_bets_value = 0
    for item in statistic:
        all_bets_value += item.bet_value
    return all_bets_value



def get_all_wins(request):
    statistic = StatisticRouletteUser.objects.filter(user=request.user)
    all_wins_value = 0
    for item in statistic:
        if item.win_value != None:
            all_wins_value += int(item.win_value)
    return all_wins_value



def send_to_other_user(request, token_recipient, value_recipient):
    current_balance = Profile.objects.get(user=request.user)
    current_balance_recipient = Profile.objects.get(token=token_recipient)
    current_balance_recipient.balance += int(value_recipient)
    current_balance_recipient.save()
    current_balance.balance -= int(value_recipient)
    current_balance.save()
    TransferTransactions.objects.create(sender=request.user.profile.nickname, recipient=current_balance_recipient.nickname, value=int(value_recipient))



def get_recipient_nickname(token_recipient):
    current_balance_recipient = Profile.objects.get(token=token_recipient)
    return current_balance_recipient.nickname