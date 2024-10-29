import pygame
import pygame_widgets


def play_solution(solution, game, widgets, show_solution, moves):
    for move in solution:
        events = pygame.event.get()
        moves += game.ares.update(move.upper())
        game.floor_group.draw(game.window)
        game.switch_group.draw(game.window)
        game.object_group.draw(game.window)
        game.number_group.draw(game.window)  
        game.ares_group.draw(game.window) 
        pygame_widgets.update(events)
        widgets['label'].draw()
        widgets['moves_label'].set_moves(f' Moves - {moves} ', 20)
        if show_solution:
            widgets['paths'].draw()
        pygame.display.update()
        pygame.time.delay(130)
    return moves
