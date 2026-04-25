CATEGORY_TEMPLATES = {
    "transaction_intensity": {
        "positive": "The customer demonstrates elevated transaction intensity, including {}.",
        "negative": "Customer transaction intensity remains stable and within expected levels, with {}."
    },
    "transaction_size_pattern": {
        "positive": "The customer shows atypical transaction size patterns, particularly {}.",
        "negative": "Transaction sizes are consistent with expected patterns, including {}."
    },
    "transaction_variability": {
        "positive": "The customer exhibits high variability in transaction behavior, including {}.",
        "negative": "Transaction behavior shows low variability and remains consistent over time, with {}."
    },
    "large_transactions": {
        "positive": "Unusually large transactions were identified, particularly {}.",
        "negative": "No unusually large transactions were identified, with transaction amounts remaining within expected ranges, including {}."
    },
    "fund_flow_pattern": {
        "positive": "The customer presents an imbalanced fund flow structure, characterized by {}.",
        "negative": "Fund flow structure appears balanced and consistent, characterized by {}."
    },
    "short_term_activity": {
        "positive": "Recent short-term activity shows unusual levels, including {}.",
        "negative": "Recent short-term activity remains within normal levels, including {}."
    },
    "activity_acceleration": {
        "positive": "There is a significant acceleration in transaction behavior, evidenced by {}.",
        "negative": "No significant acceleration in transaction behavior is observed, with activity remaining stable, including {}."
    }
}

FEATURE_METADATA = {
    "transaction_count_received": {
        "theme": "transaction_intensity",
        "description": "total number of received transactions"
    },

    "transaction_count_sent": {
        "theme": "transaction_intensity",
        "description": "total number of sent transactions"
    },

    "total_amount_received": {
        "theme": "transaction_intensity",
        "description": "aggregate monetary value of received funds"
    },

    "total_amount_sent": {
        "theme": "transaction_intensity",
        "description": "aggregate monetary value of sent funds"
    },

    # transaction size behavior

    "median_amount_received": {
        "theme": "transaction_size_pattern",
        "description": "median value of received transactions"
    },

    "median_amount_sent": {
        "theme": "transaction_size_pattern",
        "description": "median value of sent transactions"
    },

    "std_amount_received": {
        "theme": "transaction_variability",
        "description": "standard deviation of received transaction values"
    },

    "std_amount_sent": {
        "theme": "transaction_variability",
        "description": "standard deviation of sent transaction values"
    },

    "max_amount_received": {
        "theme": "transaction_variability",
        "description": "maximum received transaction value"
    },

    "max_amount_sent": {
        "theme": "transaction_variability",
        "description": "maximum sent transaction value"
    },

    # directional behavior

    "sent_received_ratio": {
        "theme": "fund_flow_pattern",
        "description": "measures imbalance between funds sent and received"
    },

    "transaction_direction_ratio": {
        "theme": "fund_flow_pattern",
        "description": "measures imbalance in number of sent vs received transactions"
    },

    # short term activity

    "total_amount_received_30d": {
        "theme": "short_term_activity",
        "description": "total received amount during the past 30 days"
    },

    "total_amount_received_7d": {
        "theme": "short_term_activity",
        "description": "total received amount during the past 7 days"
    },

    "total_amount_sent_30d": {
        "theme": "short_term_activity",
        "description": "total sent amount during the past 30 days"
    },

    "total_amount_sent_7d": {
        "theme": "short_term_activity",
        "description": "total sent amount during the past 7 days"
    },

    "transaction_count_received_30d": {
        "theme": "short_term_activity",
        "description": "received transaction count in the past 30 days"
    },

    "transaction_count_received_7d": {
        "theme": "short_term_activity",
        "description": "received transaction count in the past 7 days"
    },

    "transaction_count_sent_30d": {
        "theme": "short_term_activity",
        "description": "sent transaction count in the past 30 days"
    },

    "transaction_count_sent_7d": {
        "theme": "short_term_activity",
        "description": "sent transaction count in the past 7 days"
    },

    # temporal acceleration

    "total_amount_30d_ratio": {
        "theme": "activity_acceleration",
        "description": "measures recent increase or decrease in total transaction amount over 30 days"
    },

    "total_amount_7d_ratio": {
        "theme": "activity_acceleration",
        "description": "measures recent increase or decrease in total transaction amount over 7 days"
    },

    "transaction_count_30d_ratio": {
        "theme": "activity_acceleration",
        "description": "measures recent increase or decrease in transaction count over 30 days"
    },

    "transaction_count_7d_ratio": {
        "theme": "activity_acceleration",
        "description": "measures recent increase or decrease in transaction count over 7 days"
    }
}