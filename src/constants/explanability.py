CATEGORY_TEMPLATES = {
    "transaction_intensity": 
        "The customer demonstrates elevated transaction intensity, including {}.",

    "transaction_size_pattern":
        "The customer shows atypical transaction size patterns, particularly {}.",

    "transaction_variability":
        "The customer exhibits high variability in transaction behavior, including {}.",

    "large_transactions":
        "Unusually large transactions were identified, particularly {}.",

    "fund_flow_pattern":
        "The customer presents an imbalanced fund flow structure, characterized by {}.",

    "short_term_activity":
        "Recent short-term activity shows unusual levels, including {}.",

    "activity_acceleration":
        "There is a significant acceleration in transaction behavior, evidenced by {}."
}

FEATURE_METADATA = {

    # transaction volume

    "transaction_count_received": {
        "theme": "transaction_intensity",
        "subtheme": "incoming_activity",
        "behavior": "number of incoming transactions",
        "risk_trigger": "high",
        "context_type": "peer_comparison",
        "description": "total number of received transactions"
    },

    "transaction_count_sent": {
        "theme": "transaction_intensity",
        "subtheme": "outgoing_activity",
        "behavior": "number of outgoing transactions",
        "risk_trigger": "high",
        "context_type": "peer_comparison",
        "description": "total number of sent transactions"
    },

    "total_amount_received": {
        "theme": "transaction_intensity",
        "subtheme": "incoming_volume",
        "behavior": "total incoming transaction volume",
        "risk_trigger": "high",
        "context_type": "peer_comparison",
        "description": "aggregate monetary value of received funds"
    },

    "total_amount_sent": {
        "theme": "transaction_intensity",
        "subtheme": "outgoing_volume",
        "behavior": "total outgoing transaction volume",
        "risk_trigger": "high",
        "context_type": "peer_comparison",
        "description": "aggregate monetary value of sent funds"
    },

    # transaction size behavior

    "median_amount_received": {
        "theme": "transaction_size_pattern",
        "subtheme": "incoming_typical_size",
        "behavior": "typical incoming transaction size",
        "risk_trigger": "high",
        "context_type": "peer_comparison",
        "description": "median value of received transactions"
    },

    "median_amount_sent": {
        "theme": "transaction_size_pattern",
        "subtheme": "outgoing_typical_size",
        "behavior": "typical outgoing transaction size",
        "risk_trigger": "high",
        "context_type": "peer_comparison",
        "description": "median value of sent transactions"
    },

    "std_amount_received": {
        "theme": "transaction_variability",
        "subtheme": "incoming_variability",
        "behavior": "variability in incoming transaction sizes",
        "risk_trigger": "high",
        "context_type": "behavioral_deviation",
        "description": "standard deviation of received transaction values"
    },

    "std_amount_sent": {
        "theme": "transaction_variability",
        "subtheme": "outgoing_variability",
        "behavior": "variability in outgoing transaction sizes",
        "risk_trigger": "high",
        "context_type": "behavioral_deviation",
        "description": "standard deviation of sent transaction values"
    },

    "max_amount_received": {
        "theme": "transaction_variability",
        "subtheme": "incoming_large_value",
        "behavior": "largest incoming transaction amount",
        "risk_trigger": "high",
        "context_type": "peer_comparison",
        "description": "maximum received transaction value"
    },

    "max_amount_sent": {
        "theme": "transaction_variability",
        "subtheme": "outgoing_large_value",
        "behavior": "largest outgoing transaction amount",
        "risk_trigger": "high",
        "context_type": "peer_comparison",
        "description": "maximum sent transaction value"
    },

    # directional behavior

    "sent_received_ratio": {
        "theme": "fund_flow_pattern",
        "subtheme": "directional_balance",
        "behavior": "ratio of outgoing to incoming transaction volume",
        "risk_trigger": "extreme",
        "context_type": "behavioral_deviation",
        "description": "measures imbalance between funds sent and received"
    },

    "transaction_direction_ratio": {
        "theme": "fund_flow_pattern",
        "subtheme": "transaction_direction_bias",
        "behavior": "ratio of outgoing to incoming transaction count",
        "risk_trigger": "extreme",
        "context_type": "behavioral_deviation",
        "description": "measures imbalance in number of sent vs received transactions"
    },

    # short term activity

    "total_amount_received_30d": {
        "theme": "short_term_activity",
        "subtheme": "incoming_30d_volume",
        "behavior": "incoming transaction volume over last 30 days",
        "risk_trigger": "high",
        "context_type": "temporal_deviation",
        "description": "total received amount during the past 30 days"
    },

    "total_amount_received_7d": {
        "theme": "short_term_activity",
        "subtheme": "incoming_7d_volume",
        "behavior": "incoming transaction volume over last 7 days",
        "risk_trigger": "high",
        "context_type": "temporal_deviation",
        "description": "total received amount during the past 7 days"
    },

    "total_amount_sent_30d": {
        "theme": "short_term_activity",
        "subtheme": "outgoing_30d_volume",
        "behavior": "outgoing transaction volume over last 30 days",
        "risk_trigger": "high",
        "context_type": "temporal_deviation",
        "description": "total sent amount during the past 30 days"
    },

    "total_amount_sent_7d": {
        "theme": "short_term_activity",
        "subtheme": "outgoing_7d_volume",
        "behavior": "outgoing transaction volume over last 7 days",
        "risk_trigger": "high",
        "context_type": "temporal_deviation",
        "description": "total sent amount during the past 7 days"
    },

    "transaction_count_received_30d": {
        "theme": "short_term_activity",
        "subtheme": "incoming_30d_frequency",
        "behavior": "number of incoming transactions in last 30 days",
        "risk_trigger": "high",
        "context_type": "temporal_deviation",
        "description": "received transaction count in the past 30 days"
    },

    "transaction_count_received_7d": {
        "theme": "short_term_activity",
        "subtheme": "incoming_7d_frequency",
        "behavior": "number of incoming transactions in last 7 days",
        "risk_trigger": "high",
        "context_type": "temporal_deviation",
        "description": "received transaction count in the past 7 days"
    },

    "transaction_count_sent_30d": {
        "theme": "short_term_activity",
        "subtheme": "outgoing_30d_frequency",
        "behavior": "number of outgoing transactions in last 30 days",
        "risk_trigger": "high",
        "context_type": "temporal_deviation",
        "description": "sent transaction count in the past 30 days"
    },

    "transaction_count_sent_7d": {
        "theme": "short_term_activity",
        "subtheme": "outgoing_7d_frequency",
        "behavior": "number of outgoing transactions in last 7 days",
        "risk_trigger": "high",
        "context_type": "temporal_deviation",
        "description": "sent transaction count in the past 7 days"
    },

    # temporal acceleration

    "total_amount_30d_ratio": {
        "theme": "activity_acceleration",
        "subtheme": "volume_change_30d",
        "behavior": "change in transaction volume compared to historical baseline (30 days)",
        "risk_trigger": "extreme",
        "context_type": "temporal_acceleration",
        "description": "measures recent increase or decrease in total transaction amount over 30 days"
    },

    "total_amount_7d_ratio": {
        "theme": "activity_acceleration",
        "subtheme": "volume_change_7d",
        "behavior": "change in transaction volume compared to historical baseline (7 days)",
        "risk_trigger": "extreme",
        "context_type": "temporal_acceleration",
        "description": "measures recent increase or decrease in total transaction amount over 7 days"
    },

    "transaction_count_30d_ratio": {
        "theme": "activity_acceleration",
        "subtheme": "frequency_change_30d",
        "behavior": "change in transaction frequency compared to historical baseline (30 days)",
        "risk_trigger": "extreme",
        "context_type": "temporal_acceleration",
        "description": "measures recent increase or decrease in transaction count over 30 days"
    },

    "transaction_count_7d_ratio": {
        "theme": "activity_acceleration",
        "subtheme": "frequency_change_7d",
        "behavior": "change in transaction frequency compared to historical baseline (7 days)",
        "risk_trigger": "extreme",
        "context_type": "temporal_acceleration",
        "description": "measures recent increase or decrease in transaction count over 7 days"
    }
}