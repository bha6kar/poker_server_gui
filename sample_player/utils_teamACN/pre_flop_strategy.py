from sample_player.struct_logger import logger


def determine_hand_group_pre_flop(hand_str):
    """You would need a more sophisticated logic to determine the hand group
    based on the hand's characteristics
    For simplicity, let's assume a basic classification here"""

    if "A" in hand_str:
        return "Premium"
    elif "K" in hand_str or "Q" in hand_str or "J" in hand_str:
        return "Strong"
    elif "10" in hand_str or "9" in hand_str or "8" in hand_str:
        return "Playable"
    elif "7" in hand_str or "6" in hand_str or "5" in hand_str:
        return "Marginal"
    else:
        return "Trash"


def estimate_win_probability_single_hand(hand) -> float:
    """Define hand groups and their corresponding probabilities
    (values are arbitrary)
    hand = ['A', 'T']
    hand_str = 'AT'
    """

    hand_groups = {
        "Premium": 0.8,
        "Strong": 0.6,
        "Playable": 0.4,
        "Marginal": 0.2,
        "Trash": 0.1,
    }

    # Convert cards to a string for easy comparison
    hand_str = "".join(str(card) for card in hand)
    # logger.info(hand_str)
    # Determine the hand group for the given hand
    hand_group = determine_hand_group_pre_flop(hand_str)

    # Get the corresponding probability for the hand group
    probability = hand_groups.get(hand_group, 0.0)

    return probability


def get_pre_flop_action(hole_card, min_amount, max_amount):
    """
    Determines the appropriate pre-flop action (call, raise, or fold) based on the hole cards
    and the betting amounts.

    Parameters:
    - hole_card (list of str): The list of hole cards (e.g., ['DQ', 'S6']).
    - min_amount (float): The minimum amount to be matched or raised.
    - max_amount (float): The maximum allowable amount for a bet or raise.

    Returns:
    Tuple[str, float]: A tuple representing the recommended action and the corresponding amount.
                      - If the action is "call," the amount is the minimum amount to be matched.
                      - If the action is "raise," the amount is the recommended raise amount.
                      - If the action is "fold," the amount is always 0.

    Raises:
    None
    """
    hand_card = [s[-1] for s in hole_card]
    pre_flop_probability = estimate_win_probability_single_hand(hand_card)
    # logger.info(
    #     f"Estimated Probability of Winning teamACN {hole_card}: {pre_flop_probability}"
    # )
    logger.info("pre_flop_strategy", pre_flop_probability=pre_flop_probability)

    if max_amount == min_amount:
        return "call", min_amount
    elif max_amount < min_amount:
        return "fold", 0
    elif pre_flop_probability >= 0.8:
        raise_amount = max_amount * 0.3
        raise_amount = max(min_amount, raise_amount)
        return "raise", raise_amount
    elif pre_flop_probability >= 0.7:
        raise_amount = max_amount * 0.2
        raise_amount = max(min_amount, raise_amount)
        return "raise", raise_amount
    elif 0.3 < pre_flop_probability < 0.7:
        return "call", min_amount
    else:
        return "fold", 0
