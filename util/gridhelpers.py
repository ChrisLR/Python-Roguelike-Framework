def distance_to(actor, target):
    actor_x, actor_y = actor.location.get_local_coords()
    target_x, target_y = target.location.get_local_coords()

    # return the distance to another object
    distance_x = abs(target_x - actor_x)
    distance_y = abs(target_y - actor_y)

    if distance_x >= distance_y:
        return distance_x
    else:
        return distance_y
