# (89110, Spring 2023, Assigment #7, Fedor Naumenko, 327017893, naumenf)


def load_word_list(file_path):
    """
    Load a word list from a file and filter words based on the given word length.

    Args:
        file_path (str): Path to the file containing the word list.

    Returns:
        list: List of words with the specified length.
    """
    word_list = []

    # Read from the file
    with open(file_path, 'r') as my_file:
        # Check each word
        for word in my_file:
            word = word.strip()
            # Add it to the list
            word_list.append(word)

    return word_list


def update_settings(settings):
    """
    Update the game settings based on user input.

    Args:
        settings (dict): Dictionary containing the game settings.

    Returns:
        None
    """
    print("Enter settings:")
    user_input = input()

    # Check if input starts and ends with curly braces
    if user_input[0] != '{' or user_input[-1] != '}':
        print("Invalid settings")
        return

    # Remove the curly braces from the input
    user_input = user_input[1:len(user_input) - 1]

    # Split the input into key-value pairs
    pairs = user_input.split(',')

    # Iterate over each key-value pair
    for pair in pairs:

        new_key, new_value = pair.split(':')

        # Check if the key exists in settings
        if new_key.strip() in settings:
            if new_key.strip() == 'tries' or new_key == 'word_length':
                # Check if the value is a positive integer
                if int(new_value.strip()) > 0:
                    settings[new_key.strip()] = int(new_value.strip())
                else:
                    print("Invalid settings")
                    return
            if new_key.strip() == 'file_path':
                settings[new_key.strip()] = new_value.strip()

        else:
            # Add the key-value pair to settings
            settings[new_key.strip()] = new_value.strip()

    print("Settings were updated")


def play_game(settings, word_list, scoreboard):
    """
    Play the Wordle game based on the given settings and word list.

    Args:
        settings (dict): Dictionary containing the game settings.
        word_list (list): List of valid words for the game.
        scoreboard (dict): Dictionary to store player statistics.

    Returns:
        None
    """
    print("Enter player's name:")
    player_name = input()

    print("Enter a word:")
    word = input()

    # Checks if the word the player needs to guess is a real word
    if word not in word_list:
        print("That's not a word!")
        return

    # Checks if the length of the word is legal according to settings
    if len(word) != settings['word_length']:
        print("That word is the wrong length!")
        return

    print(f"Welcome to Wordle! You have {settings['tries']} tries to guess the word.")
    print(f"The word is {settings['word_length']} letters long.")

    # Init variables
    num_of_guesses = 0
    correct_guess = False
    clues = []

    while num_of_guesses < settings['tries'] and not correct_guess:
        print(f"Guess a word:")
        guess = input()
        num_of_guesses += 1

        # Check if the user guessed the correct answer
        if guess == word:
            print(guess)
            print("You win!")
            print("Game over!")

            # Add guess to the list of feedbacks
            clues.append(guess)
            # Print all the guess abd clues
            for clue in clues:
                print(clue)

            # Update scoreboard
            update_scoreboard(scoreboard, player_name, 'win', num_of_guesses)
            return

        # Check if the guess is of legal length
        if len(guess) != settings['word_length']:
            print("Invalid guess")
            num_of_guesses -= 1
            continue

        # Check if the guess is an actual word
        if guess not in word_list:
            print("Invalid guess")
            num_of_guesses -= 1
            continue

        # Init clue ,compare the given words letters and mark accordingly
        clue = ''
        for i in range(settings['word_length']):
            if guess[i] == word[i]:
                clue += word[i]
            elif guess[i] in word:
                clue += '+'
            else:
                clue += '-'

        # Add the clue to list of clues and print it
        clues.append(clue)
        print(clue)
    print("You lost! The word was", word)
    print("Game over!")

    # Update scoreboard accordingly
    update_scoreboard(scoreboard, player_name, 'lost', num_of_guesses)

    # Print all the clues
    for clue in clues:
        print(clue)


def update_scoreboard(scoreboard, player_name, game_result, tries):
    """
    Update the scoreboard based on the game result.

    Args:
        scoreboard (dict): Dictionary storing player statistics.
        player_name (str): Name of the player.
        game_result (str): Result of the game ('win' or 'lost').
        tries (int): Number of tries taken in the game.

    Returns:
        None
    """
    # Update the player's stats if he exists
    if player_name in scoreboard:
        scoreboard[player_name]['games_played'] += 1

        # If the player won his first game add wins and tries
        if game_result == 'win':
            scoreboard[player_name]['wins'] += 1
            scoreboard[player_name]['total_tries'] += tries

            # Calculate his average number of tries in games he won
            scoreboard[player_name]['average_tries'] = \
                scoreboard[player_name]['total_tries'] / scoreboard[player_name]['wins']

        # Calculate his win rate
        scoreboard[player_name]['win_rate'] = \
            (scoreboard[player_name]['wins'] / scoreboard[player_name]['games_played']) * 100

    # If the player doesn't exist create him
    else:

        # If the player won his first game
        if game_result == 'win':
            scoreboard[player_name] = {
                'games_played': 1,
                'wins': 1,
                'total_tries': tries,
                'win_rate': 100,
                'average_tries': tries
            }

        # If the player lost his first game
        elif game_result == 'lost':
            scoreboard[player_name] = {
                'games_played': 1,
                'wins': 0,
                'total_tries': 0,
                'win_rate': 0,
                'average_tries': 0
            }


def view_settings(settings):
    """
    View and print the game settings.

    Args:
        settings (dict): Dictionary containing the game settings.

    Returns:
        None
    """
    # Print values sorted alphabetically
    for key, value in sorted(settings.items()):
        print(f"{key}: {value}")


def get_sort_key(player_stats):
    """
    Get the sort key for sorting players' stats.

    Args:
        player_stats (tuple): Tuple containing player name and their stats.

    Returns:
        tuple: Sort key for sorting.
    """
    return -player_stats[1]['win_rate'], player_stats[0]


def view_scoreboard(scoreboard):
    """
    View and print the scoreboard.

    Args:
        scoreboard (dict): Dictionary storing player statistics.

    Returns:
        None
    """
    print("Scoreboard:")

    # Get the scoreboard sorted
    sorted_scores = sorted(scoreboard.items(), key=get_sort_key)

    # Print the sorted scoreboard
    for player, stats in sorted_scores:
        num_of_games = stats['games_played']
        win_percent = stats['win_rate']
        num_of_tries = stats['average_tries']

        # If the player haven't won yet, print NaN in average tries
        if stats['wins'] == 0:
            print(f"{player}: {num_of_games} games, {win_percent:.2f}% win rate, {'NaN'} average tries")
        else:
            print(f"{player}: {num_of_games} games, {win_percent:.2f}% win rate, {num_of_tries:.2f} average tries")


def main():
    settings = {
        'file_path': 'words.txt',
        'tries': 6,
        'word_length': 5
    }
    # Saves the words of a length given in settings
    word_list = load_word_list(settings['file_path'])
    # Used to save the players stats
    scoreboard = {}

    # Prints the menu and calls function according to the input from the user
    while True:
        print("Choose an option:")
        print("0. Exit")
        print("1. Update settings")
        print("2. Play")
        print("3. View settings")
        print("4. Scoreboard")
        choice = input()

        if choice == '0':
            break
        elif choice == '1':
            update_settings(settings)
            # Saves the words of a length given in settings
            word_list = load_word_list(settings['file_path'])
        elif choice == '2':
            play_game(settings, word_list, scoreboard)
        elif choice == '3':
            view_settings(settings)
        elif choice == '4':
            view_scoreboard(scoreboard)
        else:
            print("Invalid choice")


if __name__ == '__main__':
    main()
