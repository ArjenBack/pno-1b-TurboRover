def displayBoardGUI(board, path=None):
    import pygame as pg
    import time

    pg.init()

    WIDTH = 100

    window = pg.display.set_mode((len(board[0]) * WIDTH, len(board) * WIDTH))
    text = pg.font.SysFont("Arial", 20)
    running = True

    currentPath = 0

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE or event.key == pg.K_q:
                    running = False

        rowNr = 0
        cellNr = 0

        for row in board:
            for cell in row:
                match cell:
                    case 1:
                        pg.draw.rect(
                            window,
                            (0, 255, 0),
                            (cellNr * WIDTH, rowNr * WIDTH, WIDTH, WIDTH),
                        )
                    case 0:
                        pg.draw.rect(
                            window,
                            (255, 255, 255),
                            (cellNr * WIDTH, rowNr * WIDTH, WIDTH, WIDTH),
                        )
                    case 2:
                        pg.draw.rect(
                            window,
                            (255, 0, 0),
                            (cellNr * WIDTH, rowNr * WIDTH, WIDTH, WIDTH),
                        )
                textRender = text.render(f"({rowNr}, {cellNr})", False, (0, 0, 0))
                text_rect = textRender.get_rect()
                window.blit(
                    textRender,
                    (cellNr * WIDTH + 5, rowNr * WIDTH + 5),
                )
                cellNr += 1
            rowNr += 1
            cellNr = 0

        if path:
            if currentPath == len(path):
                currentPath = 1
            pg.draw.circle(window, (255, 100, 0), (WIDTH // 2, WIDTH // 2), 10)
            y, x = path[currentPath]
            pg.draw.circle(
                window,
                (128, 0, 128),
                (
                    x * WIDTH + WIDTH // 2,
                    y * WIDTH + WIDTH // 2,
                ),
                20,
            )
            for y, x in path[1:currentPath]:
                pg.draw.circle(
                    window,
                    (0, 0, 255),
                    (
                        x * WIDTH + WIDTH // 2,
                        y * WIDTH + WIDTH // 2,
                    ),
                    10,
                )
            currentPath += 1
        pg.display.flip()
        time.sleep(0.5)

    pg.quit()
