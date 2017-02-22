grocery_list = []


def handler(command):
    global grocery_list
    pieces = command.split()
    action = pieces[1]
    if pieces[2:]:
        o = ' '.join(pieces[2:])
    if action == 'add':
        grocery_list.append(o)
        response = "Added {}".format(o)
    elif action == 'remove':
        try:
            grocery_list.remove(o)
        except (Exception) as e:
            return "Problem removing grocery {} from list.  Was it there to begin with?".format(o)
    elif action == 'list':
        response = '\n'.join([
            "Here are your groceries:",
            *grocery_list,
        ])
    elif action == 'clear':
        grocery_list = []
        response = 'Grocery list cleared.  Hope you got what you needed...'
    return response
