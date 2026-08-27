import csv
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


# ==================================================
# SETTINGS
# ==================================================

CAUTION_DEPTH = -80
WARNING_DEPTH = -50
DANGER_DEPTH = -20

# Minimum increase in depth value considered rapid
RAPID_CHANGE = 50

# Used to detect unusual sensor readings
OUTLIER_THRESHOLD = 100

# Distance from the shallowest depth used
# to define the shallow-water zone
SHALLOW_ZONE_RANGE = 20

# Number of readings used to reduce random noise
SMOOTHING_WINDOW = 5


# ==================================================
# READ CSV DATA
# ==================================================

depth_data = []
invalid_points = []

with open("Depth Data.csv", "r") as file:

    reader = csv.DictReader(file)

    for row in reader:

        raw_depth = row["Depth (m)"]

        try:

            depth = float(raw_depth)

            depth_data.append(
                (int(row["Point"]), depth)
            )

        except ValueError:

            invalid_points.append(
                int(row["Point"])
            )


# ==================================================
# FIND SUSPICIOUS READINGS
# ==================================================

suspicious_points = []

for i in range(1, len(depth_data) - 1):

    point = depth_data[i][0]
    depth = depth_data[i][1]

    previous_depth = depth_data[i - 1][1]
    next_depth = depth_data[i + 1][1]

    difference_previous = abs(
        depth - previous_depth
    )

    difference_next = abs(
        depth - next_depth
    )

    # A reading very different from both
    # neighboring readings is suspicious.

    if (
        difference_previous > OUTLIER_THRESHOLD
        and difference_next > OUTLIER_THRESHOLD
    ):

        suspicious_points.append(point)


# ==================================================
# REMOVE SUSPICIOUS READINGS
# ==================================================

clean_data = []

for point, depth in depth_data:

    if point not in suspicious_points:

        clean_data.append(
            (point, depth)
        )


# ==================================================
# REDUCE RANDOM SENSOR NOISE
# USING A MOVING AVERAGE
# ==================================================

smoothed_data = []

for i in range(len(clean_data)):

    # Find the beginning of the current
    # smoothing window.

    start = max(
        0,
        i - SMOOTHING_WINDOW + 1
    )

    # Get the depth values inside
    # the current window.

    window = [
        depth
        for point, depth
        in clean_data[start:i + 1]
    ]

    # Calculate the average depth
    # of the current window.

    average_depth = sum(window) / len(window)

    # Store the point number and
    # smoothed depth.

    smoothed_data.append(
        (
            clean_data[i][0],
            average_depth
        )
    )


# ==================================================
# FIND SHALLOWEST POINT
# ==================================================

shallowest_point = max(
    clean_data,
    key=lambda x: x[1]
)

shallowest_depth = shallowest_point[1]


# ==================================================
# FIND SHALLOWEST ZONE
# ==================================================

shallow_zone = []

for point, depth in clean_data:

    # Distance from the shallowest depth

    distance_from_shallowest = abs(
        depth - shallowest_depth
    )

    if distance_from_shallowest <= SHALLOW_ZONE_RANGE:

        shallow_zone.append(
            (point, depth)
        )


# ==================================================
# DETERMINE FINAL SAFETY STATUS
# ==================================================

if shallowest_depth > DANGER_DEPTH:

    final_status = "DANGER"

    action = (
        "STOP and change course immediately."
    )

elif shallowest_depth > WARNING_DEPTH:

    final_status = "WARNING"

    action = (
        "Reduce speed and prepare to change course."
    )

elif shallowest_depth > CAUTION_DEPTH:

    final_status = "CAUTION"

    action = (
        "Monitor depth closely."
    )

else:

    final_status = "SAFE"

    action = (
        "Continue navigation."
    )


# ==================================================
# CHECK FOR RAPID DEPTH CHANGES
# ==================================================

rapid_changes = []

previous_depth = None

for point, depth in clean_data:

    if previous_depth is not None:

        change = depth - previous_depth

        # A positive change means the depth value
        # became less negative, so the sea floor
        # became shallower.

        if change >= RAPID_CHANGE:

            rapid_changes.append(
                (point, change)
            )

    previous_depth = depth


# ==================================================
# MONITORING REPORT
# ==================================================

print()
print("=" * 50)
print("          SEA FLOOR MONITORING REPORT")
print("=" * 50)

print()

print("--- DATA QUALITY ---")

print(
    "Valid readings      :",
    len(depth_data)
)

print(
    "Invalid readings    :",
    len(invalid_points)
)

print(
    "Suspicious readings :",
    len(suspicious_points)
)

if invalid_points:

    print(
        "Invalid points      :",
        invalid_points
    )

if suspicious_points:

    print(
        "Suspicious points   :",
        suspicious_points
    )


# ==================================================
# NOISE REDUCTION INFORMATION
# ==================================================

print()

print("--- NOISE REDUCTION ---")

print(
    "Smoothing method    : Moving average"
)

print(
    "Smoothing window    :",
    SMOOTHING_WINDOW,
    "readings"
)


# ==================================================
# DEPTH INFORMATION
# ==================================================

print()

print("--- DEPTH INFORMATION ---")

print(
    "Shallowest depth    :",
    shallowest_depth,
    "m"
)

print(
    "Shallowest point    :",
    shallowest_point[0]
)

print(
    "Shallow zone points:",
    len(shallow_zone)
)

if shallow_zone:

    print(
        "Shallow zone range  : Point",
        shallow_zone[0][0],
        "to Point",
        shallow_zone[-1][0]
    )


# ==================================================
# RAPID CHANGE INFORMATION
# ==================================================

print()

print("--- RAPID CHANGE DETECTION ---")

print(
    "Rapid changes found:",
    len(rapid_changes)
)

if rapid_changes:

    for point, change in rapid_changes:

        print(
            "Point",
            point,
            ": +",
            round(change, 2),
            "m"
        )


# ==================================================
# FINAL STATUS
# ==================================================

print()

print("--- FINAL STATUS ---")

print(
    "Status              :",
    final_status
)

print(
    "Navigation action   :",
    action
)

print()

print("=" * 50)
print("              MONITORING COMPLETE")
print("=" * 50)


# ==================================================
# PREPARE GRAPH DATA
# ==================================================

points = []
graph_depths = []

for point, depth in smoothed_data:

    points.append(point)
    graph_depths.append(depth)


# ==================================================
# CREATE ANIMATED GRAPH
# ==================================================

fig, ax = plt.subplots(figsize=(12, 6))


# Empty line
# Data will be added one point at a time

line, = ax.plot(
    [],
    [],
    marker="o",
    markersize=3,
    linewidth=1,
    label="Smoothed sea floor depth"
)


# ==================================================
# GRAPH SETTINGS
# ==================================================

ax.set_title(
    "Sea Floor Depth Monitoring"
)

ax.set_xlabel(
    "Time (seconds)"
)

ax.set_ylabel(
    "Depth (m)"
)


# Keep graph limits fixed during animation

ax.set_xlim(
    min(points),
    max(points)
)

ax.set_ylim(
    min(graph_depths) - 10,
    0
)

ax.grid(True)


# ==================================================
# ADD SAFETY LEVELS
# ==================================================

ax.axhline(
    y=CAUTION_DEPTH,
    linestyle="--",
    label="Caution depth"
)

ax.axhline(
    y=WARNING_DEPTH,
    linestyle="--",
    label="Warning depth"
)

ax.axhline(
    y=DANGER_DEPTH,
    linestyle="--",
    label="Danger depth"
)


# ==================================================
# SHALLOWEST POINT MARKER
# ==================================================

shallowest_marker = ax.scatter(
    [],
    [],
    s=120,
    label="Shallowest point"
)


# ==================================================
# LIVE STATUS TEXT
# ==================================================

status_text = ax.text(
    0.02,
    0.95,
    "",
    transform=ax.transAxes,
    fontsize=12,
    verticalalignment="top"
)


# ==================================================
# LEGEND
# ==================================================

ax.legend()


# ==================================================
# ANIMATION FUNCTION
# ==================================================

def update(frame):

    # Get all points up to the current frame

    current_points = points[:frame + 1]

    current_depths = graph_depths[:frame + 1]


    # Update the graph line

    line.set_data(
        current_points,
        current_depths
    )


    # Current smoothed depth

    current_depth = current_depths[-1]


    # ==================================================
    # DETERMINE LIVE STATUS
    # ==================================================

    if current_depth > DANGER_DEPTH:

        current_status = "DANGER"

    elif current_depth > WARNING_DEPTH:

        current_status = "WARNING"

    elif current_depth > CAUTION_DEPTH:

        current_status = "CAUTION"

    else:

        current_status = "SAFE"


    # Update status text

    status_text.set_text(
        "Current depth: "
        + str(round(current_depth, 2))
        + " m\n"
        + "Status: "
        + current_status
    )


    # ==================================================
    # SHOW SHALLOWEST POINT FOUND SO FAR
    # ==================================================

    current_shallowest_index = max(
        range(len(current_depths)),
        key=lambda i: current_depths[i]
    )

    current_shallowest_point = (
        current_points[current_shallowest_index]
    )

    current_shallowest_depth = (
        current_depths[current_shallowest_index]
    )


    shallowest_marker.set_offsets(
        [[
            current_shallowest_point,
            current_shallowest_depth
        ]]
    )


    return (
        line,
        shallowest_marker,
        status_text
    )


# ==================================================
# CREATE ANIMATION
# ==================================================

animation = FuncAnimation(
    fig,
    update,
    frames=len(points),
    interval=1000,       # 1000 milliseconds = 1 second
    repeat=False
)


# ==================================================
# DISPLAY GRAPH
# ==================================================

plt.tight_layout()

plt.show()