from math import pi, sqrt, sin, asin, ceil
from random import shuffle
import sys

def change_to_letter(change):
    return ["D","I"][int(change)]

def create_visualization(step):
    letter = change_to_letter(step[2])
    guide = ["x"] * step[0]
    for change in step[1]:
        guide[change] = letter
    return "".join(guide)

def middle_helper(steps, change, last_change):
    n = change - last_change
    if n > 0:
        steps.append("{}x".format(n))

def create_guide(step):
    letter = change_to_letter(step[2])
    steps = []
    last_change = 0
    for change in step[1]:
        middle_helper(steps, change, last_change)
        steps.append(letter)
        last_change = change +1
    middle_helper(steps, step[0], last_change)
    return " ".join(steps)

def interactive(guide):
    ins = ""
    for letter in guide:
        ins += letter
        if ins[-1] == "D":
            yield ins
            ins = ""
    if ins != "":
        yield ins

if len(sys.argv) == 4:
    diameter = eval(sys.argv[1])
    stitch_width = eval(sys.argv[2])
    stitch_height = eval(sys.argv[3])
else:
    diameter = eval(input("diameter of the sphere in mm: "))
    print("you can also enter a fraction like 25/4 if 4 stitches equal 25 mm")
    stitch_width = eval(input("width per stitch in mm: "))
    stitch_height = eval(input("height per stitch in mm: "))

n_rows = round((pi / (asin(stitch_height/diameter)))/2)
diameter = 2 * stitch_height / (2*sin(pi/(n_rows*2)))
print("number of rows: {}".format(n_rows))
radius = diameter/2

angle = pi/(n_rows)

def calc_rows(i = 0, current_height = 0, rows = []):
    if i < n_rows:
        my_angle = angle * i + (angle/2)
        my_height = sin(my_angle) * stitch_height
        my_pos = (current_height + (my_height/2))
        dist_from_cent = abs(radius - my_pos)
        circumfrence = pi * 2 * sqrt(radius**2 - (dist_from_cent)**2)
        rows.append(round(circumfrence/stitch_width))
        return calc_rows(i+1, current_height + my_height, rows)
    else:
        return rows

stitches_per_row = calc_rows()

print("acutal resulting height and width: {:.2f} mm, {:.2f} mm".format(diameter, ((max(stitches_per_row)*stitch_width)/pi)))


def shift(stitches, changes, amount):
    result = [(change + amount) % stitches for change in changes]
    result.sort()
    return result

def convert_change_pos(row_guide):
    stitches = row_guide[0]
    change_pos = [change/stitches for change in row_guide[1]]
    return change_pos

def eval_change_pos(prev_row_guide, row_guide):
    score = 0
    if prev_row_guide[1]:
        prev_row = convert_change_pos(prev_row_guide)
        prev_row = [prev_row[-1]-1] + prev_row + [prev_row[0]+1]
        row = convert_change_pos(row_guide)
        score = 0
        for stitch in row:
            neighbor = [-1,-1]
            for prev_s in prev_row:
                if prev_s < stitch:
                    if prev_s > neighbor[0]:
                        neighbor[0] = prev_s
                elif prev_s == stitch:
                    neighbor[0] = prev_s
                    neighbor[1] = prev_s
                    break
                else:
                    neighbor[1] = prev_s
                    break
            distances = [(stitch - neighbor[0]), (neighbor[1] - stitch)]
            score += min(distances)
    return score

row_guide = [(0,[], True)]

for stitches in stitches_per_row:
    prev_row_stitches = row_guide[-1][0]
    prev_row_changes = row_guide[-1][1]
    stitch_difference = stitches - prev_row_stitches
    is_increase = stitch_difference >= 0
    stitch_difference = abs(stitch_difference)
    if stitch_difference > 0:
        spaceing = stitches / stitch_difference

        changes = [round(i * spaceing) for i in range(stitch_difference)]

        best_score = -2
        best = None
        shuffled_range = list(range(stitches))
        shuffle(shuffled_range)
        for i in shuffled_range:
            option = shift(stitches, changes, i)
            score = eval_change_pos(row_guide[-1], (stitches, option))
            if score > best_score:
                best_score = score
                best = option
        row_guide.append((stitches, best, is_increase))
    else:
        row_guide.append((stitches, [], True))

row_guide.pop(0)

for row in row_guide:
    print("Row {}, {} stitches: {}".format(row_guide.index(row)+1, row[0], create_guide(row)))
