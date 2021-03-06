"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random

class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    ## Number of legal moves by player divided by number of legal moves by
    ## opponent. Returns higher values the less moves the opponent has.
    if float(len(game.get_legal_moves(player)))== 0:
        return(float(0))
    elif float(len(game.get_legal_moves(game.get_opponent(player)))) == 0 :
        return(float("inf"))
    else:
        return(5*float(len(game.get_legal_moves(player)))/float(len(game.get_legal_moves(game.get_opponent(player)))))


def custom_score_2(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    ## custom_score with the addition of the number of legal moves of the player
    ## minus the number of legal moves by the opponent. Hoping to get a result
    ## of "best of both worlds" here.
    if float(len(game.get_legal_moves(player)))== 0:
        return(float(0))
    elif float(len(game.get_legal_moves(game.get_opponent(player)))) == 0:
        return(float("inf"))
    else:
        subtract = 2*float(len(game.get_legal_moves(player)))-float(len(game.get_legal_moves(game.get_opponent(player))))
        divide = 5*float(len(game.get_legal_moves(player)))/float(len(game.get_legal_moves(game.get_opponent(player))))
        return(subtract+divide)


def custom_score_3(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    ## Same idea as custom_score_2, except that "subtract" is less heavily
    ## weighted as divide.
    if float(len(game.get_legal_moves(player)))== 0:
        return(float(0))
    elif float(len(game.get_legal_moves(game.get_opponent(player)))) == 0:
        return(float("inf"))
    else:
        subtract = float(len(game.get_legal_moves(player)))-float(len(game.get_legal_moves(game.get_opponent(player))))
        divide = 5*float(len(game.get_legal_moves(player)))/float(len(game.get_legal_moves(game.get_opponent(player))))
        return(subtract+divide)


class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """
    def __init__(self, search_depth=3, score_fn=custom_score, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout


class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************

        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            return self.minimax(game, self.search_depth)

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move

    def minimax(self, game, depth):
        """Implement depth-limited minimax search algorithm as described in
        the lectures.

        This should be a modified version of MINIMAX-DECISION in the AIMA text.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        def maxMove(self,game,depth):
            # Catch game if timer runs too long
            if self.time_left() < self.TIMER_THRESHOLD:
                raise SearchTimeout()
            # If no more moves left or depth limit has been hit return node's value
            if game.get_legal_moves() is None or len(game.get_legal_moves()) == 0 or depth == 0:
                return(self.score(game,self),game.get_player_location(game._inactive_player))
            # Get a random move to initialize moveset
            elif game.get_legal_moves() is not None and len(game.get_legal_moves()) != 0:
                priorityMove = game.get_legal_moves()[0]
            v = float("-inf")
            # Running iterations over all legal moves
            for m in game.get_legal_moves():
                minMoveVal,_ = minMove(self,game.forecast_move(m),depth-1)
                # Keeping track of priority move
                if minMoveVal > v:
                    priorityMove = m
                v = max(v,minMoveVal)
            return(v,priorityMove)
        def minMove(self,game,depth):
            # Catch game if timer runs too long
            if self.time_left() < self.TIMER_THRESHOLD:
                raise SearchTimeout()
            v = float("inf")
            # If no more moves left or depth limit has been hit return node's value
            if game.get_legal_moves() is None or len(game.get_legal_moves()) == 0 or depth == 0:
                return(self.score(game,self),game.get_player_location(game._inactive_player))
            # Get a random move to initialize moveset
            elif game.get_legal_moves() is not None and len(game.get_legal_moves()) != 0:
                priorityMove = game.get_legal_moves()[0]
            # Running iterations over all legal moves
            for m in game.get_legal_moves():
                maxMoveVal,_ = maxMove(self,game.forecast_move(m),depth-1)
                # Keeping track of priority move
                if maxMoveVal < v:
                    priorityMove = m
                v = min(v, maxMoveVal)
            return(v,priorityMove)
        v,moveChosen = maxMove(self,game,depth)
        return(moveChosen)

class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        Modify the get_move() method from the MinimaxPlayer class to implement
        iterative deepening search instead of fixed-depth search.

        **********************************************************************
        NOTE: If time_left() < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left
        self.cutoff = True
        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            depth = 0
            # Check for cutoff (which means depth has been hit) and continue
            # with a deeper search
            while(self.cutoff):
                best_move = self.alphabeta(game,depth)
                if self.cutoff:
                    depth += 1
            return(best_move)

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        """Implement depth-limited minimax search with alpha-beta pruning as
        described in the lectures.

        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        def maxMove(self,game,depth,alpha,beta):
            # Catch game if timer runs too long
            if self.time_left() < self.TIMER_THRESHOLD:
                raise SearchTimeout()
            # If no more moves left or depth limit has been hit return node's value
            if game.get_legal_moves() is None or len(game.get_legal_moves()) == 0:
                self.cutoff = False
                return(self.score(game,self),game.get_player_location(game._inactive_player))
            # Register end game and cutoff
            elif depth == 0:
                self.cutoff = True
                return(self.score(game,self),game.get_player_location(game._inactive_player))
            # Get a random move to initialize moveset
            elif game.get_legal_moves() is not None and len(game.get_legal_moves()) != 0:
                self.cutoff = False
                priorityMove = game.get_legal_moves()[0]
            # Init values for v and cutoffcurrent
            v = float("-inf")
            cutoffcurrent = True
            # Running iterations over all legal moves
            for m in game.get_legal_moves():
                minMoveVal,_ = minMove(self,game.forecast_move(m),depth-1,alpha,beta)
                # Defaulting to false once a false value has been found
                cutoffcurrent = min(self.cutoff,cutoffcurrent)
                # Keeping track of priority move
                if minMoveVal > v:
                    priorityMove = m
                v = max(v,minMoveVal)
                # Alpha beta pruning... if Beta is smaller (min value of higher
                # node), return v (skips nodes that would not return valueable
                # results)
                if v >= beta:
                    return(v,priorityMove)
                alpha = max(alpha,v)
            self.cutoff = cutoffcurrent
            return(v,priorityMove)

        def minMove(self,game,depth,alpha,beta):
            # Catch game if timer runs too long
            if self.time_left() < self.TIMER_THRESHOLD:
                raise SearchTimeout()
            # If no more moves left or depth limit has been hit return node's value
            if game.get_legal_moves() is None or len(game.get_legal_moves()) == 0:
                self.cutoff = False
                return(self.score(game,self),game.get_player_location(game._inactive_player))
            # Register end game and cutoff
            elif depth == 0:
                self.cutoff = True
                return(self.score(game,self),game.get_player_location(game._inactive_player))
            # Get a random move to initialize moveset
            elif game.get_legal_moves() is not None and len(game.get_legal_moves()) != 0:
                self.cutoff = False
                priorityMove = game.get_legal_moves()[0]
            # Init values for v and cutoffcurrent
            v = float("inf")
            cutoffcurrent = True
            # Running iterations over all legal moves
            for m in game.get_legal_moves():
                maxMoveVal,_ = maxMove(self,game.forecast_move(m),depth-1,alpha,beta)
                # Defaulting to false once a false value has been found
                cutoffcurrent = min(self.cutoff,cutoffcurrent)
                # Keeping track of priority move
                if maxMoveVal < v:
                    priorityMove = m
                v = min(v, maxMoveVal)
                # Alpha beta pruning... if alpha is larger (max value of higher
                # node), return v (skips nodes that would not return valueable
                # results)
                if v <= alpha:
                    return (v,priorityMove)
                beta = min(beta, v)
            self.cutoff = cutoffcurrent
            return(v,priorityMove)
        v,moveChosen = maxMove(self,game,depth,alpha,beta)
        return(moveChosen)
