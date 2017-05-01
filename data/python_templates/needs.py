from characters.need import Need


hunger = Need(
    "hunger",
    positive_threshold_messages={0: "You are no longer starving.",
                                 50: "You are no longer hungry.",
                                 100: "You are full."},
    negative_threshold_messages={50: "You are hungry",
                                 0: "You are very hungry.",
                                 -50: "You are starving!"},
    threshold_effects={}
)


thirst = Need(
    "thirst",
    positive_threshold_messages={0: "You are still thirsty.",
                                 50: "You are no longer thirsty.",
                                 100: "You are full."},
    negative_threshold_messages={50: "You are thirsty",
                                 0: "You are very thirsty.",
                                 -50: "You are dying of thirst!"},
    threshold_effects={}
)