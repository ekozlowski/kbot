help_text = "`grocery <command>` - Use `grocery help` for more info."

grocery_list = []

def handle(command):
    global grocery_list
    pieces = command.split()
    response = '\n'.join([
        "I know that was something to do with groceries, but I didn't understand what you meant.  Sorry.  :disappointed:",
        "",
        "Here are some things you can tell me:",
        "`grocery add <item>`  adds <item> to your grocery list.",
        "`grocery remove <item>` removes <item> from your grocery list.",
        "`grocery list` lists your groceries.",
        "`grocery clear` clears your list.",
    ])
    if pieces[0].lower() == 'help':
        return response
    try:
        action = pieces[1]
    except IndexError:
        return response
    if pieces[2:]:
        o = ' '.join(pieces[2:])
    if action == 'add':
        if not o:
            response = "Ok, I need something to add."
        else:
            grocery_list.append(o)
            response = "Got it.  Added {} to your grocery list.".format(o)
    elif action == 'remove':
        if not o:
            response = "Ok, I need something to remove."
        else:
            try:
                grocery_list.remove(o)
                response = "Removed {} from your grocery list.".format(o)
            except:
                response = "Problem removing grocery {} from list.  Was it there to begin with?".format(o)
    elif action == 'list':
        response = '\n'.join([
            "Here are your groceries:",
            *grocery_list,
        ])
    elif action == 'clear':
        grocery_list = []
        response = 'Grocery list cleared.  Hope you got what you needed...'
    return response
