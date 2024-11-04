import pygame
import pygame_widgets


def play_solution(solution, game, widgets, show_solution, moves, sum_weight):
    for move in solution:
        events = pygame.event.get()
        move_increment, weight_increment = game.ares.update(move.upper())
        moves += move_increment
        sum_weight += weight_increment
        game.floor_group.draw(game.window)
        game.switch_group.draw(game.window)
        game.object_group.draw(game.window)
        game.number_group.draw(game.window)  
        game.ares_group.draw(game.window) 
        pygame_widgets.update(events)
        widgets['label'].draw()
        widgets['moves_label'].set_moves(f' Moves - {moves} ', 20)
        widgets['weight_label'].set_moves(f' Weight - {sum_weight} ', 20)
        if show_solution:
            widgets['paths'].draw()
        pygame.display.update()
        pygame.time.delay(200)
    return moves, sum_weight
