import pygame
from modules.config import *
from modules.screen_objects import Button, Input
from modules.edge import Edge, EdgeDirected


class Menu(object):
    def __init__(self, screen, screen_manager, clock):
        self.screen = screen
        self.screen_manager = screen_manager
        self.clock = clock
        self.input_number_nodes = Input(100, 100)
        self.input_number_edges = Input(250, 100)
        self.button = Button('OK', 350, 100)
        self.button_edge_dir = Button('Aresta Direcionada', 100, 150)
        self.button_edge_dir.set_font_size(20)
        self.button_edge_weight = Button('Custo', 250, 150)
        self.button_edge_weight.set_font_size(21)
        self.font = pygame.font.Font(
            'modules/fonts/roboto/Roboto-Black.ttf', 15)
        self.text_warning = ''

    def draw(self, clock_fps=30):
        # redraw screen
        self.screen.fill(LIGHT_GRAY)
        # Draw Input box
        self.input_number_nodes.draw(self.screen)
        self.input_number_edges.draw(self.screen)

        # Draw Buttons
        self.button_edge_dir.draw(self.screen)
        self.button_edge_weight.draw(self.screen)
        self.button.draw(self.screen)

        # render labels
        label = self.font.render("N° Nodes:", True, BLACK)
        self.screen.blit(label, (self.input_number_nodes.box.left -
                                 70, self.input_number_nodes.box.top))

        label = self.font.render("N° Edges:", True, BLACK)
        self.screen.blit(label, (self.input_number_edges.box.left -
                                 70, self.input_number_edges.box.top))

        # render warning
        label_warning = self.font.render(self.text_warning, True, RED)
        self.screen.blit(label_warning,
                         (SCREEN_WIDTH / 4, SCREEN_HEIGHT - 100))

        pygame.display.flip()
        self.clock.tick(clock_fps)

    def keys_listener(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # if clicked on input_number_nodes
                if self.input_number_nodes.box.collidepoint(event.pos):
                    self.input_number_nodes.clicked()
                else:
                    self.input_number_nodes.active = False

                # if clicked on input_number_edges
                if self.input_number_edges.box.collidepoint(event.pos):
                    self.input_number_edges.clicked()
                else:
                    self.input_number_edges.active = False

                # if clicked on Button Edge Directed
                if self.button_edge_dir.box.collidepoint(event.pos):
                    # active or not edge directeds
                    self.button_edge_dir.clicked()

                # if clicked on Button Edge Weight
                if self.button_edge_weight.box.collidepoint(event.pos):
                    # active or not edges weights
                    self.button_edge_weight.clicked()

                # if clicked on Button Confirm
                if self.button.box.collidepoint(event.pos):
                    self.text_warning = ''
                    self.button.clicked()

                    # Confirm qtt_nodes and qtt_edges
                    try:
                        qtt_nodes = int(self.input_number_nodes.text)
                        qtt_edges = int(self.input_number_edges.text)
                    except:
                        self.text_warning = "Digite Valores Validos!"
                        return

                    max_edges = int((qtt_nodes*(qtt_nodes - 1)) / 2)

                    if qtt_edges > max_edges:
                        self.text_warning = "Numero de Arestas maior do que o maximo possivel!"
                    else:
                        edge_type = 0 if self.button_edge_dir.active is False else 1
                        edge_weight = 0 if self.button_edge_weight.active is False else 1
                        self.screen_manager.switch_to_graph(
                            qtt_nodes, qtt_edges, edge_type, edge_weight)
                else:
                    self.button.active = False

            if event.type == pygame.KEYDOWN:
                # typing on input_number_nodes
                if self.input_number_nodes.active:
                    if event.key == pygame.K_RETURN:
                        self.input_number_nodes.text = ''
                    self.input_number_nodes.typing(event)

                # typing on input_number_edges
                if self.input_number_edges.active:
                    if event.key == pygame.K_RETURN:
                        self.input_number_edges.text = ''
                    self.input_number_edges.typing(event)
