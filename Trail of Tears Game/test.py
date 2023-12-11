import pygame
import sys
import math

pygame.init()

# Set up the display with the desired dimensions
screen_width = 800
screen_height = 400
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Trail of Tears Game")

# Load the background images
background_title = pygame.image.load("TrailTitle.png")
background_nature = pygame.image.load("BackDropNature.png")
character_selection_background = pygame.image.load("StoryTitle.png")
character_selection = pygame.image.load("CharacterSelection.png")
lee_description_image = pygame.image.load("LeeDescription.png")
lee_house_image = pygame.image.load("LeeHouse.png")
caravan_image = pygame.image.load("Caravan.png")
food_image = pygame.image.load("Food.png")
buffalo_image = pygame.image.load("Buffalo.png")

# Load the "AnyKeyStart" font
press_any_key_text = pygame.image.load("AnyKeyStart.png")

# Set initial positions and states
background_title_rect = background_title.get_rect()
background_nature_rect = background_nature.get_rect(x=screen_width, y=-190)
character_selection_background_rect = character_selection_background.get_rect()
character_selection_rect = character_selection.get_rect(y=-50)
lee_description_rect = lee_description_image.get_rect(center=(screen_width // 2, screen_height // 2))
lee_house_rect = lee_house_image.get_rect(center=(screen_width // 2, screen_height // 2))
caravan_rect = caravan_image.get_rect(center=(screen_width // 2, screen_height // 2))
food_rect = food_image.get_rect(center=(screen_width // 2, screen_height // 2))
buffalo_rect = buffalo_image.get_rect(center=(screen_width // 2, screen_height // 2))

# Set up fonts
font_size = 16
font = pygame.font.Font(None, font_size)

# Set initial positions for text
press_any_key_rect = press_any_key_text.get_rect(center=(screen_width // 2, screen_height // 2))

# Set initial opacity and opacity change for the text
initial_opacity_text = 255
opacity_change_text = 30

# Game states
title_screen = "title_screen"
character_selection_state = "character_selection"
lee_description_state = "lee_description"
dialog_options_state = "dialog_options"
the_trail_state = "the_trail_state"
food_state = "food_state"
buffalo_state = "buffalo_state"
current_state = title_screen

# Variables to store the selected character, user's choice, and flags
selected_character = None
user_choice = None
show_continue_text = False
buffalo_clicked = False

# Running loop
running = True
clock = pygame.time.Clock()

# Function to render text with a black outline
def render_text_with_outline(text, pos, text_color, outline_color, show_follow_up_text=False):
    # Render the outline
    outline_surface = font.render(text, True, outline_color)
    outline_rect = outline_surface.get_rect(center=pos)
    outline_rect.x -= 2
    outline_rect.y -= 2
    screen.blit(outline_surface, outline_rect)

    # Render the text
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=pos)
    screen.blit(text_surface, text_rect)

    # Show follow-up text if the flag is True
    if show_follow_up_text:
        follow_up_text = "Washington Lee was forcefully removed from his house in Georgia"
        pos_follow_up = (screen_width // 2, pos[1] + 40)
        render_text_with_outline(follow_up_text, pos_follow_up, (255, 255, 255), (0, 0, 0))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if current_state == title_screen:
                current_state = character_selection_state
            elif current_state == character_selection_state:
                if event.key == pygame.K_w:
                    selected_character = "Washington Lee"
                    current_state = lee_description_state
            elif current_state == lee_description_state:
                if event.key == pygame.K_RETURN:
                    current_state = dialog_options_state
            elif current_state == dialog_options_state:
                if event.key == pygame.K_a or event.key == pygame.K_b or event.key == pygame.K_c:
                    user_choice = chr(event.key)
                    show_continue_text = True
                elif event.key == pygame.K_RETURN and show_continue_text:
                    current_state = the_trail_state
            elif current_state == the_trail_state:
                if event.key == pygame.K_RETURN:
                    current_state = food_state
            elif current_state == food_state:
                if event.key == pygame.K_RETURN:
                    current_state = buffalo_state
            elif current_state == buffalo_state and event.key == pygame.K_RETURN:
                current_state = title_screen

        elif event.type == pygame.MOUSEBUTTONDOWN and current_state == buffalo_state:
            if buffalo_rect.collidepoint(event.pos):
                buffalo_clicked = True

    screen.fill((0, 0, 0))  # Clear the screen

    if current_state == title_screen:
        pulsing_factor = 0.5 + 0.5 * math.sin(pygame.time.get_ticks() / 300.0)
        current_opacity_text = initial_opacity_text * pulsing_factor
        background_nature_rect.x -= 3

        if background_nature_rect.right <= 0:
            background_nature_rect.x = screen_width

        screen.blit(background_title, background_title_rect)
        screen.blit(background_nature, background_nature_rect)
        press_any_key_text.set_alpha(int(current_opacity_text))
        screen.blit(press_any_key_text, press_any_key_rect)

    elif current_state == character_selection_state:
        screen.blit(character_selection_background, character_selection_background_rect)
        screen.blit(character_selection, character_selection_rect)

        if selected_character:
            text_surface = font.render(f"Selected Character: {selected_character}", True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(screen_width // 2, screen_height - 50))
            screen.blit(text_surface, text_rect)

            continue_text_surface = font.render("Press Enter to Continue", True, (255, 255, 255))
            continue_text_rect = continue_text_surface.get_rect(center=(screen_width // 2, screen_height - 30))
            screen.blit(continue_text_surface, continue_text_rect)

    elif current_state == lee_description_state:
        screen.blit(lee_description_image, lee_description_rect)

    elif current_state == dialog_options_state:
        # Draw the dialog options scene with the background of "LeeHouse.png"
        screen.blit(lee_house_image, lee_house_rect)

        # Display the soldiers' dialog with an outline
        dialog_y = 200
        outline_color = (255, 0, 0)  # Red outline color

        soldiers_dialog = [
            "Hey, it's time for you to leave.",
            "You are being forced off this property by the Federal Government.",
            "Leave now and follow us."
        ]

        # Display the soldiers' dialog with an outline
        for line in soldiers_dialog:
            # Render the outline
            pos_dialog_outline = (screen_width // 2, dialog_y)
            render_text_with_outline(line, pos_dialog_outline, (255, 255, 255), (0, 0, 0), show_continue_text)

            dialog_y += 20

        # Display A, B, C options for the user
        options_text = "A. No   B. But I have family here, you cannot do this!   C. Ok"
        pos_options = (screen_width // 2, screen_height - 50)
        render_text_with_outline(options_text, pos_options, (255, 255, 255), (0, 0, 0), show_continue_text)

        # Process user choice
        if user_choice and show_continue_text:
            follow_up_text = None

            if user_choice == "a":
                follow_up_text = "Too bad, you are coming with us."
            elif user_choice == "b":
                follow_up_text = "I do not care who is here, this is a presidential order and you are leaving."
            elif user_choice == "c":
                follow_up_text = "Washington Lee was forcefully removed from his house in Georgia"

            # Display the follow-up text
            pos_follow_up = (screen_width // 2, dialog_y + 40)
            render_text_with_outline(follow_up_text, pos_follow_up, (255, 255, 255), (0, 0, 0))
        
    elif current_state == the_trail_state:
        screen.blit(caravan_image, caravan_rect)
        text_line1 = "Everyone had to walk except the elderly who were too weak; they rode in the caravans."
        text_line2 = "Press Enter to Continue"
        pos_line1 = (screen_width // 2, screen_height // 3)
        pos_line2 = (screen_width // 2, screen_height * 2 // 3)
        render_text_with_outline(text_line1, pos_line1, (255, 255, 255), (0, 0, 0))
        render_text_with_outline(text_line2, pos_line2, (255, 255, 255), (0, 0, 0))

    elif current_state == food_state:
        screen.blit(food_image, food_rect)
        text_food_line = "Your journey is long, and you need to find sustenance for your people."
        pos_food_line = (screen_width // 2, screen_height // 3)
        render_text_with_outline(text_food_line, pos_food_line, (255, 255, 255), (0, 0, 0))
        text_press_enter = "Press Enter to Continue"
        pos_press_enter = (screen_width // 2, screen_height * 2 // 3)
        render_text_with_outline(text_press_enter, pos_press_enter, (255, 255, 255), (0, 0, 0))

    elif current_state == buffalo_state:
        screen.blit(buffalo_image, buffalo_rect)

        if not buffalo_clicked:
            text_hunt_buffalo = "You Found a Buffalo! Hunt the Buffalo for Food"
            pos_hunt_buffalo = (screen_width // 2, screen_height // 3)
            render_text_with_outline(text_hunt_buffalo, pos_hunt_buffalo, (255, 255, 255), (0, 0, 0), show_continue_text)

        mouse_x, mouse_y = pygame.mouse.get_pos()
        click, _, _ = pygame.mouse.get_pressed()

        if buffalo_clicked and show_continue_text:
            outcome_text = "You successfully hunted a buffalo! Press Enter to Continue"
            pos_outcome = (screen_width // 2, screen_height // 2 + 100)
            render_text_with_outline(outcome_text, pos_outcome, (255, 255, 255), (0, 0, 0), show_continue_text)

        if not buffalo_clicked:
            text_hunt_buffalo = "You Found a Buffalo! Hunt the Buffalo for Food"
            pos_hunt_buffalo = (screen_width // 2, screen_height // 3)
            render_text_with_outline(text_hunt_buffalo, pos_hunt_buffalo, (255, 255, 255), (0, 0, 0), show_continue_text)
        else:
            outcome_text = "You successfully hunted a buffalo! Press Enter to Continue"
            pos_outcome = (screen_width // 2, screen_height // 2 + 100)
            render_text_with_outline(outcome_text, pos_outcome, (255, 255, 255), (0, 0, 0), show_continue_text)

        text_press_enter = "Press Enter to Continue"
        pos_press_enter = (screen_width // 2, screen_height - 30)
        render_text_with_outline(text_press_enter, pos_press_enter, (255, 255, 255), (0, 0, 0), show_continue_text)

        if buffalo_clicked and show_continue_text:
            user_choice = None
            show_continue_text = False
            follow_up_text = None  # Reset follow-up text
# Check for Enter key press or mouse click to transition to the next state
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            current_state = buffalo_state  # Replace with the state you want to transition to
            user_choice = None
            show_continue_text = False  # Add these lines to clear user_choice and hide continue text
            follow_up_text = None  # Reset follow-up text
        elif event.type == pygame.MOUSEBUTTONDOWN and buffalo_rect.collidepoint(event.pos):
            # Check if the mouse click is within the buffalo area
            buffalo_clicked = True
            user_choice = None
            show_continue_text = False  # Add these lines to clear user_choice and hide continue text
            follow_up_text = None  # Reset follow-up text

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
