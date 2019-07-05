class State:
    """
    ControllerState encloses general application variables
    """

    # Response state
    stop_speaking = False

    # Microphone state
    dynamic_energy_ratio = 0
    energy_threshold = 0

    # Assistant state
    first_activation = True
