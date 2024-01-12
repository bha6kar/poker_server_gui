def get_card_action(best_hand, highest_hand, min_amount, max_amount):
    if max_amount == min_amount:
        return "call", min_amount
    elif max_amount < min_amount:
        return "fold", 0
    elif best_hand == 9:
        raise_amount = max_amount * 0.4
        if min_amount > raise_amount:
            raise_amount = min_amount
        return "raise", raise_amount
    elif best_hand >= 8 and highest_hand > 8:
        raise_amount = max_amount * 0.3
        if min_amount > raise_amount:
            raise_amount = min_amount
        return "raise", raise_amount
    elif best_hand >= 7 and highest_hand > 7:
        raise_amount = max_amount * 0.2
        if min_amount > raise_amount:
            raise_amount = min_amount
        return "raise", raise_amount
    elif best_hand >= 5 and highest_hand > 7:
        raise_amount = max_amount * 0.15
        if min_amount > raise_amount:
            raise_amount = min_amount
        return "raise", raise_amount
    elif best_hand >= 2 and best_hand < 5:
        raise_amount = max_amount * 0.10
        if min_amount > raise_amount:
            raise_amount = min_amount
        return "raise", raise_amount
    elif best_hand >= 1 and best_hand < 2:
        return "call", min_amount
    else:
        return "fold", 0
