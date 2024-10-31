import pygame
import pygame_widgets

from src.events import *
from src.game import Game
from src.run_path import play_solution
from src.widgets import sidebar_widgets


def play_game(window, level=1, **widgets):
    moves = 0
    show_solution = False
    #widgets['paths'].transparency = False
    if level <= 1:
        widgets['prev_button'].hide()
    else:
        widgets['prev_button'].show()
    if level >= 10:
        widgets['next_button'].hide()
    else:
        widgets['next_button'].show()
    widgets['label'].set_text(f'Level {level}', 30)
    game = Game(level=level, window=window)
    game_loop = True
    solved_via_algorithm = False
    while game_loop:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                game_loop = False
                return {
                    'keep_playing': False,
                    'reset': -1,
                }
            elif event.type == RESTART_EVENT:
                game_loop = False
                print(f'Restarting level {level}\n')
                window.fill((0, 0, 0, 0))
                return {
                    'keep_playing': True,
                    'reset': level,
                }
            elif event.type == PREVIOUS_EVENT:
                game_loop = False
                print(f'Previous level {level - 1}\n')
                window.fill((0, 0, 0, 0))
                return {
                    'keep_playing': True,
                    'reset': level - 1,
                }
            elif event.type == NEXT_EVENT:
                game_loop = False
                print(f'Next testcase {level + 1}\n')
                window.fill((0, 0, 0, 0))
                return {
                    'keep_playing': True,
                    'reset': level + 1,
                }
            elif event.type == SOLVE_UCS_EVENT:
                print('Loading solution from output file for UCS\n')
                show_solution = True
                try:
                    with open(f'output/UCS/output-{level:02d}.txt', 'r') as f:
                        lines = f.readlines()
                        alg = lines[0].strip()
                        ans = lines[1].strip()
                        move_sequence = lines[2].strip()
                    widgets['paths'].set_text(
                        f'{alg}\n{ans}\n{move_sequence}',
                        10, 'red'
                    )
                    moves = play_solution(move_sequence, game, widgets, show_solution, moves)
                    if game.is_level_complete():
                        solved_via_algorithm = True
                except Exception as e:
                    widgets['paths'].set_text(
                        '[UCS] Solution Not Found!\nError: ' + str(e),
                        20,
                    )
            elif event.type == SOLVE_ASTARMAN_EVENT:
                print('Loading solution from output file for A*\n')
                show_solution = True
                try:
                    with open(f'output/A/output-{level:02d}.txt', 'r') as f:
                        lines = f.readlines()
                        alg = lines[0].strip()
                        ans = lines[1].strip()
                        move_sequence = lines[2].strip()
                    widgets['paths'].set_text(
                        f'{alg}\n{ans}\n{move_sequence}',
                        10, 'red'
                    )
                    moves = play_solution(move_sequence, game, widgets, show_solution, moves)
                    if game.is_level_complete():
                        solved_via_algorithm = True
                except Exception as e:
                    widgets['paths'].set_text(
                        '[A*] Solution Not Found!\nError: ' + str(e),
                        20,
                    )
        game.floor_group.draw(window)
        game.switch_group.draw(window)
        game.object_group.draw(window)
        game.number_group.draw(window)  
        game.ares_group.draw(window) 
        pygame_widgets.update(events)
        widgets['label'].draw()
        widgets['moves_label'].set_moves(f' Moves - {moves} ', 20)
        if show_solution:
            widgets['paths'].draw()
        pygame.display.update()
        if game.is_level_complete():
            print(f'Testcase Complete! - {moves} moves')
            #widgets['level_clear'].draw()
            pygame.display.update()
            game_loop = False
            wait = True
            while wait:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                        wait = False    
    del game
    print('Objects cleared!\n')
    if solved_via_algorithm:
        return {
            'keep_playing': True,
            'reset': 0,
        }
    else:
        return {
            'keep_playing': True,
            'reset': -1,
        }


def main():
    pygame.init()
    displayIcon = pygame.image.load('img/icon.png')
    pygame.display.set_icon(displayIcon)
    window = pygame.display.set_mode((1216, 640))
    pygame.display.set_caption('Ares adventure')
    level = 1
    keep_playing = True
    widgets = sidebar_widgets(window)
    while keep_playing:
        print(f'Loading testcase {level}\n')
        game_data = play_game(window, level, **widgets)
        keep_playing = game_data.get('keep_playing', False)
        if not keep_playing:
            pygame.quit()
            quit()
        reset = game_data.get('reset', -1)
        if reset == -1:
            level = min(level + 1, 5)
        elif reset == 0:
            pass
        else:
            level = reset

if __name__ == '__main__':
    main()