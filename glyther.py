import random
from dataclasses import dataclass
from PIL import Image, ImageDraw
import settings as s
import math
import numpy as np
# import matplotlib


def glyth_formation(img: Image, number_list: list, color_list: list) -> Image:
    """
    Basic glyth formation to add to an image.
    """
    name: str
    filter_function: callable
    w, h = img.size
    draw = ImageDraw.Draw(img)
    print((w, h), number_list, color_list)
    for i in range(number_list[9]):
        draw.line((w // (i+1), h // (i+1)), fill="blue", width=6)
    return img


def plan_angled_line(x, y, angle, length, width, color, img_size):
    """
    Plan a line's properties.

    @param img_size: Size of image to keep drawing in bounds.
    @param color: color of the line
    @param x: start x position
    @param y: start y position
    @param angle: angle to draw line
    @param length: length of line to draw
    @param width: thickness of line
    @return:
    """
    endx1 = x
    # endx1 = x + length * math.cos(math.radians(angle))
    endy1 = y
    # endy1 = y + length * math.sin(math.radians(angle))
    print('x:', x)
    endx2 = x + length * math.cos(math.radians(angle + 180)) * -1
    endy2 = y + length * math.sin(math.radians(angle + 180)) * -1
    return (s.clamp(endx1, 0, img_size[0]),
            s.clamp(endy1, 0, img_size[1]),
            s.clamp(endx2, 0, img_size[0]),
            s.clamp(endy2, 0, img_size[1])), width, color


def lsystem_string_maker(axioms: str, rules: dict, iterations: int) -> str:
    for _ in range(iterations):
        new_axioms = ''
        for axiom in axioms:
            if axiom in rules:
                new_axioms += rules[axiom]
            else:
                new_axioms += axiom
            axioms = new_axioms
        print(new_axioms)
    return axioms


def lsystem_rule_parser(lstring: str, start_point=(320, 320),
                        start_length=32, start_width=1, start_color=s.ORANGE) -> dict:
    """
    Takes an L-system string and creates a dictionary of line drawers.
    :param start_length:
    :param start_color:
    :param start_point:
    :param start_width:
    :param lstring:
    :return:
    """
    angle = 0
    length = start_length
    w, h = (640, 640)
    width = start_width
    color = start_color
    prev_line_tup = ((start_point[0], start_point[1], 550, 420), width, color)
    # point_list = [prev_line_tup]
    line_points_dict = {
        "main": [prev_line_tup]
    }
    for c in lstring:
        if s.ALPHANUMERIC_RULES[c.lower()].startswith("ANGLE"):
            angle += int(s.ALPHANUMERIC_RULES[c.lower()].split("ANGLE")[1])
            angle = s.clamp(angle, -360, 360)
        if s.ALPHANUMERIC_RULES[c.lower()].startswith("LINE"):
            length = int(s.ALPHANUMERIC_RULES[c.lower()].split("LINE")[1])
        if s.ALPHANUMERIC_RULES[c.lower()].startswith("FORWARD"):
            length += int(s.ALPHANUMERIC_RULES[c.lower()].split("FORWARD")[1])
        if s.ALPHANUMERIC_RULES[c.lower()].startswith("THICK"):
            width += int(s.ALPHANUMERIC_RULES[c.lower()].split("THICK")[1])
        if s.ALPHANUMERIC_RULES[c.lower()].startswith("THIN"):
            width += int(s.ALPHANUMERIC_RULES[c.lower()].split("THIN")[1])
        if s.ALPHANUMERIC_RULES[c.lower()].startswith("PUSH"):
            line_points_dict[str(len(line_points_dict))] = []
        if s.ALPHANUMERIC_RULES[c.lower()].startswith("POP"):
            pass
        line_tup = plan_angled_line(prev_line_tup[0][2], prev_line_tup[0][3],
                                    angle, length, width,
                                    color, (w, h))
        line_points_dict["main"].append(line_tup)
        prev_line_tup = line_tup
    return line_points_dict


# def lsystem_rule_parser(lstring: str, start_tup=((320, 320, 320, 320), 1, ORANGE)) -> list:
#     """
#     Takes an L-system string and creates a dictionary of line drawers.
#     :param lstring:
#     :param start_tup:
#     :return:
#     """
#     angle = 0
#     length = start_tup[0][2]
#     w, h = (start_tup[0][2] * 128, start_tup[0][3] * 2)
#     width = 1
#     prev_line_tup = start_tup
#     point_list = [prev_line_tup]
#     for c in lstring:
#         if ALPHANUMERIC_RULES[c.lower()].startswith("ANGLE"):
#             angle += int(ALPHANUMERIC_RULES[c.lower()].split("ANGLE")[1])
#             angle = s.clamp(angle, -360, 360)
#             print(f"New angle: {angle}")
#         if ALPHANUMERIC_RULES[c.lower()].startswith("LINE"):
#             length = int(ALPHANUMERIC_RULES[c.lower()].split("LINE")[1])
#             print(f"New length: {length}")
#         if ALPHANUMERIC_RULES[c.lower()].startswith("FORWARD"):
#             length += int(ALPHANUMERIC_RULES[c.lower()].split("FORWARD")[1])
#             print(f"New length: {length}")
#         if ALPHANUMERIC_RULES[c.lower()].startswith("THICK"):
#             width += int(ALPHANUMERIC_RULES[c.lower()].split("THICK")[1])
#             print(f"New width: {width}")
#         if ALPHANUMERIC_RULES[c.lower()].startswith("THIN"):
#             width += int(ALPHANUMERIC_RULES[c.lower()].split("THIN")[1])
#             print(f"New width: {width}")
#         if ALPHANUMERIC_RULES[c.lower()].startswith("PUSH"):
#             pass
#         if ALPHANUMERIC_RULES[c.lower()].startswith("POP"):
#             pass
#         line_tup = plan_angled_line(prev_line_tup[0][0], prev_line_tup[0][1],
#                                     angle, length, prev_line_tup[1],
#                                     prev_line_tup[2], (w, h))
#         point_list.append(line_tup)
#         prev_line_tup = line_tup
#     print("POINTLIST")
#     for point in point_list:
#         print(point)
#     return point_list


def segmented_line_run(start_len: int, seg_diff: int, direction_list: list, start_pos=(320, 320), rando=False) -> list:
    point_list = [start_pos]
    prev_point = start_pos
    seg_length = start_len
    if rando:
        random.shuffle(direction_list)
    for direction in direction_list:
        next_point = (prev_point[0] + (direction[0] * seg_length), prev_point[1] + (direction[1] * seg_length))
        point_list.append(next_point)
        prev_point = next_point
        seg_length += seg_diff
    return point_list


def boxline(img: Image, kre8dict: dict) -> Image:
    nl = kre8dict["number_list"]
    cl = kre8dict["color_list"]
    w, h = img.size
    draw = ImageDraw.Draw(img)
    start_point = (w // 2, h // 2)
    box_line_dir_list = [
        (-1, 0), (0, 1), (-1, 0),
        (0, 1), (1, 0), (0, -1),
        (-1, 0), (0, 1), (-1, 0),
        (1, 0), (0, 1), (-1, 0),
        (0, -1), (1, 0), (0, 1),
        (1, 0), (1, 0), (1, 0),
        (1, 0), (0, -1), (1, 0),
        (0, 1), (0, 1), (0, 1),
        (-1, 0), (0, -1), (-1, 0),
        (0, 1), (0, 1), (-1, 0),
        (0, -1), (-1, 0), (0, 1),
        (0, 1), (0, 1), (-1, 0)
    ]
    # end_point_list = segmented_line_run(64, 4, box_line_dir_list, start_pos=start_point, rando=True)
    end_point_list = segmented_line_run(w // 10, random.randint(-20, 20), box_line_dir_list, start_pos=start_point,
                                        rando=True)
    prev_point = start_point
    for point in end_point_list:
        draw.line((prev_point, point), fill=random.choice(cl), width=random.choice(nl))
        prev_point = point
    return img


def dummy(img: Image, kre8dict: dict) -> Image:
    nl = kre8dict["number_list"]
    cl = kre8dict["color_list"]
    draw = ImageDraw.Draw(img)
    for rad in nl:
        draw.regular_polygon([64 * rad, 64 * rad, rad + random.choice(nl) + 1 * 64], random.choice(nl) + 3,
                             random.choice(nl) * 36, outline=random.choice(nl), fill=random.choice(cl))
    return img


# def bare_bones(img: Image, kre8dict: dict) -> Image:
#     nl = kre8dict["number_list"]
#     cl = kre8dict["color_list"]
#     draw = ImageDraw.Draw(img)
#     w, h = img.size
#     # print(type(mujic.get_sin_wave(60)))
#     draw.line((2, 4, 90, 60))
#     # for spot in mujic.get_chirp(60):
#     #     print(spot)
#     #     rani = random.choice(nl)
#     #     draw.line((spot*rani, -spot*rani), fill=random.choice(cl))
#     return img


def squiggle_xy(a, b, c, d):
    i = np.arange(0.0, 2 * np.pi, 0.05)
    return np.sin(i * a) * np.cos(i * b), np.sin(i * c) * np.cos(i * d)


# def bare_bones(img: Image, kre8dict: dict) -> Image:
#     nl = kre8dict["number_list"]
#     cl = kre8dict["color_list"]
#     t = np.linspace(0, 10, 100*random.choice(nl))
#     # p = np.poly1d([-0.03, -1.6, 1.25, -8.0, -2.1, 4.2, 6.9])
#     p_list = []
#     colo = random.choice(cl)
#     for i in nl:
#         p_list.append((random.random()*i) * random.randint(-1, 1))
#     p = np.poly1d(p_list)
#     # w = signal.chirp(t, f0=nl[0], f1=nl[9], t1=nl[9], method='quadratic')
#     w = signal.sweep_poly(t, p)
#     # fig = plt.figure(figsize=(6, 6), facecolor=(DRS_PURPLE[0] / 255, DRS_PURPLE[1] / 255, DRS_PURPLE[2] / 255))
#     fig = plt.figure(figsize=(10, 8), facecolor=(colo[0] / 255, colo[1] / 255, colo[2] / 255))
#     plt.plot(t, w, random.choice(RANDOM_COLOR_STR_LIST))
#     plt.axis('off')
#     plt.savefig("img_buf.png", format='png')
#     draw = ImageDraw.Draw(img)

    img_buf = Image.open("img_buf.png")
    img.paste(img_buf, (-192, -80))
    # plt.title("Linear Chirp, f(0)=6, f(10)=1")
    # plt.xlabel('t (sec)')
    # plt.show()
    return img


def weird_stuff(img: Image, kre8dict: dict) -> Image:
    fig = plt.figure(figsize=(8, 8))
    outer_grid = fig.add_gridspec(4, 4, wspace=0, hspace=0)
    nl = kre8dict["number_list"]

    for a in range(4):
        for c in range(4):
            # gridspec inside gridspec
            inner_grid = outer_grid[a, c].subgridspec(3, 3, wspace=0, hspace=0)
            axs = inner_grid.subplots()  # Create all subplots for the inner grid.
            for (b, d), ax in np.ndenumerate(axs):
                ax.plot(*squiggle_xy((random.choice(nl) % 4) + 1, (random.choice(nl) % 4) + 1,
                                     (random.choice(nl) % 4) + 1, (random.choice(nl) % 4) + 1))
                ax.set(xticks=[], yticks=[])

    # show only the outside spines
    for ax in fig.get_axes():
        ss = ax.get_subplotspec()
        ax.spines.top.set_visible(ss.is_first_row())
        ax.spines.bottom.set_visible(ss.is_last_row())
        ax.spines.left.set_visible(ss.is_first_col())
        ax.spines.right.set_visible(ss.is_last_col())
    plt.show()


def flame(img: Image, kre8dict: dict) -> Image:
    """
    Glyth image that looks a bit like flames.
    """
    nl = kre8dict["number_list"]
    cl = kre8dict["color_list"]
    draw = ImageDraw.Draw(img)
    w, h = img.size
    for x in range(w):
        for y in range(h):
            if 128 > x > 32 or 256 > y > 16:
                draw.line((x + x, y * 3, 320 - y, 144 + x), random.choice(cl), random.choice(nl))
            if x == 32:
                draw.point((x, 180), random.choice(cl))
    return img


def slanters(img: Image, kre8dict: dict) -> Image:
    """
    Glyth image that looks a bit like flames.
    """
    nl = kre8dict["number_list"]
    cl = kre8dict["color_list"]
    draw = ImageDraw.Draw(img)
    pixel_num_list = []
    w, h = img.size
    for x in range(w):
        pixel_num_list.append([])
        for y in range(h):
            pixel_num_list[x].append([(x, y), random.choice(nl)])
    starting_list = random.choice(pixel_num_list)
    starting_color = random.choice(cl)
    print(starting_list)
    for lyst in starting_list:
        draw.point((lyst[0][0], lyst[0][1]), fill=starting_color)
        for i in range(1):
            colo = random.choice(cl)
            draw.line((lyst[0][0], lyst[0][1],
                       (lyst[0][0] + (lyst[1] * w // 20) * random.randint(-1, 1)),
                       (lyst[0][1] + (lyst[1] * h // 20) * random.randint(-1, 1))),
                      fill=colo,
                      width=s.clamp(lyst[1], 1, 4))
    return img


def grid(img: Image, kre8dict: dict) -> Image:
    nl = kre8dict["number_list"]
    cl = kre8dict["color_list"]
    w, h = img.size
    draw = ImageDraw.Draw(img)
    grid_size = 16
    for x in range(0, w + grid_size, grid_size):
        for y in range(0, h + grid_size, grid_size):
            draw.line((x, 0, x, h), fill=s.WHITE_SMOKE)
            draw.line((0, y, w, y), fill=s.WHITE_SMOKE)
    return img


def llines(img: Image, kre8dict: dict) -> Image:
    """
    Draw a glyph image that looks a bit like flames.
    """
    nl = kre8dict["number_list"]
    cl = kre8dict["color_list"]
    draw = ImageDraw.Draw(img)
    w, h = img.size
    prev_point = (w // 2, h // 2, w // 128, h // 2)
    prev_width = 1
    prev_color = (0, 0, 0)
    rooz = lsystem_string_maker(kre8dict['use_id'], s.ALPHANUMERIC_AXIOMS, 4)
    roost = lsystem_rule_parser(rooz)
    for roo in roost["main"]:
        point = (roo[0][0], roo[0][1], roo[0][2], roo[0][3])
        width = roo[1]
        color = roo[2]
        print(color)
        draw.line(point, fill=color, width=width)
        draw.line((point[2], point[3], prev_point[1], prev_point[0]), fill=prev_color, width=prev_width)
        draw.line((point[0], point[1], prev_point[0], prev_point[1]), fill=prev_color, width=prev_width)
        prev_point = point
        prev_width = width
        prev_color = color
    return img


def circle_grow(img: Image, kre8dict: dict) -> Image:
    """
    Makes a circle and enlarges it.
    """
    nl = random.choices(kre8dict["number_list"], k=8)
    cl = random.choices(kre8dict["color_list"], k=8)
    draw = ImageDraw.Draw(img)
    w, h = img.size
    for i in range(1, 9):
        offset = i * 32
        if w - offset <= offset or h - offset <= offset:
            break
        ellipse_coordinates = (offset, offset, w - offset, h - offset)
        draw.ellipse(ellipse_coordinates, outline=cl[i - 1], width=nl[i - 1])
    return img


def box_grow(img: Image, kre8dict: dict) -> Image:
    """
    Draws a series of concentric squares on the given image, with randomly
    chosen colors and line thickness.
    """
    number_list = kre8dict.get("number_list", [10])
    color_list = kre8dict.get("color_list", ["black"])
    draw = ImageDraw.Draw(img)
    width, height = img.size
    for i in range(number_list[9]):
        x = (i * 64) // 2 + 32
        draw.rectangle((width // 2 - x, height // 2 - x, width // 2 + x, height // 2 + x),
                       outline=random.choice(color_list),
                       # fill=random.choice(color_list),
                       width=random.choice(number_list))
    return img


def spell_circle(img: Image, kre8dict: dict) -> Image:
    """
    Shapes on shapes to make a circle for casting spells.
    """
    nl = kre8dict["number_list"]
    cl = kre8dict["color_list"]
    new_img = img
    draw = ImageDraw.Draw(img)
    use_cl = []
    for colo in cl:
        co0 = int(colo[0] * 255)
        co1 = int(colo[1] * 255)
        co2 = int(colo[2] * 255)
        use_cl.append((co0, co1, co2))
    for i in range(nl[9]):
        draw.regular_polygon((img.size[0] // 2, img.size[1] // 2, img.size[1] // 8), (nl[9] - i + 3),
                             fill=random.choice(kre8dict["color_list"]), outline=random.choice(kre8dict["color_list"]))
    return new_img


def ripples(img: Image, kre8dict: dict) -> Image:
    """
    Circles that get bigger or smaller and travel in a direction.
    "system32.eth suggests bigger circles"
    """
    nl = kre8dict["number_list"]
    cl = kre8dict["color_list"]
    w, h = img.size
    draw = ImageDraw.Draw(img)
    for i in range(10):
        num_sides = s.clamp(random.choice(nl), 3, 9)
        poly_list = s.polypointlist(num_sides, 0, 2 * (w // 7), i * (h // 10), 16)
        poly_list2 = s.polypointlist(num_sides, 0, 3 * (w // 7), i * (h // 10), 16)
        poly_list3 = s.polypointlist(num_sides, 0, 4 * (w // 7), i * (h // 10), 16)
        for point in poly_list:
            draw.ellipse((point[0], point[1], (point[0] + i * 3, point[1] + i * 3)),
                         width=random.choice(nl), fill=random.choice(cl))
        for point in poly_list2:
            draw.ellipse((point[0], point[1], (point[0] + i * 3, point[1] + i * 3)),
                         width=random.choice(nl), fill=random.choice(cl))
        for point in poly_list3:
            draw.ellipse((point[0], point[1], (point[0] + i * 3, point[1] + i * 3)),
                         width=random.choice(nl), fill=random.choice(cl))
    return img


def confetti(img: Image, kre8dict: dict) -> Image:
    """
    Confetti from a parade or something.
    """
    nl = kre8dict["number_list"]
    cl = kre8dict["color_list"]
    draw = ImageDraw.Draw(img)
    for i in range(nl[9] * nl[8]):
        start_pos = (random.randint(0, img.size[0]), random.randint(0, img.size[1]))
        random_factor = random.randint(-1, 1)
        # shape = [(12*random_factor, 12*random.randint(-3, 6)), (-12*random_factor, 12*random.randint(-3, 6)),
        #          (12*random_factor, -12*random.randint(-3, 6)), (-12*random_factor, -12*random.randint(-3, 6))]
        shape = [(12 * random_factor, 12 * random.randint(-1, 1)), (-12 * random_factor, 12 * random.randint(-1, 1)),
                 (12 * random_factor, -12 * random.randint(-1, 1)), (-12 * random_factor, -12 * random.randint(-1, 1))]
        shaped = []
        for point in shape:
            shaped.append((start_pos[0] + point[0], start_pos[1] + point[1]))
        draw.regular_polygon((start_pos[0], start_pos[1], 16), random.choice(nl) + 3,
                             outline=random.choice(cl), fill=random.choice(cl))
        draw.polygon(shaped, fill=random.choice(cl))
    return img


def julia_filter(img: Image, kre8dict: dict) -> Image:
    width, height = img.size
    rgb_img = img.convert('RGB')
    draw = ImageDraw.Draw(img)
    nl = kre8dict["number_list"]
    cl = kre8dict["color_list"]
    # center_point = (320, 320)
    center_point = (nl[0] * 64, nl[0] * 64)
    base_color = random.choice(cl)

    for x in range(0, width):
        for y in range(0, height):
            r, g, b = rgb_img.getpixel((x, y))
            if x >= center_point[0]:
                r = 255 - r
                g = 255 - g
                b = 255 - b
            if x < center_point[0]:
                r = r % (x + 1)
                g = g % (x + 1)
                b = b % (x + 1)
            if y >= center_point[1]:
                r = r % (y + 1)
                g = g % (y + 1)
                b = b % (y + 1)
            if y < center_point[1]:
                r += r % 255
                g += g % 255
                b += b % 255
            use_color = (r, g, b)
            draw.point((x, y), use_color)
    return img


def erik_filter(img: Image, kre8dict: dict) -> Image:
    width, height = img.size
    rgb_img = img.convert('RGB')
    draw = ImageDraw.Draw(img)
    nl = kre8dict["number_list"]
    cl = kre8dict["color_list"]
    # center_point = (320, 320)
    center_point = (nl[0] * 64, nl[0] * 64)
    base_color = random.choice(cl)

    for x in range(0, width):
        nx = x
        for y in range(0, height):
            ny = y
            r, g, b = rgb_img.getpixel((x, y))
            if r > 155:
                nx *= nl[2]
                ny += nl[0]
            if g > 155:
                nx += nl[1]
                ny *= nl[2]
            if b > 155:
                nx *= nl[0]
                ny += nl[1]
            # if x == center_point[0]:
            #     r = 255
            #     g = 255
            #     b = 255
            # if y == center_point[1]:
            #     r = r % (y + 1)
            #     g = g % (y + 1)
            #     b = b % (y + 1)
            nx -= nl[5]
            ny -= nl[5]
            use_color = (r, g, b)
            draw.point((s.clamp(nx, 0, width),
                        s.clamp(ny, 0, height)), use_color)
    return img

# def julia_generate(img: Image, kre8dict: dict) -> Image:
#     cl = kre8dict["color_list"]
#     xa = -2.0
#     xb = 1.0
#     ya = -1.5
#     yb = 1.5
#     max_it = 128
#     w, h = img.size
#     draw = ImageDraw.Draw(img)
#     c = complex(random.random() * 2.0 - 1.0, random.random() - 0.5)
#     for y in range(h):
#         zy = y * (yb - ya) / (h - 1) + ya
#         for x in range(w):
#             zx = x * (xb - xa) / (w - 1) + xa
#             z = complex(zx, zy)
#             for i in range(max_it):
#                 if abs(z) > 2.0:
#                     break
#                 z = z * z + c
#             r = i % 4 * 32
#             g = i % 8 * 32
#             b = i % 16 * 16
#             draw.point((x, y), fill=(r, g, b))
#     return img


def squiggles(img: Image, kre8dict: dict) -> Image:
    """
    Using sin and cos waves make some squiggly squiggles.
    """
    nl = kre8dict["number_list"]
    cl = kre8dict["color_list"]
    draw = ImageDraw.Draw(img)
    w, h = img.size
    center = h // 2
    x_increment = random.choice(nl) + 2
    # WIDTH STRETCH
    x_factor = random.choice(nl)
    # HEIGHT STRETCH
    y_amplitude = random.randint(-10, 10)
    lt = random.choice(nl)
    if lt == 0:
        lt += 1
    sine_list = []
    for y in range(-15, 15):
        for x in range(-h, h):
            y_amplitude += .001 * lt
            sine_list.append(x * x_increment)
            sine_list.append(int(math.cos(x * x_factor) * y_amplitude) + center)
            # sine_list.append(int(math.sin(x * x_factor) * y_amplitude) + center)
        draw.line(sine_list, random.choice(cl))
    return img


def circle_shapes(img: Image, kre8dict: dict) -> Image:
    """
    Shapes with a hint of circles about it.
    """
    nl = kre8dict["number_list"]
    cl = kre8dict["color_list"]
    draw = ImageDraw.Draw(img)
    for i in range(10):
        starter = random.choice(nl)
        ended = random.choice(nl)
        draw.arc([(0, 0), (img.size[0] // 2, img.size[1] // 2)],
                 start=starter, end=ended, fill=random.choice(cl),
                 width=random.choice(nl))
        draw.arc([(img.size[0] // 2, img.size[1] // 2), (img.size[0], img.size[1])],
                 start=starter, end=ended, fill=random.choice(cl),
                 width=random.choice(nl))
        draw.arc([(0, 0), (img.size[0], img.size[1])],
                 start=starter, end=ended, fill=random.choice(cl),
                 width=random.choice(nl))
    return img


def lightning(img: Image, kre8dict: dict) -> Image:
    """
    Glyther will look like a lightning bolt.
    """
    nl = kre8dict["number_list"]
    cl = kre8dict["color_list"]
    draw = ImageDraw.Draw(img)
    dir_list = []
    w, h = img.size
    for _ in range(16):
        dir_list.append((random.randint(-1, 1), 1))
    end_point_list = segmented_line_run(32, 1, direction_list=dir_list, start_pos=(w // 2, 0))
    prev_point = (w // 2, 0)
    lightning_path = lsystem_string_maker(kre8dict["use_id"], s.ALPHANUMERIC_AXIOMS, 3)
    print(cl, nl)
    for point in end_point_list:
        # ranxy = random.randint(nl[0], nl[9]) * 64
        draw.line((prev_point, point), fill=random.choice(cl), width=random.choice(nl))
        prev_point = point
        static_dir_list = []
        lightning_point_list = []
        for st in kre8dict["use_id"]:
            static_dir_list.append((random.randint(-1, 1), random.randint(-1, 1)))
            # lightning_point_list = segmented_line_run(3, 1, direction_list=static_dir_list)
            if st.lower() in s.ALPHANUMERIC_COORDS:
                lightning_point_list.append(((random.choice(s.ALPHANUMERIC_COORDS[st.lower()])[0]) + point[0],
                                             (random.choice(s.ALPHANUMERIC_COORDS[st.lower()])[1]) + point[1]))
            else:
                lightning_point_list.append(((random.choice(s.PUNCTUATION_COORDS[st.lower()])[0]) + point[0],
                                             (random.choice(s.PUNCTUATION_COORDS[st.lower()])[1]) + point[1]))
            for lpoint in lightning_point_list:
                draw.line((prev_point, lpoint), fill=random.choice(cl), width=random.choice(nl))
                prev_point = lpoint

        # for s in lightning_path:
        #     lightning_point_list.append(((random.choice(s.ALPHANUMERIC_COORDS[s])[0]) + point[0],
        #                                  (random.choice(s.ALPHANUMERIC_COORDS[s])[1]) + point[1]))
    return img


def pikupstix(img: Image, kre8dict: dict) -> Image:
    """
    Almost looks like a game of pick-up-sticks.
    @param img:
    @param kre8dict:
    @return:
    """
    nl = kre8dict["number_list"]
    cl = kre8dict["color_list"]
    draw = ImageDraw.Draw(img)
    for i in range(nl[9] + nl[7]):
        draw.line((random.randint(nl[0], nl[9]) * 64,
                   random.randint(nl[0], nl[9]) * 64,
                   random.randint(nl[0], nl[9]) * 64,
                   random.randint(nl[0], nl[9]) * 64), fill=random.choice(cl), width=random.choice(nl))
    return img


# def create_avatar(img: Image, kre8dict: dict) -> Image:
#     for glyth_option in kre8dict["Glyth"]["Avatar"]:
#         if glyth_option == "Box Lines":
#             boxline(img, kre8dict)
#         if glyth_option == "Circle Shapes":
#             circle_shapes(img, kre8dict)
#         if glyth_option == "Lightning":
#             lightning(img, kre8dict)
#         if glyth_option == "Squiggles":
#             squiggles(img, kre8dict)
#         if glyth_option == "Confetti":
#             confetti(img, kre8dict)
#         if glyth_option == "Ripples":
#             ripples(img, kre8dict)
#         if glyth_option == "Spell Circle":
#             spell_circle(img, kre8dict)
#         if glyth_option == "Spider Web":
#             spider_web(img, kre8dict)
#         if glyth_option == "Box Grow":
#             box_grow(img, kre8dict)
#         if glyth_option == "Circle Grow":
#             circle_grow(img, kre8dict)
#         if glyth_option == "Rooster":
#             llines(img, kre8dict)
#     return img


def spider_web(img: Image, kre8dict: dict) -> Image:
    nl = kre8dict["number_list"]
    cl = kre8dict["color_list"]
    w, h = img.size
    draw = ImageDraw.Draw(img)
    point_list_1 = []
    point_list_2 = []
    for i in range(0, w + (w // 4), w // 4):
        for j in range(0, h + (h // 4), h // 4):
            point_list_1.append((i, j))
            point_list_2.append((i, j))
    # rainbow_rgb_list = [RED, ORANGE, YELLOW, GRREEN, BLUE, INDIGO, VIOLET]
    for point in point_list_1:
        for point2 in point_list_2:
            draw.line((point[0], point[1], point2[0], point2[1]), width=random.choice(nl),
                      fill=random.choice(cl))
    return img

#
# def lsystem(axioms: str, rules: dict, iterations: int) -> str:
#     for _ in range(iterations):
#         new_axioms = ''
#         for axiom in axioms:
#             if axiom in rules:
#                 new_axioms += rules[axiom]
#             else:
#                 new_axioms += axiom
#             axioms = new_axioms
#         return axioms


# def mandelbrot_generate(self, oi):
#     # xa = -2.0
#     # xb = 1.0
#     # ya = -1.5
#     # yb = 1.5
#     xa = random.randint(0, oi) * .1
#     xb = random.randint(0, oi) * .1
#     ya = random.randint(0, oi) * .1
#     yb = random.randint(0, oi) * .1
#     # xa = random.randint(-oi, oi) * .1
#     # xb = random.randint(-oi, oi) * .1
#     # ya = random.randint(-oi, oi) * .1
#     # yb = random.randint(-oi, oi) * .1
#     print(f'{oi}XABY   {xa} | {xb} | {ya} | {yb}')
#     max_it = 256
#     imgx = 64
#     imgy = 64
#     imaje = Image.new("RGB", (imgx, imgy))
#     for y in range(imgy):
#         cy = y * (yb - ya) / (imgy - 1) + ya
#         for x in range(imgx):
#             cx = x * (xb - xa) / (imgx - 1) + xa
#             # cx = x * (xa + xb) / (imgy - 1) + xb
#             c = complex(cx, cy)
#             z = 0
#             for i in range(max_it):
#                 if abs(z) > 2.0:
#                     break
#                 z = z * z + c
#             r = i % 4 * 64
#             g = i % 8 * 32
#             b = i % 16 * 16
#             imaje.putpixel((x, y), b * 65536 + g * 256 + r)
#     imaje.save(f"KINVOW/Mandel_{self.use_data_dict['use_ID']}.png", "PNG")
#
# def julia_generate(self):
#     xa = -2.0
#     xb = 1.0
#     ya = -1.5
#     yb = 1.5
#     max_it = 128
#     imgx = 640
#     imgy = 640
#     imaje = Image.new("RGB", (imgx, imgy))
#     c = complex(random.random() * 2.0 - 1.0, random.random() - 0.5)
#     for y in range(imgy):
#         zy = y * (yb - ya) / (imgy - 1) + ya
#         for x in range(imgx):
#             zx = x * (xb - xa) / (imgx - 1) + xa
#             z = complex(zx, zy)
#             for i in range(max_it):
#                 if abs(z) > 2.0:
#                     break
#                 z = z * z + c
#             r = i % 4 * 32
#             g = i % 8 * 32
#             b = i % 16 * 16
#             imaje.putpixel((x, y), b * 65536 + g * 256 + r)
#     imaje.save(f"KINVOW/Julia_{self.use_data_dict['use_ID']}.png", "PNG")